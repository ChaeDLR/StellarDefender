import os

from pygame import Surface, image, transform, surfarray


__assets_directory: str = os.path.join(os.getcwd(), "game/assets")
# this dict gets populated once the method get_sprite_images gets run once
__sprite_images: dict = {}

global images


def __get_image(file_name: str, resize: tuple = None, colorkey: bool = True):
    """
    get an image from assests
    file_name: string -> file location
    resize tuple -> (width height)
    """
    img = image.load(os.path.join(__assets_directory, file_name)).convert()

    if colorkey:
        # get color of top left pixel
        colorkey = img.get_at((0, 0))
        # assign the file image
        img.set_colorkey(colorkey)

    if resize:
        img = transform.scale(img, resize)

    return img


def __get_sprite_colors(img: Surface) -> list:
    """
    Loop through a surface and grab the colors its made of
    sort from lightest(n) to darkest(0)
    """
    colors: list = []
    for row in surfarray.array3d(img):
        for pixel in row:
            rgb: list = [int(pixel[0]), int(pixel[1]), int(pixel[2]), 255]
            if rgb not in [[255, 255, 255, 255], [0, 0, 0, 255]] + colors:
                colors.append(rgb)
    colors.sort(key=sum)
    return colors


def init() -> None:
    """
    load image assets
    """
    if len(__sprite_images) == 0:
        new_images: dict = {}
        file_names: list = os.listdir(__assets_directory)

        for file_str in file_names:
            colorkey: bool = True
            img_size: tuple = (64, 64)
            # TODO: set string splitting standard and nest
            # animation types
            file_name_altered: str = file_str[:-4]

            img: Surface = __get_image(
                file_name=file_str, resize=img_size, colorkey=colorkey
            )
            new_images[file_name_altered] = {
                "image": img,
                "colors": __get_sprite_colors(img),
            }
            data


class __Images:
    def __init__(self, sprite_imgs: dict) -> None:
        for sprite in sprite_imgs:
            imgs: list = []
            for i in sprite:
                fragments: list = i.split("_")

            self.__setattr__(
                sprite,
            )


if __name__ == "__main__":
    print(__assets_directory)
