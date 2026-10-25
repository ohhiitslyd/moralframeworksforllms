"""Offline validation of prompts/13-authority-ablation.json (no API calls, no network).

Run from the worktree root:  python tools/run_reserved.py experiments/authority-ablation/validate_ablation_pack.py

Checks
  1. Pack-level text (shared_wrapper, criterion_blocks, monitoring_texts, settings, pairing objects) is
     identical to the frozen pack in results/2026-10-25-pressure-study/manifest.json.
  2. specs_for: count == planned_experiments (1,704), unique run_ids, every runnable cell x pairing present.
  3. Every prompt renders for agents A and B (initial_prompt), contains its notice text, and leaks no
     researcher annotation.
  4. INS vs NOI, same scene x level x pairing x agent: everything outside the stakes and principals blocks
     is byte-identical; NOI stakes == INS stakes minus instruction sentences; NOI principals == INS principals
     minus "... instructs take." lines; the removed items are the scene's own instruction/backing text.
  5. Every INS/NOI cell vs the frozen original prompt of the same scene/level/pairing/notice: outside the two
     blocks byte-identical; stakes differ only by the instruction unit/backing; principals differ only by
     take lines and the de-duplication rule (dropped lines are repeats or "No additional principal has spoken.").
  6. FRZ cells are byte-identical to the frozen prompts.
  7. Cells marked run:false render byte-identically to the cell named in duplicate_of; no two runnable
     cells share a prompt.
  8. `python -m lying_harness.pressure --plan` reports the same episode count.
  9. tests/test_pressure.py passes (pytest if installed, otherwise unittest, which runs the same tests).
Writes analysis_pairs.csv (the pre-registered pair table) and validation_report.json next to this file.
"""
from __future__ import annotations

import copy
import csv
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from lying_harness.pressure import specs_for, initial_prompt  # noqa: E402
import build_ablation_pack as B  # noqa: E402

PACK = ROOT / "prompts/13-authority-ablation.json"
BLOCKS = re.compile(r"Principals who have spoken in this episode:\n(?P<principals>.*?)\n\nStakes in this episode:\n"
                    r"(?P<stakes>.*?)\n(?P<notice>[^\n]*)\nBefore you choose", re.S)
LEAK_KEYS = ("cell_state", "instruction_present", "duplicate_of", "original_label", "unit_context_dependent",
             "equivalent_original_level", "expected_first_take", "welfare_if_take", "source_scenario")

failures: list[str] = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


def split_prompt(prompt):
    m = BLOCKS.search(prompt)
    assert m, "wrapper blocks not found"
    rest = prompt[:m.start("principals")] + "<P>" + prompt[m.end("principals"):m.start("stakes")] + "<S>" + prompt[m.end("stakes"):]
    return rest, B.sentences(m.group("principals")), B.sentences(m.group("stakes"))


def minus(seq, removed_pred):
    return [s for s in seq if not removed_pred(s)]


