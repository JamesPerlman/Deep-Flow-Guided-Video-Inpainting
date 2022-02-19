import os
import re
import shutil
from argparse import ArgumentParser
from pathlib import Path
from tools import video_inpaint
from utils import ffmpeg
from utils.cleanup import cleanup

parser = ArgumentParser("Extract Frames")

parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-m", "--mask", type=str, required=True)
parser.add_argument("-o", "--output", type=str, required=True)

args = parser.parse_args()

input_path = Path(args.input)
mask_path = Path(args.mask)
output_path = Path(args.output)
data_root_path = input_path.parent

input_frames_path: Path
mask_frames_path: Path
output_frames_path: Path

width: int
height: int

is_input_video = False
is_output_video = False

# clean up data root
cleanup(data_root_path)

# extract frames for input_path if necessary, also get input width and height
if input_path.is_file():
    width, height = ffmpeg.get_dimensions(input_path)
    input_frames_path = input_path.parent / f"{input_path.stem}-frames"
    ffmpeg.extract_frames(input_path, input_frames_path)
    is_input_video = True
else:
    first_frame_path = next(input_path.iterdir())
    width, height = ffmpeg.get_dimensions(first_frame_path)
    input_frames_path = input_path

# extract frames for mask_path if necessary
if mask_path.is_file():
    mask_frames_path = mask_path.parent / f"{mask_path.stem}-frames"
    ffmpeg.extract_frames(mask_path, mask_frames_path)
else:
    mask_frames_path = mask_path

# determine output_path
file_regex = re.compile("^[\w,\s-]+\.[A-Za-z]{3}$")
if file_regex.match(output_path.name) != None:
    output_frames_path = output_path.parent / f"{output_path.stem}-frames"
    is_output_video = True
else:
    output_name = input_path.stem
    output_frames_path = output_path

# run video inpaint
os.system(f"\
    python3 tools/video_inpaint.py \
        --frame_dir {input_frames_path} \
        --MASK_ROOT {mask_frames_path} \
        --img_shape 0 0 \
        --img_size {height} {width} \
        --LiteFlowNet \
        --DFC \
        --ResNet101 \
        --Propagation \
")

# collect output and combine frames
inpaint_res_path = data_root_path / "Inpaint_Res"

if output_frames_path.exists():
    shutil.rmtree(output_frames_path)

os.rename(str(inpaint_res_path), output_frames_path)

if is_output_video:
    if not output_frames_path.exists():
        output_frames_path.mkdir(parents=True)
    ffmpeg.combine_frames(output_frames_path, output_path)
    shutil.rmtree(output_frames_path, ignore_errors=True)

# cleanup
if is_input_video:
    shutil.rmtree(input_frames_path, ignore_errors=True)

cleanup(data_root_path)
