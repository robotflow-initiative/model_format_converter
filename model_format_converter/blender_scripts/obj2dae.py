import bpy
import sys

def obj2dae(from_path, to_path):
    if "Cube" in bpy.data.meshes:
        mesh = bpy.data.meshes["Cube"]
        print("removing mesh", mesh)
        bpy.data.meshes.remove(mesh)

    bpy.ops.import_scene.obj(filepath=from_path)
    bpy.ops.wm.collada_export(filepath=to_path)

argv = sys.argv
argv = argv[argv.index("--") + 1:]

obj2dae(argv[0], argv[1])