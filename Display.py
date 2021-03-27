import logging
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ExifTags
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
        self.draw_date(image, file_name)
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
        path_to_font = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'waveshare_epd/Font.ttc')
        font12 = ImageFont.truetype(path_to_font, 16)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,100,30),1)
        draw.text((10, 10), date, font=font12, fill=0)

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
