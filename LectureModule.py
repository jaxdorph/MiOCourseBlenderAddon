import bpy
from bpy.types import Operator


class LECTUREMODULE_PT_fancy(bpy.types.Panel):
    bl_label = "fancy panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "benis"

    def draw(self, context):
        layout = self.layout

        layout.label(text="fancy panel")
        layout.operator("scene.fancy_operator")



class LECTUREMODULE_OT_Fancy_world_operator(bpy.types.Operator):
    bl_idname = "scene.fancy_operator"  # {category}.{operator_name} (Look for supported categories that allow for keymaps)
    bl_label = "Fancy Operator"
    bl_description = "A short description of what the operator does"
    bl_options = {"REGISTER", "UNDO"}  # Some operators shouldn't include an 'UNDO' (read-only and temporary UI e.g)
    # bl_options = {"INTERNAL"}        # ...this would be more suitable in such cases

    @classmethod
    def poll(cls, context) -> bool:  # The result of the poll decides whether the operator should be enabled or disabled
        return True

    def execute(self, context):

        context.active_object.location = (2, 0, 0)

        #print("Goodbye World")
        return {"FINISHED"}


class OperatorMall(bpy.types.Operator):
    bl_idname = "temp.bl_idname"
    bl_label = "Temp"

    #Bestämmer när den är synlig/utgråad
    @classmethod
    def poll(cls, context):
        return True

    example = "exampleText"

    def execute(self, context):
        print(self.example)
        return ("FINISHED")



#Visar hur man kan låna från en annan operator

class SecondOperator(OperatorMall):
    bl_idname = "lectureAddon.second_operator"
    bl_label = "second_Operator"

    example = "second_exampleText"







