import logging
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ExifTags


class ImageConverter:
    DISPLAY_SIZE = (1200, 825)

    def __init__(self):
        libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
        if os.path.exists(libdir):
            sys.path.append(libdir)

    def convert(self, file_name):
        logging.info("show file: %s", file_name)
        try:
            exif = self.read_exif(file_name)
        except AttributeError:
            exif = None
            logging.error("cannot read exif %s", file_name)

        image = Image.open(file_name)

        if exif is not None:
            image = self.rotate_if_needed(image, exif)

        image = self.scale_image(image)

        if exif is not None:
            self.draw_date(image, exif)
            # self.draw_orientation(image, exif)

        return image

    def scale_image(self, image):
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

    @staticmethod
    def read_exif(file_name):
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in Image.open(file_name)._getexif().items()
            if k in ExifTags.TAGS
        }
        return exif

    @staticmethod
    def draw_date(image, exif):
        date = exif['DateTimeOriginal']
        if not date:
            return

        date = str(date[:10]).replace(":", "-")
        path_to_font = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/Font.ttc')
        font = ImageFont.truetype(path_to_font, 20)
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 0, 140, 35), "white")
        draw.text((30, 10), date, font=font, fill=0)

    @staticmethod
    def draw_orientation(image, exif):
        date = exif['Orientation']
        if not date:
            return

        date = "Orientation: " + str(date)
        path_to_font = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/Font.ttc')
        font = ImageFont.truetype(path_to_font, 20)
        draw = ImageDraw.Draw(image)
        draw.rectangle((420, 0, 640, 35), "white")
        draw.text((430, 10), date, font=font, fill=0)

    @staticmethod
    def rotate_if_needed(image, exif):
        orientation = exif['Orientation']
        if orientation == 3:
            return image.rotate(180)
        if orientation == 8:
            return image.rotate(90)
        if orientation == 6:
            return image.rotate(270)
        return image