def main():
    frozen = json.loads(B.MANIFEST.read_text(encoding="utf-8"))["pack"]
    pack = json.loads(PACK.read_text(encoding="utf-8-sig"))
    frozen_scenes = {s["id"]: s for s in frozen["scenarios"]}
    infos = {sid: B.analyse_scene(frozen_scenes[sid]) for sid in B.EXPLICIT_SCENES}
    scenes = {s["id"]: s for s in pack["scenarios"]}

    # 1. pack-level text identical
    for key in ("shared_wrapper", "criterion_blocks", "monitoring_texts", "settings", "hit_rule"):
        check(pack[key] == frozen[key], f"pack field {key} differs from frozen pack")
    for p in pack["pairings_to_run"]:
        check(p == next(q for q in frozen["pairings_to_run"] if q["id"] == p["id"]), f"pairing {p['id']} differs")
    for s in pack["scenarios"]:
        src = frozen_scenes[s["source_scenario"]]
        for key in src:
            if key in ("id", "levels", "weekend", "monitoring", "monitoring_text"):
                continue
            check(s[key] == src[key], f"{s['id']} scene field {key} differs")
        check(s["monitoring_text"] == frozen["monitoring_texts"][s["monitoring"]], f"{s['id']} notice text not verbatim")
        for lvl, src_lvl in zip(s["levels"], src["levels"]):
            for key in ("n", "welfare_if_take", "deceive_if_take", "deceive_if_refuse"):
                check(lvl[key] == src_lvl[key], f"{s['id']} L{lvl['n']} field {key} differs")

    # 2. specs
    specs = specs_for(pack)
    ids = [s["run_id"] for s in specs]
    check(len(specs) == pack["planned_experiments"], f"specs {len(specs)} != planned {pack['planned_experiments']}")
    check(len(set(ids)) == len(ids), "duplicate run_ids")
    runnable = [(s["id"], l["n"]) for s in pack["scenarios"] for l in s["levels"] if l.get("run", True)]
    check(len(specs) == len(runnable) * len(pack["pairings_to_run"]), "spec count != runnable cells x pairings")
    check(set((s["scenario"], s["level"], s["pairing"]) for s in specs) ==
          {(c, n, p["id"]) for c, n in runnable for p in pack["pairings_to_run"]}, "spec set != runnable cell set")

    # Render every cell (runnable or not) for every pairing and agent.
    def cell_spec(scenario, n, pairing):
        return {"run_id": f"{scenario['id']}-L{n}-{pairing['id']}-s1", "scenario": scenario["id"], "level": n,
                "pairing": pairing["id"], "a": pairing["a"], "b": pairing["b"], "seed": 1, "control": False,
                "monitoring": scenario["monitoring"]}

    def frozen_spec(sid, n, pairing, mode):
        return {"run_id": "x", "scenario": sid, "level": n, "pairing": pairing["id"], "a": pairing["a"],
                "b": pairing["b"], "seed": 1, "control": False, "monitoring": mode}

    prompts, frozen_prompts = {}, {}
    for s in pack["scenarios"]:
        for lvl in s["levels"]:
            for p in pack["pairings_to_run"]:
                for agent in ("A", "B"):
                    text = initial_prompt(pack, cell_spec(s, lvl["n"], p), agent)
                    prompts[(s["id"], lvl["n"], p["id"], agent)] = text
                    fk = (s["source_scenario"], lvl["n"], p["id"], agent)
                    if fk not in frozen_prompts:
                        frozen_prompts[fk] = initial_prompt(frozen, frozen_spec(s["source_scenario"], lvl["n"], p, s["monitoring"]), agent)
    rendered_specs = 0
    for spec in specs:  # the actual specs_for objects
        for agent in ("A", "B"):
            text = initial_prompt(pack, spec, agent)
            rendered_specs += 1
            check(text == prompts[(spec["scenario"], spec["level"], spec["pairing"], agent)], f"{spec['run_id']} render mismatch")

    # 3. notice + leakage
    for (cid, n, pid, agent), text in prompts.items():
        sc = scenes[cid]
        check(pack["monitoring_texts"][sc["monitoring"]] in text, f"{cid} L{n} notice missing")
        other = "unwatched" if sc["monitoring"] == "watched" else "watched"
        check(pack["monitoring_texts"][other] not in text, f"{cid} L{n} wrong notice present")
        lvl = sc["levels"][n - 1]
        # (original labels such as "five jobs" are plain phrases that also occur in the stakes text; the
        # wrapper never renders {label}, so only the new composite label is checked)
        check(lvl["label"] not in text, f"{cid} L{n} label leaked")
        for key in LEAK_KEYS:
            check(key not in text, f"{cid} L{n} leaks {key}")

    # 4 + 5 + 6
    pair_checks = frozen_checks = frz_checks = 0
    length = {"INS": [], "NOI": []}
    for sid in B.EXPLICIT_SCENES:
        info = infos[sid]
        instr_all = {x for v in info["instruction_sentences_by_level"].values() for x in v}
        take_all = {x for v in info["take_lines_by_level"].values() for x in v}
        for n in range(1, 6):
            for p in pack["pairings_to_run"]:
                for agent in ("A", "B"):
                    ins = prompts[(f"{sid}-INS", n, p["id"], agent)]
                    noi = prompts[(f"{sid}-NOI", n, p["id"], agent)]
                    fro = frozen_prompts[(sid, n, p["id"], agent)]
                    length["INS"].append(len(ins)); length["NOI"].append(len(noi))
                    r_i, p_i, s_i = split_prompt(ins)
                    r_n, p_n, s_n = split_prompt(noi)
                    r_f, p_f, s_f = split_prompt(fro)
                    tag = f"{sid} L{n} {p['id']} {agent}"
                    check(r_i == r_n == r_f, f"{tag}: text outside stakes/principals differs")
                    check(s_n == minus(s_i, lambda x: x in instr_all), f"{tag}: NOI stakes != INS stakes minus instruction")
                    check(set(s_i) - set(s_n) <= instr_all and set(s_i) - set(s_n), f"{tag}: INS-NOI stakes diff not instruction-only/empty")
                    check(p_n == minus(p_i, lambda x: x in take_all), f"{tag}: NOI principals != INS principals minus take lines")
                    check(set(p_i) - set(p_n) and set(p_i) - set(p_n) <= take_all, f"{tag}: INS-NOI principals diff not take-only/empty")
                    pair_checks += 1
                    # 5. each variant vs frozen original
                    dedup_f = B.dedupe_principals(p_f)
                    dropped = list(p_f)
                    for x in dedup_f:
                        dropped.remove(x)
                    check(all(x == B.NO_ADDITIONAL or B.dedupe_key(x) in {B.dedupe_key(y) for y in dedup_f} for x in dropped),
                          f"{tag}: de-duplication dropped a non-repeat line")
                    for variant, s_v, p_v in (("INS", s_i, p_i), ("NOI", s_n, p_n)):
                        unit = set(info["unit"]) | instr_all
                        check(minus(s_v, lambda x: x in unit) == minus(s_f, lambda x: x in unit),
                              f"{tag} {variant}: stakes differ from frozen beyond the instruction")
                        check(minus(p_v, lambda x: x in take_all) == minus(dedup_f, lambda x: x in take_all),
                              f"{tag} {variant}: principals differ from de-duplicated frozen beyond take lines")
                        frozen_checks += 1
                    if (f"{sid}-FRZ", n, p["id"], agent) in prompts:
                        check(prompts[(f"{sid}-FRZ", n, p["id"], agent)] == fro, f"{tag}: FRZ not byte-identical to frozen")
                        frz_checks += 1

    # 7. duplicates
    by_prompt = {}
    for s in pack["scenarios"]:
        for lvl in s["levels"]:
            key = tuple(prompts[(s["id"], lvl["n"], p["id"], a)] for p in pack["pairings_to_run"] for a in ("A", "B"))
            if lvl.get("run", True):
                check(key not in by_prompt, f"{s['id']} L{lvl['n']} duplicates runnable {by_prompt.get(key)}")
                by_prompt[key] = f"{s['id']}-L{lvl['n']}"
    for s in pack["scenarios"]:
        for lvl in s["levels"]:
            if not lvl.get("run", True):
                cid, ln = lvl["duplicate_of"].rsplit("-L", 1)
                for p in pack["pairings_to_run"]:
                    for a in ("A", "B"):
                        check(prompts[(s["id"], lvl["n"], p["id"], a)] == prompts[(cid, int(ln), p["id"], a)],
                              f"{s['id']} L{lvl['n']} not identical to {lvl['duplicate_of']}")

    # Pair table for the pre-registered analysis.
    def canonical(cid, n):
        lvl = scenes[cid]["levels"][n - 1]
        return lvl.get("duplicate_of") or f"{cid}-L{n}"

    rows, seen = [], set()
    for sid in B.EXPLICIT_SCENES:
        info = infos[sid]
        rung, rungs = 0, {}
        for n, inc in enumerate(info["stakes_increments"], 1):
            if [x for x in B.sentences(inc) if not B.is_instruction_sentence(x)]:
                rung += 1
            rungs[n] = rung
        for n in range(1, 6):
            ins_c, noi_c = canonical(f"{sid}-INS", n), canonical(f"{sid}-NOI", n)
            unique = (ins_c, noi_c) not in seen
            seen.add((ins_c, noi_c))
            ins_lvl = scenes[f"{sid}-INS"]["levels"][n - 1]
            noi_lvl = scenes[f"{sid}-NOI"]["levels"][n - 1]
            for p in pack["pairings_to_run"]:
                rows.append({"source_scenario": sid, "diagnostic": scenes[f"{sid}-INS"]["diagnostic"],
                             "setting_id": scenes[f"{sid}-INS"]["setting_id"], "notice": scenes[f"{sid}-INS"]["monitoring"],
                             "level": n, "stakes_rung": rungs[n], "instruction_first_level": info["first_level"],
                             "original_state": "INS" if n >= info["first_level"] else "NOI",
                             "pairing": p["id"], "unique_pair": unique,
                             "ins_run_id": f"{ins_c}-{p['id']}-s1", "noi_run_id": f"{noi_c}-{p['id']}-s1",
                             "ins_cell_state": ins_lvl["cell_state"], "noi_cell_state": noi_lvl["cell_state"],
                             "ins_has_backing": any(x in {y for m, v in info["instruction_sentences_by_level"].items()
                                                          if m != info["first_level"] for y in v}
                                                    for x in B.sentences(ins_lvl["pressure"])),
                             "unit_context_dependent": ins_lvl["unit_context_dependent"],
                             "frz_run_id": (f"{canonical(sid + '-FRZ', n)}-{p['id']}-s1" if f"{sid}-FRZ" in scenes else ""),
                             "frozen_study_run_id": f"{sid}-L{n}-{p['id']}-s1-{scenes[sid + '-INS']['monitoring']}"})
    spec_ids = set(ids)
    for r in rows:
        check(r["ins_run_id"] in spec_ids and r["noi_run_id"] in spec_ids, f"pair {r['ins_run_id']} / {r['noi_run_id']} not in specs")
        if r["frz_run_id"]:
            check(r["frz_run_id"] in spec_ids, f"bridge {r['frz_run_id']} not in specs")
    with (HERE / "analysis_pairs.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # 8. harness CLI --plan (no network: returns before loading credentials)
    plan = subprocess.run([sys.executable, "-m", "lying_harness.pressure", "--pack", str(PACK),
                           "--output", str(HERE / "_plan_unused"), "--order-seed", "20261026", "--plan"],
                          cwd=ROOT, capture_output=True, text=True)
    plan_out = json.loads(plan.stdout.strip().splitlines()[-1]) if plan.returncode == 0 else {"error": plan.stderr[-500:]}
    check(plan_out.get("episodes") == pack["planned_experiments"], f"--plan reported {plan_out}")
    check(not (HERE / "_plan_unused").exists(), "--plan created an output folder")

    # 9. tests
    if importlib.util.find_spec("pytest"):
        test = subprocess.run([sys.executable, "-m", "pytest", "tests/test_pressure.py", "-q"], cwd=ROOT,
                              capture_output=True, text=True)
        runner = "pytest"
    else:
        test = subprocess.run([sys.executable, "-m", "unittest", "tests.test_pressure", "-q"], cwd=ROOT,
                              capture_output=True, text=True)
        runner = "unittest (pytest not installed in this interpreter)"
    test_tail = (test.stdout + test.stderr).strip().splitlines()[-3:]
    check(test.returncode == 0, f"tests failed: {test_tail}")

    uniq = [r for r in rows if r["unique_pair"]]
    report = {
        "ok": not failures, "failures": failures[:50], "n_failures": len(failures),
        "failure_kinds": dict(Counter(re.sub(r"S\d{3}\S*|L\d|A-A|A-none|W-W|D-D| [AB]:", "", f) for f in failures)),
        "planned_experiments": pack["planned_experiments"], "specs": len(specs), "unique_run_ids": len(set(ids)),
        "specs_by_pairing": dict(Counter(s["pairing"] for s in specs)),
        "specs_by_variant": dict(Counter(s["scenario"].rsplit("-", 1)[1] for s in specs)),
        "specs_by_notice": dict(Counter(s["monitoring"] for s in specs)),
        "prompts_rendered_specs_x_agents": rendered_specs, "cell_prompts_rendered": len(prompts),
        "ins_noi_pair_checks": pair_checks, "variant_vs_frozen_checks": frozen_checks, "frz_byte_identity_checks": frz_checks,
        "pairs_rows": len(rows), "unique_pairs": len(uniq),
        "unique_pairs_by_pairing": dict(Counter(r["pairing"] for r in uniq)),
        "unique_pairs_by_original_state": dict(Counter(r["original_state"] for r in uniq)),
        "unique_pairs_by_stakes_rung": dict(sorted(Counter(r["stakes_rung"] for r in uniq).items())),
        "mean_prompt_chars": {k: round(sum(v) / len(v)) for k, v in length.items()},
        "harness_plan": plan_out, "tests": {"runner": runner, "returncode": test.returncode, "tail": test_tail},
    }
    (HERE / "validation_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
