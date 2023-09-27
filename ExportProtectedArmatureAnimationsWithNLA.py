bl_info = {
    "name": "Protected Armature Animations with NLA",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os
from datetime import datetime

class ExportProtectedArmatureAnimationsNLAOperator(bpy.types.Operator):
    bl_idname = "object.export_protected_armature_animations_nla_fix5"
    bl_label = "Export Protected Armature Animations with NLA (Fix 5)"

    def execute(self, context):
        # Get the active armature
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No armature selected.")
            return {'CANCELLED'}

        armature = None
        for obj in selected_objects:
            if obj.type == 'ARMATURE':
                armature = obj
                break

        if not armature:
            self.report({'ERROR'}, "No armature selected.")
            return {'CANCELLED'}

        # Store the original NLA settings and clear them
        original_use_nla = armature.animation_data.use_nla
        armature.animation_data.use_nla = True

        try:
            # Create a folder for the exports based on the current date and time
            export_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            export_folder = os.path.join(bpy.path.abspath("//"), "Blender_Animations_Exports", export_datetime)
            os.makedirs(export_folder, exist_ok=True)

            # Switch the armature object to pose mode
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')  # Switch the armature object to pose mode

            # Iterate through the actions/animations
            for action in bpy.data.actions:
                # Check if the action is marked as protected
                if action.use_fake_user:
                    # Push the action to NLA (it will automatically create a strip)
                    nla_track = armature.animation_data.nla_tracks.new()
                    nla_track.name = action.name  # Set the track name to match the action
                    nla_strip = nla_track.strips.new(action.name, 0, action=action)  # Specify "start" parameter as 0 and set the "action" parameter

                    # Set the active action in NLA
                    armature.animation_data.nla_tracks.active = nla_track

                    # Define the export file path (inside the date-time-based subfolder)
                    export_file = f"{armature.name}_{action.name}.fbx"
                    export_full_path = os.path.join(export_folder, export_file)

                    # Export the armature with the current animation
                    bpy.ops.export_scene.fbx(filepath=export_full_path, check_existing=False, filter_glob="*.fbx", use_selection=True)

                    # Remove the NLA strip after exporting
                    nla_track.strips.remove(nla_strip)

            self.report({'INFO'}, f"Exported protected armature animations with NLA to '{export_folder}' successfully.")
            return {'FINISHED'}
        finally:
            # Clean up the NLA tracks
            for nla_track in armature.animation_data.nla_tracks:
                armature.animation_data.nla_tracks.remove(nla_track)

            # Restore the original NLA settings
            armature.animation_data.use_nla = original_use_nla

            # Switch the armature object back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')  # Switch the armature object back to object mode

def menu_func_export_animations_to_flax(self, context):
    self.layout.operator(ExportProtectedArmatureAnimationsNLAOperator.bl_idname)

def register():
    bpy.utils.register_class(ExportProtectedArmatureAnimationsNLAOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_animations_to_flax)

def unregister():
    bpy.utils.unregister_class(ExportProtectedArmatureAnimationsNLAOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_animations_to_flax)

if __name__ == "__main__":
    register()
