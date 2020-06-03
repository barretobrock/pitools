"""Camera-related procedures"""
import datetime
import os
from picamera import PiCamera
from typing import Optional, List, Tuple


class PiCam(PiCamera):
    """Wrapper class for PiCamera"""
    def __init__(self):
        super().__init__()

    def capture_image(self, save_dir: str, res: Tuple[int, int] = (1280, 720), framerate: int = 24,
                      extra_text: str = '', timestamp: bool = True, vflip: bool = False, hflip: bool = False):
        # Captue image and return path of where it is saved
        filename = '{}.png'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        save_path = os.path.join(save_dir, filename)
        camera = self.PiCamera()
        camera.resolution = res
        camera.framerate = framerate
        cam_text = ''
        camera.vflip = vflip
        camera.hflip = hflip

        if timestamp:
            cam_text = '{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if extra_text != '':
            cam_text = '{}-{}'.format(extra_text, cam_text)
        camera.annotate_text = cam_text
        camera.capture(save_path)
        return save_path
