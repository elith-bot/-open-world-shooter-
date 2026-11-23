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
for asset, stem in []:
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


# Pinned upstream art; verify Git blob hashes before installing.
import hashlib
pro = {"assets/pro/Pistol.glb":{"path":"content/models/realism/pistol_p45.glb","sha":"bd7600e4dc435a27244a4503edbfd5e652758f8c"},"assets/pro/Rifle.glb":{"path":"content/models/realism/ar_a4.glb","sha":"2f348c07f03406e55ec814ace427c370595a1845"},"assets/pro/SMG.glb":{"path":"content/models/realism/smg_mp9.glb","sha":"1d4b05c367fc3ec4b7bc69d240a4114cde3aec7e"},"assets/pro/Sniper.glb":{"path":"content/models/realism/sniper_s90.glb","sha":"29a7cc5eaa7f406c1c79fe70abd859783f3a1f52"},"assets/pro/boulder_01/boulder_01.bin":{"path":"content/models/props/boulder_01/boulder_01.bin","sha":"b7e374c653f5a87c36570a75f854f62e077974e4"},"assets/pro/boulder_01/boulder_01_1k.gltf":{"path":"content/models/props/boulder_01/boulder_01_1k.gltf","sha":"d9a76340e587790f2e4287564c7e95e72545d185"},"assets/pro/boulder_01/textures/boulder_01_arm_1k.jpg":{"path":"content/models/props/boulder_01/textures/boulder_01_arm_1k.jpg","sha":"0e00a7870e4823215516750616a7f17850e711a6"},"assets/pro/boulder_01/textures/boulder_01_diff_1k.jpg":{"path":"content/models/props/boulder_01/textures/boulder_01_diff_1k.jpg","sha":"1a55b27906174331617289b6db54d9e852640e75"},"assets/pro/boulder_01/textures/boulder_01_nor_gl_1k.jpg":{"path":"content/models/props/boulder_01/textures/boulder_01_nor_gl_1k.jpg","sha":"18f12d5e43fed3d48882eca22181ba9476e818b3"},"assets/pro/concrete_road_barrier_02/concrete_road_barrier_02.bin":{"path":"content/models/props/concrete_road_barrier_02/concrete_road_barrier_02.bin","sha":"fd2a8ef5eae99f4af6f4d097e5150a2094f15016"},"assets/pro/concrete_road_barrier_02/concrete_road_barrier_02_1k.gltf":{"path":"content/models/props/concrete_road_barrier_02/concrete_road_barrier_02_1k.gltf","sha":"d5848a74dfefd0f72f00416b41197b393ed1622b"},"assets/pro/concrete_road_barrier_02/textures/concrete_road_barrier_02_arm_1k.jpg":{"path":"content/models/props/concrete_road_barrier_02/textures/concrete_road_barrier_02_arm_1k.jpg","sha":"aa44169ba603aa953951af27306673eb47c7be93"},"assets/pro/concrete_road_barrier_02/textures/concrete_road_barrier_02_diff_1k.jpg":{"path":"content/models/props/concrete_road_barrier_02/textures/concrete_road_barrier_02_diff_1k.jpg","sha":"5e6e2e17fec465704aa978d19f85d9c38c786116"},"assets/pro/concrete_road_barrier_02/textures/concrete_road_barrier_02_nor_gl_1k.jpg":{"path":"content/models/props/concrete_road_barrier_02/textures/concrete_road_barrier_02_nor_gl_1k.jpg","sha":"070c6eace9c1c29ee6425ceb89f4e4227971e6bc"},"assets/pro/covered_car/covered_car.bin":{"path":"content/models/props/covered_car/covered_car.bin","sha":"44cdf96c80d05c958e34c84f75e0e4c5e880bb45"},"assets/pro/covered_car/covered_car_1k.gltf":{"path":"content/models/props/covered_car/covered_car_1k.gltf","sha":"0441c346f0d57ad7854cf46ee7d38b985d1ccbf8"},"assets/pro/covered_car/textures/covered_car_arm_1k.jpg":{"path":"content/models/props/covered_car/textures/covered_car_arm_1k.jpg","sha":"dac43f1f1feccb520c0ad36defcbf0e722c4490d"},"assets/pro/covered_car/textures/covered_car_diff_1k.jpg":{"path":"content/models/props/covered_car/textures/covered_car_diff_1k.jpg","sha":"264a957622d616a6faab4cb2106578bb79eafc70"},"assets/pro/covered_car/textures/covered_car_nor_gl_1k.jpg":{"path":"content/models/props/covered_car/textures/covered_car_nor_gl_1k.jpg","sha":"a30094c4b0139863f31bb16eeb55a2136529df0d"},"assets/pro/fern_02/fern_02.bin":{"path":"content/models/props/fern_02/fern_02.bin","sha":"b6ae3752172b2f6d074f05d433accdc96b357f2a"},"assets/pro/fern_02/fern_02_1k.gltf":{"path":"content/models/props/fern_02/fern_02_1k.gltf","sha":"ec7509ee8e280964d78eaeab28348d855c88d98d"},"assets/pro/fern_02/textures/fern_02_arm_1k.jpg":{"path":"content/models/props/fern_02/textures/fern_02_arm_1k.jpg","sha":"37ed142c42ef6752152fd063163faec109cd1af7"},"assets/pro/fern_02/textures/fern_02_diff_1k.jpg":{"path":"content/models/props/fern_02/textures/fern_02_diff_1k.jpg","sha":"2f0223cbf1a77daadd38813ffff1fa6d389d49ca"},"assets/pro/fern_02/textures/fern_02_nor_gl_1k.jpg":{"path":"content/models/props/fern_02/textures/fern_02_nor_gl_1k.jpg","sha":"a1dcaeb21a65624912e95fbd102a09a5ed2c89f4"},"assets/pro/plastic_crate_02/plastic_crate_02.bin":{"path":"content/models/props/plastic_crate_02/plastic_crate_02.bin","sha":"a732d3e2723fe0b276096d310dc2b457c05db9da"},"assets/pro/plastic_crate_02/plastic_crate_02_1k.gltf":{"path":"content/models/props/plastic_crate_02/plastic_crate_02_1k.gltf","sha":"d05ad15eaf052db749e871041bb0bd01c990d36c"},"assets/pro/plastic_crate_02/textures/plastic_crate_02_arm_1k.jpg":{"path":"content/models/props/plastic_crate_02/textures/plastic_crate_02_arm_1k.jpg","sha":"b5bd4de79ebbb353a037ea2ba65092234b0d6172"},"assets/pro/plastic_crate_02/textures/plastic_crate_02_diff_1k.jpg":{"path":"content/models/props/plastic_crate_02/textures/plastic_crate_02_diff_1k.jpg","sha":"6a9fa4c3049d81b0eedb2db2ebed4af56cbde900"},"assets/pro/plastic_crate_02/textures/plastic_crate_02_nor_gl_1k.jpg":{"path":"content/models/props/plastic_crate_02/textures/plastic_crate_02_nor_gl_1k.jpg","sha":"6cff07890a10513927f39b1998beb6e4724e5efe"},"assets/external/grass-color.jpg":{"path":"content/materials/leafy_grass/leafy_grass_diff_2k.jpg","sha":"f8030622313b178303b7024cf5ee6919e951e45d"},"assets/external/grass-normal.jpg":{"path":"content/materials/leafy_grass/leafy_grass_nor_gl_2k.jpg","sha":"42f8aa5bbc118ab850ea201b5d1cf9ef82b1d24a"},"assets/external/asphalt-color.jpg":{"path":"content/materials/asphalt_02/asphalt_02_diff_2k.jpg","sha":"1c999e8944617c8b197afa920202cd29eaa590d7"},"assets/external/asphalt-normal.jpg":{"path":"content/materials/asphalt_02/asphalt_02_nor_gl_2k.jpg","sha":"054858f6cf83aa42e8ce7bf238dad9535a8fa22f"},"assets/pro/licenses/detailed-firearms.txt":{"path":"content/licenses/detailed-firearms.txt","sha":"b8a474537d3c9d110fd4723760d6eed3d59fae15"},"assets/pro/licenses/3dmodelscc0-guns.txt":{"path":"content/licenses/3dmodelscc0-guns.txt","sha":"e385ed98f186c0015c3f1f5eccabc2fc109336a7"},"assets/pro/licenses/polyhaven-environment.txt":{"path":"content/licenses/polyhaven-environment.txt","sha":"19e49776a882d334d3504075215e7801e3249a1a"}}
for name, item in pro.items():
 p=root/name
 def valid(data):
  return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==item["sha"]
 if p.is_file() and valid(p.read_bytes()): continue
 if os.environ.get("OFFLINE")=="1": continue
 try:
  p.parent.mkdir(parents=True,exist_ok=True)
  print("Importing",name,flush=True)
  with urllib.request.urlopen("https://raw.githubusercontent.com/kter1/fps-mode-public/41fc12d8bb095dcd03451060d2aa62a96d9667d5/"+item["path"],timeout=60) as response: data=response.read()
  if not valid(data): raise RuntimeError("Asset hash mismatch")
  temp=p.with_suffix(p.suffix+".part"); temp.write_bytes(data); os.replace(temp,p)
 except Exception as e: print("Professional asset unavailable:",name,e)
(root/"assets/pro-manifest.json").write_text(json.dumps({name[7:]: (root/name).is_file() for name in pro}))

manifest={stem+"-"+suffix:(root/("assets/external/"+stem+"-"+suffix+".jpg")).is_file() for stem in ("grass","asphalt") for suffix in ("color","normal")}
(root/"assets/texture-manifest.json").write_text(json.dumps(manifest))
