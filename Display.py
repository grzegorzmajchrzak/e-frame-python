import logging

from IT8951 import constants
from IT8951.display import AutoEPDDisplay


class Display:

    def show(self, image):
        self.print_epd(image)
        return True

    @staticmethod
    def print_epd(img):
        try:
            display = AutoEPDDisplay(vcom=-1.84, rotate=None, spi_hz=24000000)
            epd = display.epd
            display.clear()
            display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
            dims = (display.width, display.height)
            paste_coords = [int((dims[i] - img.size[i]) / 2) for i in (0, 1)]  # center image

            display.frame_buf.paste(img, paste_coords)
            display.draw_full(constants.DisplayModes.GC16)
        except IOError as e:
            logging.error(e)
