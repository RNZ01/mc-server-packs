#!/usr/bin/env python3
import hashlib
import os
import shutil
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

TAG = os.environ.get("PACK_VERSION", "26.2-0.1")
NAME = os.environ.get("PACK_NAME", f"Combined-Packs-{TAG}.zip")
REPO = os.environ["GITHUB_REPOSITORY"]

root = Path("mc-resource-packs")
out_dir = Path("dist")
out_dir.mkdir(exist_ok=True)
out_zip = out_dir / NAME
notes = out_dir / "release-notes.txt"

packs = sorted(p for p in root.glob("*.zip") if p.name != NAME)
if not packs:
    sys.exit("No .zip resource packs found in mc-resource-packs/")

with tempfile.TemporaryDirectory() as tmp:
    merged = Path(tmp) / "merged"
    merged.mkdir()

    # Same rule Minecraft uses for stacked packs: later/higher-priority packs win.
    # Priority here is filename sort order, so prefix packs with 01-, 02-, etc.
    for pack in packs:
        with zipfile.ZipFile(pack) as z:
            for member in z.infolist():
                target = (merged / member.filename).resolve()
                if not str(target).startswith(str(merged.resolve())):
                    raise SystemExit(f"Refusing unsafe zip path in {pack}: {member.filename}")
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(member) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(p for p in merged.rglob("*") if p.is_file()):
            z.write(path, path.relative_to(merged).as_posix())

sha1 = hashlib.sha1(out_zip.read_bytes()).hexdigest()
pack_id = str(uuid.uuid4())
url = f"https://github.com/{REPO}/releases/download/{TAG}/{NAME}"
escaped_url = url.replace(":", "\\:")

notes.write_text("\n".join([
    "require-resource-pack=false",
    f"resource-pack={escaped_url}",
    f"resource-pack-id={pack_id}",
    'resource-pack-prompt={"text"\\:"This server recommends using the resource pack for the best experience."}',
    f"resource-pack-sha1={sha1}",
    "",
]), encoding="utf-8")

print(f"Built {out_zip}")
print(f"Merged packs: {', '.join(p.name for p in packs)}")
print(f"SHA1: {sha1}")
