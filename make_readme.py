"""Regenerate README.md with an Open-in-Colab badge for every notebook.

Run from the repo root after adding or renaming notebooks:
    python3 make_readme.py
"""
from pathlib import Path
from urllib.parse import quote

OWNER, REPO, BRANCH = "CNielsen94", "applied-math-aaubs", "main"
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

def colab_url(path):
    return f"https://colab.research.google.com/github/{OWNER}/{REPO}/blob/{BRANCH}/{quote(path)}"

def title(nb):
    name = nb.stem
    for tag in ["_(Anvendt_mat,_HA2026)", "_(Applied_Math,_EBA2026)"]:
        name = name.replace(tag, "")
    return name.replace("_", " ")

def order(nb):
    n = nb.name
    if "Introduk" in n or "Introduction" in n: return (0, n)
    if n.startswith("Supplement"): return (1, n)
    if "velser" in n or "Exercises" in n: return (3, n)
    return (2, n)

def section(root, heading, folders):
    lines = [f"## {heading}", ""]
    for folder, label in folders:
        nbs = sorted((root / folder).glob("*.ipynb"), key=order)
        if not nbs:
            continue
        lines += [f"### {label}", "", "| Notebook | Open |", "|---|---|"]
        for nb in nbs:
            rel = nb.as_posix()
            lines.append(f"| [{title(nb)}]({quote(rel)}) | [![Open in Colab]({BADGE})]({colab_url(rel)}) |")
        lines.append("")
    return lines

DA = [("lektion-1-intro-og-funktioner", "Lektion 1: Introduktion, funktioner og differentiering (+ Supplement A/B/C)"),
      ("lektion-2-funktioner-fortsat", "Lektion 2: Funktioner og differentiering, fortsat"),
      ("lektion-3-optimering", "Lektion 3: Optimering"),
      ("lektion-4-funktioner-af-flere-variable", "Lektion 4: Funktioner af flere variable"),
      ("lektion-5-lineaere-ligninger", "Lektion 5: Lineære ligninger"),
      ("lektion-6-vektorer-og-matricer", "Lektion 6: Vektorer og matricer"),
      ("lektion-7-matrix-multiplikation", "Lektion 7: Matrix-multiplikation"),
      ("lektion-8-inverse-matricer-og-determinanter", "Lektion 8: Inverse matricer og determinanter"),
      ("case", "Case: Din elregning (kumulative udsnit efter hver lektion)")]
EN = [("intro", "Introduction to Python (+ Supplement A/B/C)"),
      ("lesson-1-linear-equations", "Lesson 1: Linear equations"),
      ("lesson-2-vectors-and-matrices", "Lesson 2: Vectors and matrices"),
      ("lesson-3-matrix-multiplication", "Lesson 3: Matrix multiplication"),
      ("lesson-4-inverse-matrices-determinants", "Lesson 4: Inverse matrices and determinants"),
      ("lesson-5-functions-differentiation", "Lesson 5: Functions and differentiation"),
      ("lesson-6-functions-continued", "Lesson 6: Functions and differentiation, continued"),
      ("lesson-7-optimization", "Lesson 7: Optimization"),
      ("lesson-8-multivariable-functions", "Lesson 8: Multivariable functions"),
      ("case", "Case: Your electricity bill (cumulative slices after each lesson)")]

head = """# Applied Mathematics with Python (AAU Business School)

Python notebooks for the first-semester course *Anvendt Matematik* (HA, Danish) /
*Applied Mathematics* (EBA, English) at Aalborg University Business School, 2026.
The course is a refresher of upper-secondary mathematics (functions, differentiation,
optimisation, linear algebra) taught alongside an introduction to Python. The textbook
is Jacques, *Mathematics for Economics and Business*. The two editions cover the same
material; the Danish edition runs calculus first, the English edition runs linear
algebra first.

Each lesson has a lecture notebook and an exercise notebook. Solution sets are not
included here. A running case (your electricity bill, using live prices from
Energi Data Service) grows by one chapter per lesson.

## How to use the notebooks

Click an **Open in Colab** badge. The notebook opens in Google Colab directly from
this repository and runs in the browser, nothing to install. To keep your own edits,
choose *File → Save a copy in Drive* in Colab. If you prefer to run locally, clone
the repository and open the `.ipynb` files in Jupyter; the notebooks use `numpy`,
`sympy`, `matplotlib`, `scipy` and `pandas`.

Start with the supplements (A, B, C) if you have never written Python before, then
follow the lessons in order.

"""
root = Path(".")
out = head.splitlines()
out += section(root, "Dansk udgave (HA)", [(f"da/{f}", l) for f, l in DA])
out += ["Desuden: [AI-studiemakker](da/AI_studiemakker_(Anvendt_mat,_HA2026).md), en prompt til en AI-assistent, der "
        "hjælper med kurset uden at løse opgaverne for dig.", ""]
out += section(root, "English edition (EBA)", [(f"en/{f}", l) for f, l in EN])
out += ["## Regenerating this README", "", "`python3 make_readme.py` rebuilds the tables from the notebooks on disk.", ""]
Path("README.md").write_text("\n".join(out), encoding="utf-8")
print("README.md written:", len(out), "lines")
