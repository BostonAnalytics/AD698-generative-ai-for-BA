from pathlib import Path

folders = [
    r"C:\Users\nakul\Downloads\d2l-pytorch-colab-master",
    r"C:\Users\nakul\Downloads\d2l-en-master",
]

exts = {'.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp'}

for folder in folders:
    p = Path(folder)
    if not p.exists():
        print(f"MISSING: {folder}")
        continue
    images = sorted([f for f in p.rglob("*") if f.suffix.lower() in exts])
    print(f"\n=== {p.name} === ({len(images)} images)")
    for img in images:
        rel = str(img.relative_to(p))
        print(f"  {rel}")
