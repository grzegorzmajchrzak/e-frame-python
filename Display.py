import logging
import os
import sys

from PIL import Image

from waveshare_epd import epd7in5_V2


class Display:
    DISPLAY_SIZE = (800, 480)

    def __init__(self):
        libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
        if os.path.exists(libdir):
            sys.path.append(libdir)
        logging.basicConfig(level=logging.DEBUG)

    def show(self, file_name):
        image = self.scaled_image(file_name)
        self.print_epd(image)
        return True

    def scaled_image(self, file_name):
        image = Image.open(file_name)
        if image.size != self.DISPLAY_SIZE:
            image.thumbnail(self.DISPLAY_SIZE, Image.ANTIALIAS)
        if image.mode != 1:
            image = image.convert('1')
        if image.size == self.DISPLAY_SIZE:
            return image

        w = int((self.DISPLAY_SIZE[0] - image.size[0]) / 2)
        h = int((self.DISPLAY_SIZE[1] - image.size[1]) / 2)
        result_image = Image.new('1', self.DISPLAY_SIZE, 1)
        result_image.paste(image, (w, h))
        return result_image

    def print_epd(self, image):
        try:
            epd = epd7in5_V2.EPD()
            logging.info("init and Clear")
            epd.init()
            epd.Clear()

            logging.info("print img")
            epd.display(epd.getbuffer(image))
            epd.sleep()
        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd7in5_V2.epdconfig.module_exit()
            exit()
