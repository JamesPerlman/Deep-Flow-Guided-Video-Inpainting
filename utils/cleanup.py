import os
from pathlib import Path
import shutil


def cleanup(dataset_root: Path):

    data_path = dataset_root / 'data'
    if data_path.exists():
        shutil.rmtree(data_path)

    flow_path = dataset_root / 'Flow'
    if flow_path.exists():
        shutil.rmtree(flow_path)

    flow_res_path = dataset_root / 'Flow_res'
    if flow_res_path.exists():
        shutil.rmtree(flow_res_path)

    video_txt_path = dataset_root / 'video.txt'
    if video_txt_path.exists():
        video_txt_path.unlink()

    video_flow_txt_path = dataset_root / 'video_flow.txt'
    if video_flow_txt_path.exists():
        video_flow_txt_path.unlink()
