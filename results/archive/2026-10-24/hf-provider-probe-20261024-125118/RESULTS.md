# Hugging Face provider compatibility probe

Tested Qwen/Qwen3-32B through nscale, deepinfra, and featherless-ai using the actual positive-control planning prompt, thinking enabled, temperature 0.6, seed 10000, and a 4096-token budget. Three independent requests were submitted concurrently. These probes are not experimental outcomes.

All three requests returned HTTP 403 before inference: "This authentication method does not have sufficient permissions to call Inference Providers on behalf of user [account omitted]". This is a token permission failure, not a rate limit. No generated responses, reasoning, or usable generation-throughput measurements were obtained. Approximately 1.8 seconds per request measures rejection latency only.

Next step: enable **Make calls to Inference Providers** on the Hugging Face token, then repeat `python -m lying_harness.benchmark_hf`. Verify reasoning and schema compatibility before testing sustained concurrency. Pin the successful provider and keep any provider-backed study separate from the existing Modal study.

The credential is stored only in ignored `.env.hf`; result files contain no credential.
