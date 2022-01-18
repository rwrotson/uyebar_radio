import sys, io, os
import random
from random import randrange
import json
import string

import mutagen.mp3
import mutagen.flac
from PIL import Image

"""
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
"""

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

"""
def save_to_file(id):
    with open('/home/user/covers_dir/song_data.json', 'r') as read_file:
        data = json.load(read_file)
    data3 = data['3']
    data['3'] = data['2']
    data['2'] = data['1']
    data['1'] = id
    with open('/home/user/covers_dir/song_data.json', 'w') as write_file:
        json.dump(data, write_file)
    try:
        os.remove(f'/home/user/covers_dir/{data3}_cover.jpg')
    except FileNotFoundError:
        pass
"""

def get_from_files(local_file, covers_dir, st_covers_dir, cover_name, ch_number):
    """
    Get cover from mp3 or flac file: cover-{number_of_channel}-{number_of_picture}
    """
    try:
        os.rename(f'/home/user/covers_dir/cover-{ch_number}-2.jpg', f'/home/user/covers_dir/cover-{ch_number}-3.jpg')
    except FileNotFoundError:
        pass
    try:
        os.rename(f'/home/user/covers_dir/cover-{ch_number}-1.jpg', f'/home/user/covers_dir/cover-{ch_number}-2.jpg')
    except FileNotFoundError:
        pass
    if local_file.endswith('mp3'):
        metadata = mutagen.mp3.MP3(local_file)
        try:
            content = metadata.tags.get('APIC:').data
            content = io.BytesIO(content)
            image = Image.open(content)
        except BaseException:
            image = Image.open(f'{st_covers_dir}{randrange(1,5)}.jpg')
    elif local_file.endswith('flac'):
        metadata = mutagen.flac.FLAC(local_file)
        try:
            content = metadata.pictures[0].data
            content = io.BytesIO(content)
            image = Image.open(content)
        except BaseException:
            image = Image.open(f'{st_covers_dir}{randrange(1,5)}.jpg')
    #id = id_generator()
    # resize_image(image, 600).save(f'{covers_dir}/{id}_{cover_name}')
    resize_image(image, 600).convert('RGB').save(f'{covers_dir}/cover-{ch_number}-1.jpg')
    #save_to_file(id)


get_from_files(sys.argv[1], "/home/user/covers_dir/", "/home/user/st_covers/", "cover.jpg", sys.argv[2])
