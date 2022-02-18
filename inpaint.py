import os
import shutil
from argparse import ArgumentParser
from pathlib import Path
from utils import ffmpeg

parser = ArgumentParser("Extract Frames")

parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-m", "--mask", type=str, required=True)
parser.add_argument("-o", "--output", type=str, required=True)

args = parser.parse_args()

input_path = Path(args.input)
mask_path = Path(args.mask)
output_path = Path(args.output)

input_frames_path: Path
mask_frames_path: Path
output_frames_path: Path

# extract frames for input_path if necessary
if input_path.is_file():
    input_frames_path = input_path.parent / f"{input_path.stem}-frames"
    ffmpeg.extract_frames(input_path, input_frames_path)
else:
    input_frames_path = input_path

# extract frames for mask_path if necessary
if mask_path.is_file():
    mask_frames_path = mask_path.parent / f"{mask_path.stem}-frames"
    ffmpeg.extract_frames(mask_path, mask_frames_path)
else:
    mask_frames_path = mask_path

# determine output_path
if output_path.is_file():
    output_frames_path = output_path.parent / f"{output_path.stem}-frames"
else:
    output_name = input_path.stem
    output_frames_path = output_path
    output_path = output_path / f"{output_name}.mp4"

os.system(f"\
    python tools/video_inpaint.py \
        --frame_dir {input_frames_path} \
        --MASK_ROOT {mask_frames_path} \
        --output_root {output_frames_path} \
        --img_shape 0 0 \
        --MS --th_warp 3 --FIX_MASK \
")

ffmpeg.combine_frames(output_frames_path, output_path)

# cleanup
exit()
shutil.rmtree(input_frames_path)
shutil.rmtree(mask_frames_path)
shutil.rmtree(output_frames_path)