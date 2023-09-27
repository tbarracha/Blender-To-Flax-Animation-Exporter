# Blender To Flax Animation Exporter
A Blender 3.X addon that exports action animations as separate fbx files with only the armature for use in the [Flax Engine](https://flaxengine.com/)

## Usage
Install the addon and select ``File > Export > Protected Armature Animations with NLA`` and Export Animations. It will export all actions of the selected armature that are saved using a fake user (have the little shield with a checkmark next to them) as individual fbx files in the same folder as your .blend file. The naming scheme is blendfilename_action.fbx. Import to Stride. Every fbx contains a single action, the mesh, and the skeleton.

## Made for a youtube tutorial on the [Flax Engine](https://flaxengine.com/) that you can find here:
https://www.youtube.com/playlist?list=PL2fvSWIOdqqQqD5Fr1FkafSflERpm5YaQ
