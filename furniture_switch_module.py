import bpy
from bpy.types import Operator

def load_furniture_asset(object_name):
    """
    Placeholder function to load furniture objects.
    Replace this with actual logic to append/link .blend assets.
    """
    # For now, just create a cube as a dummy object
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = object_name
    return obj

class MIO_OT_switch_furniture(Operator):
    """Switch the selected furniture object to a new model"""
    bl_idname = "mio.switch_furniture"
    bl_label = "Switch Selected Furniture"
    bl_options = {'REGISTER', 'UNDO'}

    # Property passed from the panel
    new_model: bpy.props.StringProperty()

    def execute(self, context):
        selected = context.selected_objects

        if not selected:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        for obj in selected:
            location = obj.location.copy()
            rotation = obj.rotation_euler.copy()
            scale = obj.scale.copy()

            # Delete old object
            bpy.data.objects.remove(obj, do_unlink=True)

            # Load new object
            new_obj = load_furniture_asset(self.new_model)

            # Apply location, rotation, scale
            new_obj.location = location
            new_obj.rotation_euler = rotation
            new_obj.scale = scale

        self.report({'INFO'}, f"Switched {len(selected)} object(s) to {self.new_model}")
        return {'FINISHED'}
