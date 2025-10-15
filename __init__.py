bl_info = {
    "name": "MiOCourseBlenderAddon",
    "description": "Simple interior room designer with furniture switching",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "3D Viewport > N Panel > MiO",
    "support": "COMMUNITY",
    "category": "3D View",
}

import bpy

# Reload modules for development
if "bpy" in locals():
    from importlib import reload
    from . import spawn_room_module
    from . import furniture_switch_module
    reload(spawn_room_module)
    reload(furniture_switch_module)
else:
    from . import spawn_room_module
    from . import furniture_switch_module

# List of classes to register
classes = [
    spawn_room_module.MIOProperties,
    spawn_room_module.MIO_OT_spawn_room,
    spawn_room_module.MIO_PT_main,
    furniture_switch_module.MIO_OT_switch_furniture,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mio_props = bpy.props.PointerProperty(type=spawn_room_module.MIOProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mio_props

if __name__ == "__main__":
    register()
