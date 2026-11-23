import pathlib, urllib.request, os
root=pathlib.Path(__file__).resolve().parent
files={
  "vendor/three.module.js": "https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.js",
  "vendor/addons/loaders/GLTFLoader.js": "https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/loaders/GLTFLoader.js",
  "vendor/addons/utils/BufferGeometryUtils.js": "https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/utils/BufferGeometryUtils.js",
  "vendor/LICENSE": "https://cdn.jsdelivr.net/npm/three@0.160.1/LICENSE",
  "assets/external/building-a.glb": "https://raw.githubusercontent.com/Hidencod/tge-assets/main/packs/city-kit-commercial/building-a.glb",
  "assets/external/building-b.glb": "https://raw.githubusercontent.com/Hidencod/tge-assets/main/packs/city-kit-commercial/building-b.glb",
  "assets/external/tree.glb": "https://raw.githubusercontent.com/Hidencod/tge-assets/main/packs/nature-kit/tree-pinetalla-detailed.glb",
  "assets/external/crate.glb": "https://raw.githubusercontent.com/Hidencod/tge-assets/main/packs/pirate-kit/crate.glb"
}
for name,url in files.items():
 p=root/name
 if p.is_file() and p.stat().st_size>0: continue
 print("Downloading",name,flush=True)
 p.parent.mkdir(parents=True,exist_ok=True)
 temp=p.with_suffix(p.suffix+".part")
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"OpenWorldShooter/0.10"}),timeout=45) as response: data=response.read()
 if name.endswith(".glb") and data[:4]!=b"glTF": raise RuntimeError("Invalid GLB "+name)
 if not data: raise RuntimeError("Empty "+name)
 temp.write_bytes(data)
 os.replace(temp,p)
# Optional CC0 photo textures from Poly Haven; keep the existing world playable if unavailable.
import json
for asset, stem in ([] if os.environ.get("OFFLINE")=="1" else [("grass_01","grass"),("asphalt_02","asphalt")]):
 try:
  keys=[("diff","color"),("nor_gl","normal")]
  for key,suffix in keys:
   p=root/("assets/external/"+stem+"-"+suffix+".jpg")
   if p.is_file() and p.stat().st_size>0: continue
   with urllib.request.urlopen(urllib.request.Request("https://api.polyhaven.com/files/"+asset,headers={"User-Agent":"OpenWorldShooter/0.10 (local game asset installer)"}),timeout=20) as response: meta=json.load(response)
   url=meta[key]["1k"]["jpg"]["url"]
   with urllib.request.urlopen(url,timeout=45) as response: data=response.read()
   if not data.startswith(b"\xff\xd8"): raise RuntimeError("Expected JPEG")
   temp=p.with_suffix(".part")
   temp.write_bytes(data)
   os.replace(temp,p)
 except Exception as e: print("Optional texture unavailable:",asset,e)
print("Local assets ready")

manifest={stem+"-"+suffix:(root/("assets/external/"+stem+"-"+suffix+".jpg")).is_file() for stem in ("grass","asphalt") for suffix in ("color","normal")}
(root/"assets/texture-manifest.json").write_text(json.dumps(manifest))
