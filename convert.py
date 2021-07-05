import os
import argparse
from model_format_converter.no_blender_scripts import obj2urdf, xacro2urdf
from model_format_converter.no_blender_scripts import URDF

def parse_args():
    parser = argparse.ArgumentParser(description='Model format conversion')
    parser.add_argument('-id', '--input_dir', type=str, default=None, help='the dir of input models')
    parser.add_argument('-i', '--input_file', type=str, default=None, help='the file path of input object')
    parser.add_argument('-od', '--output_dir', type=str, default=None, help='the dir to save converted models')
    parser.add_argument('-o', '--output_file', type=str, default=None, help='the file to save converted model.')
    parser.add_argument('-f', '--from_format', type=str, default=None, help='original model format')
    parser.add_argument('-t', '--to_format', type=str, default=None, help='target model format')
    
    args = parser.parse_args()

    if args.input_file is not None and args.input_dir is not None:
        raise argparse.ArgumentError("input_file and input_dir cannot be simutaneously set, currently\
                                    input_file is {}, input_dir is {}".format(args.input_file, args.input_dir))
    if args.input_file is None and args.input_dir is None:
        raise argparse.ArgumentError("input_file and input_dir cannot be simutaneously set None")
    if args.output_file is not None and args.output_dir is not None:
        raise argparse.ArgumentError("output_file and output_dir cannot be simutaneously set, currently\
                                    output_file is {}, output_dir is {}".format(args.output_file, args.output_dir))
    if args.from_format is None:
        print("from_format is not specified...")
        if args.input_dir is not None:
            print("automatically infer from format is only supported for single file.")
            raise
        else:
            print("it will automatically inferred.")
            args.from_format = args.input_file.split(".")[-1].lower()
            print("the detected format is ", args.from_format)
    else:
        args.from_format = args.from_format.lower()
            
    convert_dict = {"obj":["fbx", "dae", "urdf"], "urdf":["fbx", "dae"], "xacro":["urdf"], "dae":["obj"], "fbx":["obj"]}
    if args.from_format not in convert_dict.keys():
        raise argparse.ArgumentError("from format {} is currently not supported.".format(args.from_format))
    if args.to_format not in convert_dict[args.from_format]:
        raise argparse.ArgumentError("from {} to {} is not supported.".format(args.from_format, args.to_format))
    return args

def blender_function_call_single(input_file, output_file, from_format, to_format):
    if output_file is not None:
        f = os.popen("blender --background --python model_format_converter/blender_scripts/"+from_format+"2"+to_format+".py -- "+input_file+" "+output_file)
        print(f.read())
    else:
        output_file = ".".join(input_file.split(".")[:-1])+"."+to_format
        f = os.popen("blender --background --python model_format_converter/blender_scripts/"+from_format+"2"+to_format+".py -- "+input_file+" "+output_file)
        print(f.read())

def blender_function_call(args):
    if args.input_file is not None:
        blender_function_call_single(args.input_file, args.output_file, args.from_format, args.to_format)
    else: # handle a dir
        if args.output_dir is not None:
            output_dir = args.output_dir
        else:
            output_dir = args.input_dir
        from_obj_list = [x for x in os.listdir(args.input_dir) if x.split(".")[-1]==args.from_format]
        for from_obj in from_obj_list:
            input_file = os.path.join(args.input_dir, from_obj)
            output_name = os.path.splitext(from_obj)[0]+"."+args.to_format
            output_file = os.path.join(output_dir, output_name)
            blender_function_call_single(input_file, output_file, args.from_format, args.to_format)

def no_blender_function_call(args, func=None):
    if args.input_file is not None:
        if args.output_file is not None:
            func(args.input_file, args.output_file)
        else:
            output_file = ".".join(args.input_file.split(".")[:-1])+"."+args.to_format
            func(args.input_file, output_file)
    else:
        if args.output_dir is not None:
            func(args.input_dir, args.output_dir, dir_mode=True)
        else:
            func(args.input_dir, args.input_dir, dir_mode=True)

def main():
    args = parse_args()

    #print(args)
    # handle blender scripts
    if args.from_format == "obj":
        if args.to_format in ['fbx', 'dae']:
            blender_function_call(args)
        else:
            no_blender_function_call(args, func=obj2urdf)
    if args.from_format == "dae":
        if args.to_format in ["obj"]:
            blender_function_call(args)
    if args.from_format == "urdf":
        #blender_function_call(args)
        urdf = URDF.load(args.input_file)
        print(urdf.visual_geometry_fk)
        urdf.animate()
    if args.from_format == "xacro":
        no_blender_function_call(args, func=xacro2urdf)



if __name__ == "__main__":
    main()