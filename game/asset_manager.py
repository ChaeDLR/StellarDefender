import os

from pygame import Surface, image, transform, surfarray


class Assets:
    __assets_directory: str = os.path.abspath(os.path.join(os.getcwd(), "game/assets"))
    # this dict gets populated once the method get_sprite_images gets run once
    __sprite_images: dict = {}

    def __init__(self):
        self.__load(self.__assets_directory)

    def __load(self, path: str, imgs_dict: dict) -> None:
        """Load __sprite_images: dict with all the images in the path arg directory"""
        img_size: tuple = (64, 64)
        for file in os.listdir(path):
            if file[len(file) - 4 :] == ".png":
                # animation types
                str_parts = img[:-4].split("_")

                img: Surface = self.__load_image(file_name=file, resize=img_size)
                img.__setattr__("colors", self.__get_sprite_colors(img))

                if imgs_dict:
                    imgs_dict[str_parts[0]] = img
                else:
                    self.__sprite_images[str_parts[0]] = img
            else:

                # for img in os.listdir(os.path.join(self.__assets_directory, file)):
                #     print(f"Parts = {str_parts}")
                # Grab key
                key: str = file
                # recall
                print(os.path.abspath(os.path.join(path, file)))
                # self.__load(os.path.abspath(os.path.join(path, file)))

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

    def get_image(cls, key: str) -> Surface or dict:
        try:
            return cls.__sprite_images[key]
        except KeyError as ex:
            raise ex.with_traceback()


if __name__ == "__main__":
    asset_test: Assets = Assets()
