"""Camera-related procedures"""
import os
from datetime import datetime
from picamera import PiCamera
from typing import Tuple


class PiCam(PiCamera):
    """Wrapper class for PiCamera"""
    def __init__(self):
        super().__init__()

    def capture_image(self, save_dir: str, res: Tuple[int] = (1280, 720),
                      framerate: int = 24, extra_text: str = '', timestamp: bool = True,
                      vflip: bool = False, hflip: bool = False) -> str:
        """
        Capture image and return path of where it is saved.
        :param save_dir:
        :param res:
        :param framerate:
        :param extra_text:
        :param timestamp:
        :param vflip:
        :param hflip:
        :return:
        """
        # Capture image and return path of where it is saved
        filename = f'{datetime.now():%Y%m%d_%H%M%S}.png'
        save_path = os.path.join(save_dir, filename)
        self.resolution = res
        self.framerate = framerate
        cam_text = ''
        self.vflip = vflip
        self.hflip = hflip

        if timestamp:
            cam_text = f'{datetime.now():%Y-%m-%d %H:%M:%S}'
        if extra_text != '':
            cam_text = f'{extra_text}-{cam_text}'
        self.annotate_text = cam_text
        self.capture(save_path)
        return save_path
