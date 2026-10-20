#!/usr/bin/env python3
"""Slice the case master into cumulative per-lesson snapshots.

Run from this folder:  python3 slice_case.py
Regenerate after ANY edit to the master - the slices are derived files.
"""
import copy
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

MASTER = "Case_Your_Electricity_Bill_MASTER.ipynb"
CHAPTER_RE = re.compile(r"^#{1,2} Chapter (\d)")
OUT_NAME = "Case_Your_Electricity_Bill_after_Lesson_{n}.ipynb"
TITLE_SUFFIX = " - after Lesson {n}"
TEASER = (
    "### To be continued\n"
    "The case grows with the course: the next chapter unlocks after **Lesson {next_n}** - {next_title}"
)


def main():
    nb = json.load(open(os.path.join(HERE, MASTER)))
    cells = nb["cells"]

    starts = {}
    titles = {}
    for i, c in enumerate(cells):
        if c["cell_type"] != "markdown":
            continue
        first = "".join(c["source"]).strip().splitlines()[0] if c["source"] else ""
        m = CHAPTER_RE.match(first)
        if m:
            n = int(m.group(1))
            starts[n] = i
            titles[n] = re.sub(r"^(Kapitel \d+ \(efter lektion \d+\):|Chapter \d+ -)\s*", "", re.sub(r"^#+\s*", "", first).strip()).strip()
            titles[n] = re.sub(r"\s*\*\(after Lesson[^)]*\)\*\s*$", "", titles[n]).strip()
    assert sorted(starts) == list(range(1, 9)), f"chapters found: {sorted(starts)}"

    for n in range(1, 9):
        end = starts[n + 1] if n < 8 else len(cells)
        slice_cells = copy.deepcopy(cells[:end])
        # mark the title so students can see which snapshot they have
        s0 = "".join(slice_cells[0]["source"])
        lines = s0.splitlines()
        lines[0] = lines[0] + TITLE_SUFFIX.format(n=n)
        slice_cells[0]["source"] = ("\n".join(lines) + "\n").splitlines(keepends=True)
        if n < 8:
            slice_cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": TEASER.format(next_n=n + 1, next_title=titles[n + 1]).splitlines(keepends=True),
            })
        out = {
            "cells": slice_cells,
            "metadata": nb["metadata"],
            "nbformat": nb["nbformat"],
            "nbformat_minor": nb["nbformat_minor"],
        }
        path = os.path.join(HERE, OUT_NAME.format(n=n))
        with open(path, "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"{OUT_NAME.format(n=n)}: {len(slice_cells)} cells")


if __name__ == "__main__":
    main()
