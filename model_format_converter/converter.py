import os
from model_format_converter.no_blender_scripts import obj2urdf, xacro2urdf, URDF
import pickle

class Converter:
    def __init__(self, 
                input_file, 
                to_format,
                output_file=None,
                from_format=None,
                dir_mode=False,
                blender_vis=False,
                urdf_tmp_path=None,
                delete_tmp_after=False) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.from_format = from_format
        self.to_format = to_format
        self.dir_mode = dir_mode
        self.blender_vis=blender_vis
        self.urdf_tmp_path=urdf_tmp_path
        self.delete_tmp_after = delete_tmp_after

        if os.path.isdir(input_file) != self.dir_mode:
            raise ValueError("Please make sure dir_mode and input_file is consistent.\
                            If it is a file, set dir_mode=False\
                             else, set dir_mode=True")
        
        if self.output_file is None:
            if self.dir_mode:
                self.output_file = self.input_file
            else:
                self.output_file = ".".join(self.input_file.split(".")[:-1])+"."+self.to_format


        if self.from_format is None:
            print("from_format is not specified...")
            if self.dir_mode:
                raise ValueError("automatically infer from format is only supported for single file.")
            else:
                print("it will automatically inferred.")
                self.from_format = self.input_file.split(".")[-1].lower()
                print("the detected format is ", self.from_format)
        else:
            self.from_format = self.from_format.lower()
        
        convert_dict = {"obj":["fbx", "dae", "urdf"], "urdf":["fbx", "dae"], "xacro":["urdf"], "dae":["obj"], "fbx":["obj"]}
        if self.from_format not in convert_dict.keys():
            raise ValueError("from format {} is currently not supported.".format(self.from_format))
        if self.to_format not in convert_dict[self.from_format]:
            raise ValueError("from {} to {} is not supported.".format(self.from_format, self.to_format))
        if self.from_format == "urdf" and self.urdf_tmp_path is None:
            raise ValueError("You mush pass a urdf_tmp_path to convert the urdf!")

    def convert(self):
        # handle blender scripts
        blender_pair = {"obj":["fbx", "dae"], "urdf":["fbx", "dae"], "dae":["obj"], "fbx":["obj"]}
        try:
            if self.to_format in blender_pair[self.from_format]:
                self.blender_function_call()
            else:
                self.no_blender_function_call(func=eval("{}2{}".format(self.from_format, self.to_format)))
        except KeyError:
            self.no_blender_function_call(func=eval("{}2{}".format(self.from_format, self.to_format)))

    def blender_function_call_single(self, input_file, output_file):
        if self.from_format != "urdf":
            if self.blender_vis:
                f = os.popen("blender --python model_format_converter/blender_scripts/"+self.from_format+"2"+self.to_format+".py -- "+input_file+" "+output_file)
                print(f.read())
            else:
                f = os.popen("blender --background --python model_format_converter/blender_scripts/"+self.from_format+"2"+self.to_format+".py -- "+input_file+" "+output_file)
                print(f.read())
        else:
            urdfData = URDF.load(input_file)
            urdf_structure = urdfData.link_fk(use_names=True, return_parent=True)
            pickle.dump(urdf_structure, open(self.urdf_tmp_path, "wb"))
            if self.blender_vis:
                f = os.popen("blender --python model_format_converter/blender_scripts/"+self.from_format+"2"+self.to_format+".py -- "+input_file+" "+output_file+" "+self.urdf_tmp_path)
                print(f.read())
            else:
                f = os.popen("blender --background --python model_format_converter/blender_scripts/"+self.from_format+"2"+self.to_format+".py -- "+input_file+" "+output_file+" "+self.urdf_tmp_path)
                print(f.read())
            if self.delete_tmp_after:
                os.remove(self.urdf_tmp_path)
            

    def blender_function_call(self):
        if self.dir_mode:
            from_obj_list = [x for x in os.listdir(self.input_file) if x.split(".")[-1]==self.from_format]
            for from_obj in from_obj_list:
                input_file = os.path.join(self.input_file, from_obj)
                output_name = os.path.splitext(from_obj)[0]+"."+self.to_format
                output_file = os.path.join(self.output_file, output_name)
                self.blender_function_call_single(input_file, output_file)
        else:
            self.blender_function_call_single(self.input_file, self.output_file)

    def no_blender_function_call(self, func=None):
        func(self.input_file, self.output_file, dir_mode=self.dir_mode)