import bpy
import sys


def fbx2obj(from_path, to_path):
    # print all objects
    #for obj in bpy.data.objects:
    #    print(obj.name)

    if "Cube" in bpy.data.meshes:
        mesh = bpy.data.meshes["Cube"]
        print("removing mesh", mesh)
        bpy.data.meshes.remove(mesh)

    bpy.ops.import_scene.fbx(filepath=from_path)
    bpy.ops.export_scene.obj(filepath=to_path)
    

argv = sys.argv
argv = argv[argv.index("--") + 1:]

fbx2obj(argv[0], argv[1])