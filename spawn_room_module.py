import bpy
from bpy.types import Panel

class Mio(Panel):
    bl_label = "Mio"
    bl_idname = "ROOMSPAWNER_PT_mio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MiO"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Room Spawner UI")
        layout.operator("template.hello_world")
        layout.operator("mio.reload_addon", icon="FILE_REFRESH")

