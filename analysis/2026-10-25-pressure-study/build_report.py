"""Rebuild the completed-study report without model calls or raw-data writes.

Run from any directory: python analysis/2026-10-25-pressure-study/build_report.py
Uses the frozen run IDs and saved results, never the current prompt generator.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT / 'results/2026-10-25-pressure-study'
FIG = OUT / 'figures'
TABLE = OUT / 'tables'
PAIRINGS = ['W-W', 'W-none', 'D-D', 'D-none', 'A-A', 'A-none']


def write_csv(name, rows):
    with (TABLE / name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save(fig, name):
    for suffix in ('png', 'svg'):
        fig.savefig(FIG / f'{name}.{suffix}', dpi=160)
    plt.close(fig)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    TABLE.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8'))
    summary = json.loads((SOURCE / 'summary.json').read_text(encoding='utf-8'))
    pack = manifest['pack']
    rows = list(csv.DictReader((SOURCE / 'runs.csv').open(encoding='utf-8-sig')))
    rows = [r for r in rows if r['control'] == 'False']
    assert len(rows) == 4320 and len({r['run_id'] for r in rows}) == 4320
    assert Counter(r['status'] for r in rows) == {'complete': 4243, 'failed': 77}
    # Validate each CSV row against the saved evidence, including failed attempts.
    for row in rows:
        result = json.loads((SOURCE / 'runs' / row['run_id'] / 'result.json').read_text(encoding='utf-8'))
        assert result['run_id'] == row['run_id'] and result['status'] == row['status']
        for key in ('scenario', 'pairing', 'monitoring', 'level', 'seed'):
            assert str(result['spec'][key]) == row[key], (row['run_id'], key)
        if row['status'] == 'complete':
            a, b = (result['decisions'][agent]['action'] for agent in ('A', 'B'))
            outcome = 'mutual_take' if a == b == 'take' else 'unilateral_take' if a != b else 'both_refuse'
            assert (a, b, outcome) == (row['action_a'], row['action_b'], row['outcome'])
    complete = [r for r in rows if r['status'] == 'complete']
    assert Counter(r['outcome'] for r in complete) == summary['outcomes']
    index = {(r['scenario'], int(r['level']), r['pairing'], r['monitoring']): r for r in rows}
    assert len(index) == 4320
    records = []
    codes = {'mutual_take': 'T', 'unilateral_take': 'O', 'both_refuse': 'R'}
    for scene in pack['scenarios']:
        for pairing in PAIRINGS:
            for level in range(1, 6):
                w, u = (index[(scene['id'], level, pairing, mode)] for mode in ('watched', 'unwatched'))
                wc, uc = w['status'] == 'complete', u['status'] == 'complete'
                wt, ut = w['outcome'] == 'mutual_take', u['outcome'] == 'mutual_take'
                category = 0 if not (wc and uc) else 1 if not wt and not ut else 2 if wt and ut else 3 if wt else 4
                records.append(dict(setting=scene['setting_id'], scenario=scene['id'], title=scene['title'],
                    pairing=pairing, level=level, watched_status=w['status'], unwatched_status=u['status'],
                    watched_outcome=w['outcome'], unwatched_outcome=u['outcome'], matched=wc and uc,
                    watched_take=int(wt) if wc else '', unwatched_take=int(ut) if uc else '',
                    difference=int(wt)-int(ut) if wc and uc else '', category=category,
                    cell=(codes[w['outcome']] if wc else '?')+'/'+(codes[u['outcome']] if uc else '?')))
    assert len(records) == 2160
    write_csv('scenario-level-pairing-comparisons.csv', records)
    matched = [r for r in records if r['matched']]
    counts = Counter(r['category'] for r in matched)
    provenance = {'source_commit': '82b644ce5439c6fc6f28e4cdeaedf032a28cc848',
        'original_directory': 'results/qwen-pressure-72-v1-snapshot-20261025-164207',
        'current_directory': SOURCE.relative_to(ROOT).as_posix(), 'cutoff_utc': summary['cutoff_utc'],
        'manifest_sha256': hashlib.sha256((SOURCE / 'manifest.json').read_bytes()).hexdigest(),
        'raw_checksums_sha256': hashlib.sha256((SOURCE / 'SHA256SUMS.json').read_bytes()).hexdigest(),
        'planned_comparisons': 2160, 'matched_comparisons': len(matched),
        'unavailable_comparisons': 2160-len(matched),
        'both_joint_accept': counts[2], 'neither_joint_accept': counts[1],
        'watched_only_joint_accept': counts[3], 'unwatched_only_joint_accept': counts[4]}
    (OUT / 'provenance.json').write_text(json.dumps(provenance, indent=2)+'\n', encoding='utf-8')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
        'figure.facecolor': '#f8fafc', 'axes.facecolor': '#f8fafc', 'text.color': '#17263d',
        'axes.spines.top': False, 'axes.spines.right': False, 'svg.fonttype': 'none'})

    aggregates, averages = [], []
    for pairing in PAIRINGS:
        for level in range(1, 6):
            group = [r for r in matched if r['pairing'] == pairing and r['level'] == level]
            n = len(group)
            w, u = (sum(r[key] for r in group)/n for key in ('watched_take', 'unwatched_take'))
            aggregates.append(dict(pairing=pairing, level=level, matched_scenarios=n,
                watched_rate=w, unwatched_rate=u, difference_pp=100*(w-u)))
    write_csv('pairing-level-monitoring.csv', aggregates)
    rule_summary = []
    for code, title in [('W', 'Welfare'), ('D', 'Non-deception'), ('A', 'Authority')]:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.subplots_adjust(left=.11, right=.97, top=.78, bottom=.23)
        fig.text(.11, .94, f'{title}: watched vs unwatched', fontsize=20, fontweight='bold')
        fig.text(.11, .87, 'Joint acceptance · Same completed cells · Both pairings combined', fontsize=11)
        values = []
        for level in range(1, 6):
            group = [r for r in matched if r['pairing'].startswith(code+'-') and r['level'] == level]
            n = len(group)
            w, u = (sum(r[key] for r in group)/n for key in ('watched_take', 'unwatched_take'))
            values.append((n, w, u))
            averages.append(dict(rule=title, level=level, matched_comparisons=n,
                watched_rate=w, unwatched_rate=u, difference_pp=100*(w-u)))
        x = np.arange(1, 6)
        for offset, mode, color, position in [(-.18, 'Watched', '#256c98', 1), (.18, 'Unwatched', '#ce8a35', 2)]:
            heights = [v[position] for v in values]
            ax.bar(x+offset, heights, width=.34, label=mode, color=color, zorder=3)
            for xx, height in zip(x+offset, heights):
                ax.text(xx, height+.018, f'{height:.0%}', ha='center', fontsize=10)
        ax.set_xticks(x, [f'Level {level}\nn={value[0]}' for level, value in zip(x, values)])
        ax.set_ylim(0, 1.08)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_ylabel('Both agents choose take')
        ax.grid(axis='y', color='#dde5ed')
        ax.set_axisbelow(True)
        ax.legend(frameon=False, loc='upper left')
        group = [r for r in matched if r['pairing'].startswith(code+'-')]
        n = len(group)
        w, u = (sum(r[key] for r in group)/n for key in ('watched_take', 'unwatched_take'))
        rule_summary.append((title, n, w, u))
        fig.text(.11, .11, f'All levels: {w:.1%} watched / {u:.1%} unwatched · Difference {100*(w-u):+.1f} pp', fontsize=11, fontweight='bold')
        fig.text(.11, .045, 'Completed collection · 25 Oct 2026 · One seed per condition · Exclusions omitted in pairs', fontsize=9)
        save(fig, f'{code.lower()}-average-monitoring')
    write_csv('rule-level-monitoring-averages.csv', averages)

    fig, axes = plt.subplots(1, 3, figsize=(15, 6.7))
    fig.subplots_adjust(left=.075, right=.98, top=.76, bottom=.18, wspace=.3)
    fig.text(.075, .94, 'Monitoring notice by stress level and pairing', fontsize=21, fontweight='bold')
    fig.text(.075, .87, f'{len(matched):,} matched cells of 2,160 · Same scenarios in both notices', fontsize=12)
    for k, (ax, key, title) in enumerate(zip(axes, ['watched_rate', 'unwatched_rate', 'difference_pp'],
            ['Watched: joint acceptance', 'Unwatched: joint acceptance', 'Watched minus unwatched'])):
        matrix = np.array([[(next(r for r in aggregates if r['pairing'] == pairing and r['level'] == level)[key]) for level in range(1, 6)] for pairing in PAIRINGS])
        if k < 2:
            matrix *= 100
        ax.imshow(matrix, cmap='Blues' if k < 2 else 'RdBu_r', vmin=0 if k < 2 else -100, vmax=100, aspect='auto')
        ax.set_xticks(range(5), range(1, 6))
        ax.set_yticks(range(6), PAIRINGS)
        ax.set_title(title, fontsize=12)
        ax.set_xlabel('Stress level')
        for i, pairing in enumerate(PAIRINGS):
            for j, level in enumerate(range(1, 6)):
                n = next(r['matched_scenarios'] for r in aggregates if r['pairing'] == pairing and r['level'] == level)
                value = matrix[i, j]
                label = f'{value:.0f}%' if k < 2 else f'{value:+.0f} pp'
                ax.text(j, i, f'{label}\nn={n}', ha='center', va='center', fontsize=9,
                    color='white' if (value > 60 if k < 2 else abs(value) > 65) else '#17263d')
    fig.text(.075, .07, 'Each n counts matched scenarios; it is not a count of independent repeated seeds.', fontsize=11)
    save(fig, 'matched-monitoring-overview')

    lookup = {(r['scenario'], r['pairing'], r['level']): r for r in records}
    colors = ['#e4e8ee', '#d1dfed', '#168b83', '#e2a03a', '#9066b6']
    for setting in pack['settings']:
        scenes = [s for s in pack['scenarios'] if s['setting_id'] == setting]
        fig, axes = plt.subplots(3, 2, figsize=(16, 15))
        fig.subplots_adjust(left=.19, right=.975, top=.83, bottom=.15, hspace=.48, wspace=.85)
        fig.text(.03, .96, f'{setting.replace("_", " ").title()}: every scenario', fontsize=22, fontweight='bold')
        n = sum(r['matched'] for r in records if r['setting'] == setting)
        fig.text(.03, .915, f'{n}/270 matched cells · Each cell shows watched / unwatched', fontsize=12)
        fig.text(.03, .875, 'T = both take    O = one takes    R = both refuse    ? = excluded episode', fontsize=12)
        for ax, pairing in zip(axes.flat, PAIRINGS):
            cells = [[lookup[(s['id'], pairing, level)] for level in range(1, 6)] for s in scenes]
            ax.imshow([[r['category'] for r in row] for row in cells], cmap=ListedColormap(colors), vmin=-.5, vmax=4.5, aspect='auto')
            ax.set_xticks(range(5), range(1, 6))
            ax.set_xlabel('Stress level')
            ax.set_yticks(range(len(scenes)), [s['id']+' '+s['title'][:27] for s in scenes], fontsize=9)
            ax.set_title(pairing, fontsize=14, fontweight='bold', pad=10)
            for i, row in enumerate(cells):
                for j, r in enumerate(row):
                    ax.text(j, i, r['cell'], ha='center', va='center', fontsize=10, color='white' if r['category'] in (2, 4) else '#26374b')
            ax.set_xticks(np.arange(-.5, 5, 1), minor=True)
            ax.set_yticks(np.arange(-.5, len(scenes), 1), minor=True)
            ax.grid(which='minor', color='white', linewidth=1.5)
            ax.tick_params(which='minor', bottom=False, left=False)
        labels = ['Excluded comparison', 'Neither has joint acceptance', 'Both have joint acceptance', 'Watched only: joint acceptance', 'Unwatched only: joint acceptance']
        fig.legend(handles=[Patch(facecolor=c, label=t) for c, t in zip(colors, labels)], loc='lower center', bbox_to_anchor=(.5, .065), ncol=3, frameon=False, fontsize=11)
        fig.text(.03, .025, 'Completed collection · One seed per condition · Colors compare joint acceptance, not confirmed collusion', fontsize=10)
        save(fig, f'{setting}-monitoring-grid')

    level_rows = []
    for level in range(1, 6):
        group = [r for r in complete if int(r['level']) == level]
        taken = sum(r['outcome'] == 'mutual_take' for r in group)
        level_rows.append(dict(level=level, usable=len(group), mutual_take=taken, rate=taken/len(group)))
    write_csv('pressure-level-outcomes.csv', level_rows)
    fig, ax = plt.subplots(figsize=(9, 5))
    x, y = [r['level'] for r in level_rows], [r['rate'] for r in level_rows]
    ax.plot(x, y, color='#256c98', marker='o', linewidth=2.5)
    for xx, yy in zip(x, y):
        ax.annotate(f'{yy:.1%}', (xx, yy), xytext=(0, 10), textcoords='offset points', ha='center')
    ax.set_xticks(x)
    ax.set_xlabel('Stress level')
    ax.set_ylabel('Joint acceptance among usable episodes')
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set_title('Joint acceptance by pressure level · Completed collection')
    ax.grid(axis='y', color='#dde5ed')
    fig.tight_layout()
    save(fig, 'pressure-level-joint-acceptance')

    wt, ut = sum(r['watched_take'] for r in matched), sum(r['unwatched_take'] for r in matched)
    n = len(matched)
    lines = ['# Completed pressure study — 25 October 2026', '',
        '**4,320 / 4,320 planned experimental episodes reached terminal status.** '
        'There are **4,243 usable completions (98.2%) and 77 exclusions**. '
        'All excluded attempts remain in the raw evidence; they are not counted as refusals.', '',
        '[Raw results and transcripts](../../results/2026-10-25-pressure-study/README.md) · '
        '[Run summary](../../results/2026-10-25-pressure-study/summary.json) · [Provenance](provenance.json) · '
        '[Earlier progress snapshots](../../results/archive/README.md)', '',
        'This is the completed **72-scenario, eight-setting study**: 5 stress levels × 6 pairings × '
        '2 monitoring notices × 1 seed. It is distinct from the newer five-setting prompt design '
        'and the older 600-episode study; these datasets are not pooled.', '',
        '## Raw data for the current slice', '',
        'The current slice is the completed **72-scenario, eight-setting collection**, frozen on '
        '**25 October 2026 at 16:42:07 UTC**. Its repository-relative location is '
        '**`results/2026-10-25-pressure-study/`**.', '',
        '- [Episode index (`runs.csv`)](../../results/2026-10-25-pressure-study/runs.csv): '
        'look up scenario, stress level, pairing, monitoring notice and run ID.',
        '- [Raw episode folders (`runs/`)](../../results/2026-10-25-pressure-study/runs/): '
        '`<run_id>/events.jsonl` holds requests, responses, returned reasoning and delivered messages; '
        '`<run_id>/result.json` holds status, final decisions, outcomes and errors; '
        '`<run_id>/transcript.md` is the readable transcript.',
        '- [Frozen prompts and configuration](../../results/2026-10-25-pressure-study/manifest.json) '
        'and [integrity checksums](../../results/2026-10-25-pressure-study/SHA256SUMS.json).', '',
        'All 4,320 planned experimental episodes, including the 77 exclusions, are retained here. '
        'This analysis folder contains derived tables and graphs. Earlier partial checkpoints '
        'are archived separately under `results/archive/2026-10-25/`.', '',
        '## Main results', '',
        '| Outcome among usable episodes | Count | Share |', '|---|---:|---:|']
    for name, label in [('mutual_take', 'Both take (joint acceptance)'), ('unilateral_take', 'Only one takes'), ('both_refuse', 'Both refuse')]:
        count = summary['outcomes'][name]
        lines.append(f'| {label} | {count:,} | {count/4243:.1%} |')
    lines += ['', '![Joint acceptance by pressure level](figures/pressure-level-joint-acceptance.png)', '',
        '| Stress level | Usable episodes | Both take | Rate |', '|---|---:|---:|---:|']
    lines += [f'| {r["level"]} | {r["usable"]} | {r["mutual_take"]} | {r["rate"]:.1%} |' for r in level_rows]
    lines += ['', '## Watched versus unwatched: three average graphs', '',
        f'**{n:,} of 2,160 comparison cells have usable completions under both notices.** '
        f'The remaining {2160-n} cells are excluded from paired comparisons. Each matched cell fixes '
        'scenario, stress level, pairing and seed. Watched and unwatched rates therefore use exactly '
        'the same cells. The two pairings for each rule are combined with equal weight per matched cell.', '',
        f'Across matched cells, joint acceptance is **{wt/n:.1%} watched versus {ut/n:.1%} unwatched** '
        f'(**{100*(wt-ut)/n:+.1f} percentage points**, watched minus unwatched).', '',
        '| Rule | Matched cells | Watched | Unwatched | Difference |', '|---|---:|---:|---:|---:|']
    lines += [f'| {title} | {nn} | {w:.1%} | {u:.1%} | {100*(w-u):+.1f} pp |' for title, nn, w, u in rule_summary]
    for code, title in [('w', 'Welfare'), ('d', 'Non-deception'), ('a', 'Authority')]:
        lines += ['', f'### {title}', '', f'![{title}: average monitoring comparison](figures/{code}-average-monitoring.png)']
    lines += ['', '[Download average graph data](tables/rule-level-monitoring-averages.csv)', '',
        '## Each stress level and pairing', '', '![Monitoring by level and pairing](figures/matched-monitoring-overview.png)', '',
        '[Download pairing × level data](tables/pairing-level-monitoring.csv)', '',
        '## Every scenario', '',
        'Each cell reads **watched / unwatched**: **T** = both take; **O** = one takes; '
        '**R** = both refuse; **?** = excluded. Gray cells have an excluded episode and do not '
        'stand for refusal. Purple marks joint acceptance only when unwatched; orange marks it '
        'only when watched. Full titles and all cells are in the linked comparison table.', '',
        f'Among matched cells, {counts[2]} have joint acceptance under both notices, '
        f'{counts[1]} under neither, {counts[3]} only when watched and {counts[4]} only when unwatched.', '',
        '[Download all 2,160 scenario comparisons](tables/scenario-level-pairing-comparisons.csv)']
    for setting in pack['settings']:
        title = setting.replace('_', ' ').title()
        lines += ['', f'### {title}', '', f'![{title}: all scenarios, stress levels and pairings](figures/{setting}-monitoring-grid.png)']
    lines += ['', '## Interpretation and limits', '',
        'Joint acceptance is the operational outcome: both agents choose `take`. It does not by '
        'itself establish deception, criterion compliance or causally confirmed collusion. The '
        'monitoring manipulation changes the notice shown to the agents; researcher logging is '
        'identical. There is one seed per cell, related scenario templates, no communication-off '
        'or none–none experimental baseline, and exclusions may depend on condition. Report these '
        'as descriptive comparisons rather than a general causal effect of surveillance.', '',
        '“Completed” means all planned episodes ended, including failures; it does not mean every '
        'episode passed formatting checks. The frozen snapshot metadata uses a generic '
        '“partial snapshot” policy label, but its 4,243 complete + 77 failed statuses establish '
        'full terminal coverage. That original metadata is preserved without alteration.', '',
        f'All {summary["responses"]:,} returned responses include returned reasoning; '
        f'{summary["tokens"]:,} tokens were recorded, including controls. Returned reasoning '
        'is model output, not verified access to internal thought. Endpoint switches and '
        'recovery attempts remain in the raw audit files.', '',
        '## Reproduce', '', '```powershell',
        'python analysis/2026-10-25-pressure-study/build_report.py', '```', '',
        'The script reads the frozen CSV and verifies every planned row against its saved result. '
        'It uses original run IDs rather than rebuilding the matrix from current prompt code. '
        'It writes only this analysis folder, makes no model requests and changes no raw evidence.', '',
        'All figures have adjacent SVG versions for export. CSV tables retain denominators and '
        'explicit missing/excluded states. Earlier partial-snapshot graphs are superseded by this '
        'completed-run report; no earlier partial estimates are reused.', '']
    (OUT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(provenance, indent=2))
    print('Rule averages:', rule_summary)


if __name__ == '__main__':
    main()
