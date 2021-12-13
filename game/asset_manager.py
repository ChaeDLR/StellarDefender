import os

from pygame import Surface, image, transform, surfarray


class Assets:
    __assets_directory: str = os.path.abspath(os.path.join(os.getcwd(), "game/assets"))
    # this dict gets populated once the method get_sprite_images gets run once
    __sprite_images: dict = {}

    def __init__(self):
        file_names: list = os.listdir(self.__assets_directory)
        colorkey: bool = True
        img_size: tuple = (64, 64)

        for file_str in file_names:
            if file_str[len(file_str) - 4 :] == ".png":
                continue
                # animation types
                file_name_altered: str = file_str[:-4]

                img: Surface = self.__get_image(
                    file_name=file_str, resize=img_size, colorkey=colorkey
                )
                img.__setattr__("colors", self.__get_sprite_colors(img))

                self.__sprite_images[file_name_altered] = img

            else:
                str_parts = img[:-4].split("_")
                ship_type: dict = {}
                for img in os.listdir(os.path.join(self.__assets_directory, file_str)):
                    print(f"Parts = {str_parts}")

    def __get_image(self, file_name: str, resize: tuple = None, colorkey: bool = True):
        """
        get an image from assests
        file_name: string -> file location
        resize tuple -> (width height)
        """
        img = image.load(os.path.join(self.__assets_directory, file_name)).convert()

        if colorkey:
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


if __name__ == "__main__":
    asset_test: Assets = Assets()
