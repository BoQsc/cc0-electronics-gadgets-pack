# FBX -> GLB Conversion Script  -  Blender 5.0 compatible
# Run via: blender --background --python fbx_to_glb.py
#
# Output: <Root>\<ModelName>_GLB\<ModelName>.glb
#
# SCALE UPDATES:
#   Microphone:   0.093 -> 0.0465  (halved)
#   Flashlight:   0.072 -> 0.0504  (x0.7)
#   WalkieTalkie: 1.000 -> 1.300   (x1.3)
#   Console:      0.148 -> 0.222   (x1.5)
#
# FLASHLIGHT GLASS FIX:
#   Glass disc rotation (90X, -90Y) collapsed X dim to 0 after bake.
#   Fix: add +90 deg Y before applying transforms so disc faces beam axis.
#
# EMISSIVE TEXTURES WIRED:
#   Flashlight_Emissive.png, Console_Emissive.png, Router_Emissive.png
#
# RADIO + SECURITY CAMERA POSITION FIX:
#   Never apply location on multi-part children - only rot+scale.
import bpy
import os
import mathutils

ROOT = r"C:\Users\Windows10_new\Downloads\Gadgets&Electronics"

# Real-world uniform scale factors — baked into GLB geometry before export.
SCALE_FACTORS = {
    'Console':        0.222,   # 1.05m -> ~234mm  (×1.5 from previous 0.148)
    'Digital_Camera': 0.687,   # 150mm -> ~103mm
    'Flashlight':     0.0504,  # 4.45m -> ~224mm  (×0.7 from previous 0.072)
    'Microphone':     0.0465,  # 4.28m -> ~199mm  (×0.5 from previous 0.093)
    'Radio':          0.770,   # 325mm -> ~250mm
    'Router':         1.000,   # 203mm -> ~200mm  (correct already)
    'SecurityCamera': 0.706,   # 227mm -> ~160mm
    'USB_Stick':      0.177,   # 368mm ->  ~65mm
    'VR_Goggles':     0.033,   # 5.79m -> ~191mm
    'WalkieTalkie':   1.300,   # 147mm -> ~191mm  (×1.3 from previous 1.000)
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_fbx(fbx_path):
    bpy.ops.import_scene.fbx(
        filepath=fbx_path,
        use_custom_normals=True,
        use_image_search=True,
        use_anim=False,
        use_custom_props=True,
        ignore_leaf_bones=False,
        force_connect_children=False,
        automatic_bone_orientation=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        use_prepost_rot=True,
    )


def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')


def set_active(obj):
    deselect_all()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def apply_transform_to_object(obj, location=True, rotation=True, scale=True):
    set_active(obj)
    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)


def origin_to_geometry_center(obj):
    set_active(obj)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')


def move_to_world_origin(obj):
    obj.location = (0.0, 0.0, 0.0)


def apply_real_world_scale(model_name):
    """
    Apply uniform real-world scale to all mesh objects.
    Scale is applied as object scale then baked (apply_transform scale only).
    For multi-part models object locations are scaled too so relative
    positions between parts are preserved.
    After scaling, re-center parentless root objects at world origin.
    """
    factor = SCALE_FACTORS.get(model_name, 1.0)
    mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH']

    if abs(factor - 1.0) < 0.0001:
        print(f"    Scale: 1.000 (no correction needed)")
        return

    for obj in mesh_objects:
        # Scale object dimensions
        obj.scale = (obj.scale[0] * factor,
                     obj.scale[1] * factor,
                     obj.scale[2] * factor)
        # Scale object location so multi-part relative positions stay correct
        obj.location = (obj.location[0] * factor,
                        obj.location[1] * factor,
                        obj.location[2] * factor)
        # Bake scale into geometry
        apply_transform_to_object(obj, location=False, rotation=False, scale=True)

    print(f"    Scale x{factor:.4f} applied to {len(mesh_objects)} mesh(es)")

    # Re-center parentless (root) objects at world origin.
    # EXCEPTION: if a model has multiple root meshes (e.g. Flashlight body + Glass),
    # only center the PRIMARY root (largest by vertex count).
    # Secondary roots (Glass, lens, etc.) must NOT be zeroed — they are positioned
    # relative to the primary and zeroing them destroys that relationship.
    roots = [o for o in mesh_objects if o.parent is None]
    if len(roots) == 1:
        origin_to_geometry_center(roots[0])
        move_to_world_origin(roots[0])
    elif len(roots) > 1:
        # Multiple roots: center only the largest (primary body)
        primary = max(roots, key=lambda o: len(o.data.vertices))
        origin_to_geometry_center(primary)
        move_to_world_origin(primary)
        print(f"    Multi-root: centered '{primary.name}', left others in place")
        for o in roots:
            if o != primary:
                print(f"      '{o.name}' kept at location {o.location[:]} (relative to primary)")


