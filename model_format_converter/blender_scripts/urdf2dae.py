import pickle
import sys
import os
import bpy

def import2scene(path, ext):
    if ext == ".stl":
        bpy.ops.import_mesh.stl(filepath=path)
    elif ext == ".obj":
        bpy.ops.import_scene.obj(filepath=path)
    elif ext == ".dae":
        bpy.ops.wm.collada_import(filepath=path)
    else:
        raise ValueError("Extension of {} is not supported right now!".format(ext))

def urdf2fbx(from_path, to_path, urdf_tmp_path):

    print("Warning! If your urdf has geometric primitive as link, this may fail! We will fix later!")
    
    urdf_structure = pickle.load(open(urdf_tmp_path, "rb"))
    
    if "Cube" in bpy.data.meshes:
        mesh = bpy.data.meshes["Cube"]
        print("removing mesh", mesh)
        bpy.data.meshes.remove(mesh)
    
    # import each link into the blender, and transform it to the recorded poses

    # assume the data structure is meshes/xxx.obj
    # the abs dir is the same from the from_path
    # if urdf is in /a/b/c/robot.urdf, then the models are in /a/b/meshes/*
    data_dir_path = os.path.dirname(from_path) + "/../meshes/"
    model_list = os.listdir(data_dir_path)
    for model_name in model_list:
        raw_name, _ = os.path.splitext(model_name)
        if raw_name in urdf_structure.keys():
            urdf_structure[raw_name]["model_name"] = model_name
    
    for key in urdf_structure.keys():
        try:
            obj_file_path = data_dir_path + urdf_structure[key]['model_name']
            _, obj_ext = os.path.splitext(urdf_structure[key]['model_name'])
            import2scene(obj_file_path, obj_ext.lower())
        except KeyError:
            print("Incomplete models!")
            sys.exit(2)
    
    # create hierarchy
    objects = bpy.data.objects
    for key in objects.keys():
        if key in urdf_structure.keys():
            
            if urdf_structure[key]["parent_name"] is not None:
                parent_key = urdf_structure[key]["parent_name"]
                objects[key].parent = objects[parent_key]
            # do transformation after set the parenting hierarchy
            objects[key].matrix_world = urdf_structure[key]["pose"].T
    bpy.ops.wm.collada_export(filepath=to_path)

argv = sys.argv
argv = argv[argv.index("--") + 1:]

urdf2fbx(argv[0], argv[1], argv[2])