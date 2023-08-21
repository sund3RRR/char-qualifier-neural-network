from PIL import Image
from PIL import ImageOps

def find_up_crop_bound(image : Image.Image) -> int:
    for y in range(0, image.height):
        for x in range(0, image.width):
            pixel = image.getpixel((x,y))
            if pixel[0] != 0:
                return y

def find_down_crop_bound(image : Image.Image) -> int:
    for y in range(image.height - 1, 1, -1):
        for x in range(0, image.width):
            pixel = image.getpixel((x,y))
            if pixel[0] != 0:
                return y + 1

def find_right_crop_bound(image : Image.Image) -> int:
    for x in range(image.width - 1, 1, -1):
        for y in range(0, image.height):
            pixel = image.getpixel((x,y))
            if pixel[0] != 0:
                return x + 1

def find_left_crop_bound(image : Image.Image) -> int:
    for x in range(0, image.width):
        for y in range(0, image.height):
            pixel = image.getpixel((x,y))
            if pixel[0] != 0:
                return x


def rework_image_to_network(image :Image.Image, size :tuple[int,int]) -> Image.Image:
    image = image.convert('RGB')
    image = ImageOps.invert(image)
    shakal_size = (round(size[0] * (image.width / image.height)), size[1])
    image = image.resize(shakal_size)

    x0 = find_left_crop_bound(image)
    y0 = find_up_crop_bound(image)
    x1 = find_right_crop_bound(image)
    y1 = find_down_crop_bound(image)
    image = image.crop((x0, y0, x1, y1))

    if image.width < image.height:
        new_shakal_size = (round(size[0] * (image.width / image.height)), size[1])
        image = image.resize(new_shakal_size)
    else:
        new_shakal_size = (size[0], round(size[1] * (image.height/image.width)))
        image = image.resize(new_shakal_size)

    cropped_image = Image.new("RGB", size)
    cropped_image.paste(image)

    return cropped_image