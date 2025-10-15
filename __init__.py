import bpy

bl_info = {
    "name": "MiOCourseBlenderAddon",
    "description": "Simple interior room designer addon with room and furniture spawning functionality.",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "3D Viewport > N Panel > MiO",
    "support": "COMMUNITY",
    "category": "3D View",
}

# ——————————————————————————————————————————————————————————
# MARK: IMPORTS
# ——————————————————————————————————————————————————————————

import bpy

# When reloading inside Blender’s text editor:
if "bpy" in locals():
    from importlib import reload
    reload(spawn_room_module)
    reload(furniture_switch_module)
else:
    from . import spawn_room_module
    from . import furniture_switch_module


# ——————————————————————————————————————————————————————————
# MARK: CLASS REGISTRATION
# ——————————————————————————————————————————————————————————

# All classes Blender should know about go here
classes = [
    spawn_room_module.MIOProperties,
    spawn_room_module.MIO_OT_spawn_room,
    spawn_room_module.MIO_PT_main,
    furniture_switch_module.MIO_OT_switch_furniture,
]


# ——————————————————————————————————————————————————————————
# MARK: REGISTER / UNREGISTER
# ——————————————————————————————————————————————————————————

def register():
    """Register all addon classes and properties."""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Property group registered here (required by assignment)
    bpy.types.Scene.mio_props = bpy.props.PointerProperty(type=spawn_room_module.MIOProperties)


def unregister():
    """Unregister all addon classes and clean up properties."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.mio_props


if __name__ == "__main__":
    register()
