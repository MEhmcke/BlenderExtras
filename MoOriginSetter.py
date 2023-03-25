bl_info = {
    "name": "Mo Origin Setter",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from mathutils import Vector


class MoOriginSetter(bpy.types.Operator):
    """Set the object origin to the currently selected verts"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "mo.origin_to_selection"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Origin to selection"            # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}           # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # saving the mode and cursor location to swap to it at the end
        startingMode = bpy.context.active_object.mode
        startingCursorLoc = bpy.context.scene.cursor.location

        # the selection is only updated on object mode switch
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        currentObject = bpy.context.active_object

        # the selected vertices (with consideration for object transform)
        selectedVerts = list()

        # finding all selected vertices
        for vert in currentObject.data.vertices:
            #print(vert.select)    
            if (vert.select == True):
                selectedVerts.append(currentObject.matrix_world @ vert.co)

        if (len(selectedVerts) > 0):
            # setting the position of the 3d cursor
            bpy.context.scene.cursor.location = sum([vert for vert in selectedVerts], Vector()) / len(selectedVerts)

            # setting the origin to the 3d cursor
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # swap to startingMode again
        # bpy.ops.object.mode_set(mode=startingMode)
        bpy.ops.object.mode_set(mode='OBJECT')
        # reset cursor location
        bpy.context.scene.cursor.location = startingCursorLoc

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(MoOriginSetter.bl_idname)

def register():
    bpy.utils.register_class(MoOriginSetter)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(MoOriginSetter)
    
    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()