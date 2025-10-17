bl_info = {
    "name": "MiO Course Blender Addon",
    "author": "Johan Axdorph",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "View3D > N Panel > MiO",
    "description": "Spawn rooms, switch furniture, and change wall/floor colors",
    "category": "3D View",
}

import bpy

# Import our modules
from . import spawn_room_module
from . import furniture_switch_module

# Collect all classes to register
classes = (
    # Room classes
    spawn_room_module.MIORoomProperties,
    spawn_room_module.MIO_OT_spawn_room,
    spawn_room_module.MIO_OT_scale_room,
    spawn_room_module.MIO_OT_update_room_colors,
    spawn_room_module.MIO_OT_reset_room,
    spawn_room_module.MIO_PT_room_spawner,

    # Furniture classes
    furniture_switch_module.MIOFurnitureProperties,
    furniture_switch_module.MIO_OT_switch_furniture,
    furniture_switch_module.MIO_PT_furniture_switcher,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add scene properties
    bpy.types.Scene.mio_room_props = bpy.props.PointerProperty(type=spawn_room_module.MIORoomProperties)
    bpy.types.Scene.mio_furniture_props = bpy.props.PointerProperty(type=furniture_switch_module.MIOFurnitureProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Remove scene properties
    if hasattr(bpy.types.Scene, "mio_room_props"):
        del bpy.types.Scene.mio_room_props
    if hasattr(bpy.types.Scene, "mio_furniture_props"):
        del bpy.types.Scene.mio_furniture_props


if __name__ == "__main__":
    register()
