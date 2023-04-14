import logging
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ExifTags
from IT8951.display import AutoEPDDisplay
from IT8951 import constants


class Display:
    DISPLAY_SIZE = (1200, 825)

    def __init__(self):
        libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
        if os.path.exists(libdir):
            sys.path.append(libdir)
        logging.basicConfig(level=logging.DEBUG)

    def show(self, file_name):
        print("try to show: "+file_name)
        image = self.scaled_image(file_name)
        try:
            self.draw_date(image, file_name)
        except AttributeError:
            print("cannot read create date"+file_name)
        self.print_epd(image)
        return True

    def scaled_image(self, file_name):
        image = Image.open(file_name)
        if image.size != self.DISPLAY_SIZE:
            image.thumbnail(self.DISPLAY_SIZE, Image.ANTIALIAS)
        if image.mode != 'L':
            image = image.convert('L')
        if image.size == self.DISPLAY_SIZE:
            return image

        w = int((self.DISPLAY_SIZE[0] - image.size[0]) / 2)
        h = int((self.DISPLAY_SIZE[1] - image.size[1]) / 2)
        result_image = Image.new('L', self.DISPLAY_SIZE, 1)
        result_image.paste(image, (w, h))
        return result_image

    def draw_date(self, image, file_name):
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in Image.open(file_name)._getexif().items()
            if k in ExifTags.TAGS
        }
        date = exif['DateTimeOriginal']
        if not date:
            return

        date = str(date[:10]).replace(":","-")
        path_to_font = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/Font.ttc')
        font12 = ImageFont.truetype(path_to_font, 16)
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 0, 120, 30), "white")
        draw.text((30, 10), date, font=font12, fill=0)

    def print_epd(self, img):
        try:
            display = AutoEPDDisplay(vcom=-1.84, rotate=None, spi_hz=24000000)
            epd = display.epd
            logging.info('  display size: {}x{}'.format(epd.width, epd.height))
            display.clear()
            display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
            dims = (display.width, display.height)
            paste_coords = [int((dims[i] - img.size[i])/2) for i in (0, 1)]  # center image

            display.frame_buf.paste(img, paste_coords)
            display.draw_full(constants.DisplayModes.GC16)
        except IOError as e:
            logging.info(e)
