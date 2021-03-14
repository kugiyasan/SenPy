from pathlib import Path
from typing import Iterator


def get_extensions() -> Iterator[str]:
    here = Path(__file__).parent.parent.parent
    for path in ("cogs", "cogs/Games"):
        for f in (here / path).iterdir():
            if f.is_file():
                pathname = str(f.relative_to(here))
                if pathname[-3:] != ".py":
                    continue
                yield pathname[:-3].replace("/", ".").replace("\\", ".")