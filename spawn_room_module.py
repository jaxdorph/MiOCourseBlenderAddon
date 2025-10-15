import bpy
from bpy.types import Operator, Panel

# Optional future import for real models
# from .furniture_switch_module import load_furniture_asset


# ——————————————————————————————————————————————————————————
# MARK: PROPERTIES
# ——————————————————————————————————————————————————————————
# Holds room type selection and other addon properties
# ——————————————————————————————————————————————————————————

class MIOProperties(bpy.types.PropertyGroup):
    """Holds addon settings such as room type selection."""
    room_type: bpy.props.EnumProperty(
        name="Room Type",
        description="Select which room to spawn",
        items=[
            ("KITCHEN", "Kitchen", ""),
            ("LIVING", "Living Room", ""),
            ("BEDROOM", "Bedroom", "")
        ],
        default="KITCHEN"
    )


# ——————————————————————————————————————————————————————————
# MARK: ROOM SPAWNER OPERATOR
# ——————————————————————————————————————————————————————————
# Handles creating a simple placeholder room setup
# ——————————————————————————————————————————————————————————

class MIO_OT_spawn_room(Operator):
    """Spawn a simple placeholder room. Later this will
    use actual 3D models loaded from .blend asset libraries."""
    bl_idname = "mio.spawn_room"
    bl_label = "Spawn Room"
    bl_description = "Spawn a selected room with placeholder furniture"

    def execute(self, context):
        props = context.scene.mio_props
        room = props.room_type

        # Clear old objects for testing (temporary)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Placeholder logic based on room type
        if room == "KITCHEN":
            self.spawn_kitchen(context)
        elif room == "LIVING":
            self.spawn_living(context)
        elif room == "BEDROOM":
            self.spawn_bedroom(context)

        self.report({'INFO'}, f"Spawned a {room.lower()}!")
        return {'FINISHED'}

    # ——————————————————————————————————————————————————————
    # MARK: ROOM BUILDERS
    # ——————————————————————————————————————————————————————
    # Simple placeholder geometry now, will use load_furniture_asset() later
    # ——————————————————————————————————————————————————————

    def spawn_kitchen(self, context):
        """Create placeholder kitchen geometry."""
        print("[MiO] Spawning placeholder kitchen...")
        bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 1))   # Room base
        bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 0.5)) # Counter
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, 0, 0.5))# Table

        # FUTURE:
        # table = load_furniture_asset("Kitchen", "Table_Modern")
        # fridge = load_furniture_asset("Kitchen", "Fridge_01")
        # cabinets = load_furniture_asset("Kitchen", "Cabinet_Set_01")

    def spawn_living(self, context):
        """Create placeholder living room geometry."""
        print("[MiO] Spawning placeholder living room...")
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(0, 0, 1))  # Sofa placeholder
        bpy.ops.mesh.primitive_cube_add(size=2, location=(2, 1, 0.5))         # Table

        # FUTURE:
        # sofa = load_furniture_asset("Living", "Sofa_Modern")
        # tv = load_furniture_asset("Living", "TV_Stand_01")

    def spawn_bedroom(self, context):
        """Create placeholder bedroom geometry."""
        print("[MiO] Spawning placeholder bedroom...")
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=0.3, location=(0, 0, 0.15))  # Bed base
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 1.5, 0.5))                 # Dresser

        # FUTURE:
        # bed = load_furniture_asset("Bedroom", "Bed_Classic")
        # nightstand = load_furniture_asset("Bedroom", "Nightstand_02")


# ——————————————————————————————————————————————————————————
# MARK: MAIN UI PANEL
# ——————————————————————————————————————————————————————————
# Appears under the “MiO” tab in the 3D Viewport’s N-panel
# ——————————————————————————————————————————————————————————

class MIO_PT_main(Panel):
    """Main user interface for the MiO Add-on."""
    bl_label = "MiO"
    bl_idname = "MIO_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mio_props

        layout.label(text="Room Spawner")
        layout.prop(props, "room_type", text="Room Type")
        layout.operator("mio.spawn_room", icon="HOME")

        layout.separator()
        layout.label(text="Furniture Controls")

        # Add a text input to type the new model name
        layout.prop(context.scene.mio_props, "furniture_model", text="New Model Name")

        # Button to switch selected furniture
        layout.operator(
            "mio.switch_furniture",
            text="Switch Selected Furniture",
            icon="FILE_REFRESH"
        )

