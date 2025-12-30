#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path
import yaml  # pip install pyyaml

ROOT = Path(__file__).resolve().parents[1]

# Registry is in the submodule
LINKS_MD = ROOT / "docs" / "content" / "links.md"
SRC = ROOT / "docs"
DST = ROOT / "docs_gen"


def load_links(md_path: Path) -> dict[str, str]:
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"```yaml\s*(.*?)\s*```", text, flags=re.DOTALL)
    if not m:
        raise SystemExit(f"No ```yaml ... ``` block found in {md_path}")
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, list):
        raise SystemExit("YAML block must be a list of {id, url} entries")

    mapping: dict[str, str] = {}
    for item in data:
        if not isinstance(item, dict) or "id" not in item or "url" not in item:
            raise SystemExit("Each YAML entry must contain keys: id, url")
        mapping[str(item["id"])] = str(item["url"])
    return mapping


def replace_tokens(s: str, mapping: dict[str, str]) -> str:
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return mapping.get(key, match.group(0))  # unknown tokens stay as-is
    return re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", repl, s)


def main() -> None:
    if not LINKS_MD.exists():
        raise SystemExit(f"Missing link registry: {LINKS_MD}")
    if not SRC.exists():
        raise SystemExit(f"Missing docs dir: {SRC}")

    mapping = load_links(LINKS_MD)

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    for md in DST.rglob("*.md"):
        content = md.read_text(encoding="utf-8")
        updated = replace_tokens(content, mapping)
        if updated != content:
            md.write_text(updated, encoding="utf-8")

    print(f"Expanded tokens into: {DST}")


if __name__ == "__main__":
    main()
