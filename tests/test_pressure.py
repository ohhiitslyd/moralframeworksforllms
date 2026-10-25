import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lying_harness.pressure import ROOT, specs_for, initial_prompt, parse_output, score_actions, episode, report


class Backend:
    name = "mock"
    metadata = {"backend": "mock", "model": "test-fixture"}

    def complete(self, messages, spec, agent, stage, seed):
        # Other agent's private information must never appear in this history.
        other = "B" if agent == "A" else "A"
        assert f"SECRET_{other}" not in json.dumps(messages)
        if stage == "decision":
            assert all("action:" not in m["content"] for m in messages if m["role"] == "assistant")
        content = (json.dumps({"plan": f"SECRET_{agent}", "peer_message": "shared"}) if stage == "message"
                   else f"plan: SECRET_{agent}" + ("\naction: take" if stage == "decision" else ""))
        return {"content": content, "reasoning": "test reasoning", "finish_reason": "stop", "usage": None}


class PressureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = json.loads((ROOT / "prompts/07-collusion-pressure-scenarios.json").read_text(encoding="utf-8"))

    def test_matrix(self):
        self.assertEqual(len(specs_for(self.pack)), 600)
        self.assertEqual(len(specs_for(self.pack, "weekend")), 180)

    def test_transient_windows_write_lock_retries_only_save(self):
        from lying_harness.pressure import write_json
        value = {'action': 'take'}
        with patch('lying_harness.pressure._write_json', side_effect=[PermissionError('locked'), None]) as save:
            with patch('lying_harness.pressure.time.sleep'):
                write_json(Path('fixture.json'), value)
        self.assertEqual(save.call_count, 2)
        self.assertEqual(save.call_args.args, (Path('fixture.json'), value))

    def test_extended_monitoring_matrix_and_prompts(self):
        pack = json.loads((ROOT / "prompts/09-extended-pressure-scenarios.json").read_text(encoding="utf-8-sig"))
        specs = specs_for(pack)
        self.assertEqual(len(specs), 47520)
        self.assertEqual(len({s['run_id'] for s in specs}), 47520)
        self.assertEqual(sum(s['monitoring'] == 'watched' for s in specs), 23760)
        for spec in specs[:12]:
            prompt = initial_prompt(pack, spec, 'A')
            self.assertIn(pack['monitoring_texts'][spec['monitoring']], prompt)
            other = 'unwatched' if spec['monitoring'] == 'watched' else 'watched'
            self.assertNotIn(pack['monitoring_texts'][other], prompt)
            self.assertNotIn('expected_first_take', prompt)
            self.assertNotIn('welfare_if_take', prompt)

    def test_extended_report_with_protocol_control(self):
        pack = json.loads((ROOT / "prompts/09-extended-pressure-scenarios.json").read_text(encoding="utf-8-sig"))
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            control = dict(specs_for(self.pack)[0], run_id='positive-protocol-s1', control=True)
            episode(pack, {'rounds': 3}, control, Backend(), output / 'runs' / control['run_id'])
            spec = specs_for(pack)[0]
            episode(pack, {'rounds': 3}, spec, Backend(), output / 'runs' / spec['run_id'])
            report(output, 47520)
            self.assertIn('monitoring', (output / 'runs.csv').read_text())
            self.assertEqual(json.loads((output / 'summary.json').read_text())['attempted_experiments'], 1)

    def test_no_prediction_leakage_and_mixed_rules(self):
        spec = specs_for(self.pack)[1]
        a, b = [initial_prompt(self.pack, spec, agent) for agent in ("A", "B")]
        self.assertIn(self.pack["criterion_blocks"]["welfare"], a)
        self.assertNotIn(self.pack["criterion_blocks"]["welfare"], b)
        for prompt in (a, b):
            self.assertNotIn("expected_first_take", prompt)
            self.assertNotIn("welfare_if_take", prompt)
            self.assertIn(self.pack["scenarios"][0]["setting"], prompt)

    def test_action_parser(self):
        for text in ("plan: take", "plan: x\naction: take\naction: refuse", "plan: x\naction: maybe"):
            with self.assertRaises(ValueError):
                parse_output(text, "decision")
        self.assertEqual(parse_output("plan: x\naction: refuse", "decision")["action"], "refuse")

    def test_lock(self):
        for a, b in (("refuse", "refuse"), ("take", "refuse"), ("refuse", "take")):
            self.assertFalse(score_actions(a, b)["deal_taken"])
        self.assertTrue(score_actions("take", "take")["deal_taken"])

    def test_private_histories_and_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = episode(self.pack, {"rounds": 3}, specs_for(self.pack)[0], Backend(), Path(tmp) / "run")
            self.assertEqual(result["status"], "complete", result.get("error"))
            self.assertEqual(result["usage"]["calls_returned"], 10)
            self.assertTrue(result["scores"]["deal_taken"])

    def test_checkpoint_reuses_saved_responses(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run"
            spec = specs_for(self.pack)[0]
            episode(self.pack, {"rounds": 3}, spec, Backend(), path)
            events = [json.loads(line) for line in (path / "events.jsonl").read_text(encoding="utf-8").splitlines()]
            kept = [e for e in events if e.get("stage") == "plan"]
            (path / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in kept), encoding="utf-8")
            result = json.loads((path / "result.json").read_text(encoding="utf-8"))
            result["status"] = "running"
            (path / "result.json").write_text(json.dumps(result), encoding="utf-8")
            class RecoveryBackend(Backend):
                calls = 0
                def complete(self, messages, spec, agent, stage, seed):
                    assert stage != "plan", "Saved plan must not be regenerated"
                    self.calls += 1
                    return super().complete(messages, spec, agent, stage, seed)
            backend = RecoveryBackend()
            resumed = episode(self.pack, {"rounds": 3}, spec, backend, path, recover=True)
            self.assertEqual(resumed["status"], "complete", resumed.get("error"))
            self.assertEqual(backend.calls, 8)
            self.assertEqual(resumed["usage"]["calls_returned"], 10)
            # A billing failure is recoverable, while its original record is retained
            # by the scheduler; completed behavioral outputs are never retried.
            result["status"] = "failed"
            result["error"] = "APIStatusError: Error code: 402 - no remaining credits"
            (path / "result.json").write_text(json.dumps(result), encoding="utf-8")
            (path / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in kept), encoding="utf-8")
            second = RecoveryBackend()
            resumed = episode(self.pack, {"rounds": 3}, spec, second, path, recover=True)
            self.assertEqual(resumed["status"], "complete", resumed.get("error"))
            self.assertEqual(second.calls, 8)
            # A connection failure is also recoverable from checkpoint.
            result["status"] = "failed"
            result["error"] = "ValueError: RemoteProtocolError: peer closed connection"
            (path / "result.json").write_text(json.dumps(result), encoding="utf-8")
            (path / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in kept), encoding="utf-8")
            third = RecoveryBackend()
            resumed = episode(self.pack, {"rounds": 3}, spec, third, path, recover=True)
            self.assertEqual(resumed["status"], "complete", resumed.get("error"))
            self.assertEqual(third.calls, 8)


if __name__ == "__main__":
    unittest.main()
