import subprocess, shutil
from pathlib import Path
from pypdf import PdfWriter  # pip install pypdf

folder = Path(".")  # folder containing q1.tex ... q20.tex
out = PdfWriter()


def run(cmd):
    subprocess.run(
        cmd, cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


for i in range(1, 21):
    name = f"q{i}"
    if not (folder / f"{name}.tex").exists():
        print(f"{name}.tex not found, skipping")
        continue
    tex = ["pdflatex", "-interaction=nonstopmode", f"{name}.tex"]
    run(tex)
    if (folder / f"{name}.idx").exists():  # needed for the index question
        run(["makeindex", name])
    run(tex)
    run(tex)  # extra runs resolve TOC, refs, citations
    pdf = folder / f"{name}.pdf"
    if pdf.exists():
        out.append(str(pdf), outline_item=f"Q.{i}")  # adds a bookmark per question
        print(f"Added Q.{i}")
    else:
        print(f"Q.{i} failed to compile, check {name}.log")

out.write("all_questions.pdf")
out.close()
print("Created all_questions.pdf")