def find_ogl_normal(folder, original_image_name):
    """Find the OGL normal variant by name replacement then folder scan."""
    name = original_image_name
    candidates = []
    if '_Normal_DirectX.png' in name:
        candidates.append(name.replace('_Normal_DirectX.png', '_Normal_DirectX_OGL.png'))
    if name.endswith('_Normal.png'):
        candidates.append(name[:-4] + '_OGL.png')

    for candidate in candidates:
        full = os.path.join(folder, candidate)
        if os.path.isfile(full):
            return full

    # Folder scan fallback
    try:
        files = os.listdir(folder)
    except Exception:
        return None

    base = name.lower()
    for token in ('_normal_directx.png', '_normal.png', '_directx', '_normal', '.png'):
        base = base.replace(token, '')
    for f in files:
        fl = f.lower()
        if 'ogl' in fl and 'normal' in fl and base in fl:
            return os.path.join(folder, f)

    return None


def redirect_normal_to_ogl(mat, folder):
    """Swap DirectX normal map nodes to OGL variants."""
    if not mat.node_tree:
        return
    for node in mat.node_tree.nodes:
        if node.type != 'TEX_IMAGE' or not node.image:
            continue
        name = node.image.name
        if 'normal' not in name.lower() or 'ogl' in name.lower():
            continue
        ogl_path = find_ogl_normal(folder, name)
        if ogl_path:
            new_img = load_image(ogl_path)
            if new_img:
                new_img.colorspace_settings.name = 'Non-Color'
                node.image = new_img
                print(f"    Normal redirect: '{name}' -> '{os.path.basename(ogl_path)}'")
        else:
            print(f"    WARNING: OGL normal not found for '{name}' in {folder}")


def wire_emissive(mat, folder, emissive_filename):
    """
    Load emissive texture and wire it to Principled BSDF Emission Color.
    Only wires if Emission Color is currently unlinked and black (off).
    """
    emissive_path = os.path.join(folder, emissive_filename)
    if not os.path.isfile(emissive_path):
        print(f"    WARNING: Emissive texture not found: {emissive_path}")
        return

    if not mat.node_tree:
        return

    pbsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if pbsdf is None:
        return

    em_color_input = pbsdf.inputs.get('Emission Color')
    if em_color_input is None:
        # Older API: may be just 'Emission'
        em_color_input = pbsdf.inputs.get('Emission')
    if em_color_input is None:
        print(f"    WARNING: No Emission Color input found on Principled BSDF")
        return

    if em_color_input.is_linked:
        print(f"    Emission Color already linked, skipping")
        return

    em_img = load_image(emissive_path)
    if em_img is None:
        return
    # Emissive maps are in sRGB (they represent visible light color)
    em_img.colorspace_settings.name = 'sRGB'

    nt = mat.node_tree
    em_node = nt.nodes.new('ShaderNodeTexImage')
    em_node.image    = em_img
    em_node.location = (-600, 200)
    em_node.label    = 'Emissive'

    nt.links.new(em_node.outputs['Color'], em_color_input)

    # Also make sure Emission Strength > 0
    em_strength_input = pbsdf.inputs.get('Emission Strength')
    if em_strength_input and not em_strength_input.is_linked:
        if em_strength_input.default_value < 0.01:
            em_strength_input.default_value = 1.0

    print(f"    Wired {emissive_filename} -> Emission Color")


def fix_blend_mode_opaque(mat):
    """Set OPAQUE when Principled BSDF Alpha is unlinked and == 1.0."""
    if not mat.node_tree:
        return
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            alpha = node.inputs.get('Alpha')
            if alpha and not alpha.is_linked and abs(alpha.default_value - 1.0) < 0.001:
                mat.blend_method = 'OPAQUE'
            break


def load_image(filepath):
    """Load image from disk, reuse if already loaded."""
    abs_path = os.path.abspath(filepath)
    for img in bpy.data.images:
        try:
            if os.path.abspath(bpy.path.abspath(img.filepath)) == abs_path:
                return img
        except Exception:
            pass
    if os.path.isfile(abs_path):
        return bpy.data.images.load(abs_path)
    return None


