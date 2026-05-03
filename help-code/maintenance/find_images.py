from pathlib import Path

folders = [
    r"C:\Users\nakul\Downloads\notebooks-main",
    r"C:\Users\nakul\Downloads\nlp-notebooks-master",
    r"C:\Users\nakul\Downloads\iuryt.github.io-main",
    r"C:\Users\nakul\Downloads\arXiv-2510.25445v1",
    r"C:\Users\nakul\Downloads\arXiv-2603.14558v2",
    r"C:\Users\nakul\Downloads\arXiv-2107.13586v1",
    r"C:\Users\nakul\Downloads\arXiv-2312.10997v5",
    r"C:\Users\nakul\Downloads\d2l-pytorch-colab-master",
    r"C:\Users\nakul\Downloads\arXiv-2303.18223v19",
    r"C:\Users\nakul\Downloads\arXiv-2512.10493v2",
    r"C:\Users\nakul\Downloads\arXiv-2503.18419v1",
    r"C:\Users\nakul\Downloads\d2l-en-master",
    r"D:\Repositories\AD698-generative-ai-for-BA\help-code",
]

exts = {'.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp', '.pdf'}

for folder in folders:
    p = Path(folder)
    if not p.exists():
        print(f"MISSING: {folder}")
        continue
    images = sorted([f for f in p.rglob("*") if f.suffix.lower() in exts])
    print(f"\n=== {p.name} === ({len(images)} images)")
    for img in images:
        print(f"  {img.relative_to(p)}")
