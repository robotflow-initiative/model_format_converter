from model_format_converter.converter import Converter

converter = Converter(input_file="/home/zen/robotflow_series/hand/dh3_urdf/urdf/dh3_urdf.urdf", to_format="fbx", 
                        urdf_tmp_path="/home/zen/robotflow_series/model_format_converter/tmp.pickle", blender_vis=False,
                        delete_tmp_after=True)
converter.convert()