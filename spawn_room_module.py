import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import EnumProperty, PointerProperty


# ——————————————————————————————————————————————————————————————————————
# MARK: PROPERTIES
# ——————————————————————————————————————————————————————————————————————
class MIOProperties(PropertyGroup):
    room_type: EnumProperty(
        name="Room Type",
        description="Choose which room to spawn",
        items=[
            ("KITCHEN", "Kitchen", ""),
            ("LIVING", "Living Room", ""),
            ("BEDROOM", "Bedroom", "")
        ],
        default="KITCHEN",
    )


# ——————————————————————————————————————————————————————————————————————
# MARK: OPERATOR
# ——————————————————————————————————————————————————————————————————————
class MIO_OT_spawn_room(Operator):
    bl_idname = "mio.spawn_room"
    bl_label = "Spawn Room"
    bl_description = "Spawn the selected room type"

    def execute(self, context):
        props = context.scene.mio_props
        room = props.room_type

        # Clear previous objects (for testing)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # ------------------------
        # Spawn room base (floor)
        # ------------------------
        bpy.ops.mesh.primitive_cube_add(size=4, location=(0,0,0))
        floor = context.active_object
        floor.name = f"{room}_Floor"
        floor.scale[2] = 0.1  # Flatten cube to make a floor

        # ------------------------
        # Spawn walls (simplified)
        # ------------------------
        for x in [-2, 2]:
            bpy.ops.mesh.primitive_cube_add(size=4, location=(x,0,1))
            wall = context.active_object
            wall.scale[0] = 0.1
            wall.scale[2] = 1
        for y in [-2, 2]:
            bpy.ops.mesh.primitive_cube_add(size=4, location=(0,y,1))
            wall = context.active_object
            wall.scale[1] = 0.1
            wall.scale[2] = 1

        # ------------------------
        # Spawn furniture depending on room type
        # ------------------------
        if room == "KITCHEN":
            # Kitchen table
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.5))
            table = context.active_object
            table.name = "Kitchen_Table"
            table.scale[0] = 1
            table.scale[1] = 0.5
            table.scale[2] = 0.5

            # Stove
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-1.2,0.8,0.25))
            stove = context.active_object
            stove.name = "Stove"

        elif room == "LIVING":
            # Sofa
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.25))
            sofa = context.active_object
            sofa.name = "Sofa"
            sofa.scale[0] = 1.5
            sofa.scale[1] = 0.5
            sofa.scale[2] = 0.5

            # Coffee table
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0,-1,0.2))
            coffee = context.active_object
            coffee.name = "Coffee_Table"

        elif room == "BEDROOM":
            # Bed
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.25))
            bed = context.active_object
            bed.name = "Bed"
            bed.scale[0] = 1.5
            bed.scale[1] = 1
            bed.scale[2] = 0.5

            # Nightstand
            bpy.ops.mesh.primitive_cube_add(size=0.3, location=(1,-1,0.15))
            nightstand = context.active_object
            nightstand.name = "Nightstand"

        self.report({'INFO'}, f"Spawned a {room.lower()}!")
        return {'FINISHED'}




# ——————————————————————————————————————————————————————————————————————
# MARK: UI PANEL
# ——————————————————————————————————————————————————————————————————————
class MIO_PT_main(Panel):
    bl_label = "MiO"
    bl_idname = "MIO_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.mio_props

        layout.label(text="Room Spawner")
        layout.prop(props, "room_type", text="Room Type")
        layout.operator("mio.spawn_room", icon="HOME")