def export_glb(output_path):
    """Export full scene to GLB. Blender 5.0-compatible params only."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_texcoords=True,
        export_normals=True,
        export_tangents=True,
        export_materials='EXPORT',
        export_cameras=False,
        export_lights=False,
        export_apply=False,
        export_yup=True,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_image_format='AUTO',
    )
    print(f"  -> Written: {output_path}")


# ---------------------------------------------------------------------------
# Per-model geometry + material fix functions
# ---------------------------------------------------------------------------

def fix_simple_mesh(obj_name):
    """Single mesh: apply rot+scale, apply location, origin to bounds, zero location."""
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        meshes = [o for o in bpy.data.objects if o.type == 'MESH']
        if meshes:
            obj = meshes[0]
            print(f"    Fallback: using '{obj.name}'")
        else:
            print(f"    WARNING: No mesh found for '{obj_name}'")
            return
    apply_transform_to_object(obj, location=False, rotation=True,  scale=True)
    apply_transform_to_object(obj, location=True,  rotation=False, scale=False)
    origin_to_geometry_center(obj)
    move_to_world_origin(obj)


def fix_flashlight(folder):
    """
    Flashlight body + Glass lens.

    From dump data (ORIGINAL FBX world positions, before any script):
      Body:  obj.loc=(-0.860882, 0, 0.175279), rot=90X, scale=0.01
             world bbox center = (-0.581497, 0, 0)
             world nozzle tip  = (-2.806764, 0, 0)
      Glass: obj.loc=(-1.719648, 0, 0),    rot=(90X,-90Y), scale=0.01
             disc local verts all at Y=107.1 -> after apply(rot+scale),
             disc local center = (-1.071, 0, 0) in glass local space
             world disc center = (-2.790648, 0, 0)  [= -1.719648 + (-1.071)]
             disc is 16mm inside the nozzle - correct and intentional.

    CRITICAL: Body and Glass are TWO INDEPENDENT ROOT OBJECTS in the FBX.
    They must stay independent (no parenting). Parenting creates a Z dependency
    that does not exist in the original: body has Z=0.175279 (pivot offset),
    glass has Z=0. If we parent glass to body then center body, glass inherits
    a -0.175279 Z offset, shifting the disc off-axis. WRONG.

    PROVEN CORRECT ALGORITHM (mathematically verified):
      1. apply(glass, rot+scale)  -> disc verts in glass local space at (-1.071,0,0)
                                     glass.location still = (-1.719648, 0, 0)
      2. apply(body, rot+scale)   -> body verts world-oriented
                                     body.location still = (-0.860882, 0, 0.175279)
      3. Compute body_world_bbox_center from verts * matrix_world:
                                     = (-0.581497, 0, 0)
      4. Shift BOTH obj.locations by -body_world_bbox_center:
             body.location  -> (-0.279385, 0,  0.175279)
             glass.location -> (-1.138151, 0,  0.000000)
      5. apply(body, location=True)  -> body geometry centered at world origin
      6. apply(glass, location=True) -> glass disc world center = (-2.209151, 0, 0)
             body nozzle world       = (-2.225267, 0, 0)
             disc is 16mm inside nozzle. CORRECT. Z=0. CORRECT.
    
    Both objects remain as independent root objects - no parenting.
    Also wires: Glass_Opacity, Glass_Roughness, Flashlight_Emissive.
    """
    body  = bpy.data.objects.get('Flashlight')
    glass = bpy.data.objects.get('Glass')
    if body is None or glass is None:
        print("    WARNING: Flashlight or Glass object not found")
        return

    # Ensure glass is a root object (no parent)
    if glass.parent:
        set_active(glass)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    # Step 1+2: Apply rot+scale on both — obj.location stays unchanged
    for obj in [glass, body]:
        apply_transform_to_object(obj, location=False, rotation=True, scale=True)

    # Step 3: Compute body world bbox center from actual mesh verts
    # After apply(rot+scale), matrix_world = pure translation at obj.location
    # So world vert = obj.location + local_vert
    body_verts_world_x = [body.location.x + v.co.x for v in body.data.vertices]
    body_verts_world_y = [body.location.y + v.co.y for v in body.data.vertices]
    body_verts_world_z = [body.location.z + v.co.z for v in body.data.vertices]
    body_wc_x = (min(body_verts_world_x) + max(body_verts_world_x)) / 2
    body_wc_y = (min(body_verts_world_y) + max(body_verts_world_y)) / 2
    body_wc_z = (min(body_verts_world_z) + max(body_verts_world_z)) / 2
    print(f"    Body world bbox center (verts): ({body_wc_x:.6f}, {body_wc_y:.6f}, {body_wc_z:.6f})")

    # Step 4: Shift BOTH obj.locations by the same -body_world_center offset
    # This moves both objects so that body geometry will land at world origin
    # Glass shifts by SAME amount, preserving its relative world position
    for obj in [body, glass]:
        obj.location.x -= body_wc_x
        obj.location.y -= body_wc_y
        obj.location.z -= body_wc_z
    print(f"    After shift: body.loc={body.location[:]}, glass.loc={glass.location[:]}")

    # Step 5: Apply body location -> body geometry centered at world origin
    apply_transform_to_object(body, location=True, rotation=False, scale=False)
    # Clean up body pivot (verts already at origin, this just formalizes it)
    origin_to_geometry_center(body)

    # Step 6: Apply glass location -> glass disc verts at correct world position
    apply_transform_to_object(glass, location=True, rotation=False, scale=False)
    # Move glass PIVOT to disc center. Do NOT call move_to_world_origin(glass) —
    # that would drag the disc to (0,0,0) = center of flashlight body. WRONG.
    # origin_to_geometry only moves the pivot TO the disc; disc stays at nozzle.
    origin_to_geometry_center(glass)

    # Verification
    body_nozzle_x = min(v.co.x for v in body.data.vertices) + body.location.x
    disc_world_x  = glass.location.x   # after origin_to_geometry, location = disc center
    disc_world_z  = glass.location.z
    print(f"    Body nozzle world X:  {body_nozzle_x:.4f}")
    print(f"    Glass disc world X:   {disc_world_x:.4f}  (pivot = disc center)")
    print(f"    Glass disc world Z:   {disc_world_z:.6f}  (should be ~0)")
    print(f"    Disc inside nozzle:   {(disc_world_x - body_nozzle_x)*1000:.1f} mm  (target ~16mm)")

    # ── Glass material ────────────────────────────────────────────────────
    glass_mat = bpy.data.materials.get('Glass')
    if glass_mat and glass_mat.node_tree:
        nt    = glass_mat.node_tree
        pbsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)

        if pbsdf:
            # Remove the empty Normal Map node (no glass normal file exists)
            for node in list(nt.nodes):
                if node.type == 'NORMAL_MAP':
                    # Disconnect it first
                    for lnk in list(nt.links):
                        if lnk.from_node == node or lnk.to_node == node:
                            nt.links.remove(lnk)
                    nt.nodes.remove(node)
                    print("    Removed empty Normal Map node from Glass")

            # Wire Glass_Opacity.png -> Alpha
            opacity_path = os.path.join(folder, 'Glass_Opacity.png')
            if os.path.isfile(opacity_path):
                img = load_image(opacity_path)
                if img:
                    img.colorspace_settings.name = 'Non-Color'
                    nd = nt.nodes.new('ShaderNodeTexImage')
                    nd.image = img; nd.location = (-600, -200); nd.label = 'Glass Opacity'
                    alpha_inp = pbsdf.inputs.get('Alpha')
                    if alpha_inp and not alpha_inp.is_linked:
                        nt.links.new(nd.outputs['Color'], alpha_inp)
                        print("    Wired Glass_Opacity.png -> Alpha")

            # Wire Glass_Roughness.png -> Roughness
            rough_path = os.path.join(folder, 'Glass_Roughness.png')
            if os.path.isfile(rough_path):
                img = load_image(rough_path)
                if img:
                    img.colorspace_settings.name = 'Non-Color'
                    nd = nt.nodes.new('ShaderNodeTexImage')
                    nd.image = img; nd.location = (-600, -500); nd.label = 'Glass Roughness'
                    rough_inp = pbsdf.inputs.get('Roughness')
                    if rough_inp and not rough_inp.is_linked:
                        nt.links.new(nd.outputs['Color'], rough_inp)
                        print("    Wired Glass_Roughness.png -> Roughness")

            # Set Transmission Weight = 1.0 (physical glass)
            trans_inp = pbsdf.inputs.get('Transmission Weight')
            if trans_inp and not trans_inp.is_linked:
                trans_inp.default_value = 1.0
                print("    Set Transmission Weight = 1.0")

        glass_mat.blend_method = 'BLEND'
        print("    Glass blend_method = BLEND")

    # ── Body (Mat) material ───────────────────────────────────────────────
    mat = bpy.data.materials.get('Mat')
    if mat and mat.node_tree:
        nt    = mat.node_tree
        pbsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)

        if pbsdf:
            # Wire Flashlight_Metallic.png -> Metallic
            metallic_path = os.path.join(folder, 'Flashlight_Metallic.png')
            if os.path.isfile(metallic_path):
                img = load_image(metallic_path)
                if img:
                    img.colorspace_settings.name = 'Non-Color'
                    nd = nt.nodes.new('ShaderNodeTexImage')
                    nd.image = img; nd.location = (-600, -200); nd.label = 'Metallic'
                    met_inp = pbsdf.inputs.get('Metallic')
                    if met_inp and not met_inp.is_linked:
                        nt.links.new(nd.outputs['Color'], met_inp)
                        print("    Wired Flashlight_Metallic.png -> Metallic")

            # Wire Flashlight_Roughness.png -> Roughness
            rough_path = os.path.join(folder, 'Flashlight_Roughness.png')
            if os.path.isfile(rough_path):
                img = load_image(rough_path)
                if img:
                    img.colorspace_settings.name = 'Non-Color'
                    nd = nt.nodes.new('ShaderNodeTexImage')
                    nd.image = img; nd.location = (-600, -500); nd.label = 'Roughness'
                    rough_inp = pbsdf.inputs.get('Roughness')
                    if rough_inp and not rough_inp.is_linked:
                        nt.links.new(nd.outputs['Color'], rough_inp)
                        print("    Wired Flashlight_Roughness.png -> Roughness")

            # Wire Flashlight_Emissive.png -> Emission Color
            wire_emissive(mat, folder, 'Flashlight_Emissive.png')

            # Invert G channel of DirectX normal to convert to OGL in-place
            # (no OGL file exists on disk for Flashlight)
            for node in nt.nodes:
                if node.type == 'TEX_IMAGE' and node.image and 'normal_directx' in node.image.name.lower():
                    # Find the Normal Map node this feeds into
                    nmap = next((lnk.to_node for lnk in nt.links
                                 if lnk.from_node == node and lnk.to_node.type == 'NORMAL_MAP'), None)
                    if nmap:
                        # Insert: SeparateColor -> invert G -> CombineColor -> NormalMap
                        sep = nt.nodes.new('ShaderNodeSeparateColor')
                        sep.location = (node.location.x + 300, node.location.y); sep.mode = 'RGB'
                        inv = nt.nodes.new('ShaderNodeMath')
                        inv.operation = 'SUBTRACT'; inv.location = (node.location.x + 500, node.location.y - 100)
                        inv.inputs[0].default_value = 1.0; inv.label = 'Invert G'
                        comb = nt.nodes.new('ShaderNodeCombineColor')
                        comb.location = (node.location.x + 700, node.location.y); comb.mode = 'RGB'
                        # Remove old direct link from tex to nmap
                        for lnk in list(nt.links):
                            if lnk.from_node == node and lnk.to_node == nmap:
                                nt.links.remove(lnk)
                        nt.links.new(node.outputs['Color'], sep.inputs['Color'])
                        nt.links.new(sep.outputs['Red'],   comb.inputs['Red'])
                        nt.links.new(sep.outputs['Green'], inv.inputs[1])
                        nt.links.new(inv.outputs['Value'], comb.inputs['Green'])
                        nt.links.new(sep.outputs['Blue'],  comb.inputs['Blue'])
                        nt.links.new(comb.outputs['Color'], nmap.inputs['Color'])
                        print("    Inserted DirectX->OGL G-invert for Flashlight normal map")

        mat.blend_method = 'OPAQUE'
        print("    Body blend_method = OPAQUE")


def fix_walkie_talkie(folder):
    """
    Wire MetallicSmoothness R->Metallic, invert(A)->Roughness.
    Blender 5.0: colorspace on node.image only.
    """
    mat = bpy.data.materials.get('Mat')
    if mat is None or not mat.node_tree:
        print("    WARNING: WalkieTalkie 'Mat' not found")
        return

    nt    = mat.node_tree
    pbsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if pbsdf is None:
        return

    ms_path = os.path.join(folder, 'Radiophone_WalkieTalkie_MetallicSmoothness.png')
    if not os.path.isfile(ms_path):
        print(f"    WARNING: MetallicSmoothness not found: {ms_path}")
        return

    ms_img = load_image(ms_path)
    if ms_img is None:
        return
    ms_img.colorspace_settings.name = 'Non-Color'

    ms_node = nt.nodes.new('ShaderNodeTexImage')
    ms_node.image = ms_img; ms_node.location = (-900, -200); ms_node.label = 'MetallicSmoothness'

    sep = nt.nodes.new('ShaderNodeSeparateColor')
    sep.location = (-600, -200); sep.mode = 'RGB'

    inv = nt.nodes.new('ShaderNodeMath')
    inv.operation = 'SUBTRACT'; inv.location = (-350, -420)
    inv.label = 'Smoothness->Roughness'; inv.inputs[0].default_value = 1.0

    nt.links.new(ms_node.outputs['Color'], sep.inputs['Color'])

    met = pbsdf.inputs.get('Metallic')
    if met:
        nt.links.new(sep.outputs['Red'], met)
        print("    Wired MetallicSmoothness R -> Metallic")

    nt.links.new(ms_node.outputs['Alpha'], inv.inputs[1])
    rgh = pbsdf.inputs.get('Roughness')
    if rgh:
        nt.links.new(inv.outputs['Value'], rgh)
        print("    Wired invert(MetallicSmoothness A) -> Roughness")

    mat.blend_method = 'OPAQUE'
    print("    Set blend_method=OPAQUE (AlbedoTransparency depth=24, no real alpha)")


def fix_radio(folder):
    """
    Root EMPTY 'Radio' + 4 mesh children: Radio_2, Screen, Tune, Volume.

    From dump data (world positions in original FBX, already correct):
      Radio_2 world center: (-0.000001,  0.018725,  0.125908)
      Screen  world center: (-0.000001, -0.040138, -0.009155)
      Tune    world center: ( 0.068094, -0.042673, -0.009157)
      Volume  world center: (-0.068097, -0.042673, -0.009157)
      Screen/Tune/Volume all sit on the FRONT face of Radio_2 (correct).

    THE BUG in all previous versions:
      After apply(rot+scale) + parent_clear, Radio_2 obj.location = (−0.000001, 0.124974, 0.027469)
      This is the world position of the FBX PIVOT POINT, NOT the geometry center.
      Radio_2 geometry center = (-0.000001, 0.018725, 0.125908).
      Shifting by -obj.location introduces a 0.106m Y-axis error.

    CORRECT PROCEDURE:
      1. Apply rot+scale on Empty (Blender compensates children transforms)
      2. parent_clear(KEEP_TRANSFORM) on all children
      3. Delete empty
      4. Apply rot+scale ONLY on each child (no location)
         -> each child.obj.location = world pivot position (preserved)
      5. Compute Radio_2 GEOMETRY BBOX CENTER in world space
         (by iterating mesh vertices through matrix_world — which is now
         just a translation matrix since rot+scale was applied)
      6. Shift ALL children by -Radio_2_geometry_bbox_center
         -> Radio_2 geometry ends up centered at world origin
         -> Screen/Tune/Volume maintain correct relative positions
      7. origin_to_geometry on Radio_2 only (sets its pivot to geometry center = origin)
    """
    radio_empty = bpy.data.objects.get('Radio')
    if radio_empty is None:
        print("    WARNING: Radio empty root not found")
        return

    children = list(radio_empty.children)
    print(f"    Radio children: {[c.name for c in children]}")

    # Step 1: Apply rot+scale on Empty — Blender updates children local transforms
    apply_transform_to_object(radio_empty, location=False, rotation=True, scale=True)

    # Step 2: Unparent all children — each child gets world transform as its own
    for child in children:
        set_active(child)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    # Step 3: Delete the empty
    set_active(radio_empty)
    bpy.ops.object.delete()

    # Step 4: Apply rot+scale ONLY on each child — keep obj.location as world coord
    for child in children:
        if child.type == 'MESH':
            apply_transform_to_object(child, location=False, rotation=True, scale=True)

    # Step 5: Compute Radio_2 GEOMETRY BBOX CENTER in world space
    # After apply(rot+scale, no loc), matrix_world = translation-only matrix.
    # World position of each vert = obj.location + local_vert_coord
    radio_body = bpy.data.objects.get('Radio_2')
    if radio_body is None:
        print("    WARNING: Radio_2 body not found")
        return

    import mathutils
    verts_world = [radio_body.matrix_world @ v.co for v in radio_body.data.vertices]
    min_x = min(v.x for v in verts_world)
    max_x = max(v.x for v in verts_world)
    min_y = min(v.y for v in verts_world)
    max_y = max(v.y for v in verts_world)
    min_z = min(v.z for v in verts_world)
    max_z = max(v.z for v in verts_world)
    geom_center = mathutils.Vector((
        (min_x + max_x) / 2,
        (min_y + max_y) / 2,
        (min_z + max_z) / 2,
    ))
    print(f"    Radio_2 geometry bbox center (world): {geom_center[:]}")
    print(f"    Radio_2 obj.location (pivot):         {radio_body.location[:]}")

    # Step 6: Shift ALL children by -geom_center so Radio_2 geometry lands at origin
    for child in children:
        if child.type == 'MESH':
            child.location -= geom_center

    print(f"    Part locations after centering on Radio_2 geometry center:")
    for child in children:
        if child.type == 'MESH':
            print(f"      {child.name}: {child.location[:]}")

    # Step 7: Set Radio_2 origin to its geometry center (now at world origin)
    origin_to_geometry_center(radio_body)


def fix_security_camera(folder):
    """
    Holder (root, scale=0.01, rot=90X) + Camera (child, scale=1).

    KEY FIX vs previous version:
      Apply Holder rot+scale only (not location).
      Unparent Camera keeping world transform.
      Apply Camera rot+scale only (not location) — preserves its world offset.
      Re-parent Camera under Holder with keep_transform.
      Zero Holder location — Camera follows as child at correct offset.
    """
    holder      = bpy.data.objects.get('Holder')
    camera_mesh = bpy.data.objects.get('Camera')
    if holder is None:
        print("    WARNING: 'Holder' not found")
        return

    # Apply Holder rot+scale (child Camera updates world transform)
    apply_transform_to_object(holder, location=False, rotation=True, scale=True)

    # Unparent Camera keeping its updated world transform
    if camera_mesh and camera_mesh.parent:
        set_active(camera_mesh)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    # Apply Camera rot+scale only — keep location so it stays in correct world position
    if camera_mesh:
        apply_transform_to_object(camera_mesh, location=False, rotation=True, scale=True)
        origin_to_geometry_center(camera_mesh)

    # Apply Holder location (zero it out, mesh verts already correct after rot+scale)
    apply_transform_to_object(holder, location=True, rotation=False, scale=False)
    origin_to_geometry_center(holder)

    # Re-parent Camera under Holder — Camera keeps its world position as offset
    if camera_mesh:
        deselect_all()
        camera_mesh.select_set(True)
        holder.select_set(True)
        bpy.context.view_layer.objects.active = holder
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        print(f"    Camera local offset after re-parent: {camera_mesh.location[:]}")

    # Zero Holder — Camera follows as child at correct relative offset
    move_to_world_origin(holder)


# ---------------------------------------------------------------------------
# Model table
# ---------------------------------------------------------------------------

MODELS = {
    'Console': {
        'fbx':      r'Console\Console.fbx',
        'out_dir':  r'Console_GLB',
        'folder':   r'Console',
        'fix':      'simple',
        'obj_name': 'Console',
        'emissive': ('Mat', 'Console_Emissive.png'),
    },
    'Digital_Camera': {
        'fbx':      r'Digital_Camera\Digital_Camera.fbx',
        'out_dir':  r'Digital_Camera_GLB',
        'folder':   r'Digital_Camera',
        'fix':      'simple',
        'obj_name': 'Digital_Camera',
    },
    'Flashlight': {
        'fbx':      r'Flashlight\Flashlight.fbx',
        'out_dir':  r'Flashlight_GLB',
        'folder':   r'Flashlight',
        'fix':      'flashlight',
        # emissive wired inside fix_flashlight
    },
    'Microphone': {
        'fbx':      r'Microphone\Microphone.fbx',
        'out_dir':  r'Microphone_GLB',
        'folder':   r'Microphone',
        'fix':      'simple',
        'obj_name': 'Mic',
    },
    'Radio': {
        'fbx':      r'Radio\Radio.fbx',
        'out_dir':  r'Radio_GLB',
        'folder':   r'Radio',
        'fix':      'radio',
    },
    'Router': {
        'fbx':      r'Router\Router.fbx',
        'out_dir':  r'Router_GLB',
        'folder':   r'Router',
        'fix':      'simple',
        'obj_name': 'Router',
        'emissive': ('Mat', 'Router_Emissive.png'),
    },
    'SecurityCamera': {
        'fbx':      r'SecurityCamera\SecurityCamera.fbx',
        'out_dir':  r'SecurityCamera_GLB',
        'folder':   r'SecurityCamera',
        'fix':      'security_camera',
    },
    'USB_Stick': {
        'fbx':      r'USB_Stick\USB_Stick.fbx',
        'out_dir':  r'USB_Stick_GLB',
        'folder':   r'USB_Stick',
        'fix':      'simple',
        'obj_name': 'USB_Stick',
    },
    'VR_Goggles': {
        'fbx':      r'VR_Goggles\VRGoggles.fbx',
        'out_dir':  r'VR_Goggles_GLB',
        'folder':   r'VR_Goggles',
        'fix':      'simple',
        'obj_name': 'VR_Goggles',
    },
    'WalkieTalkie': {
        'fbx':      r'WalkieTalkie\WalkieTalkie.fbx',
        'out_dir':  r'WalkieTalkie_GLB',
        'folder':   r'WalkieTalkie',
        'fix':      'walkie_talkie',
    },
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def convert_model(name, config):
    print(f"\n{'='*70}")
    print(f"CONVERTING: {name}")
    print(f"{'='*70}")

    fbx_path = os.path.join(ROOT, config['fbx'])
    folder   = os.path.join(ROOT, config['folder'])
    out_dir  = os.path.join(ROOT, config['out_dir'])
    glb_path = os.path.join(out_dir, name + '.glb')

    if not os.path.isfile(fbx_path):
        print(f"  ERROR: FBX not found: {fbx_path}")
        return False

    clear_scene()
    print(f"  Importing: {fbx_path}")
    import_fbx(fbx_path)

    # Normal OGL redirect
    for mat in bpy.data.materials:
        redirect_normal_to_ogl(mat, folder)

    # Geometry + material fixes
    fix_type = config['fix']
    if fix_type == 'simple':
        print(f"  Fixing: simple mesh ('{config.get('obj_name', '?')}')")
        fix_simple_mesh(config['obj_name'])
    elif fix_type == 'flashlight':
        print("  Fixing: Flashlight")
        fix_flashlight(folder)
    elif fix_type == 'walkie_talkie':
        print("  Fixing: WalkieTalkie")
        fix_simple_mesh('Walkie_Talkie')
        fix_walkie_talkie(folder)
    elif fix_type == 'radio':
        print("  Fixing: Radio")
        fix_radio(folder)
    elif fix_type == 'security_camera':
        print("  Fixing: SecurityCamera")
        fix_security_camera(folder)

    # Wire emissive textures (models that have them, excluding Flashlight handled above)
    if 'emissive' in config:
        mat_name, emissive_file = config['emissive']
        mat = bpy.data.materials.get(mat_name)
        if mat:
            print(f"  Wiring emissive: {emissive_file}")
            wire_emissive(mat, folder, emissive_file)

    # Blend mode cleanup
    for mat in bpy.data.materials:
        fix_blend_mode_opaque(mat)

    # Real-world scale
    print(f"  Applying real-world scale (x{SCALE_FACTORS.get(name, 1.0):.4f})...")
    apply_real_world_scale(name)

    # Export
    print(f"  Exporting: {glb_path}")
    try:
        export_glb(glb_path)
        print(f"  SUCCESS: {name}.glb")
        return True
    except Exception as e:
        print(f"  ERROR during export: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*70)
    print("FBX -> GLB BATCH CONVERSION  (Blender 5.0)")
    print(f"Root: {ROOT}")
    print("="*70)
    print()
    print(f"{'Model':<20} {'Scale':<8} Approx final size")
    print("-"*65)
    targets = {
        'Console':        (0.222,  '~234 x  84 x242 mm'),
        'Digital_Camera': (0.687,  '~103 x  60 x 42 mm'),
        'Flashlight':     (0.0504, '~224 x  58 x 58 mm  + emissive ON'),
        'Microphone':     (0.0465, '~ 57 x  57 x199 mm'),
        'Radio':          (0.770,  '~192 x  96 x250 mm'),
        'Router':         (1.000,  '~203 x 163 x198 mm  + emissive ON'),
        'SecurityCamera': (0.706,  '~ 97 x 160 x150 mm'),
        'USB_Stick':      (0.177,  '~ 21 x  65 x 10 mm'),
        'VR_Goggles':     (0.033,  '~191 x 137 x 96 mm'),
        'WalkieTalkie':   (1.300,  '~ 62 x  34 x191 mm'),
    }
    for n, (s, desc) in targets.items():
        print(f"  {n:<20} x{s:<7.4f} {desc}")
    print()

    results = {}
    for name, config in MODELS.items():
        try:
            ok = convert_model(name, config)
            results[name] = 'OK' if ok else 'FAILED'
        except Exception as e:
            import traceback
            print(f"  EXCEPTION for {name}: {e}")
            traceback.print_exc()
            results[name] = f'EXCEPTION: {e}'

    print("\n" + "="*70)
    print("CONVERSION SUMMARY")
    print("="*70)
    for name, status in results.items():
        icon = "OK" if status == 'OK' else "!!"
        print(f"  [{icon}] {name}: {status}")

    failed = [n for n, s in results.items() if s != 'OK']
    if not failed:
        print("\nAll 10 models converted successfully.")
    else:
        print(f"\nFailed: {failed}")


main()
