# Art preview
Pinned FPS Mode source: 41fc12d8bb095dcd03451060d2aa62a96d9667d5
Downloads verified against upstream Git blob hashes. Source licenses downloaded alongside assets. Existing character and buildings remain until validated replacements are available. Weapon orientation and mobile performance require device testing.

V0.12: additional scanned wall materials, environment props and CC0-derived arms downloaded; arms not yet attached or animated. Existing building meshes are retained and retextured. No mobile runtime test.

V0.13 performance pass: revert incompatible wall UV overrides, reduce prop density, distance-cull actors/static fitted props and limit render resolution/shadows. Existing assets retained. No new character or building mesh. Device validation pending.

V0.14: single-flight visibility-aware local latency polling and basic camera weapon recoil, ADS shift and reload tilt. No new meshes or skeletal animations; device test pending.

V0.15 licensed world pack: genuine CC0 GLB houses, two pine trees with InstancedMesh, distant proxy LOD, HDRI sky, gently displaced terrain, KayKit skinned combatant with idle/walk/run (stylized placeholder), FP arms loaded from prior CC0 file. Requires phone testing.

V0.15.1: opt-in KTX2 GPU compression (toktx + Pillow) and KTX2Loader with JPEG fallback. No KTX2 conversion is claimed unless the optional encoder is installed and outputs validated locally. Correct terrain smoothing along roads.

V0.15.3: lazy skinned enemy allocation only as opponents enter ~640 game units; prevents initializing 65 expensive skeletons at boot.
