import os

from pygame import Surface, image, transform, surfarray
from copy import deepcopy


class Assets:
    __assets_directory: str = os.path.abspath(os.path.join(os.getcwd(), "game/assets"))
    # this dict gets populated once the method get_sprite_images gets run once
    __sprite_images: dict = {}

    def __init__(self):
        self.__load(self.__assets_directory, self.__sprite_images)

    def __load(self, path: str, imgs_dict: dict) -> None:
        """Load __sprite_images: dict with all the images in the path arg directory"""
        img_size: tuple = (64, 64)
        temp_imgs: list = []
        for file in os.listdir(path):
            if file[len(file) - 4 :] == ".png":
                img: Surface = self.__load_image(file_name=file, resize=img_size)
                img.__setattr__("colors", self.__get_sprite_colors(img))

                if file[:-4].isdigit():
                    temp_imgs.append(img)
                else:
                    # single .pngs with their key in the title
                    str_parts = file[:-4].split("_")
                    imgs_dict[str_parts[0]] = img
                    print(f"\nKey = {str_parts[0]}\nValue = {img}\n")
            else:
                imgs_dict[file] = {}
                self.__load(
                    os.path.abspath(os.path.join(path, file)),
                    imgs_dict[file],
                )

        if len(temp_imgs) > 0:
            pathprts: list = path.split("\\")
            imgs_dict[pathprts[len(pathprts) - 1]] = temp_imgs

    def __load_image(self, file_name: str, resize: tuple[int, int] = None):
        """
        get an image from assests
        file_name: string -> file location
        resize tuple -> (width height)
        """
        img = image.load(os.path.join(self.__assets_directory, file_name)).convert()

        # get color of top left pixel
        colorkey = img.get_at((0, 0))
        # assign the file image
        img.set_colorkey(colorkey)

        if resize:
            img = transform.scale(img, resize)

        return img

    def __get_sprite_colors(self, img: Surface) -> list:
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

    @classmethod
    def get_image(cls, key: str | list) -> Surface or dict:
        """Return img surface object or dict with all of the surface's pngs"""
        try:
            return deepcopy(cls.__sprite_images[key])
        except KeyError as ex:
            raise ex.with_traceback()


if __name__ == "__main__":
    asset_test: Assets = Assets()
