bl_info = {
    "name": "Mo Explorer",
    "blender": (2, 80, 0),
    "category": "Blender",
}

import bpy
import os
import subprocess
import datetime

class MoShowLastExport(bpy.types.Operator):
    bl_idname = "mo.show_last_export"
    bl_label = "Show Last Export"

    def execute(self, context):
        projectDir = bpy.path.abspath("//")
        latestExportDate = datetime.datetime(1990, 1, 1)
        latestExport = ""    
        
        # Go trough all dirs 
        for dirs in os.walk(projectDir):
            for name in dirs:
                # Search for "Exports"
                if "Exports" in name:
                    for files in os.walk(name):
                        # Go trough all the files (files are at index 2)
                        for export in files[2]:
                            # Get full path to image
                            singleExportPath = files[0] + "\\" + export
                            # Get timestamp & convert to DateTime object
                            m_time = os.path.getmtime(singleExportPath)
                            dt_m = datetime.datetime.fromtimestamp(m_time)
                            # If this image is newer update variables
                            if (dt_m > latestExportDate):
                                latestExport = singleExportPath
                                latestExportDate = dt_m 
                            #print('\nnext date is: ', latestExportDate)
                            #print('\nImage is: ' + latestExport)
        if latestExport.endswith(".png") or latestExport.endswith(".jpg"):
            os.startfile(latestExport)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

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
        layout.operator("mo.show_last_export")

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_custom_menu")


classes = (
    TOPBAR_MT_custom_menu,
    MoShowProjectFolder,
	MoShowLastExport,
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