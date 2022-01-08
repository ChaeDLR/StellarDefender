import os

from pygame import Surface, image, transform


class Assets:
    __assets_directory: str = os.path.abspath(os.path.join(os.getcwd(), "game/images"))
    # this dict gets populated once the method get_sprite_images gets run once
    __sprite_images: dict = {}

    def __load(cls, path: str, imgs_dict: dict, prev_key: str = None) -> None:
        """Load (__sprite_images: dict) with all the images in the path arg directory"""
        if prev_key:
            imgs_dict[prev_key] = {}
        img_size: tuple = (64, 64)
        temp_imgs: list = []

        try:
            for file in os.listdir(path):
                if file[len(file) - 4 :] == ".png":
                    img: Surface = cls.__load_image(
                        path=os.path.join(path, file), resize=img_size
                    )

                    if file[:-4].isdigit():
                        temp_imgs.append(img)
                    else:
                        # single .pngs with their key in the title
                        str_parts = file[:-4].split("_")
                        imgs_dict[str_parts[0]] = img

                else:
                    if prev_key:
                        cls.__load(
                            cls,
                            os.path.abspath(os.path.join(path, file)),
                            imgs_dict[prev_key],
                            file,
                        )
                    else:
                        cls.__load(
                            cls,
                            os.path.abspath(os.path.join(path, file)),
                            imgs_dict,
                            file,
                        )
        except NotADirectoryError as ex:
            print(f"{ex.filename} not an accepted file type.")

        if len(temp_imgs) > 0:
            imgs_dict[prev_key] = temp_imgs

    def __load_image(path: str, resize: tuple[int, int] = None):
        """
        get an image from assests
        file_name: string -> file location
        resize tuple -> (width height)
        """
        img = image.load(path).convert()

        # get color of top left pixel
        colorkey = img.get_at((0, 0))
        # assign the file image
        img.set_colorkey(colorkey)

        if resize:
            img = transform.scale(img, resize)
        return img

    @classmethod
    def get_image(cls, key: str) -> Surface or dict:
        """Return img surface object or dict with all of the surface's pngs"""
        try:
            if isinstance(sub_dict := cls.__sprite_images[key], dict):
                copy_dict: dict = {}
                for subkey in sub_dict:
                    copy_dict[subkey] = [surf.copy() for surf in sub_dict[subkey]]
                return copy_dict
            else:
                return cls.__sprite_images[key].copy()
        except (KeyError, ValueError) as ex:
            raise ex.with_traceback()

    @classmethod
    def init(cls) -> None:
        cls.__load(cls, cls.__assets_directory, cls.__sprite_images)


if __name__ == "__main__":
    Assets.init()
