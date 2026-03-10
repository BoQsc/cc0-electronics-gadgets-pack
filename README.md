```

C:\Users\Windows10_new\Downloads>"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe" --background --python "C:\Users\Windows10_new\Downloads\fbx_to_glb (10).py"
Blender 5.0.1 (hash a3db93c5b259 built 2025-12-16 01:32:30)

======================================================================
FBX -> GLB BATCH CONVERSION  (Blender 5.0)
Root: C:\Users\Windows10_new\Downloads\Gadgets&Electronics
======================================================================

Model                Scale    Approx final size
-----------------------------------------------------------------
  Console              x0.2220  ~234 x  84 x242 mm
  Digital_Camera       x0.6870  ~103 x  60 x 42 mm
  Flashlight           x0.0504  ~224 x  58 x 58 mm  + emissive ON
  Microphone           x0.0465  ~ 57 x  57 x199 mm
  Radio                x0.7700  ~192 x  96 x250 mm
  Router               x1.0000  ~203 x 163 x198 mm  + emissive ON
  SecurityCamera       x0.7060  ~ 97 x 160 x150 mm
  USB_Stick            x0.1770  ~ 21 x  65 x 10 mm
  VR_Goggles           x0.0330  ~191 x 137 x 96 mm
  WalkieTalkie         x1.3000  ~ 62 x  34 x191 mm


======================================================================
CONVERTING: Console
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Console\Console.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Console_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Console
  Fixing: simple mesh ('Console')
  Wiring emissive: Console_Emissive.png
    Wired Console_Emissive.png -> Emission Color
  Applying real-world scale (x0.2220)...
    Scale x0.2220 applied to 1 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Console_GLB\Console.glb
INFO Draco mesh compression is available, use library at C:\Program Files (x86)\Steam\steamapps\common\Blender\5.0\scripts\addons_core\io_scene_gltf2\extern_draco.dll
21:34:05 | INFO: Starting glTF 2.0 export
21:34:05 | INFO: Extracting primitive: Mesh
21:34:05 | INFO: Primitives created: 1
21:34:05 | INFO: Finished glTF 2.0 export in 0.23910260200500488 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Console_GLB\Console.glb
  SUCCESS: Console.glb

======================================================================
CONVERTING: Digital_Camera
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Digital_Camera\Digital_Camera.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Digital_Camera_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Digital_Camera
  Fixing: simple mesh ('Digital_Camera')
  Applying real-world scale (x0.6870)...
    Scale x0.6870 applied to 1 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Digital_Camera_GLB\Digital_Camera.glb
21:34:05 | INFO: Starting glTF 2.0 export
21:34:05 | INFO: Extracting primitive: Mesh
21:34:05 | INFO: Primitives created: 1
21:34:05 | INFO: Finished glTF 2.0 export in 0.05266714096069336 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Digital_Camera_GLB\Digital_Camera.glb
  SUCCESS: Digital_Camera.glb

======================================================================
CONVERTING: Flashlight
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Flashlight\Flashlight.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Flashlight_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Flashlight
  Fixing: Flashlight
    Body world bbox center (verts): (-0.581497, 0.000000, -0.000000)
    After shift: body.loc=(-0.2793847322463989, 0.0, 0.17527855932712555), glass.loc=(-1.1381516456604004, 0.0, 1.4901161193847656e-08)
    Body nozzle world X:  -2.2253
    Glass disc world X:   -2.2092  (pivot = disc center)
    Glass disc world Z:   -0.000000  (should be ~0)
    Disc inside nozzle:   16.1 mm  (target ~16mm)
    Removed empty Normal Map node from Glass
    Wired Glass_Opacity.png -> Alpha
    Wired Glass_Roughness.png -> Roughness
    Set Transmission Weight = 1.0
    Glass blend_method = BLEND
    Wired Flashlight_Metallic.png -> Metallic
    Wired Flashlight_Roughness.png -> Roughness
    Wired Flashlight_Emissive.png -> Emission Color
    Inserted DirectX->OGL G-invert for Flashlight normal map
    Body blend_method = OPAQUE
  Applying real-world scale (x0.0504)...
    Scale x0.0504 applied to 2 mesh(es)
    Multi-root: centered 'Flashlight', left others in place
      'Glass' kept at location (-0.11134124547243118, -3.0040741005876725e-09, -3.0040741005876725e-09) (relative to primary)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Flashlight_GLB\Flashlight.glb
21:34:06 | INFO: Starting glTF 2.0 export
21:34:06 | INFO: Extracting primitive: Mesh
21:34:06 | WARNING: More than one shader node tex image used for a texture. The resulting glTF sampler will behave like the first shader node tex image.
21:34:06 | INFO: Primitives created: 1
21:34:06 | INFO: Extracting primitive: Mesh.001
21:34:07 | WARNING: More than one shader node tex image used for a texture. The resulting glTF sampler will behave like the first shader node tex image.
21:34:07 | INFO: Primitives created: 1
21:34:07 | INFO: Finished glTF 2.0 export in 1.238668441772461 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Flashlight_GLB\Flashlight.glb
  SUCCESS: Flashlight.glb

======================================================================
CONVERTING: Microphone
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Microphone\Microphone.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Microphone_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Microphone
  Fixing: simple mesh ('Mic')
  Applying real-world scale (x0.0465)...
    Scale x0.0465 applied to 1 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Microphone_GLB\Microphone.glb
21:34:07 | INFO: Starting glTF 2.0 export
21:34:07 | INFO: Extracting primitive: Mesh
21:34:07 | INFO: Primitives created: 1
21:34:07 | INFO: Finished glTF 2.0 export in 0.04822540283203125 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Microphone_GLB\Microphone.glb
  SUCCESS: Microphone.glb

======================================================================
CONVERTING: Radio
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Radio\Radio.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Radio_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Radio
  Fixing: Radio
    Radio children: ['Radio_2', 'Screen', 'Tune', 'Volume']
    Radio_2 geometry bbox center (world): (-8.866190910339355e-07, 0.018724661320447922, 0.1259077787399292)
    Radio_2 obj.location (pivot):         (-1.0793494311656104e-06, 0.12497439235448837, 0.027468977496027946)
    Part locations after centering on Radio_2 geometry center:
      Radio_2: (-1.927303401316749e-07, 0.10624973475933075, -0.0984387993812561)
      Screen: (1.6766534827183932e-09, -0.05922389775514603, -0.1350628286600113)
      Tune: (0.06809531152248383, -0.06096223369240761, -0.1350647509098053)
      Volume: (-0.0680956244468689, -0.06096223369240761, -0.1350647509098053)
  Applying real-world scale (x0.7700)...
    Scale x0.7700 applied to 4 mesh(es)
    Multi-root: centered 'Radio_2', left others in place
      'Screen' kept at location (1.2910231772522707e-09, -0.04560239985585213, -0.10399837791919708) (relative to primary)
      'Tune' kept at location (0.05243339017033577, -0.046940919011831284, -0.10399986058473587) (relative to primary)
      'Volume' kept at location (-0.05243363231420517, -0.046940919011831284, -0.10399986058473587) (relative to primary)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Radio_GLB\Radio.glb
21:34:07 | INFO: Starting glTF 2.0 export
21:34:07 | INFO: Extracting primitive: Mesh
21:34:07 | INFO: Primitives created: 1
21:34:07 | INFO: Extracting primitive: Mesh.001
21:34:07 | INFO: Primitives created: 1
21:34:07 | INFO: Extracting primitive: Mesh.002
21:34:07 | INFO: Primitives created: 1
21:34:07 | INFO: Extracting primitive: Mesh.003
21:34:07 | WARNING: Mesh.003: Could not calculate tangents. Please try to triangulate the mesh first.
21:34:07 | INFO: Primitives created: 1
21:34:07 | INFO: Finished glTF 2.0 export in 0.07336974143981934 s

Warning: Mesh.003: Could not calculate tangents. Please try to triangulate the mesh first.
  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Radio_GLB\Radio.glb
  SUCCESS: Radio.glb

======================================================================
CONVERTING: Router
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Router\Router.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Router_Normal.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Router
  Fixing: simple mesh ('Router')
  Wiring emissive: Router_Emissive.png
    Wired Router_Emissive.png -> Emission Color
  Applying real-world scale (x1.0000)...
    Scale: 1.000 (no correction needed)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Router_GLB\Router.glb
21:34:07 | INFO: Starting glTF 2.0 export
21:34:07 | INFO: Extracting primitive: Mesh
21:34:07 | WARNING: Mesh: Could not calculate tangents. Please try to triangulate the mesh first.
21:34:08 | INFO: Primitives created: 1
21:34:08 | INFO: Finished glTF 2.0 export in 0.21332454681396484 s

Warning: Mesh: Could not calculate tangents. Please try to triangulate the mesh first.
  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\Router_GLB\Router.glb
  SUCCESS: Router.glb

======================================================================
CONVERTING: SecurityCamera
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\SecurityCamera\SecurityCamera.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'SecurityCamera_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\SecurityCamera
  Fixing: SecurityCamera
    Camera local offset after re-parent: (0.0, 0.008433827199041843, -0.03706773370504379)
  Applying real-world scale (x0.7060)...
    Scale x0.7060 applied to 2 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\SecurityCamera_GLB\SecurityCamera.glb
21:34:08 | INFO: Starting glTF 2.0 export
21:34:08 | INFO: Extracting primitive: Mesh
21:34:09 | INFO: Primitives created: 1
21:34:09 | INFO: Extracting primitive: Mesh.001
21:34:09 | INFO: Primitives created: 1
21:34:09 | INFO: Finished glTF 2.0 export in 0.7874186038970947 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\SecurityCamera_GLB\SecurityCamera.glb
  SUCCESS: SecurityCamera.glb

======================================================================
CONVERTING: USB_Stick
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\USB_Stick\USB_Stick.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'USB_Stick_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\USB_Stick
  Fixing: simple mesh ('USB_Stick')
  Applying real-world scale (x0.1770)...
    Scale x0.1770 applied to 1 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\USB_Stick_GLB\USB_Stick.glb
21:34:09 | INFO: Starting glTF 2.0 export
21:34:09 | INFO: Extracting primitive: Mesh
21:34:09 | INFO: Primitives created: 1
21:34:09 | INFO: Finished glTF 2.0 export in 0.1746997833251953 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\USB_Stick_GLB\USB_Stick.glb
  SUCCESS: USB_Stick.glb

======================================================================
CONVERTING: VR_Goggles
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\VR_Goggles\VRGoggles.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'VRGoggles_Normal_DirectX.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\VR_Goggles
  Fixing: simple mesh ('VR_Goggles')
  Applying real-world scale (x0.0330)...
    Scale x0.0330 applied to 1 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\VR_Goggles_GLB\VR_Goggles.glb
21:34:09 | INFO: Starting glTF 2.0 export
21:34:09 | INFO: Extracting primitive: Mesh
21:34:09 | WARNING: Mesh: Could not calculate tangents. Please try to triangulate the mesh first.
21:34:10 | INFO: Primitives created: 1
21:34:10 | INFO: Finished glTF 2.0 export in 0.18904995918273926 s

Warning: Mesh: Could not calculate tangents. Please try to triangulate the mesh first.
  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\VR_Goggles_GLB\VR_Goggles.glb
  SUCCESS: VR_Goggles.glb

======================================================================
CONVERTING: WalkieTalkie
======================================================================
  Importing: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\WalkieTalkie\WalkieTalkie.fbx
FBX version: 7500
    WARNING: OGL normal not found for 'Radiophone_WalkieTalkie_Normal.png' in C:\Users\Windows10_new\Downloads\Gadgets&Electronics\WalkieTalkie
  Fixing: WalkieTalkie
    Wired MetallicSmoothness R -> Metallic
    Wired invert(MetallicSmoothness A) -> Roughness
    Set blend_method=OPAQUE (AlbedoTransparency depth=24, no real alpha)
  Applying real-world scale (x1.3000)...
    Scale x1.3000 applied to 1 mesh(es)
  Exporting: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\WalkieTalkie_GLB\WalkieTalkie.glb
21:34:10 | INFO: Starting glTF 2.0 export
21:34:10 | INFO: Extracting primitive: Mesh
21:34:10 | WARNING: More than one shader node tex image used for a texture. The resulting glTF sampler will behave like the first shader node tex image.
21:34:10 | INFO: Primitives created: 1
21:34:10 | INFO: Finished glTF 2.0 export in 0.41588306427001953 s

  -> Written: C:\Users\Windows10_new\Downloads\Gadgets&Electronics\WalkieTalkie_GLB\WalkieTalkie.glb
  SUCCESS: WalkieTalkie.glb

======================================================================
CONVERSION SUMMARY
======================================================================
  [OK] Console: OK
  [OK] Digital_Camera: OK
  [OK] Flashlight: OK
  [OK] Microphone: OK
  [OK] Radio: OK
  [OK] Router: OK
  [OK] SecurityCamera: OK
  [OK] USB_Stick: OK
  [OK] VR_Goggles: OK
  [OK] WalkieTalkie: OK

All 10 models converted successfully.

Blender quit

C:\Users\Windows10_new\Downloads>
```
