import bpy
import sys


def obj2fbx(from_path, to_path):
    # print all objects
    #for obj in bpy.data.objects:
    #    print(obj.name)

    if "Cube" in bpy.data.meshes:
        mesh = bpy.data.meshes["Cube"]
        print("removing mesh", mesh)
        bpy.data.meshes.remove(mesh)

    bpy.ops.import_scene.obj(filepath=from_path)
    bpy.ops.export_scene.fbx(filepath=to_path)

argv = sys.argv
argv = argv[argv.index("--") + 1:]

obj2fbx(argv[0], argv[1])