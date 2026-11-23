#!/usr/bin/env python3
"""Optional offline preparation of GPU-compressed KTX2 textures.

Requires the external Khronos toktx encoder and Pillow. The game works
without either and falls back to its original local JPEG textures.
"""
import json
import pathlib
import shutil
import subprocess
import tempfile

root=pathlib.Path(__file__).resolve().parent
folder=root/"assets/ktx2"
folder.mkdir(parents=True,exist_ok=True)
names=["grass-color","grass-normal","asphalt-color","asphalt-normal"]
encoder=shutil.which("toktx")
try:
 from PIL import Image
except ImportError:
 Image=None
if not encoder or Image is None:
 print("KTX2 encoder / Pillow unavailable; using existing JPEG textures",flush=True)
else:
 for name in names:
  source=root/"assets/external"/(name+".jpg")
  output=folder/(name+".ktx2")
  if not source.is_file() or output.is_file(): continue
  try:
   with tempfile.TemporaryDirectory() as temp:
    png=pathlib.Path(temp)/(name+".png")
    with Image.open(source) as image: image.convert("RGB").save(png)
    cmd=[encoder,"--t2","--genmipmap","--encode",("uastc" if "normal" in name else "etc1s"),str(output),str(png)]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=150)
   if output.stat().st_size<128: raise RuntimeError("Output too small")
   print("KTX2 prepared",name,flush=True)
  except Exception as e:
   output.unlink(missing_ok=True)
   print("KTX2 optional conversion failed:",name,str(e)[:180],flush=True)
(folder.parent/"ktx2-manifest.json").write_text(json.dumps({name:(folder/(name+".ktx2")).is_file() for name in names}))
