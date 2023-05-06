bl_info = {
    "name": "Mo Orientation Helper",
    "blender": (3, 30, 0),
    "category": "3D View",
}

import bpy
import bmesh

class MoOrientationHelper(bpy.types.Operator):
    """Create a new orientation at the selected vertices"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "mo.create_vertex_orientation"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Create Vertex Orientation"            # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}           # Enable undo for the operator.

    def execute(self, context):
        if (bpy.context.active_object.mode == 'EDIT'):
            obj = bpy.context.edit_object
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            
            # Save all currently selected vertices to reselect them later
            selectedVerts = list()
            for vert in bm.verts:
                print(vert.select)
                if (vert.select == True):
                    selectedVerts.append(vert)
                    
            # Create/delete face temporarily to create orientation
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.material_slot_assign()
            bpy.ops.transform.create_orientation(name='MoOrientation', use=True)
            bpy.ops.mesh.delete(type='ONLY_FACE')
                        
            for v in selectedVerts:
                v.select = True
            
            # Switch object mode to update
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.mode_set(mode = 'EDIT')
            bmesh.update_edit_mesh(me)

            return {'FINISHED'}            # Lets Blender know the operator finished successfully.
        else:
            return {'CANCELLED'}           # Object was not in edit mode

def menu_func(self, context):
    self.layout.operator(MoOrientationHelper.bl_idname)

addon_keymaps = []

def register():
    bpy.utils.register_class(MoOrientationHelper)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        # Shift + F is just an example and can be reassigned in the keymap
        kmi = km.keymap_items.new("mo.create_vertex_orientation", type='F', value='PRESS', shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(MoOrientationHelper)
    
    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()