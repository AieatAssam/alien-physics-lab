#!/usr/bin/env python3
"""Generate a fake lab repository for LOCAL DEVELOPMENT of the site only.

Everything written here is invented. Never deploy or publish its output.

Usage:
    python site/fixtures/make_fixture.py /tmp/fx
    python site/build_data.py --repo /tmp/fx --out site/public/data

Python 3.12, standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import shutil
from pathlib import Path

LABS = {
    "lab-a": ("orbit-harness", "model-alpha",
              "A cautious experimentalist.\nRepeats every run twice before trusting it."),
    "lab-b": ("orbit-harness", "model-beta",
              "A bold theorist.\nPrefers one striking run to a dozen dull ones."),
    "lab-c": ("grid-harness", "model-gamma",
              "A sceptic.\nTries hard to falsify every claim it reads."),
}
NIGHTS = ["2026-11-01", "2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06"]
SPECIES = ["A", "B", "C"]
DURATION = 20.0
DT = 0.05
L = 10.0
PURPOSES = [
    "measure radial decay of a single orbiter",
    "test whether three-body orbits conserve energy",
    "probe collisions in a crowded chamber",
    "check the inverse-square prediction at short range",
]


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def simulate(rng: random.Random, n: int, vanish_id: int | None):
    cx = L / 2 + rng.uniform(-0.6, 0.6)
    cy = L / 2 + rng.uniform(-0.6, 0.6)
    parts = [
        {
            "id": i,
            "species": SPECIES[i % 3],
            "r": rng.uniform(1.2, 3.6),
            "w": rng.choice([-1, 1]) * rng.uniform(0.5, 1.4),
            "ph": rng.uniform(0, 2 * math.pi),
        }
        for i in range(n)
    ]
    vanish_t = round(DURATION * rng.uniform(0.4, 0.7), 4)
    steps = int(round(DURATION / DT))
    samples = []
    for k in range(steps + 1):
        t = round(k * DT, 4)
        ps = []
        for p in parts:
            if vanish_id == p["id"] and t >= vanish_t:
                continue
            x = cx + p["r"] * math.cos(p["w"] * t + p["ph"])
            y = cy + p["r"] * math.sin(p["w"] * t + p["ph"])
            x = min(max(x, 0.0), L)
            y = min(max(y, 0.0), L)
            ps.append({"id": p["id"], "species": p["species"], "pos": [round(x, 4), round(y, 4)]})
        samples.append({"t": t, "particles": ps})
    events = []
    if vanish_id is not None:
        events.append({"t": vanish_t, "type": "vanish", "id": vanish_id})
    for _ in range(rng.randint(1, 3)):
        events.append({"t": round(rng.uniform(1, DURATION - 1), 4), "type": "collision",
                       "id": rng.randrange(n)})
    events.sort(key=lambda e: e["t"])
    return samples, events


def biased(samples, bias: float):
    out = []
    for s in samples:
        ps = []
        for p in s["particles"]:
            x, y = p["pos"]
            ps.append({"id": p["id"], "species": p["species"],
                       "pos": [round(min(max(x + bias * math.sin(s["t"]), 0), L), 4),
                               round(min(max(y - bias * math.cos(s["t"]), 0), L), 4)]})
        out.append({"t": s["t"], "particles": ps})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path, help="fixture repo directory to (re)create")
    args = ap.parse_args()
    root: Path = args.out
    rng = random.Random(7)

    for sub in ("labs", "results", "requests", "predictions", "papers", "reviews",
                "ledger", "scores", "protocol", "seasons", "events.jsonl"):
        target = root / sub
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    root.mkdir(parents=True, exist_ok=True)

    # labs
    for lab, (harness, model, persona) in LABS.items():
        persona_lines = "\n".join("  " + ln for ln in persona.splitlines())
        write_text(root / "labs" / lab / "lab.yml",
                   f"harness: {harness}\nmodel: {model}\npersona: |\n{persona_lines}\n")
        notes = "\n\n".join(
            f"## Night {i + 1}\n\nRan the planned sweep. Residuals stayed within the expected band and "
            f"the energy drift was small. Next I want to repeat the close-approach runs with a finer "
            f"sample step, because the vanish events cluster near the chamber wall in the {lab} setup."
            for i in range(len(NIGHTS))
        )
        write_text(root / "labs" / lab / "NOTEBOOK.md", "# Notebook\n\n" + notes + "\n")

    # experiments: (lab, name, n_particles, vanish_id, status)
    specs = [
        ("lab-a", "orbit-01", 3, None, "ok"),
        ("lab-a", "orbit-02", 4, 1, "ok"),
        ("lab-a", "orbit-03", 2, None, "ok"),
        ("lab-a", "orbit-04", 5, 0, "ok"),
        ("lab-a", "orbit-05", 3, None, "ok"),
        ("lab-b", "orbit-01", 6, 2, "ok"),
        ("lab-b", "orbit-02", 3, None, "ok"),
        ("lab-b", "orbit-03", 4, None, "ok"),
        ("lab-b", "orbit-04", 2, 0, "ok"),
        ("lab-c", "grid-01", 4, None, "ok"),
        ("lab-c", "grid-02", 3, 1, "ok"),
        ("lab-c", "grid-03", 5, None, "ok"),
        ("lab-c", "grid-04", 2, None, "failed"),
    ]
    predicted_ids = {"lab-a/orbit-03", "lab-b/orbit-02"}
    for i, (lab, name, n, vanish_id, status) in enumerate(specs):
        rid = f"{lab}/{name}"
        purpose = PURPOSES[i % len(PURPOSES)]
        write_json(root / "requests" / lab / f"{name}.json", {
            "request_id": rid, "lab": lab, "purpose": purpose,
            "L": L, "duration": DURATION, "sample_dt": DT,
        })
        samples, events = simulate(rng, n, vanish_id)
        if status != "ok":
            write_json(root / "results" / lab / f"{name}.json",
                       {"request_id": rid, "status": status, "error": "fake failure for testing"})
            continue
        write_json(root / "results" / lab / f"{name}.json",
                   {"request_id": rid, "status": "ok", "samples": samples, "events": events})
        if rid in predicted_ids:
            write_json(root / "predictions" / "public" / lab / f"{name}.json",
                       {"request_id": rid, "samples": biased(samples, 0.2)})

    # papers
    papers = [
        ("P-0001", "lab-a", "accepted", 0.82, 0.90, [], ["lab-a/orbit-03"],
         "Radial decay follows the predicted curve"),
        ("P-0002", "lab-b", "contested", 0.61, 0.58, [], ["lab-b/orbit-02"],
         "Three-body energy is conserved to a tight tolerance"),
        ("P-0003", "lab-b", "submitted", 0.44, 0.50, [], ["lab-b/orbit-03"],
         "Close approaches scatter without loss"),
        ("P-0004", "lab-c", "accepted", 0.77, 0.85, ["P-0003"], ["lab-c/grid-01"],
         "Grid collisions obey a sharper inverse law"),
        ("P-0005", "lab-a", "retracted", 0.39, 0.40, [], ["lab-a/orbit-04"],
         "Vanishing particles leave a residual field"),
    ]
    status_events = []
    for pid, lab, status, skill, cal, supersedes, evidence, title in papers:
        md = (
            f"# {title}\n\n"
            "We report a series of runs in the simulated chamber. The main observation is stated "
            "below, followed by the evidence we rely on.\n\n"
            "- the sweep used a fixed sample step\n"
            "- residuals were computed per species\n"
            "- see the [harness notes](https://example.com/harness) for setup\n\n"
            "<script>alert('not rendered')</script>\n\n"
            "Discussion: the result is consistent across repeats, although the tail of the distribution "
            "is heavier than the simplest model allows.\n"
        )
        write_text(root / "papers" / pid / "paper.md", md)
        write_json(root / "papers" / pid / "claim.json", {
            "title": title, "lab": lab,
            "claims": [{
                "statement": f"{title.lower()} within a 5 percent tolerance",
                "domain": "orbital dynamics",
                "evidence": evidence,
                "predicted_error": round(rng.uniform(0.02, 0.12), 3),
            }],
            "cites": [p[0] for p in papers if p[0] < pid][:1],
            "supersedes": supersedes,
        })
        write_json(root / "papers" / pid / "status.json", {"status": status, "skill": skill, "calibration": cal, "lab": lab})
        status_events.append((pid, lab, status))

    # reviews (file per reviewing lab; standing file optional)
    write_json(root / "reviews" / "P-0002" / "lab-c.json", {
        "lab": "lab-c", "verdict": "falsified",
        "comment": "The energy drift is larger than claimed in the third sweep.",
        "evidence": ["lab-b/orbit-02"],
    })
    write_json(root / "reviews" / "P-0002" / "lab-c.standing.json", {"standing": "supported"})
    write_json(root / "reviews" / "P-0002" / "lab-a.json", {
        "lab": "lab-a", "verdict": "supported",
        "comment": "Repeated the close-approach run and reproduced the energy plateau.",
        "evidence": ["lab-b/orbit-02"],
    })
    write_json(root / "reviews" / "P-0002" / "lab-a.standing.json", {"standing": "supported"})
    write_json(root / "reviews" / "P-0005" / "lab-c.json", {
        "lab": "lab-c", "verdict": "falsified",
        "comment": "The residual field disappears when the vanish events are filtered.",
        "evidence": ["lab-a/orbit-04"],
    })
    write_json(root / "reviews" / "P-0005" / "lab-c.standing.json", {"standing": "unsupported"})
    write_json(root / "reviews" / "P-0004" / "lab-a.json", {
        "lab": "lab-a", "verdict": "inconclusive",
        "comment": "Needs a longer sweep before the exponent can be trusted.",
        "evidence": ["lab-c/grid-01"],
    })

    # ledgers
    for lab in LABS:
        entries = []
        for i, night in enumerate(NIGHTS):
            entries.append({
                "date": night,
                "research_used": 4 + i * 2 + (1 if lab == "lab-b" else 0),
                "review_used": 1 + (i % 3),
                "research_allowance": 40,
                "review_allowance": 15,
            })
        write_json(root / "ledger" / f"{lab}.json", {"entries": entries})

    # scores: knowledge index and coverage rise over six nights
    ki = [0.21, 0.34, 0.42, 0.47, 0.55, 0.61]
    cov = [0.12, 0.20, 0.31, 0.38, 0.44, 0.50]
    pids = [p[0] for p in papers]
    for i, night in enumerate(NIGHTS):
        write_json(root / "scores" / f"{night}.json", {
            "date": night,
            "knowledge_index": ki[i],
            "coverage": cov[i],
            "papers": {pid: {"skill": round(0.5 + 0.05 * i, 3), "calibration": round(0.5 + 0.04 * i, 3)}
                       for pid in pids[: 2 + i // 2]},
        })

    # events.jsonl, one row per status change, dated over the nights
    lines = []
    for i, (pid, lab, status) in enumerate(status_events):
        date = NIGHTS[min(i, len(NIGHTS) - 1)]
        lines.append(json.dumps({
            "date": date, "paper_id": pid, "lab": lab, "status": status,
            "cause": "replicated in an independent run" if status == "accepted" else "review outcome",
        }))
    if status_events:
        lines.append(json.dumps({"date": NIGHTS[-1], "paper_id": "P-0005", "lab": "lab-a",
                                 "status": "retracted", "cause": "residual traced to a filtering bug"}))
    write_text(root / "events.jsonl", "\n".join(lines) + "\n")

    # protocol and season reveal
    write_json(root / "protocol" / "season.json", {
        "season": 1, "night": 7, "difficulty": "standard",
        "L": L, "species": SPECIES,
    })
    write_json(root / "seasons" / "1" / "reveal.json", {
        "structural_score": 0.71,
        "items": [
            {"name": "inverse-square force", "kind": "law",
             "true_law": "F = k / r^2", "believed_law": "F = k / r^2.04", "status": "partly"},
            {"name": "energy conservation", "kind": "law",
             "true_law": "E is conserved", "believed_law": "E is conserved", "status": "discovered"},
            {"name": "collision damping", "kind": "law",
             "true_law": "damping ~ v", "believed_law": "no damping found", "status": "missed"},
        ],
    })

    print(f"make_fixture: wrote fake repo to {root}")


if __name__ == "__main__":
    main()
