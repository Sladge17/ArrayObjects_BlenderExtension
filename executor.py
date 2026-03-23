from pathlib import Path



path = "Projects/ObjectMultiplyer"
entrypoint = "__init__.py"

filename = Path(path, entrypoint).resolve()
with open(filename) as text:
    source = text.read()

exec(compile(
    source=source,
    filename=filename,
    mode='exec',
))
