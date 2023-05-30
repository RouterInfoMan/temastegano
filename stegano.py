from PIL import Image
import numpy as np


def stegano_decode(pixel):
    out = list(color & 1 for color in pixel)
    out2 = list(x for x in out)
    return out2

def get_pixels(image):
    with Image.open(image) as img:
        px = img.getdata()
    px_out = list()
    for x in px:
        px_out.append(list(x))
    return px_out

def convert_to_char(bits):
    chars = {tuple(map(int,f"{n:08b}")):n for n in range(256)}
    temp = []
    out = []
    for i in range(8):
        temp.append(bits[i::8])
    unzipped = zip(*temp)
    for b in unzipped:
        out.append(bytes([chars[b]]).decode('ascii', errors='ignore'))
    return ("".join(out))

def stegano_decrypt(image):
    img = Image.open(image)
    px = img.getdata()
    pixels = list()
    for x in px:
        y = list(x)
        if len(y) == 4:
            y.pop()
        pixels.append(list(y))
    decrypted_pixs = [stegano_decode(x) for x in pixels]
    bits = [x for y in decrypted_pixs for x in y]
    out = convert_to_char(bits)
    return out.split('\x00')[0]

def stegano_encrypt(image, message):
    img = Image.open(image)
    px = img.getdata()
    pixels = list()
    for x in px:
        y = list(x)
        pixels.append(list(y))
    index = 0
    channel = 0
    for caracter in message:
        for i in range(7, -1, -1):
            pixels[index][channel] = (pixels[index][channel] & 0XFE) | ((ord(caracter) >> i) & 1)
            channel = channel + 1
            if channel == 3:
                channel = 0
                index = index + 1
    for i in range(7, -1, -1):
        pixels[index][channel] = (pixels[index][channel] & 0XFE) | 0
        channel = channel + 1
        if channel == 3:
            channel = 0
            index = index + 1
    arr = np.array(pixels, dtype=np.uint8)
    original_img_arr = arr.reshape(img.size[1], img.size[0], 4)
    original_img_arr = np.transpose(original_img_arr, (0, 1, 2))
    out_img = Image.fromarray(original_img_arr)
    return out_img

