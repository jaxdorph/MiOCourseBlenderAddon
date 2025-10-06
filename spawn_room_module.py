import bpy
from bpy.types import Panel, Operator


class Mio(Panel):
    bl_label = "Mio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nåt eget"
    bl_context = "objectmode"  # Optional for limiting access to the panel to a certain context


    def draw(self, context):
        #props = context.scene.hello_world_properties

        layout = self.layout

        layout.label(text="Mio")
        layout.prop(props, "custom_1")
        layout.prop(props, "custom_2")
        layout.operator("template.hello_world")

        header, panel = layout.panel("my_subpanel_id", default_closed=False)
        header.label(text="My Subpanel")
        if panel:
            panel.label(text="Success")