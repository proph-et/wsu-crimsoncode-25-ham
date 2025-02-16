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


# ------------------ import image -------------------------
start_time = time.time()
img = Image.open("input2.jpg").convert('RGB')
end_time = time.time()
execution_time = end_time - start_time
print("Execution time for import image:", execution_time, "seconds")

# ------------------ resize image -------------------------
start_time = time.time()
width, height = img.size
small_width = int(width * 0.04)
small_height = int(height * 0.04)
imgSmall = img.resize((small_width, small_height))
# result = imgSmall.resize(img.size, Image.NEAREST)
result = imgSmall
end_time = time.time()
execution_time = end_time - start_time
print("Execution time for resize image:", execution_time, "seconds")

# -------------------- contrast image ----------------------
start_time = time.time()
enhancer = ImageEnhance.Contrast(result)
contrast_image = enhancer.enhance(2.0)
end_time = time.time()
execution_time = end_time - start_time
print("Execution time for contrast image:", execution_time, "seconds")

# -------------------- create color palette ------------------
start_time = time.time()
new_colors = [
    (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0),
    (0, 0, 255), (255, 0, 255), (255, 255, 0), (0, 255, 255),
    (169, 169, 169), (255, 165, 0), (255, 224, 189), (255, 192, 203),
    (0, 128, 128),
]
end_time = time.time()
execution_time = end_time - start_time
print("Execution time for create color palette:", execution_time, "seconds")

# --------------------------- convert image to color palette -----------------
start_time = time.time()
new_image = convert_image(contrast_image, new_colors)
end_time = time.time()
execution_time = end_time - start_time
print("Execution time for convert image:", execution_time, "seconds")

new_image.save('result2.jpg')

# os.startfile('result2.jpg')

width, height = new_image.size

hex_pixels = []
pixels = list(new_image.getdata())
for tup in pixels:
    hex_pixels.append(rgb_to_hex(tup))
# print(hex_pixels)

new_image_size = (width, height)
print(new_image_size)


