import os
from pygame import Surface, image, transform, surfarray


class AssetManager:

    asset_directory: str = os.path.join(os.getcwd(), "game/assets")
    # this dict gets populated once the method get_sprite_images gets run once
    sprite_images: dict = None

    def __get_image(cls, file_name: str, resize: tuple = None, colorkey: bool = True):
        """
        get an image from assests
        file_name: string -> file location
        resize tuple -> (width height)
        """
        img = image.load(os.path.join(cls.asset_directory, file_name)).convert()

        if colorkey:
            # get color of top left pixel
            colorkey = img.get_at((0, 0))
            # assign the file image
            img.set_colorkey(colorkey)

        if resize:
            img = transform.scale(img, resize)

        return img

    def get_sprite_colors(cls, img: Surface) -> list:
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
    def get_sprite_images(cls) -> dict:
        """
        load and run game assests
        """
        if cls.sprite_images:
            return cls.sprite_images
        else:
            new_images: dict = {}
            file_names: list = os.listdir(cls.asset_directory)

            for file_str in file_names:
                colorkey: bool = True
                img_size: tuple = (64, 64)
                file_name_altered: str = file_str[:-4]

                img: Surface = cls.__get_image(
                    cls, file_name=file_str, resize=img_size, colorkey=colorkey
                )
                new_images[file_name_altered] = {
                    "image": img,
                    "colors": cls.get_sprite_colors(cls, img),
                }

            AssetManager.sprite_images = new_images
            return new_images


if __name__ == "__main__":
    print(AssetManager.asset_directory)
