import bpy
from bpy.props import PointerProperty, EnumProperty, FloatVectorProperty
from bpy.types import PropertyGroup, Operator, Panel
from . import furniture_loader


# -----------------------------------------------------------------------------
# PROPERTY GROUP
# Stores the selected room, category, model, and color for UI
# -----------------------------------------------------------------------------
class MIOFurnitureProperties(PropertyGroup):

    # Dropdown: Room type (bedroom, livingroom, kitchen)
    def update_room(self, context):
        # Update category options when room changes
        self.furniture_category = None
        self.furniture_model = None

    rooms = [(r, r.capitalize(), "") for r in furniture_loader.FURNITURE_LIBRARY.keys()]
    furniture_room: EnumProperty(
        name="Room",
        description="Select a room",
        items=rooms,
        update=update_room
    )

    # Dropdown: Furniture category (Sofas, Beds, etc.)
    def update_category(self, context):
        # Reset model selection when category changes
        self.furniture_model = None

    @property
    def categories(self):
        room = self.furniture_room
        return [(c, c, "") for c in furniture_loader.get_room_categories(room)] if room else []

    furniture_category: EnumProperty(
        name="Category",
        description="Select furniture category",
        items=lambda self, context: self.categories,
        update=update_category
    )

    # Dropdown: Specific furniture model
    @property
    def models(self):
        room = self.furniture_room
        cat = self.furniture_category
        return [(m, m, "") for m in furniture_loader.get_models_for_category(room, cat)] if room and cat else []

    furniture_model: EnumProperty(
        name="Model",
        description="Select specific furniture model",
        items=lambda self, context: self.models
    )

    # Color picker for tinting furniture
    color: FloatVectorProperty(
        name="Color",
        description="Change furniture color (tints original materials)",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )


# -----------------------------------------------------------------------------
# OPERATOR: Spawn selected furniture model
# -----------------------------------------------------------------------------
class MIO_OT_spawn_furniture(Operator):
    bl_idname = "mio.spawn_furniture"
    bl_label = "Spawn Furniture"
    bl_description = "Spawn the selected furniture model into the scene"

    def execute(self, context):
        props = context.scene.mio_furniture_props

        if not (props.furniture_room and props.furniture_category and props.furniture_model):
            self.report({'ERROR'}, "Please select Room, Category, and Model")
            return {'CANCELLED'}

        # Load the furniture via the loader module
        obj = furniture_loader.load_furniture_asset(
            room_type=props.furniture_room,
            category=props.furniture_category,
            model_name=props.furniture_model
        )

        if obj is None:
            self.report({'ERROR'}, "Failed to load furniture")
            return {'CANCELLED'}

        # Set the object active
        context.view_layer.objects.active = obj

        # Apply color override if not default white
        if props.color != (1.0, 1.0, 1.0):
            bpy.ops.mio.set_furniture_color()

        return {'FINISHED'}


# -----------------------------------------------------------------------------
# OPERATOR: Apply color to selected furniture
# Works on both single objects and collections/empties
# -----------------------------------------------------------------------------
class MIO_OT_set_furniture_color(Operator):
    bl_idname = "mio.set_furniture_color"
    bl_label = "Apply Color"
    bl_description = "Apply selected color to furniture while keeping original materials/textures"

    def execute(self, context):
        props = context.scene.mio_furniture_props
        obj = context.active_object

        if obj is None:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}

        # Gather all objects to modify
        objects_to_color = [obj]

        # If the object is an empty with children, include all children
        if obj.type == 'EMPTY' and obj.children:
            objects_to_color = obj.children
        # If it is a collection instance, include objects in collection
        elif obj.instance_collection:
            objects_to_color = obj.instance_collection.objects

        # Apply color to all materials of each object
        for o in objects_to_color:
            for mat_slot in o.material_slots:
                mat = mat_slot.material
                if mat and mat.node_tree:
                    # Look for Principled BSDF
                    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                    if bsdf:
                        # Only override color input, keeps textures intact
                        bsdf.inputs['Base Color'].default_value = (*props.color, 1.0)

        self.report({'INFO'}, f"Color applied to {obj.name}")
        return {'FINISHED'}


# -----------------------------------------------------------------------------
# PANEL: UI in N-panel
# -----------------------------------------------------------------------------
class MIO_PT_furniture_panel(Panel):
    bl_label = "MiO Furniture"
    bl_idname = "MIO_PT_furniture_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mio_furniture_props

        layout.label(text="Select Furniture to Spawn:")

        layout.prop(props, "furniture_room")
        layout.prop(props, "furniture_category")
        layout.prop(props, "furniture_model")
        layout.operator("mio.spawn_furniture", icon="ADD")

        layout.separator()
        layout.label(text="Optional Color Tint:")
        layout.prop(props, "color")
        layout.operator("mio.set_furniture_color", icon="COLOR")


# -----------------------------------------------------------------------------
# REGISTER CLASSES
# -----------------------------------------------------------------------------
classes = [
    MIOFurnitureProperties,
    MIO_OT_spawn_furniture,
    MIO_OT_set_furniture_color,
    MIO_PT_furniture_panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mio_furniture_props = PointerProperty(type=MIOFurnitureProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mio_furniture_props


if __name__ == "__main__":
    register()
