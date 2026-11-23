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
 with urllib.request.urlopen(url,timeout=45) as response: data=response.read()
 if name.endswith(".glb") and data[:4]!=b"glTF": raise RuntimeError("Invalid GLB "+name)
 if not data: raise RuntimeError("Empty "+name)
 temp.write_bytes(data)
 os.replace(temp,p)
print("Local assets ready")
