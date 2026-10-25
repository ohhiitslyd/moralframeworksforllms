"""Small provider compatibility probe; never part of experimental outcomes."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import httpx
from dotenv import dotenv_values

from .pressure import STAGES, initial_prompt, parse_output, specs_for


def main():
    root = Path(__file__).resolve().parents[1]
    token = dotenv_values(root / '.env.hf')['HF_TOKEN']
    output = root / 'results' / ('hf-provider-probe-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S'))
    output.mkdir(parents=True)
    pack = json.loads((root / 'prompts/09-extended-pressure-scenarios.json').read_text(encoding='utf-8'))
    spec = specs_for(pack, 'weekend')[0]
    messages = [{'role': 'system', 'content': initial_prompt(pack, spec, 'A')},
                {'role': 'user', 'content': STAGES['plan']}]

    def probe(provider):
        payload = dict(model=f'Qwen/Qwen3-32B:{provider}', messages=messages,
                       temperature=0.6, max_tokens=4096,
                       seed=10000, chat_template_kwargs={'enable_thinking': True})
        start = time.monotonic()
        record = {'provider': provider, 'request': payload, 'purpose': 'compatibility probe, not study data'}
        try:
            with httpx.Client(timeout=180, follow_redirects=True) as client:
                r = client.post('https://router.huggingface.co/v1/chat/completions',
                                headers={'Authorization': 'Bearer ' + token}, json=payload)
            record.update(http_status=r.status_code, response=r.json(),
                          retry_after=r.headers.get('retry-after'))
            if r.status_code == 200:
                choice = record['response']['choices'][0]
                message = choice['message']
                reasoning = message.get('reasoning') or message.get('reasoning_content')
                record['reasoning_available'] = bool(reasoning)
                record['finish_reason'] = choice.get('finish_reason')
                try:
                    parse_output(message.get('content') or '', 'plan')
                    record['schema_valid'] = True
                except ValueError as e:
                    record.update(schema_valid=False, schema_error=str(e))
        except Exception as e:
            record['error'] = f'{type(e).__name__}: {e}'.replace(token, '[REDACTED]')
        record['latency_seconds'] = round(time.monotonic() - start, 3)
        (output / f'{provider}.json').write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
        summary = {k: record.get(k) for k in ('provider', 'http_status', 'latency_seconds', 'reasoning_available', 'schema_valid', 'finish_reason', 'error')}
        print(json.dumps(summary), flush=True)
        return summary

    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(probe, ['nscale', 'deepinfra', 'featherless-ai']))
    (output / 'summary.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    print(str(output), flush=True)


if __name__ == '__main__':
    main()
