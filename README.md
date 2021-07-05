# Model Format Converter

URDF is an important file format regarding robot-related tasks. We build some tools for URDF-centered format conversion.

## Supported Format Convertion
> notes: for these functionality with blender required, please install blender first, setup blender to work please refer to below.

+ [x] obj2fbx/fbx2obj: blender required
+ [x] obj2dae/dae2obj: blender required
+ [x] obj2urdf
+ [ ] xacro2urdf
+ [x] urdf2fbx: blender required
+ [x] urdf2dae: blender required

## Installation
```
python setup.py develop
```

## How to use
1. Setup blende (For functionalities requires Blender). Download blender from [here](https://www.blender.org/). Decompress it and move to a proper location.
```
# export the blender to path
export PATH="/path/to/blender/executable:$PATH"
```
2. Test with converter
+ Convert URDF to something else
```python
from model_format_converter.converter import Converter

converter = Converter(input_file="/path/to/input/file/or/dir", to_format="fbx", urdf_tmp_path="/tmp.pickle", blender_vis=False, delete_tmp_after=True)
converter.convert()
```
+ Convert Other Format
```python
from model_format_converter.converter import Converter

converter = Converter(input_file="/path/to/input/file/or/dir", to_format="fbx", blender_vis=False)
converter.convert()
```