import bpy
from bpy.types import Panel, Operator, PropertyGroup

# -----------------------------
# Properties
# -----------------------------
class MIOProperties(PropertyGroup):
    """Holds addon settings for room type and furniture selection."""
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

    furniture_model: bpy.props.StringProperty(
        name="Furniture Model",
        description="Name of the furniture model to switch selected object to",
        default="Table_Modern"
    )

# -----------------------------
# Room Spawner Operator
# -----------------------------
class MIO_OT_spawn_room(bpy.types.Operator):
    """Spawns a room of the selected type with basic furniture"""
    bl_idname = "mio.spawn_room"
    bl_label = "Spawn Room"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        room_type = context.scene.mio_props.room_type
        self.report({'INFO'}, f"Spawning a {room_type}...")

        # Optional: deselect all
        bpy.ops.object.select_all(action='DESELECT')

        if room_type == "KITCHEN":
            # Floor
            bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
            floor = context.active_object
            floor.name = "Kitchen_Floor"

            # Table
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
            table = context.active_object
            table.name = "Kitchen_Table"

            # Chair
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1, 0, 0.25))
            chair = context.active_object
            chair.name = "Kitchen_Chair"

        elif room_type == "LIVING":
            # Floor
            bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
            floor = context.active_object
            floor.name = "Living_Floor"

            # Sofa
            bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
            sofa = context.active_object
            sofa.name = "Living_Sofa"

            # Coffee Table
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 1, 0.25))
            coffee_table = context.active_object
            coffee_table.name = "Living_CoffeeTable"

        elif room_type == "BEDROOM":
            # Floor
            bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
            floor = context.active_object
            floor.name = "Bedroom_Floor"

            # Bed
            bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
            bed = context.active_object
            bed.name = "Bedroom_Bed"

            # Nightstand
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1.5, 0, 0.25))
            nightstand = context.active_object
            nightstand.name = "Bedroom_Nightstand"

        else:
            self.report({'WARNING'}, f"Unknown room type: {room_type}")
            return {'CANCELLED'}

        return {'FINISHED'}


# -----------------------------
# MiO Panel
# -----------------------------
class MIO_PT_main(Panel):
    """Main UI panel for MiO add-on"""
    bl_label = "MiO"
    bl_idname = "MIO_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mio_props

        # Room spawner section
        layout.label(text="Room Spawner")
        layout.prop(props, "room_type", text="Room Type")
        layout.operator("mio.spawn_room", icon="HOME")

        layout.separator()
        layout.label(text="Furniture Controls")

        # Text input for the new furniture model
        layout.prop(props, "furniture_model", text="New Model Name")

        # Button to switch selected furniture
        op = layout.operator(
            "mio.switch_furniture",
            text="Switch Selected Furniture",
            icon="FILE_REFRESH"
        )
        # Pass the text property to the operator
        op.new_model = props.furniture_model
