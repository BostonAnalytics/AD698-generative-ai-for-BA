import nbformat
import glob
from pathlib import Path

notebooks = glob.glob('help-code/Rag/*.ipynb')
for nb_path in notebooks:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    code = ""
    for cell in nb.cells:
        if cell.cell_type == 'code':
            code += cell.source + "\n\n"
    
    out_path = nb_path.replace('.ipynb', '.py')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f'Converted {nb_path} to {out_path}')
