bl_info = { 
    "name": "MiOCourseBlenderAddon",
    "description": "Simple interior room designer with modular furniture switching.",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "3D Viewport > N Panel > MiO",
    "support": "COMMUNITY",
    "category": "3D View",
}

# ——————————————————————————————————————————————————————
# IMPORTS
# ——————————————————————————————————————————————————————
import bpy

# During development, allow reloading the submodules
if "bpy" in locals():
    from importlib import reload
    from . import spawn_room_module
    from . import furniture_switch_module
    reload(spawn_room_module)
    reload(furniture_switch_module)
else:
    from . import spawn_room_module
    from . import furniture_switch_module


# ——————————————————————————————————————————————————————
# REGISTRATION
# ——————————————————————————————————————————————————————
# List all operator, panel, and property classes here
classes = [
    spawn_room_module.MIOProperties,              # Property group for room settings
    spawn_room_module.MIO_OT_spawn_room,          # Operator for spawning rooms
    spawn_room_module.MIO_PT_main,                # Main MiO panel in N-panel
    furniture_switch_module.MIO_OT_switch_furniture,  # Operator for furniture switching
]


def register():
    """Register all add-on classes and properties."""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Store MiO properties on the Scene
    bpy.types.Scene.mio_props = bpy.props.PointerProperty(
        type=spawn_room_module.MIOProperties
    )


def unregister():
    """Unregister all add-on classes and remove properties."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.mio_props


# Only run register() when executed directly (useful for dev reloads)
if __name__ == "__main__":
    register()
