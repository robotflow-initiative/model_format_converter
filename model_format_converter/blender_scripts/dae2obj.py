import bpy
import sys

def dae2obj(from_path, to_path):
    if "Cube" in bpy.data.meshes:
        mesh = bpy.data.meshes["Cube"]
        print("removing mesh", mesh)
        bpy.data.meshes.remove(mesh)
    
    bpy.ops.wm.collada_import(filepath=from_path)
    bpy.ops.export_scene.obj(filepath=to_path)

argv = sys.argv
argv = argv[argv.index("--") + 1:]

dae2obj(argv[0], argv[1])
