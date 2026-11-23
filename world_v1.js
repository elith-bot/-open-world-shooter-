
// CC0 optional art pipeline for Open World.  Falls back to existing assets if files are absent.
const ASSET_PATHS={
 Combatant:'pro/v1/combatant.glb',MoveClips:'pro/v1/movement.glb',GeneralClips:'pro/v1/general.glb',
 HouseA:'pro/v1/house_a.glb',HouseB:'pro/v1/house_b.glb',HouseC:'pro/v1/house_c.glb',
 HouseD:'pro/v1/house_d.glb',HouseE:'pro/v1/house_e.glb',
 PineA:'pro/v1/pine_a.glb',PineB:'pro/v1/pine_b.glb',Outpost:'pro/v1/outpost.glb',
 Arms:'pro/arms.glb'
};
export async function loadWorldPack(T){
 const pack={};let available={};
 try{const r=await fetch('./assets/pro-manifest.json',{cache:'no-store'});if(r.ok)available=await r.json()}catch(e){console.warn('Asset manifest',e)}
 const {GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js'),loader=new GLTFLoader();
 const {clone}=await import('three/addons/utils/SkeletonUtils.js');pack.skinnedClone=clone;
 await Promise.all(Object.entries(ASSET_PATHS).map(async([name,path])=>{
  if(!available[path])return;
  let timer;
  try{
   const gltf=await Promise.race([loader.loadAsync('./assets/'+path),new Promise((_,reject)=>timer=setTimeout(()=>reject(Error('Model timeout: '+name)),12500))]);
   if(name.endsWith('Clips'))pack[name]=gltf.animations;
   else pack[name]=gltf.scene;
  }catch(e){console.warn('Optional art fallback',name,e)}
  finally{clearTimeout(timer)}
 }));
 pack.hasSky=!!available['pro/v1/sky.hdr'];
 return pack;
}
export async function installSky(T,scene,pack){
 if(!pack.hasSky)return false;
 try{
  const {RGBELoader}=await import('three/addons/loaders/RGBELoader.js');
  let sky=await new RGBELoader().loadAsync('./assets/pro/v1/sky.hdr');
  sky.mapping=T.EquirectangularReflectionMapping;scene.background=sky;
  // The background is independent of the expensive environment reflections.
  return true;
 }catch(e){console.warn('Sky fallback',e);return false}
}
export function makeTerrain(T,ground,size){
 const previous=ground.geometry,geo=new T.PlaneGeometry(size,size,80,80);
 geo.rotateX(-Math.PI/2);
 const positions=geo.getAttribute('position');
 for(let i=0;i<positions.count;i++){
  const x=positions.getX(i)+size/2,z=positions.getZ(i)+size/2;
  const vx=Math.abs(((x-400+4000)%800)-400),vz=Math.abs(((z-400+4000)%800)-400);
  const roadClear=Math.max(0,Math.min(1,(Math.min(vx,vz)-45)/65));
  const nearCenter=Math.min(1,Math.hypot(x-2000,z-2000)/850);
  const roll=(Math.sin(x*.009)*Math.cos(z*.007)*1.9+Math.sin(x*.017+z*.013)*.7);
  positions.setY(i,roll*roadClear*(.18+.65*nearCenter)-.25);
 }
 positions.needsUpdate=true;geo.computeVertexNormals();
 ground.geometry=geo;ground.position.set(size/2,0,size/2);
 if(previous)previous.dispose();
}
export function makeCombatant(T,scene,pack,color){
 if(!pack.Combatant||!pack.skinnedClone)return null;
 try{
  const holder=new T.Group(),body=pack.skinnedClone(pack.Combatant),b=new T.Box3().setFromObject(body);
  const dim=b.getSize(new T.Vector3()),center=b.getCenter(new T.Vector3());
  if(!(dim.y>0))return null;
  body.position.set(-center.x,-b.min.y,-center.z);
  body.traverse(o=>{
   if(/cape|quiver/i.test(o.name))o.visible=false;
   if(!o.isMesh)return;
   o.castShadow=false;o.receiveShadow=false;
   if(o.material){
    const modify=m=>{const c=m.clone();if(c.color)c.color.multiply(new T.Color(color===0x447b91?0x9bbca7:0xb0a08b));return c};
    o.material=Array.isArray(o.material)?o.material.map(modify):modify(o.material);
   }
  });
  const normalized=new T.Group();normalized.scale.setScalar(43/dim.y);normalized.add(body);holder.add(normalized);
  const mixer=new T.AnimationMixer(body),clips=[...(pack.GeneralClips||[]),...(pack.MoveClips||[])],actions={};
  for(const clip of clips){if(/^(Idle_A|Walking_A|Running_A|Death_A)$/i.test(clip.name))actions[clip.name]=mixer.clipAction(clip)}
  const first=actions.Idle_A||actions.Walking_A||actions.Running_A;if(first)first.play();
  holder.userData.actorAnimation={mixer,actions,current:first===actions.Idle_A?'Idle_A':first===actions.Walking_A?'Walking_A':'Running_A',lastX:null,lastZ:null};
  scene.add(holder);return holder;
 }catch(e){console.warn('Combatant fallback',e);return null}
}
export function animateCombatant(group,desired,dt){
 const data=group?.userData?.actorAnimation;if(!data)return;
 const wanted=data.actions[desired]||data.actions.Idle_A||data.actions.Walking_A;
 if(!wanted)return;
 if(data.current!==desired){
  for(const a of Object.values(data.actions))if(a!==wanted)a.fadeOut(.18);
  wanted.reset().fadeIn(.18).play();data.current=desired;
 }
 data.mixer.update(Math.min(.05,dt));
}
export function buildLodBuilding(T,scene,template,b){
 if(!template)return false;
 try{
  const origin=new T.Group(),building=template.clone(true),bounds=new T.Box3().setFromObject(building);
  const dim=bounds.getSize(new T.Vector3()),c=bounds.getCenter(new T.Vector3());
  if(!dim.x||!dim.y||!dim.z)return false;
  building.position.set(-c.x,-bounds.min.y,-c.z);origin.add(building);
  origin.scale.set(b.w/dim.x,b.z/dim.y,b.h/dim.z);
  const lod=new T.LOD();lod.position.set(b.x+b.w/2,0,b.y+b.h/2);
  lod.addLevel(origin,0);
  const far=new T.Mesh(new T.BoxGeometry(b.w,b.z,b.h),new T.MeshLambertMaterial({color:0x857c69}));
  far.position.y=b.z/2;far.castShadow=false;far.receiveShadow=false;
  lod.addLevel(far,360);
  lod.userData.staticProp=true;scene.add(lod);
  return true;
 }catch(e){console.warn('Building LOD fallback',e);return false}
}
export function instancedForest(T,scene,pack,trees){
 const output=[];
 for(const [slot,name] of ['PineA','PineB'].entries()){
  const source=pack[name];if(!source)continue;
  try{
   source.updateMatrixWorld(true);
   const bound=new T.Box3().setFromObject(source),dim=bound.getSize(new T.Vector3()),center=bound.getCenter(new T.Vector3());
   if(!dim.x||!dim.y||!dim.z)continue;
   const locations=trees.filter((_,i)=>i%2===slot);
   const meshes=[];source.traverse(m=>{if(m.isMesh&&!m.isSkinnedMesh)meshes.push(m)});
   for(const m of meshes){
    const inst=new T.InstancedMesh(m.geometry,m.material,locations.length);inst.frustumCulled=false;
    inst.castShadow=false;inst.receiveShadow=false;inst.userData.totalInstances=locations.length;
    const origin=new T.Matrix4().makeTranslation(-center.x,-bound.min.y,-center.z);
    const scale=new T.Matrix4().makeScale(22/dim.x,44/dim.y,22/dim.z);
    const centerShift=scale.clone().multiply(origin),pos=new T.Matrix4(),mat=new T.Matrix4();
    locations.forEach((t,i)=>{
     pos.makeTranslation(t.x,0,t.y);
     mat.copy(pos).multiply(centerShift).multiply(m.matrixWorld);
     inst.setMatrixAt(i,mat);
    });
    inst.instanceMatrix.needsUpdate=true;scene.add(inst);output.push(inst);
   }
  }catch(e){console.warn('Instanced tree fallback',e)}
 }
 return output;
}
export function attachArms(T,camera,pack){
 if(!pack.Arms)return null;
 try{
  const g=new T.Group(),body=pack.skinnedClone(pack.Arms);
  const b=new T.Box3().setFromObject(body),d=b.getSize(new T.Vector3()),c=b.getCenter(new T.Vector3());
  if(!(d.length()>0))return null;
  body.position.sub(c);
  const holder=new T.Group();holder.scale.setScalar(18/Math.max(d.x,d.y,d.z));holder.add(body);g.add(holder);
  g.position.set(-2,-12,-23);camera.add(g);return g;
 }catch(e){console.warn('First-person arms fallback',e);return null}
}
