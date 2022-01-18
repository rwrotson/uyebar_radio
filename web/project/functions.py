import random

from PIL import Image
import imghdr

from project.models import Channel

def validate_image(stream):
    """
    Check the image if it malicious
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def crop_center(img):
    """
    Crops a biggest square from picture's centre
    """
    image = Image.open(img)
    width, height = image.size
    if width == height:
        return image
    elif width > height:
        return image.crop(
            ((width - height) / 2, 0, height + (width - height) / 2, height)
        )
    else:
        return image.crop(
            (0, (height - width) / 2, width, width + (height - width) / 2)
        )


def resize_image(image, new_size):
    """
    Resizes image keeping aspect ratio
    """
    if max(image.size) != new_size:
        k = float(new_size) / float(max(image.size))
        new_image = image.resize(
            tuple([int(k * x) for x in image.size]), Image.ANTIALIAS
        )
        image.close()
    else:
        new_image = image
    return new_image


def crop_and_resize(image):
    """
    Crops and resizes picture to the square of 600x600
    """
    return resize_image(crop_center(image), 600)


def get_tags():
    tags_dict = {}
    channels = Channel.query.all()
    for i in range(len(channels)):
        id = channels[i].id
        tag_list = channels[i].tags.split(', ')
        tag_string = ', '.join(random.sample(tag_list, 6))
        while len(tag_string) > 140:
            tag_string = ', '.join(random.sample(tag_list, 8))
        tags_dict[id] = tag_string
    return tags_dict
