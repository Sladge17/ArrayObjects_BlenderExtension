from pathlib import Path
import sys



path = "Projects/ArrayObjects/source"
entrypoint = "__init__.py"

sys.path.append(path)

filename = Path(path, entrypoint).resolve()
with open(filename) as text:
    source = text.read()

exec(compile(
    source=source,
    filename=filename,
    mode='exec',
))
