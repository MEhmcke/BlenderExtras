bl_info = {
    "name" : "Mo Globals",
    "blender" : (3, 3, 0),
    "location" : "View3D",
    "category" : "3D View"
}

import bpy
from bpy.types import Operator
from bpy.types import Panel

class MoChangeClippingValues(Operator):
    bl_idname = "mo.change_clipping_values"
    bl_label = "Change Clipping Values"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        scene = context.scene
        props = scene.MoGlobalsProps
        if props.global_clip_start < props.global_clip_end:
            # Get every viewport from all workspaces and set clipping values
            for workspace in bpy.data.workspaces:
                for screen in workspace.screens:
                    for area in screen.areas:        
                        if area.type == "VIEW_3D":
                                area.spaces.active.clip_start = props.global_clip_start
                                area.spaces.active.clip_end = props.global_clip_end
                  
            # Get every camera and set clipping values
            for camera in bpy.data.cameras:
                camera.clip_start = props.global_clip_start
                camera.clip_end = props.global_clip_end
            return {'FINISHED'}
        else:
            return{'CANCELLED'}

class GLOBALS_PT_MoGlobalSettings(Panel):
    bl_label = "Globals"
    bl_idname = 'globals.ui'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Globals"    
    bl_context = "objectmode"    
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene.MoGlobalsProps,'global_clip_start')
        layout.prop(scene.MoGlobalsProps,'global_clip_end')
        col = layout.column(align=True)
        prop = col.operator(MoChangeClippingValues.bl_idname, text="Change Clipping Values")


class MoGlobalsProperties(bpy.types.PropertyGroup):
    global_clip_start: bpy.props.FloatProperty(name = 'Global Clip Start',
                    default = 0.1,
                    min = 0.0)
                    
    global_clip_end: bpy.props.FloatProperty(name = 'Global Clip End',
                    default = 1000.0,
                    min = 0.0)
    
classes = [
    MoChangeClippingValues,
    GLOBALS_PT_MoGlobalSettings,
    MoGlobalsProperties,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.MoGlobalsProps = bpy.props.PointerProperty(type = MoGlobalsProperties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.MoGlobalsProps


if __name__ == '__main__':
    register()