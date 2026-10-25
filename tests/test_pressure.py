import json
from pathlib import Path
import tempfile
import unittest

from lying_harness.pressure import ROOT, specs_for, initial_prompt, parse_output, score_actions, episode
from lying_harness.settings import SETTINGS


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
        cls.pack = json.loads((ROOT / "prompts/09-extended-pressure-scenarios.json").read_text(encoding="utf-8"))

    def test_matrix(self):
        self.assertEqual(len(self.pack["scenarios"]), 792)
        self.assertEqual(len(specs_for(self.pack)), 47520)
        self.assertEqual(len(specs_for(self.pack, "weekend")), 540)
        self.assertEqual(len(specs_for(self.pack, monitoring=["watched"])), 23760)

    def test_setting_is_a_variable(self):
        self.assertEqual(tuple(self.pack["settings"]), SETTINGS)
        seen = {row["setting_id"] for row in self.pack["scenarios"]}
        self.assertEqual(seen, set(SETTINGS))
        for setting in SETTINGS:
            group = [row for row in self.pack["scenarios"] if row["setting_id"] == setting]
            self.assertEqual(len(group), 99, setting)
            mix = {k: sum(row["diagnostic"] == k for row in group)
                   for k in ("welfare", "nondeception", "authority")}
            self.assertEqual(mix, {"welfare": 33, "nondeception": 33, "authority": 33}, setting)

    def test_no_prediction_leakage_and_mixed_rules(self):
        spec = next(row for row in specs_for(self.pack) if row["pairing"] == "W-none")
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


if __name__ == "__main__":
    unittest.main()
