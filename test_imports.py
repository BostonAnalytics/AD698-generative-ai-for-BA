import sys
import glob
import re

for pyfile in glob.glob('help-code/Rag/*.py'):
    with open(pyfile, 'r', encoding='utf-8') as f:
        content = f.read()
    
    imports = re.findall(r'^(?:from\s+[\w\.]+\s+import\s+.*|import\s+.*)', content, re.MULTILINE)
    
    print(f'Testing imports in {pyfile}')
    for imp in imports:
        try:
            exec(imp)
        except Exception as e:
            print(f'ERROR in {pyfile}: {imp}')
            print(e)
