bl_info = {
    "name": "Mo Camera Switcher",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from mathutils import Vector


class MoCameraSwitcher(bpy.types.Operator):
    """Switches around the active camera in the scene"""        # Use this as a tooltip for menu items and buttons.
    bl_idname = "mo.camera_switcher"                            # Unique identifier for buttons and menu items to reference.
    bl_label = "Camera Switcher"                                # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}                           # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        currentScene = bpy.context.scene
        allCameras = list()
        currentActiveCamera = currentScene.camera

        # Get all cameras in the scene
        for object in currentScene.objects:
            if (object.type == 'CAMERA'):
                allCameras.append(object)

        
        if (len(allCameras) > 1):
            # Go to next / to first camera
            if (len(allCameras) - 1 <= allCameras.index(currentActiveCamera)):
                currentScene.camera = allCameras[0]
            else:
                currentScene.camera = allCameras[allCameras.index(currentActiveCamera) + 1]
            
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(MoCameraSwitcher.bl_idname)

def register():
    bpy.utils.register_class(MoCameraSwitcher)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(MoCameraSwitcher)
    
    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()