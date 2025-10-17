"""
furniture_switch_module.py

- Property group describing room_type, category, model
- Model list is populated dynamically by calling loader.list_furniture_models()
- Switch operator clears MiO_Furniture and appends the chosen .blend
- UI in MiO tab
"""

import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import EnumProperty


class MIOFurnitureProperties(PropertyGroup):
    room_type: EnumProperty(
        name="Room Type",
        items=[
            ("livingroom", "Living Room", ""),
            ("bedroom", "Bedroom", ""),
            ("kitchen", "Kitchen", ""),
        ],
        default="livingroom",
    )

    category: EnumProperty(
        name="Category",
        items=[
            ("Sofas", "Sofas", ""),
            ("Coffee Tables", "Coffee Tables", ""),
            ("Beds", "Beds", ""),
            ("Wardrobes", "Wardrobes", ""),
            ("Kitchen Tables", "Kitchen Tables", ""),
            ("Kitchen Chairs", "Kitchen Chairs", ""),
        ],
        default="Sofas",
    )

    model: EnumProperty(
        name="Model",
        description="Choose a .blend model to append",
        items=lambda self, context: MIOFurnitureProperties._get_model_items(self, context)
    )

    @staticmethod
    def _get_model_items(self, context):
        # Import loader locally to avoid circular import during module load
        try:
            from . import furniture_loader_module
        except Exception as e:
            print(f"[MiO] loader import error: {e}")
            return [("NONE", "Loader error", "")]
        files = furniture_loader_module.list_furniture_models(self.room_type, self.category)
        if not files:
            return [("NONE", "No models found", "")]
        return [(f, f.replace(".blend", ""), "") for f in files]


class MIO_OT_switch_furniture(Operator):
    bl_idname = "mio.switch_furniture"
    bl_label = "Switch Furniture"
    bl_description = "Replace currently spawned furniture with the selected model"

    def execute(self, context):
        props = context.scene.mio_furniture_props

        if props.model == "NONE":
            self.report({"WARNING"}, "No model selected")
            return {"CANCELLED"}

        # local import
        try:
            from . import furniture_loader_module
        except Exception as e:
            self.report({"ERROR"}, f"Loader import failed: {e}")
            return {"CANCELLED"}

        # clear prior furniture
        furniture_loader_module.clear_spawned_furniture()

        # append selected model
        appended = furniture_loader_module.load_furniture_model(props.room_type, props.category, props.model)
        if not appended:
            self.report({"ERROR"}, f"Failed to load {props.model}")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Loaded {props.model} ({len(appended)} objects).")
        return {"FINISHED"}


class MIO_PT_furniture_switcher(Panel):
    bl_label = "Furniture Switcher"
    bl_idname = "MIO_PT_furniture_switcher"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mio_furniture_props

        layout.label(text="Furniture")
        layout.prop(props, "room_type")
        layout.prop(props, "category")
        layout.prop(props, "model")
        layout.operator("mio.switch_furniture", icon="FILE_REFRESH")


# helper classes tuple (if you want to register this module alone)
classes = (
    MIOFurnitureProperties,
    MIO_OT_switch_furniture,
    MIO_PT_furniture_switcher,
)
