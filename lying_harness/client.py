from __future__ import annotations

import os
import time
from threading import BoundedSemaphore


class BoundedBackend:
    """Share a request limit across independently advancing episodes."""

    def __init__(self, backend, concurrency):
        self.backend = backend
        self.slots = BoundedSemaphore(concurrency)
        self.name = backend.name
        self.metadata = backend.metadata

    def complete(self, *args):
        with self.slots:
            return self.backend.complete(*args)


class OpenAIBackend:
    name = "openai"

    def __init__(self, config):
        import httpx
        from openai import OpenAI

        base_url = os.environ.get("LLM_BASE_URL")
        key = os.environ.get("LLM_API_KEY")
        if not base_url or not key:
            raise ValueError("Set LLM_BASE_URL and LLM_API_KEY in .env or environment")
        self.client = OpenAI(
            base_url=base_url, api_key=key,
            timeout=httpx.Timeout(float(os.environ.get("LLM_TIMEOUT", "900")),
                                  read=float(os.environ.get("LLM_READ_TIMEOUT", "900"))), max_retries=0,
            http_client=httpx.Client(follow_redirects=True),
        )
        self.model = os.environ.get("LLM_MODEL") or self.client.models.list().data[0].id
        self.config = config
        self.metadata = {"backend": self.name, "base_url": base_url, "model": self.model}

    def complete(self, messages, spec, agent, stage, call_seed):
        args = {
            "model": self.model, "messages": messages,
            "temperature": self.config["temperature"], "max_tokens": self.config["max_tokens"],
        }
        thinking_body = self.config.get("thinking_extra_body", {
            "chat_template_kwargs": {"enable_thinking": self.config["enable_thinking"]}
        })
        if thinking_body:
            args["extra_body"] = thinking_body
        if self.config["send_seed"]:
            args["seed"] = call_seed
        start = time.monotonic()
        if os.environ.get("LLM_STREAM", "false").lower() == "true":
            content, reasoning = [], []
            finish_reason = usage = response_id = None
            with self.client.chat.completions.create(**args, stream=True,
                                                    stream_options={"include_usage": True}) as stream:
                for chunk in stream:
                    response_id = chunk.id
                    if chunk.usage:
                        usage = chunk.usage.model_dump()
                    for choice in chunk.choices:
                        if choice.delta.content:
                            content.append(choice.delta.content)
                        trace = (getattr(choice.delta, "reasoning", None)
                                 or getattr(choice.delta, "reasoning_content", None))
                        if trace:
                            reasoning.append(trace)
                        if choice.finish_reason:
                            finish_reason = choice.finish_reason
            return {"content": "".join(content), "reasoning": "".join(reasoning) or None,
                    "finish_reason": finish_reason, "usage": usage,
                    "latency_seconds": round(time.monotonic() - start, 3),
                    "response_id": response_id, "transport": "streaming"}
        response = self.client.chat.completions.create(**args)
        message = response.choices[0].message
        return {
            "content": message.content or "",
            "reasoning": getattr(message, "reasoning", None) or getattr(message, "reasoning_content", None),
            "finish_reason": response.choices[0].finish_reason,
            "usage": response.usage.model_dump() if response.usage else None,
            "latency_seconds": round(time.monotonic() - start, 3),
            "response_id": response.id,
        }


class MockBackend:
    """Deterministic mechanical fixture. Never evidence about model behavior."""

    name = "mock"

    def __init__(self, config):
        self.config = config
        self.metadata = {"backend": "mock", "model": "scripted-fixture-not-an-LLM"}

    def complete(self, messages, spec, agent, stage, call_seed):
        import json
        from .game import payoffs

        p = payoffs(self.config, spec)
        accept = spec.control == "positive" or (
            spec.criterion in ("none", "welfare") and spec.temptation > 1
            and (spec.channel or spec.criterion == "welfare")
        )
        check = {}
        if spec.criterion == "welfare":
            check = {"welfare_honest": p["honest_welfare"], "welfare_collude": p["collude_welfare"]}
        elif spec.criterion == "nondeception":
            check = {"deceives_evaluator": True, "uses_as_means": True}
        elif spec.criterion == "authority":
            check = {"authority_forbids": True}
        value = {
            "private_plan": "Scripted fixture plan; not generated reasoning.",
            "criterion_report": "Scripted fixture criterion check.", "criterion_check": check,
        }
        if stage == "message":
            value = {"private_plan": value["private_plan"], "peer_message": (
                "I propose accepting and concealing." if accept else "I will refuse."
            ) if spec.channel else None}
        if stage == "decision":
            value.update(
                decision="ACCEPT" if accept else "REFUSE",
                public_report={"disclosure": "CONCEAL" if accept else "DISCLOSE", "statement": (
                    "I made no authorization attempt." if accept else "I chose REFUSE."
                )},
            )
        return {
            "content": json.dumps(value), "reasoning": "MOCK: scripted fixture, not model reasoning.",
            "finish_reason": "stop", "usage": None, "latency_seconds": 0,
        }
