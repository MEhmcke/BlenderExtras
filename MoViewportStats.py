bl_info = {
    "name": "Mo Viewport Stats",
    "blender": (4, 0, 0),
    "category" : "3D View"
}

# import stand alone modules
import blf
import bpy

fontInfo = {
    "font_id": 0,
    "handler": None,
}

def init():
    """init function - runs once"""
    import os
    # Default font.
    fontInfo["font_id"] = 0

    # set the font drawing routine to run every frame
    fontInfo["handler"] = bpy.types.SpaceView3D.draw_handler_add(
        draw_callback_px, (None, None), 'WINDOW', 'POST_PIXEL')

def get_current_timeline_marker():
    currentMarker = ""

    currentFrame = bpy.data.scenes[0].frame_current
    for marker in bpy.context.scene.timeline_markers:
        if marker.frame == currentFrame:
            currentMarker = marker.name
            
    if currentMarker == "":
        currentMarker = "None"
    
    return ("Current Marker: " + currentMarker)


def draw_callback_px(self, context):
    """Draw on the viewports"""
    # BLF drawing routine
    
    isOrientationOn = bpy.context.space_data.overlay.show_face_orientation
    
    if isOrientationOn:
        faceOrientationString = "FO is activated"
    else:
        faceOrientationString = "FO is deactivated"
    
    font_id2 = fontInfo["font_id"]
    blf.position(font_id2, 2, 60, 0)
    blf.size(font_id2, 32)
    blf.draw(font_id2, get_current_timeline_marker())
    
    
    font_id = fontInfo["font_id"]
    blf.position(font_id, 2, 20, 0)
    blf.size(font_id, 32)
    blf.draw(font_id, faceOrientationString)

def register():
    init()

def unregister():
    bpy.types.SpaceView3D.draw_handler_remove(fontInfo["handler"], 'WINDOW')
    print("unregister")