"""Verify the results reorganization against the original committed evidence.

python tools/verify_results_layout.py
Reads the current Git index, the original source trees and the completed run.
It never writes to raw results or starts a model request.
"""
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '0b69c19b'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    mapping = json.loads((ROOT / 'docs/results-layout.json').read_text(encoding='utf-8'))
    index = {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, path = item.split(b'\t', 1)
            mode, blob, stage = meta.decode().split()
            assert stage == '0', f'Unresolved conflict: {path!r}'
            index[path.decode()] = blob
    checked = 0
    for item in git('ls-tree', '-r', '-z', BASELINE, '--', 'results').split(b'\0'):
        if not item:
            continue
        meta, name = item.split(b'\t', 1)
        original = name.decode()
        blob = meta.decode().split()[2]
        new = original
        for old, dest in mapping.items():
            if original.startswith(old+'/'):
                new = dest+original[len(old):]
                break
        assert new != original, f'Unclassified old results: {original}'
        assert index.get(new) == blob, f'Raw data changed: {new}'
        checked += 1

    source = ROOT / 'results/2026-10-25-pressure-study'
    checksums = json.loads((source / 'SHA256SUMS.json').read_text(encoding='utf-8'))
    for relative, expected in checksums.items():
        path = (source / relative).resolve()
        assert path.is_relative_to(source.resolve())
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative

    # Verify the new entry points against the staged tree, including sparse archives.
    pages = ['README.md', 'RESULTS.md', 'analysis/README.md',
        'analysis/2026-10-25-pressure-study/README.md', 'results/README.md',
        'results/archive/README.md', 'docs/results-layout.md']
    links = 0
    for name in pages:
        for suffix in ('.md', '.html'):
            page = str(Path(name).with_suffix(suffix)).replace('\\', '/')
            text = (ROOT / page).read_text(encoding='utf-8')
            urls = re.findall(r'\]\(([^\s)]+)\)', text) if suffix == '.md' else re.findall(r'(?:href|src)="([^"]+)"', text)
            for url in urls:
                if re.match(r'\w+:|#|/', url):
                    continue
                path = unquote(url.split('#')[0])
                target = posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
                exists = target in index or any(p.startswith(target.rstrip('/')+'/') for p in index)
                assert exists, f'Broken link in {page}: {url}'
                links += 1
    result = {'raw_files_preserved': checked, 'completed_run_checksums_verified': len(checksums),
        'navigation_links_checked': links, 'unresolved_conflicts': 0}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
