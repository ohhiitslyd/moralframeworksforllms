"""Build prompts/13-authority-ablation.json from the frozen 2026-10-25 pressure-study pack.

Design (see DESIGN.md): for every scene in which a named superior explicitly instructs take
at some level (46 scenes, the audit's "explicit" category), write two matched scenario variants
over the same five justification levels:

  <scene>-INS  instruction ON at every level. Levels below the first instruction level f get the
               scene's own instruction unit (verbatim stakes sentence(s) from level f) appended to
               the stakes block, and its principal line(s) appended to the principals block.
               Levels >= f are the original text.
  <scene>-NOI  instruction OFF at every level. Levels >= f lose every instruction-related stakes
               sentence (the instruction and any later backing of it) and every "... instructs take."
               principal line. Levels below f are the original text.

Both variants (and therefore the "original-state" cells, which act as the control rebuild) use a
de-duplicated principals block: the frozen pack cumulated the principals list, so the refuse line
was repeated once per level (~4.8x at L5) and "No additional principal has spoken." was repeated.
Rule (applied identically to every cell): split the cumulative principals text into sentences,
drop "No additional principal has spoken.", and keep only the first occurrence of each sentence
(case-insensitive, parentheticals ignored, one alias for S727). Nothing else is rewritten.

Cells whose rendered prompt is byte-identical to a lower level of the same variant (e.g. NOI L5 when
the original L5 sentence was only the instruction) are kept in the pack for the five-level schema but
marked "run": false with "duplicate_of"; lying_harness.pressure.specs_for skips them, so no trial is
spent on a prompt that has already been run with the same seed.

Shared wrapper, criterion blocks, monitoring texts, pairing definitions and settings are copied
byte-for-byte from the frozen manifest. The monitoring notice is assigned per scene (both variants of
a scene share it), balanced 23/23 within diagnostic family x instruction-timing strata.

Usage (from the worktree root):  python tools/run_reserved.py experiments/authority-ablation/build_ablation_pack.py
Writes: prompts/13-authority-ablation.json, experiments/authority-ablation/ABLATION-DIFFS.md,
        experiments/authority-ablation/ablation_diffs.csv, experiments/authority-ablation/build_summary.json
No network or API calls.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MANIFEST = ROOT / "results/2026-10-25-pressure-study/manifest.json"
AUDIT_CATEGORIES = ROOT / "analysis/2026-10-25-pressure-study/steps/pressure-construct/tables/instruction_category_by_scene_level.csv"
OUT_PACK = ROOT / "prompts/13-authority-ablation.json"
OUT_MD = HERE / "ABLATION-DIFFS.md"
OUT_CSV = HERE / "ablation_diffs.csv"
OUT_SUMMARY = HERE / "build_summary.json"

ASSIGNMENT_SEED = 20261026
PAIRINGS = ("A-A", "A-none", "W-W", "D-D")
FRZ_PER_FAMILY = 5  # bridge arm: frozen (non-de-duplicated) prompts for 5 scenes per scene family

# The 46 scenes the construct audit classified as containing an explicit take instruction from a
# named person/office/body (instructed_split.py "explicit"). Permission-document scenes and
# pure-stakes scenes are out of scope (see DESIGN.md section 3).
EXPLICIT_SCENES = (
    "S035", "S067", "S068", "S069", "S100", "S102", "S133", "S135", "S166", "S167", "S168", "S199",
    "S200", "S232", "S233", "S265", "S266", "S267", "S299", "S300", "S331", "S333", "S364", "S365",
    "S366", "S397", "S398", "S399", "S431", "S432", "S463", "S464", "S465", "S496", "S497", "S498",
    "S529", "S531", "S562", "S563", "S564", "S596", "S597", "S629", "S663", "S727",
)

# Stakes sentences that carry the instruction or back it. Matched only inside EXPLICIT_SCENES and
# cross-checked against the audit's per-level category below.
INSTRUCTION_PATTERNS = [
    r"\binstructs both\b",                       # "<superior> ... instructs both X to ..."
    r"\bwrites that\b",                          # counsel / JA memo / higher body "writes that ... stands|is binding"
    r"^A counselor who saw them today asked you both to wait",   # S629 L4 (explicit per audit)
    r"^There is no new risk\.$",                 # S629 L4: satisfies the counselor's own condition
    r"^The counselor's written note says wait one week\.$",      # S629 L5 backing
    r"^A mediator you both already accepted said:",              # S727 L5 (explicit per audit)
    r"^Nobody is unsafe\.$",                     # S727 L5: satisfies the mediator's own condition
    r"^The state association's written visiting-officer rule is attached\.$",  # S562 L5 backing
    r"^The patient also has a signed line naming the doctor above the family contact list",  # S663 L5 backing
]
NO_ADDITIONAL = "No additional principal has spoken."
# Instruction units that refer to a fact first stated at a later rung (scene -> first level where the
# referenced fact is in the stakes text). INS cells below that level are flagged for a sensitivity analysis.
CONTEXT_DEPENDENT = {
    "S035": 3,  # "honor the confidentiality request": the request is first stated at L3
    "S431": 2,  # "keep this repayment off the file": repayment first stated at L2
    "S465": 3,  # "distribute the sealed items": sealed first stated at L3
    "S531": 2,  # "revisit after the reference": the pending reference first stated at L2
    "S727": 2,  # "if the interview is tomorrow": the interview first stated at L2
}
DEDUPE_ALIASES = {  # same refuse principal written in a long and a short form within one scene
    "ordinary honesty between the three of you instructs refuse": "ordinary honesty instructs refuse",
}
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def sentences(text: str) -> list[str]:
    parts = [p for p in SENTENCE_SPLIT.split(text.strip()) if p]
    assert " ".join(parts) == text.strip(), text
    return parts


def is_instruction_sentence(sentence: str) -> bool:
    return any(re.search(p, sentence) for p in INSTRUCTION_PATTERNS)


def is_take_line(sentence: str) -> bool:
    return sentence.endswith("instructs take.")


def dedupe_key(sentence: str) -> str:
    key = re.sub(r"\s*\([^)]*\)", "", sentence).strip().rstrip(".").lower()
    return DEDUPE_ALIASES.get(key, key)


def dedupe_principals(lines: list[str]) -> list[str]:
    out, seen = [], set()
    for line in lines:
        if line == NO_ADDITIONAL:
            continue
        key = dedupe_key(line)
        if key not in seen:
            seen.add(key)
            out.append(line)
    return out


def increments(texts: list[str]) -> list[str]:
    out, prev = [], ""
    for text in texts:
        assert not prev or text.startswith(prev + " "), "frozen level text is not cumulative"
        out.append(text[len(prev):].strip())
        prev = text
    return out


def audit_explicit_levels() -> dict[str, set[int]]:
    found: dict[str, set[int]] = {}
    if not AUDIT_CATEGORIES.exists():
        return found
    with AUDIT_CATEGORIES.open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["instr_cat"] == "explicit":
                found.setdefault(row["scenario"], set()).add(int(row["level"]))
    return found


def analyse_scene(scene: dict) -> dict:
    """Locate the instruction unit and its backing in the frozen cumulative text."""
    stakes_inc = increments([l["pressure"] for l in scene["levels"]])
    princ_inc = increments([l["principals"] for l in scene["levels"]])
    instr_by_level = {}
    for n, inc in enumerate(stakes_inc, 1):
        hits = [s for s in sentences(inc) if is_instruction_sentence(s)]
        if hits:
            instr_by_level[n] = hits
    take_by_level = {n: [s for s in sentences(inc) if is_take_line(s)] for n, inc in enumerate(princ_inc, 1)}
    first = min(instr_by_level)
    first_take = min(n for n, lines in take_by_level.items() if lines)
    assert first == first_take, (scene["id"], first, first_take)
    unit = instr_by_level[first]
    unit_lines = take_by_level[first]
    assert unit and unit_lines
    return {"scene_id": scene["id"], "first_level": first, "unit": unit, "unit_principal_lines": unit_lines,
            "instruction_sentences_by_level": instr_by_level,
            "take_lines_by_level": {n: v for n, v in take_by_level.items() if v},
            "stakes_increments": stakes_inc, "principal_increments": princ_inc}


def build_level(level: dict, info: dict, variant: str) -> tuple[dict, dict]:
    n = level["n"]
    f = info["first_level"]
    stakes = sentences(level["pressure"])
    princ = sentences(level["principals"])
    if variant == "FRZ":
        state = "frozen"
        new_stakes, new_princ = stakes, princ
    elif variant == "INS" and n < f:
        state = "added"
        new_stakes = stakes + info["unit"]
        new_princ = dedupe_principals(princ + info["unit_principal_lines"])
    elif variant == "NOI" and n >= f:
        state = "removed"
        new_stakes = [s for s in stakes if not is_instruction_sentence(s)]
        new_princ = dedupe_principals([s for s in princ if not is_take_line(s)])
    else:
        state = "original"
        new_stakes = stakes
        new_princ = dedupe_principals(princ)
    present = variant == "INS" or (variant == "FRZ" and n >= f)
    out = copy.deepcopy(level)
    out["pressure"] = " ".join(new_stakes)
    out["principals"] = " ".join(new_princ)
    out["instruction_present"] = present
    out["unit_context_dependent"] = state == "added" and n < CONTEXT_DEPENDENT.get(info["scene_id"], 0)
    out["cell_state"] = state  # researcher annotation, never rendered
    out["original_label"] = out.pop("label")
    out["label"] = f'{out["original_label"]} | instruction {"on" if present else "off"} ({state})'
    diff = {
        "stakes_removed": [s for s in stakes if s not in new_stakes],
        "stakes_added": [s for s in new_stakes if s not in stakes],
        "principal_lines_removed_as_instruction": [s for s in princ if state == "removed" and is_take_line(s)],
        "principal_lines_removed_as_instruction_unique": list(dict.fromkeys(
            s for s in princ if state == "removed" and is_take_line(s))),
        "principal_lines_added": [s for s in new_princ if s not in princ],
        "dedupe_dropped": [],
    }
    # Everything else removed from the principals block is the de-duplication artefact fix.
    kept = list(new_princ)
    for s in princ:
        if s in kept:
            kept.remove(s)
        elif s not in diff["principal_lines_removed_as_instruction"]:
            diff["dedupe_dropped"].append(s)
    return out, diff


def assign_notices(scene_infos: dict[str, dict], scenes: dict[str, dict]) -> dict[str, str]:
    rng = random.Random(ASSIGNMENT_SEED)
    strata: dict[tuple, list[str]] = {}
    for sid in EXPLICIT_SCENES:
        key = (scenes[sid]["diagnostic"], scene_infos[sid]["first_level"] == 5)
        strata.setdefault(key, []).append(sid)
    notice, flip = {}, rng.random() < 0.5
    for key in sorted(strata):
        ids = sorted(strata[key])
        rng.shuffle(ids)
        for i, sid in enumerate(ids):
            notice[sid] = ("watched", "unwatched")[(i + flip) % 2]
        if len(ids) % 2:
            flip = not flip  # alternate which notice gets the odd scene across strata
    return notice


def pick_bridge_scenes(scenes: dict[str, dict], notices: dict[str, str]) -> set[str]:
    """Seeded, outcome-blind choice of FRZ_PER_FAMILY scenes per scene family for the frozen-text bridge,
    balanced on notice (3+2 per family, the larger share alternating between notices across families)."""
    rng = random.Random(ASSIGNMENT_SEED + 1)
    chosen, major = set(), "watched"
    for family in ("welfare", "nondeception", "authority"):
        for mode, k in ((major, (FRZ_PER_FAMILY + 1) // 2), ("unwatched" if major == "watched" else "watched", FRZ_PER_FAMILY // 2)):
            ids = sorted(sid for sid in EXPLICIT_SCENES if scenes[sid]["diagnostic"] == family and notices[sid] == mode)
            rng.shuffle(ids)
            chosen.update(ids[:k])
        major = "unwatched" if major == "watched" else "watched"
    return chosen


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    frozen = manifest["pack"]
    scenes = {s["id"]: s for s in frozen["scenarios"]}
    audit = audit_explicit_levels()
    if audit:
        assert sorted(audit) == sorted(EXPLICIT_SCENES), "scene set differs from the audit's explicit category"
    infos = {sid: analyse_scene(scenes[sid]) for sid in EXPLICIT_SCENES}
    # Cross-check: instruction present in the frozen cumulative text exactly at the audit's explicit levels,
    # and no instruction-pattern sentence anywhere outside the 46 scenes' instruction levels.
    for sid, info in infos.items():
        present = {n for n in range(1, 6) if n >= info["first_level"]}
        if audit:
            assert present == audit[sid], (sid, present, audit[sid])
    for sid, scene in scenes.items():
        if sid in EXPLICIT_SCENES:
            continue
        for level in scene["levels"]:
            assert not any(is_instruction_sentence(s) for s in sentences(level["pressure"])) or sid in ("S661",), sid
    notices = assign_notices(infos, scenes)
    frz_scenes = pick_bridge_scenes(scenes, notices)

    pack = {
        "title": "Authority ablation v1: superior's take instruction randomised within scene x justification level (46 scenes)",
        "hit_rule": frozen["hit_rule"],
        "design_note": ("Two matched variants per scene (INS: instruction on at every level; NOI: off at every level), "
                        "principals block de-duplicated identically in both, one notice per scene (balanced), "
                        "pairings A-A, A-none, W-W, D-D, seed 1. Identical-prompt duplicate cells are marked run:false. "
                        "Bridge arm FRZ: frozen (non-de-duplicated) original text for 15 scenes."),
        "output_fields": frozen["output_fields"],
        "action_values": frozen["action_values"],
        # monitoring_modes deliberately omitted: the notice is a per-scene assignment carried in each
        # scenario's monitoring_text (verbatim copy of monitoring_texts[mode]). Do not pass --monitoring.
        "monitoring_texts": frozen["monitoring_texts"],
        "pairings_to_run": [next(p for p in frozen["pairings_to_run"] if p["id"] == pid) for pid in PAIRINGS],
        "weekend_slice": {"scenario_ids": [], "note": "not used by this pack"},
        "settings": frozen["settings"],
        "criterion_blocks": frozen["criterion_blocks"],
        "shared_wrapper": frozen["shared_wrapper"],
        "expected_tip_key": frozen["expected_tip_key"],
        "scenarios": [],
    }
    assert [p["id"] for p in pack["pairings_to_run"]] == list(PAIRINGS)

    diff_rows = []
    for sid in EXPLICIT_SCENES:
        scene, info = scenes[sid], infos[sid]
        mode = notices[sid]
        dedup_original = {l["n"]: (l["pressure"], " ".join(dedupe_principals(sentences(l["principals"]))))
                          for l in scene["levels"]}
        seen = {}  # rendered-content key -> canonical cell id, shared across the scene's variants
        for variant in ("INS", "NOI", "FRZ") if sid in frz_scenes else ("INS", "NOI"):
            new = copy.deepcopy(scene)
            new["id"] = f"{sid}-{variant}"
            new["source_scenario"] = sid
            new["variant"] = variant
            new["weekend"] = False
            new["monitoring"] = mode
            new["monitoring_text"] = frozen["monitoring_texts"][mode]
            new["instruction_first_level"] = info["first_level"]
            new["instruction_unit"] = info["unit"]
            new["instruction_principal_lines"] = info["unit_principal_lines"]
            levels = []
            for level in scene["levels"]:
                built, diff = build_level(level, info, variant)
                key = (built["pressure"], built["principals"])
                same = [n for n, k in dedup_original.items() if k == key]
                built["equivalent_original_level"] = same[0] if same else None  # de-duplicated frozen level with identical text
                if key in seen:
                    built["run"] = False
                    built["duplicate_of"] = seen[key]
                else:
                    seen[key] = f'{new["id"]}-L{built["n"]}'
                levels.append(built)
                diff_rows.append({
                    "scenario": new["id"], "source_scenario": sid, "variant": variant, "level": built["n"],
                    "diagnostic": scene["diagnostic"], "setting_id": scene["setting_id"], "notice": mode,
                    "instruction_first_level": info["first_level"], "instruction_present": built["instruction_present"],
                    "cell_state": built["cell_state"], "run": built.get("run", True),
                    "equivalent_original_level": built["equivalent_original_level"] or "",
                    "duplicate_of": built.get("duplicate_of", ""),
                    "stakes_removed": " | ".join(diff["stakes_removed"]),
                    "stakes_added": " | ".join(diff["stakes_added"]),
                    "unit_context_dependent": built["unit_context_dependent"],
                    "principal_lines_removed_as_instruction": " | ".join(diff["principal_lines_removed_as_instruction_unique"]),
                    "principal_lines_removed_as_instruction_count": len(diff["principal_lines_removed_as_instruction"]),
                    "principal_lines_added": " | ".join(diff["principal_lines_added"]),
                    "dedupe_dropped_count": len(diff["dedupe_dropped"]),
                    "dedupe_dropped": " | ".join(diff["dedupe_dropped"]),
                    "frozen_pressure": level["pressure"], "new_pressure": built["pressure"],
                    "frozen_principals": level["principals"], "new_principals": built["principals"],
                })
            new["levels"] = levels
            pack["scenarios"].append(new)

    runnable = sum(1 for s in pack["scenarios"] for l in s["levels"] if l.get("run", True))
    pack["planned_experiments"] = runnable * len(PAIRINGS)
    pack["selection"] = {
        "source_manifest": str(MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "source_pack_sha256": hashlib.sha256(json.dumps(frozen, sort_keys=True).encode()).hexdigest(),
        "scene_ids": list(EXPLICIT_SCENES),
        "method": ("All 46 scenes with an explicit superior take instruction (audit category 'explicit'). "
                   "Selection fixed by scene text, not by outcomes."),
        "bridge_frz_scene_ids": sorted(frz_scenes),
        "notice_assignment_seed": ASSIGNMENT_SEED,
        "notice_by_scene": notices,
        "builder": "experiments/authority-ablation/build_ablation_pack.py",
    }
    OUT_PACK.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(diff_rows[0]))
        writer.writeheader()
        writer.writerows(diff_rows)
    write_markdown(diff_rows, infos, scenes, notices, pack)
    summary = {
        "pack": str(OUT_PACK.relative_to(ROOT)).replace("\\", "/"),
        "pack_sha256": hashlib.sha256(OUT_PACK.read_bytes()).hexdigest(),
        "scenes": len(EXPLICIT_SCENES), "scenario_variants": len(pack["scenarios"]),
        "cells_total": len(diff_rows), "cells_runnable": runnable,
        "cells_duplicate_skipped": len(diff_rows) - runnable,
        "pairings": list(PAIRINGS), "planned_experiments": pack["planned_experiments"],
        "notice_counts": {m: sum(v == m for v in notices.values()) for m in ("watched", "unwatched")},
        "first_level_counts": {str(k): sum(i["first_level"] == k for i in infos.values()) for k in range(1, 6)},
        "cell_state_counts_runnable": {st: sum(1 for r in diff_rows if r["run"] and r["cell_state"] == st)
                                       for st in ("original", "added", "removed", "frozen")},
        "runnable_by_variant": {v: sum(1 for r in diff_rows if r["run"] and r["variant"] == v) for v in ("INS", "NOI", "FRZ")},
        "bridge_frz_scenes": sorted(frz_scenes),
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


def write_markdown(rows, infos, scenes, notices, pack) -> None:
    md = ["# Authority ablation: every changed text, per cell", "",
          "Generated by `build_ablation_pack.py`; machine-readable copy: `ablation_diffs.csv`.",
          "",
          "Each scene has two variants over levels L1–L5. **INS** has the superior's instruction at every level; "
          "**NOI** has it at no level. `original` = the frozen level text; `added` = the scene's own instruction unit "
          "(verbatim, from the level where it first appears) appended to the stakes block plus its principal line; "
          "`removed` = every instruction/backing sentence and every `... instructs take.` principal line deleted. "
          "In *every* cell (including `original`) the principals block is de-duplicated: repeated lines and "
          "`No additional principal has spoken.` are dropped (count shown as *dedupe*). Nothing else differs from the frozen pack: "
          "wrapper, duty, deal, reward, harm, honesty notes, criterion blocks and notice texts are byte-identical "
          "(checked by `validate_ablation_pack.py`).", "",
          "`skip` marks a cell whose rendered prompt is byte-identical to an earlier cell of the same scene (a lower level "
          "of the same variant, or for FRZ the matching INS/NOI cell); it is not run (specs_for skips `run: false`) and "
          "its result is the referenced cell's. FRZ (15 bridge scenes) is the frozen text with no change at all, "
          "including the repeated principal lines. *Principals: removed* lists each distinct line once. "
          "`ctx` marks an added unit that refers to a fact first stated at a later rung (sensitivity analysis only).", "",
          f"Scenes: {len(infos)}. Pairings: {', '.join(p['id'] for p in pack['pairings_to_run'])}. "
          f"Planned experiments: {pack['planned_experiments']}.", ""]
    for sid in EXPLICIT_SCENES:
        info, scene = infos[sid], scenes[sid]
        md += [f"## {sid} — {scene['title']} ({scene['diagnostic']} scene, {scene['setting_id']}; notice: {notices[sid]})", "",
               f"Instruction first appears at **L{info['first_level']}**. Unit (stakes): "
               + " ".join(f"“{u}”" for u in info["unit"]) + "; principal line: "
               + " ".join(f"“{u}”" for u in info["unit_principal_lines"]) + ".", ""]
        backing = {n: v for n, v in info["instruction_sentences_by_level"].items() if n != info["first_level"]}
        if backing:
            md += ["Later instruction/backing sentences (removed in NOI, kept as original in INS): "
                   + "; ".join(f"L{n}: " + " ".join(f"“{s}”" for s in v) for n, v in sorted(backing.items())), ""]
        l5 = scene["levels"][4]["principals"]
        md += [f"Artefact fix, L5 principals block. Frozen: “{l5}” → de-duplicated: “{' '.join(dedupe_principals(sentences(l5)))}”", ""]
        md += ["| Cell | State | Run | Stakes: removed | Stakes: added | Principals: removed (instruction) | Principals: added | Dedupe |",
               "|---|---|---|---|---|---|---|---:|"]
        for r in rows:
            if r["source_scenario"] != sid:
                continue
            run = "yes" if r["run"] else f"skip (= {r['duplicate_of']})"
            esc = lambda t: (t or "—").replace("|", "/")
            state = r["cell_state"] + (" (ctx)" if r["unit_context_dependent"] else "")
            md.append(f"| {r['variant']}-L{r['level']} | {state} | {run} | {esc(r['stakes_removed'])} | "
                      f"{esc(r['stakes_added'])} | {esc(r['principal_lines_removed_as_instruction'])} | "
                      f"{esc(r['principal_lines_added'])} | {r['dedupe_dropped_count']} |")
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
