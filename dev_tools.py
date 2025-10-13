import bpy
import importlib
import sys

class MIO_OT_reload_addon(bpy.types.Operator):
    """Reload this add-on without restarting Blender"""
    bl_idname = "mio.reload_addon"
    bl_label = "Reload Add-on"
    bl_options = {"REGISTER"}

    def execute(self, context):
        addon_name = "MiOCourseBlenderAddon"  # <-- your add-on folder name
        
        if addon_name in sys.modules:
            addon_module = sys.modules[addon_name]
            try:
                if hasattr(addon_module, "unregister"):
                    addon_module.unregister()
                importlib.reload(addon_module)
                if hasattr(addon_module, "register"):
                    addon_module.register()
                self.report({"INFO"}, f"Reloaded {addon_name} successfully.")
            except Exception as e:
                self.report({"ERROR"}, f"Failed to reload: {e}")
                import traceback
                traceback.print_exc()
        else:
            self.report({"WARNING"}, f"Add-on '{addon_name}' not found in sys.modules.")
        return {"FINISHED"}
