bl_info = {
    "name": "Mo Explorer",
    "blender": (2, 80, 0),
    "category": "Blender",
}

import bpy
import subprocess

class MoShowProjectFolder(bpy.types.Operator):
    bl_idname = "mo.show_project_folder"
    bl_label = "Show Project Folder"

    def execute(self, context):
        subprocess.Popen('explorer ' + bpy.path.abspath("//"))
        return {'FINISHED'}

class TOPBAR_MT_custom_menu(bpy.types.Menu):
    bl_label = "Explorer"

    def draw(self, context):
        layout = self.layout
        layout.operator("mo.show_project_folder")

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_custom_menu")


classes = (
    TOPBAR_MT_custom_menu,
    MoShowProjectFolder,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_custom_menu.menu_draw)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_custom_menu.menu_draw)
    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()