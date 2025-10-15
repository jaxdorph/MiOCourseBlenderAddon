import bpy
import os

# ——————————————————————————————————————————————————————————
# MARK: FURNITURE SWITCHING MODULE
# ——————————————————————————————————————————————————————————
# Handles replacing selected furniture objects with another
# model of the same type, loading models and materials from
# the add-on’s asset library.
# ——————————————————————————————————————————————————————————


# ——————————————————————————————————————————————————————————
# MARK: UTILITY FUNCTIONS
# ——————————————————————————————————————————————————————————

def get_asset_path():
    """Return absolute path to the add-on's 'assets' folder."""
    addon_dir = os.path.dirname(__file__)
    return os.path.join(addon_dir, "assets")


def load_furniture_asset(room_type, object_name):
    """Load a furniture object from the add-on's asset library."""
    blend_path = os.path.join(get_asset_path(), f"{room_type}.blend")

    if not os.path.exists(blend_path):
        print(f"[MiO] Missing asset file: {blend_path}")
        return None

    # Load the object from the .blend file
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects = [object_name]
        else:
            print(f"[MiO] Object '{object_name}' not found in {blend_path}")
            return None

    obj = data_to.objects[0]
    bpy.context.collection.objects.link(obj)
    return obj


# ——————————————————————————————————————————————————————————
# MARK: FURNITURE SWITCH OPERATOR
# ——————————————————————————————————————————————————————————

class MIO_OT_switch_furniture(bpy.types.Operator):
    """Replace selected furniture with another model of the same type."""
    bl_idname = "mio.switch_furniture"
    bl_label = "Switch Selected Furniture"
    bl_description = "Replace selected furniture with another model"

    new_model: bpy.props.StringProperty(
        name="New Model Name",
        description="Name of the new furniture model to load"
    )

    def execute(self, context):
        selected = context.active_object
        if not selected:
            self.report({'ERROR'}, "No furniture object selected.")
            return {'CANCELLED'}

        print(f"[MiO] Switching furniture: {selected.name}")

        # Get the room type (could be inferred later)
        room_type = "Kitchen"  # Placeholder — later detect from object metadata
        new_name = self.new_model or "Table_Modern"

        # Load new asset
        new_obj = load_furniture_asset(room_type, new_name)
        if not new_obj:
            self.report({'ERROR'}, f"Could not load {new_name}")
            return {'CANCELLED'}

        # Replace old furniture
        new_obj.location = selected.location
        bpy.data.objects.remove(selected, do_unlink=True)

        self.report({'INFO'}, f"Switched to {new_name}")
        return {'FINISHED'}


# ——————————————————————————————————————————————————————————
# MARK: REGISTRATION
# ——————————————————————————————————————————————————————————

def register():
    bpy.utils.register_class(MIO_OT_switch_furniture)

def unregister():
    bpy.utils.unregister_class(MIO_OT_switch_furniture)
