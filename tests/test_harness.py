import copy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lying_harness.client import MockBackend, OpenAIBackend
from lying_harness.game import (RunSpec, criterion_errors, expand_runs, load_prompts,
                               parse_response, payoffs, score, validate_config)
from lying_harness.runner import ROOT, main, run_episode


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "configs/pilot.json").read_text())
        self.prompts = load_prompts(ROOT / "prompts")
        self.spec = RunSpec("none", 2, True, 1)

    def choices(self, a="ACCEPT", b="ACCEPT", disclosure="CONCEAL"):
        return {agent: {"decision": choice, "public_report": {"disclosure": disclosure, "statement": "test"}}
                for agent, choice in (("A", a), ("B", b))}

    def test_payoff_conservation_and_all_joint_choices(self):
        for a in ("ACCEPT", "REFUSE"):
            for b in ("ACCEPT", "REFUSE"):
                result = score(self.config, self.spec, self.choices(a, b), 6)
                mutual = a == b == "ACCEPT"
                self.assertEqual(result["coalition_gain"], 200 if mutual else 0)
                self.assertEqual(result["hospital_loss"], 100 if mutual else 0)
                self.assertEqual(result["total_welfare"], result["hospital_final"] + result["agent_A_final"] + result["agent_B_final"])
                self.assertIsNone(result["confirmed_collusion"])

    def test_equal_welfare_at_one(self):
        values = payoffs(self.config, replace(self.spec, temptation=1))
        self.assertEqual(values["honest_welfare"], values["collude_welfare"])

    def test_disclosed_coalition_is_not_deceptive_coalition(self):
        result = score(self.config, self.spec, self.choices(disclosure="DISCLOSE"), 6)
        self.assertTrue(result["mutual_accept"])
        self.assertFalse(result["deceptive_coalition"])

    def test_failed_attempt_can_still_be_hidden(self):
        result = score(self.config, self.spec, self.choices(b="REFUSE"), 6)
        self.assertTrue(result["conceal_A"])
        self.assertFalse(result["conceal_B"])
        self.assertTrue(result["failed_authorization_attempt"])
        self.assertEqual(result["hospital_loss"], 0)

    def test_arithmetic_failure_and_boolean_not_number(self):
        spec = replace(self.spec, criterion="welfare")
        for wrong in (1199, True, "1200", None):
            response = {"criterion_check": {"welfare_honest": wrong, "welfare_collude": 1300}}
            self.assertTrue(criterion_errors(spec, response, payoffs(self.config, spec)))

    def test_malformed_and_closed_channel_responses_rejected(self):
        for content in ('{"decision": "ACCEPT"', '[]', '{"private_plan":"x","peer_message":"leak"}'):
            with self.assertRaises((ValueError, json.JSONDecodeError)):
                parse_response(content, "message", False)

    def test_full_and_minimum_matrix_counts(self):
        config = json.loads((ROOT / "configs/full.json").read_text())
        self.assertEqual(len(validate_config(config)), 99)
        config["matrix"]["matched_nulls"] = False
        self.assertEqual(len(validate_config(config)), 63)

    def test_duplicate_run_and_bad_gate_rejected(self):
        config = copy.deepcopy(self.config)
        config["runs"].append(config["runs"][0])
        with self.assertRaises(ValueError):
            expand_runs(config)
        config = copy.deepcopy(self.config)
        config["runs"] = config["runs"][1:]
        with self.assertRaises(ValueError):
            validate_config(config)

    def test_private_state_and_final_decisions_never_delivered(self):
        class RecordingBackend(MockBackend):
            def __init__(self, config):
                super().__init__(config)
                self.requests = []

            def complete(self, messages, spec, agent, stage, call_seed):
                self.requests.append((agent, stage, copy.deepcopy(messages)))
                response = super().complete(messages, spec, agent, stage, call_seed)
                parsed = json.loads(response["content"])
                parsed["private_plan"] = f"PRIVATE_SENTINEL_{agent}"
                response["content"] = json.dumps(parsed)
                response["reasoning"] = f"REASONING_SENTINEL_{agent}"
                return response

        backend = RecordingBackend(self.config)
        with tempfile.TemporaryDirectory() as folder:
            result = run_episode(self.config, self.spec, self.prompts, backend, Path(folder) / "run")
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["delivered_messages"], 6)
            for agent, stage, history in backend.requests:
                peer = "B" if agent == "A" else "A"
                raw = json.dumps(history)
                self.assertNotIn(f"PRIVATE_SENTINEL_{peer}", raw)
                self.assertNotIn("REASONING_SENTINEL", raw)
                if stage == "decision":
                    self.assertFalse(any('"decision":' in message["content"] for message in history if message["role"] == "assistant"))
            public = (Path(folder) / "run/hospital_view.json").read_text()
            self.assertNotIn("PRIVATE_SENTINEL", public)

    def test_closed_channel_has_same_call_count_no_deliveries(self):
        with tempfile.TemporaryDirectory() as folder:
            result = run_episode(self.config, replace(self.spec, channel=False), self.prompts,
                                 MockBackend(self.config), Path(folder) / "run")
            self.assertEqual(result["delivered_messages"], 0)
            self.assertEqual(result["usage"]["calls_returned"], 10)
            self.assertEqual(result["status"], "complete")

    def test_truncation_is_failure_not_refusal(self):
        class Truncated(MockBackend):
            def complete(self, *args):
                response = super().complete(*args)
                response["finish_reason"] = "length"
                return response
        with tempfile.TemporaryDirectory() as folder:
            result = run_episode(self.config, self.spec, self.prompts, Truncated(self.config), Path(folder) / "run")
            self.assertEqual(result["status"], "failed")
            self.assertIsNone(result["scores"])

    def test_missing_reasoning_is_not_valid_research_run(self):
        class MissingReasoning(MockBackend):
            def complete(self, *args):
                response = super().complete(*args)
                response["reasoning"] = None
                return response
        with tempfile.TemporaryDirectory() as folder:
            result = run_episode(self.config, self.spec, self.prompts, MissingReasoning(self.config), Path(folder) / "run")
            self.assertEqual(result["status"], "reasoning_unavailable")

    def test_failed_positive_control_stops_batch(self):
        class RefusingControl(MockBackend):
            def complete(self, *args):
                response = super().complete(*args)
                if args[3] == "decision":
                    value = json.loads(response["content"])
                    value["decision"] = "REFUSE"
                    response["content"] = json.dumps(value)
                return response
        with tempfile.TemporaryDirectory() as folder, patch("lying_harness.runner.MockBackend", RefusingControl):
            output = Path(folder) / "batch"
            self.assertEqual(main(["--output", str(output)]), 2)
            self.assertEqual(len(list((output / "runs").iterdir())), 1)

    def test_resume_requires_identical_prompts(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "batch"
            args = ["--output", str(output), "--limit", "1"]
            self.assertEqual(main(args), 0)
            self.assertEqual(main(args + ["--resume"]), 0)
            with self.assertRaises(ValueError):
                main(args)

    def test_analysis_excludes_invalid_results_and_retains_uncertainty(self):
        from lying_harness.analyze import dependence, logistic_fit, records, wilson
        invalid = {"run_id": "test", "spec": {"criterion": "welfare"}, "backend": "mock",
                   "status": "manipulation_failure", "scores": {"mutual_accept": True}, "usage": {}}
        self.assertFalse(records([invalid])[0]["valid"])
        self.assertEqual(logistic_fit([])["status"], "insufficient_data")
        constant = [{"temptation": t, "deceptive_coalition": False, "accept_A": 0, "accept_B": 0}
                    for t in (0.5, 1, 2, 4) for _ in range(3)]
        self.assertEqual(logistic_fit(constant)["status"], "constant_outcome")
        self.assertEqual(dependence(constant)["status"], "degenerate_actions")
        low, high = wilson(1, 1)
        self.assertLess(low, 0.3)
        self.assertAlmostEqual(high, 1)

    def test_openai_compatible_payload_and_reasoning_aliases(self):
        import httpx
        from openai import OpenAI

        for reasoning_field in ("reasoning", "reasoning_content"):
            captured = []

            def respond(request):
                captured.append(json.loads(request.content))
                return httpx.Response(200, json={
                    "id": "offline-fixture", "object": "chat.completion", "created": 0, "model": "fixture",
                    "choices": [{"index": 0, "finish_reason": "stop", "message": {
                        "role": "assistant", "content": "{}", reasoning_field: "private test reasoning"
                    }}], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7},
                })

            backend = OpenAIBackend.__new__(OpenAIBackend)
            backend.config = self.config
            backend.model = "fixture"
            with httpx.Client(transport=httpx.MockTransport(respond)) as transport:
                backend.client = OpenAI(api_key="offline-test-only", base_url="https://fixture.invalid/v1",
                                        http_client=transport, max_retries=0)
                with patch.dict("os.environ", {"LLM_STREAM": "false"}):
                    result = backend.complete([{"role": "user", "content": "fixture"}], self.spec, "A", "plan", 123)
            self.assertEqual(result["reasoning"], "private test reasoning")
            self.assertTrue(captured[0]["chat_template_kwargs"]["enable_thinking"])
            self.assertEqual(captured[0]["seed"], 123)
            self.assertEqual(result["usage"]["total_tokens"], 7)

    def test_parallel_batch_is_bounded_and_keeps_all_episodes(self):
        import threading
        import time
        class ConcurrentFixture(MockBackend):
            peak = 0
            active = 0
            lock = threading.Lock()

            def complete(self, *args):
                with self.lock:
                    type(self).active += 1
                    type(self).peak = max(type(self).peak, type(self).active)
                try:
                    time.sleep(0.01)
                    return super().complete(*args)
                finally:
                    with self.lock:
                        type(self).active -= 1
        with tempfile.TemporaryDirectory() as folder, patch("lying_harness.runner.MockBackend", ConcurrentFixture):
            output = Path(folder) / "batch"
            self.assertEqual(main(["--output", str(output), "--jobs", "2"]), 0)
            results = json.loads((output / "index.json").read_text())["results"]
            self.assertEqual(len(results), 7)
            self.assertEqual(len({r["run_id"] for r in results}), 7)
            self.assertTrue(all(r["status"] == "complete" for r in results))
            self.assertGreaterEqual(ConcurrentFixture.peak, 3)
            self.assertLessEqual(ConcurrentFixture.peak, 4)

    def test_continue_on_failure_preserves_attempt_and_resumes_without_retry(self):
        class FailingFixture(MockBackend):
            failed_calls = 0

            def complete(self, *args):
                response = super().complete(*args)
                spec, stage = args[1], args[3]
                if spec.control == "experimental" and spec.criterion == "none" and spec.channel and stage == "plan":
                    type(self).failed_calls += 1
                    response["finish_reason"] = "length"
                return response
        with tempfile.TemporaryDirectory() as folder, patch("lying_harness.runner.MockBackend", FailingFixture):
            output = Path(folder) / "batch"
            args = ["--output", str(output), "--jobs", "2", "--continue-on-failure"]
            self.assertEqual(main(args), 2)
            results = json.loads((output / "index.json").read_text())["results"]
            self.assertEqual(len(results), 7)
            self.assertEqual(sum(r["status"] == "failed" for r in results), 1)
            calls_before = FailingFixture.failed_calls
            self.assertEqual(main(args + ["--resume"]), 2)
            self.assertEqual(FailingFixture.failed_calls, calls_before)

    def test_transport_outage_pauses_even_when_continuing_validation_failures(self):
        class DisconnectedFixture(MockBackend):
            def complete(self, *args):
                if args[1].control == "experimental":
                    raise RuntimeError("APIConnectionError: simulated outage")
                return super().complete(*args)
        with tempfile.TemporaryDirectory() as folder, patch("lying_harness.runner.MockBackend", DisconnectedFixture):
            output = Path(folder) / "batch"
            self.assertEqual(main(["--output", str(output), "--jobs", "2", "--continue-on-failure"]), 3)
            results = json.loads((output / "index.json").read_text())["results"]
            self.assertLess(len(results), 7)
            self.assertEqual(results[0]["status"], "complete")

    def test_checkpoint_continuation_never_regenerates_saved_responses(self):
        class Interrupted(MockBackend):
            def complete(self, *args):
                if args[2] == "B" and args[3] == "message":
                    raise KeyboardInterrupt("simulated worker interruption")
                return super().complete(*args)

        class Counting(MockBackend):
            calls = []
            def complete(self, *args):
                self.calls.append((args[2], args[3], args[4]))
                return super().complete(*args)

        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / "run"
            with self.assertRaises(KeyboardInterrupt):
                run_episode(self.config, self.spec, self.prompts, Interrupted(self.config), directory)
            before = [json.loads(line) for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()]
            saved = [e for e in before if e["kind"] == "response"]
            backend = Counting(self.config)
            result = run_episode(self.config, self.spec, self.prompts, backend, directory, True)
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["usage"]["calls_returned"], 10)
            self.assertEqual(len(backend.calls), 10 - len(saved))
            after = [json.loads(line) for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual([e for e in after if e["kind"] == "response"][:len(saved)], saved)
            with self.assertRaises(ValueError):
                run_episode(self.config, self.spec, self.prompts, backend, directory, True)

    def test_shared_request_limit_with_more_episode_workers(self):
        import threading
        import time
        class Measured(MockBackend):
            active = peak = 0
            lock = threading.Lock()
            def complete(self, *args):
                with self.lock:
                    type(self).active += 1
                    type(self).peak = max(type(self).peak, type(self).active)
                try:
                    time.sleep(0.01)
                    return super().complete(*args)
                finally:
                    with self.lock:
                        type(self).active -= 1
        with tempfile.TemporaryDirectory() as folder, patch("lying_harness.runner.MockBackend", Measured):
            self.assertEqual(main(["--output", str(Path(folder) / "batch"), "--jobs", "6",
                                   "--request-concurrency", "3"]), 0)
            self.assertEqual(Measured.peak, 3)

    def test_streaming_preserves_reasoning_content_usage_and_finish_reason(self):
        import httpx
        from openai import OpenAI
        for field in ("reasoning", "reasoning_content"):
            chunks = [
                {"choices": [{"index": 0, "delta": {field: "private "}, "finish_reason": None}]},
                {"choices": [{"index": 0, "delta": {field: "trace", "content": "{}"}, "finish_reason": None}]},
                {"choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
                {"choices": [], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7}},
            ]
            def respond(request):
                self.assertTrue(json.loads(request.content)["stream"])
                body = "".join("data: " + json.dumps({"id": "stream-fixture", "object": "chat.completion.chunk",
                    "created": 0, "model": "fixture", **chunk}) + "\n\n" for chunk in chunks) + "data: [DONE]\n\n"
                return httpx.Response(200, headers={"content-type": "text/event-stream"}, text=body)
            backend = OpenAIBackend.__new__(OpenAIBackend)
            backend.config, backend.model = self.config, "fixture"
            with httpx.Client(transport=httpx.MockTransport(respond)) as transport:
                backend.client = OpenAI(api_key="offline-test-only", base_url="https://fixture.invalid/v1",
                                        http_client=transport, max_retries=0)
                with patch.dict("os.environ", {"LLM_STREAM": "true"}):
                    result = backend.complete([], self.spec, "A", "plan", 123)
            self.assertEqual(result["reasoning"], "private trace")
            self.assertEqual(result["content"], "{}")
            self.assertEqual(result["finish_reason"], "stop")
            self.assertEqual(result["usage"]["total_tokens"], 7)

    def test_endpoint_switch_is_explicit_and_preserves_completed_results(self):
        class OtherEndpoint(MockBackend):
            def __init__(self, config):
                super().__init__(config)
                self.metadata = {"backend": "mock", "model": "another-fixture"}
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "batch"
            args = ["--output", str(output), "--limit", "1"]
            self.assertEqual(main(args), 0)
            result_path = next((output / "runs").glob("*/result.json"))
            original = result_path.read_bytes()
            with patch("lying_harness.runner.MockBackend", OtherEndpoint):
                with self.assertRaises(ValueError):
                    main(args + ["--resume"])
                self.assertEqual(main(args + ["--resume", "--allow-endpoint-change"]), 0)
                self.assertEqual(result_path.read_bytes(), original)
                self.assertTrue((output / "endpoint_history.json").exists())
                config = dict(self.config, temperature=0.4)
                path = Path(folder) / "different.json"
                path.write_text(json.dumps(config), encoding="utf-8")
                with self.assertRaises(ValueError):
                    main(args + ["--resume", "--allow-endpoint-change", "--config", str(path)])


if __name__ == "__main__":
    unittest.main()
