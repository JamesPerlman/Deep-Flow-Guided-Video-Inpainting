import os
from pathlib import Path
import re
import subprocess as sp


def safe_str(string_like) -> str:
    return re.sub(r'([\" \'])', r'\\\1', str(string_like))


def get_fps(video_path: Path) -> str:
    return sp.getoutput(f" \
        ffprobe \
            -v 0 \
            -of csv=p=0 \
            -select_streams v:0 \
            -show_entries stream=r_frame_rate \
            \"{video_path}\" \
    ")

def get_dimensions(video_path) -> (int, int):
    dims_str = sp.getoutput(f" \
        ffprobe \
            -v error \
            -select_streams v \
            -show_entries stream=width,height \
            -of csv=p=0:s=, \
            \"{video_path}\" \
    ")

    dims = dims_str.split(",", maxsplit=1)

    return (int(dims[0]), int(dims[1]))

def get_frame_count(video_path: Path) -> int:
    frames_str = sp.getoutput(f" \
        ffprobe -v error \
            -select_streams v:0 \
            -count_frames \
            -show_entries stream=nb_read_frames \
            -print_format default=nokey=1:noprint_wrappers=1 \
            \"{video_path}\" \
        ")
    return int(frames_str)


def extract_frames(
    input_video_path: Path,
    output_frames_path: Path,
    crop: str = "in_w:in_h:0:0",
    img_format: str = "png",
    size: str = "-1:-1",
    skip_frames: int = 0,
):
    if skip_frames < 1:
        skip_frames = 1

    input_video_fps = get_fps(input_video_path)

    output_frames_path.mkdir(parents=True, exist_ok=True)

    os.system(f" \
        ffmpeg \
            -i \"{input_video_path}\" \
            -r \"{input_video_fps}\" \
            -vsync vfr \
            -vf \"\
                crop={crop}, \
                scale={size}, \
                select=not(mod(n\,{skip_frames})), \
                mpdecimate, \
                setpts=N/FRAME_RATE/TB \
            \" \
            -start_number 0 \
            \"{output_frames_path}/%05d.{img_format}\" \
    ")


def combine_frames(
    input_frames_path: Path,
    output_video_path: Path,
    fps: str = "30"
):
    # fetch all images and save to a playlist
    playlist_path = input_frames_path / "playlist.txt"
    if playlist_path.is_file():
        playlist_path.unlink()
    print(input_frames_path)
    playlist_str = "\n".join(
        [f"file '{safe_str(img_path.name)}'" for img_path in input_frames_path.iterdir()])

    print(playlist_str)
    with open(playlist_path, "w") as f:
        f.write(playlist_str)

    os.system(f"\
        ffmpeg \
            -f concat \
            -i {playlist_path} \
            -r {fps} \
            -c:v libx264 \
            -pix_fmt yuv420p \
            {output_video_path} \
        ")
