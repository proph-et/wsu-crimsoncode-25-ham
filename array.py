from PIL import Image, ImageEnhance
import numpy as np
import os
import time

def rgb_to_hex(rgb_val):
    r = rgb_val[0]
    g = rgb_val[1]
    b = rgb_val[2]
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def convert_image(img, approved_colors):
    img_array = np.array(img)
    approved_colors = np.array(approved_colors)

    # euclidean RGB distance calculation for all pixels against the palette colors
    # sqrt((RBG-RBG)^2+(RBG-RBG)^2)
    distances = np.sqrt(np.sum((img_array[..., None, :] - approved_colors) ** 2, axis=3))

    # for each pixel, it finds the index of the color in approved_colors that has the smallest distance
    nearest_indices = np.argmin(distances, axis=2)

    # map each pixel to the nearest color
    img_array = approved_colors[nearest_indices]

    # ensure the result array has the correct data type (unsigned 8-bit integer)
    img_array = img_array.astype(np.uint8)
    # print(img_array)

    # convert the numpy array back to an image
    return Image.fromarray(img_array)


def image(input):

    img = Image.open(input).convert('RGB')

# ------------------ resize image -------------------------

    width, height = img.size
    small_width = int(width * 0.04)
    small_height = int(height * 0.04)
    imgSmall = img.resize((small_width, small_height))
    # result = imgSmall.resize(img.size, Image.NEAREST)
    result = imgSmall

    # -------------------- contrast image ----------------------

    enhancer = ImageEnhance.Contrast(result)
    contrast_image = enhancer.enhance(2.0)

    # -------------------- create color palette ------------------

    new_colors = [
        (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0),
        (0, 0, 255), (255, 0, 255), (255, 255, 0), (0, 255, 255),
        (169, 169, 169), (255, 165, 0), (255, 224, 189), (255, 192, 203),
        (0, 128, 128),
    ]

    # --------------------------- convert image to color palette -----------------

    new_image = convert_image(contrast_image, new_colors)

    new_image.save('result2.jpg')

    # os.startfile('result2.jpg')

    width, height = new_image.size

    hex_pixels = []
    pixels = list(new_image.getdata())
    for tup in pixels:
        hex_pixels.append(rgb_to_hex(tup))
    # print(hex_pixels)

    new_image_size = (width, height)
    return (new_image_size, hex_pixels)



