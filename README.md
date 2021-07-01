# Model Format Converter

URDF is an important file format regarding robot-related tasks. We build some tools for URDF-centered format conversion.

## Supported Format Convertion
> notes: for these functionality with blender required, please install blender first, setup blender to work please refer to below.

+ [x] obj2fbx: blender required
+ [x] obj2dae: blender required
+ [ ] obj2urdf
+ [ ] xacro2urdf
+ [ ] urdf2fbx: blender required
+ [ ] urdf2dae: blender required

## If blender required
> usually a display is required, I have not make it work without a screen
1. Setup blender. Download blender from [here](https://www.blender.org/). Decompress it and move to a proper location.
```
# export the blender to path
export PATH="/path/to/blender/executable:$PATH"
```

2. Run the individual convert code. You will need to change the path by hand in the script.
```
blender --python blender_scripts/script.py
blender --bachground --python blender_scripts/script.py
```

3. Use a high-level python script to control the blender scripts
```
# a single file
python convert.py -f obj -t fbx -i xxx.obj -o xxx.fbx

# a dir
python convert.py -f obj -t fbx -id /path/to/input/models -od /python/to/output/models
```

## If blender is not required
1. Run the individual convert code.

2. Use a high-level python script to control non-blender scripts