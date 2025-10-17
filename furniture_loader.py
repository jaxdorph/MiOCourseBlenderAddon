# ============================================================
# furniture_loader_module.py
# ------------------------------------------------------------
# Handles listing and loading furniture models from assets.
# ============================================================

import bpy
import os

# Root directory for all furniture assets
ASSET_ROOT = os.path.join(
    os.path.dirname(__file__), "assets"
)

# Subdirectories for each room type and category
FURNITURE_PATHS = {
    "bedroom": {
        "Beds": os.path.join(ASSET_ROOT, "bedroom", "Beds"),
        "Wardrobes": os.path.join(ASSET_ROOT, "bedroom", "Wardrobes"),
    },
    "kitchen": {
        "Kitchen Tables": os.path.join(ASSET_ROOT, "kitchen", "Kitchen Tables"),
        "Kitchen Chairs": os.path.join(ASSET_ROOT, "kitchen", "Kitchen Chairs"),
    },
    "livingroom": {
        "Sofas": os.path.join(ASSET_ROOT, "livingroom", "Sofas"),
        "Coffee Tables": os.path.join(ASSET_ROOT, "livingroom", "Coffee Tables"),
    },
}


def list_furniture_models(room_type, category):
    """Return a list of .blend files for the given room type and category."""
    models = []
    try:
        folder = FURNITURE_PATHS[room_type][category]
    except KeyError:
        print(f"[MiO Loader] Invalid room_type/category: {room_type}/{category}")
        return []

    if not os.path.exists(folder):
        print(f"[MiO Loader] Path does not exist: {folder}")
        return []

    for file in os.listdir(folder):
        if file.lower().endswith(".blend"):
            models.append(file)
    return models


def load_furniture_model(room_type, category, blend_name):
    """Append the furniture model from its .blend file and return appended objects."""
    try:
        folder = FURNITURE_PATHS[room_type][category]
    except KeyError:
        print(f"[MiO Loader] Invalid type/category: {room_type}/{category}")
        return []

    blend_path = os.path.join(folder, blend_name)
    if not os.path.exists(blend_path):
        print(f"[MiO Loader] Missing file: {blend_path}")
        return []

    # Collect object names before import to detect new ones
    existing_objects = set(bpy.data.objects.keys())

    # Objects inside the .blend file
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        # Try to import all top-level objects (Empty + children)
        data_to.objects = data_from.objects

    appended_objs = []
    for obj in data_to.objects:
        if obj is None:
            continue
        bpy.context.scene.collection.objects.link(obj)
        appended_objs.append(obj)

    # Ensure materials are linked properly (they should come with the object)
    for obj in appended_objs:
        if hasattr(obj.data, "materials"):
            for mat in obj.data.materials:
                if mat and mat.name not in bpy.data.materials:
                    bpy.data.materials.append(mat)

    # Move imported objects into a “MiO_Furniture” collection
    coll_name = "MiO_Furniture"
    mio_coll = bpy.data.collections.get(coll_name)
    if not mio_coll:
        mio_coll = bpy.data.collections.new(coll_name)
        bpy.context.scene.collection.children.link(mio_coll)

    for obj in appended_objs:
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        if obj.name not in mio_coll.objects:
            mio_coll.objects.link(obj)

    print(f"[MiO Loader] Appended {len(appended_objs)} objects from {blend_name}")
    return appended_objs


def clear_spawned_furniture():
    """Remove all furniture objects from the 'MiO_Furniture' collection."""
    coll = bpy.data.collections.get("MiO_Furniture")
    if not coll:
        return

    objs_to_remove = [obj for obj in coll.objects]
    for obj in objs_to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"[MiO Loader] Cleared {len(objs_to_remove)} furniture objects.")
