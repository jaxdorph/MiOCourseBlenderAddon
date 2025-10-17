import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, FloatVectorProperty

# ============================================================
# Room Properties
# ============================================================
class MIORoomProperties(PropertyGroup):
    room_length: FloatProperty(
        name="Room Length",
        description="Length of the room (X axis)",
        default=4.0,
        min=1.0,
        max=20.0,
    )
    room_width: FloatProperty(
        name="Room Width",
        description="Width of the room (Y axis)",
        default=3.0,
        min=1.0,
        max=20.0,
    )
    room_height: FloatProperty(
        name="Room Height",
        description="Height of the room (Z axis)",
        default=2.5,
        min=1.0,
        max=5.0,
    )

    wall_color: FloatVectorProperty(
        name="Wall Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.8, 0.8, 1.0),
        description="Color of the walls",
    )

    floor_color: FloatVectorProperty(
        name="Floor Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.5, 0.4, 0.3, 1.0),
        description="Color of the floor",
    )


# ============================================================
# Spawn Room Operator
# ============================================================
class MIO_OT_spawn_room(Operator):
    bl_idname = "mio.spawn_room"
    bl_label = "Spawn Room"
    bl_description = "Create a basic room with floor and four walls"

    def execute(self, context):
        props = context.scene.mio_room_props

        # Remove old room if any
        old_room = bpy.data.objects.get("Room")
        if old_room:
            bpy.data.objects.remove(old_room, do_unlink=True)
        for obj in bpy.data.objects:
            if obj.name.startswith("MiO_"):
                bpy.data.objects.remove(obj, do_unlink=True)

        length, width, height = props.room_length, props.room_width, props.room_height
        wall_thickness = 0.1

        # Create floor
        bpy.ops.mesh.primitive_plane_add(size=1)
        floor = bpy.context.active_object
        floor.name = "MiO_Floor"
        floor.scale = (length / 2, width / 2, 1)
        floor.location = (0, 0, 0)

        # Helper to create a wall
        def create_wall(name, size_x, size_y, loc):
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
            wall = bpy.context.active_object
            wall.name = name
            wall.scale = (size_x / 2, size_y / 2, height / 2)
            return wall

        half_len = length / 2
        half_wid = width / 2

        # Base z-offset so walls sit flush on floor
        z_offset = height / 2 - 0.6

        # Create walls with requested offsets
        back_wall = create_wall(
            "MiO_Wall_Back", length, wall_thickness,
            (0, -half_wid + wall_thickness / 2 - 0.7, z_offset)
        )
        front_wall = create_wall(
            "MiO_Wall_Front", length, wall_thickness,
            (0 + 0.95, half_wid - wall_thickness / 2 - 0.7, z_offset)
        )
        left_wall = create_wall(
            "MiO_Wall_Left", wall_thickness, width,
            (-half_len + wall_thickness / 2 + 0.95, 0, z_offset)
        )
        right_wall = create_wall(
            "MiO_Wall_Right", wall_thickness, width,
            (half_len - wall_thickness / 2, 0, z_offset)
        )

        # Assign materials
        wall_mat = self._get_or_create_material("MiO_Wall_Mat", props.wall_color)
        floor_mat = self._get_or_create_material("MiO_Floor_Mat", props.floor_color)
        for wall in [back_wall, front_wall, left_wall, right_wall]:
            self._assign_material(wall, wall_mat)
        self._assign_material(floor, floor_mat)

        # Join into one object
        objs = [floor, back_wall, front_wall, left_wall, right_wall]
        bpy.context.view_layer.objects.active = floor
        for o in objs:
            o.select_set(True)
        bpy.ops.object.join()

        joined = bpy.context.active_object
        joined.name = "Room"
        joined.location = (0, 0, 0)

        self.report({'INFO'}, "Room created successfully.")
        return {'FINISHED'}

    def _get_or_create_material(self, name, color):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
        return mat

    def _assign_material(self, obj, mat):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)


# ============================================================
# Scale Room Operator
# ============================================================
class MIO_OT_scale_room(Operator):
    bl_idname = "mio.scale_room"
    bl_label = "Scale Room"
    bl_description = "Scale the existing room to match updated dimensions"

    def execute(self, context):
        props = context.scene.mio_room_props
        room = bpy.data.objects.get("Room")

        if not room:
            self.report({"WARNING"}, "No room found. Please spawn one first.")
            return {"CANCELLED"}

        room.scale = (
            props.room_length / 4.0,
            props.room_width / 3.0,
            props.room_height / 2.5,
        )

        self.report({"INFO"}, "Room scaled successfully.")
        return {"FINISHED"}


# ============================================================
# Update Colors Live Operator
# ============================================================
class MIO_OT_update_room_colors(Operator):
    bl_idname = "mio.update_room_colors"
    bl_label = "Apply Room Colors"
    bl_description = "Update wall and floor colors live"

    def execute(self, context):
        props = context.scene.mio_room_props

        wall_mat = bpy.data.materials.get("MiO_Wall_Mat")
        floor_mat = bpy.data.materials.get("MiO_Floor_Mat")

        if wall_mat and wall_mat.node_tree:
            bsdf = wall_mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = props.wall_color

        if floor_mat and floor_mat.node_tree:
            bsdf = floor_mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = props.floor_color

        self.report({'INFO'}, "Colors updated live.")
        return {'FINISHED'}


# ============================================================
# Reset Room Operator
# ============================================================
class MIO_OT_reset_room(Operator):
    bl_idname = "mio.reset_room"
    bl_label = "Reset Room"
    bl_description = "Delete the current room and reset all settings to default"

    def execute(self, context):
        props = context.scene.mio_room_props

        # Delete the room object
        room = bpy.data.objects.get("Room")
        if room:
            bpy.data.objects.remove(room, do_unlink=True)

        # Delete leftover MiO_ objects
        for obj in bpy.data.objects:
            if obj.name.startswith("MiO_"):
                bpy.data.objects.remove(obj, do_unlink=True)

        # Delete materials
        for mat_name in ["MiO_Wall_Mat", "MiO_Floor_Mat"]:
            mat = bpy.data.materials.get(mat_name)
            if mat:
                bpy.data.materials.remove(mat, do_unlink=True)

        # Reset all properties
        props.room_length = 4.0
        props.room_width = 3.0
        props.room_height = 2.5
        props.wall_color = (0.8, 0.8, 0.8, 1.0)
        props.floor_color = (0.5, 0.4, 0.3, 1.0)

        self.report({'INFO'}, "Room and settings reset.")
        return {'FINISHED'}


# ============================================================
# Panel UI
# ============================================================
class MIO_PT_room_spawner(Panel):
    bl_label = "Room Spawner"
    bl_idname = "MIO_PT_room_spawner"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mio_room_props

        layout.label(text="Room Dimensions (m):")
        layout.prop(props, "room_length")
        layout.prop(props, "room_width")
        layout.prop(props, "room_height")

        layout.operator("mio.spawn_room", icon="CUBE")
        layout.operator("mio.scale_room", icon="FULLSCREEN_ENTER")

        layout.separator()
        layout.label(text="Room Colors:")
        layout.prop(props, "wall_color")
        layout.prop(props, "floor_color")
        layout.operator("mio.update_room_colors", icon="COLORSET_01_VEC")

        layout.separator()
        layout.operator("mio.reset_room", icon="TRASH")


# ============================================================
# Registration
# ============================================================
classes = (
    MIORoomProperties,
    MIO_OT_spawn_room,
    MIO_OT_scale_room,
    MIO_OT_update_room_colors,
    MIO_OT_reset_room,
    MIO_PT_room_spawner,
)
