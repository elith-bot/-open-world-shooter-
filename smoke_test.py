#!/usr/bin/env python3
"""Local sanity check; does not claim a rendered performance benchmark."""
import ast, json, pathlib, sys, struct
root=pathlib.Path(__file__).resolve().parent
for path in ("setup_assets.py","server.py","prepare_ktx2.py"):
 ast.parse((root/path).read_text())
 print("Python syntax OK:",path)
for name in ("asset_sources_v1.json","scenecrate_sources.json"):
 items=json.loads((root/name).read_text())
 assert items, name
 print("Manifest OK:",name,len(items))
manifest=root/"assets/pro-manifest.json"
if manifest.exists():
 files=json.loads(manifest.read_text())
 missing=[k for k,v in files.items() if not v and k.startswith("pro/v1/")]
 print("Optional world pack ready:",sum(v for k,v in files.items() if k.startswith("pro/v1/")),"missing:",len(missing))
 for k in missing: print(" OPTIONAL MISSING:",k)
else: print("Asset manifest not written yet")
print("Static checks passed (visual compatibility requires phone testing).")
