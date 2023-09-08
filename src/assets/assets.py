import os

from pygame import Surface, image, transform, mask, mixer
from pygame.constants import BLEND_ALPHA_SDL2


_images_directory: str = os.path.abspath(os.path.join(os.getcwd(), "assets/images"))
# this dict gets populated once the method get_sprite_images gets run once
_sprite_images: dict = {}


def _load(path: str, imgs_dict: dict, prev_key: str = None) -> None:
    """Recursive method that loads _sprite_images with
       all the images in the path arg directory

    Args:
        path (str): head directory location
        imgs_dict (dict): dictionary being populated
        prev_key (str, optional): key of previous directory. Defaults to None.
    """
    if prev_key:
        imgs_dict[prev_key] = {}
    img_size: tuple = (64, 64)
    temp_imgs: list = []

    try:
        for file in os.listdir(path):
            if file[-4:] == ".png":
                if file[0].isdigit():
                    img: Surface = _load_image(os.path.join(path, file))
                    img: Surface = transform.scale(img, img_size)
                    temp_imgs.append(img)

                else:
                    img: Surface = _load_image(
                        os.path.join(path, file),
                    )
                    str_parts = file[:-4].split("_")

                    if str_parts[-1] == "sheet":
                        img = _get_subimages(img)
                    imgs_dict[str_parts[0]] = img

            elif not file[0] == ".":
                if prev_key:
                    _load(
                        os.path.abspath(os.path.join(path, file)),
                        imgs_dict[prev_key],
                        file,
                    )
                else:
                    _load(
                        os.path.abspath(os.path.join(path, file)),
                        imgs_dict,
                        file,
                    )
    except NotADirectoryError as ex:
        print(f"{ex.filename} not an accepted file type.")
    if len(temp_imgs) > 0:
        imgs_dict[prev_key] = temp_imgs


def _load_image(path: str) -> Surface:
    """Get an image from a given path

    Args:
        path (str): file location

    Returns:
        Surface: pygame surface with the colorkey set to the color of the top left (0,0) pixel
    """
    img = image.load(path).convert()
    img.set_colorkey(img.get_at((0, 0)))
    return img


def _get_subimages(image: Surface) -> list[Surface]:
    """Remove as much as the colorkey as possible from the image

    Args:
        image (Surface): pygame Surface
        size (tuple, optional): . Defaults to None.

    Returns:
        list[Surface]: _description_
    """
    _img = image
    _colorkey = _img.get_at((0, 0))
    _mask = mask.from_surface(_img, threshold=174)
    _rects = _mask.get_bounding_rects()

    _images = list()
    for surf, rect in [
        (
            Surface(
                _rect.size,
                flags=BLEND_ALPHA_SDL2,
            ),
            _rect,
        )
        for _rect in _rects
    ]:
        surf.blit(_img, (0, 0), area=rect)
        surf.set_colorkey(_colorkey)
        _images.append(surf)

    return _images


def init() -> None:
    _load(_images_directory, _sprite_images)


def get_image(key: str) -> Surface | dict:
    """Return img surface object or dict with all of the surface's pngs

    Args:
        key (str): images key (filename)

    Raises:
        KeyError | ValyeError: Invalid key

    Returns:
        Surface or dict: a single image or a dict containing images
    """
    try:
        if isinstance(sub_dict := _sprite_images[key], dict):
            copy_dict: dict = {}
            for subkey in sub_dict:
                copy_dict[subkey] = [surf.copy() for surf in sub_dict[subkey]]
            return copy_dict
        else:
            return _sprite_images[key].copy()
    except (KeyError, ValueError) as ex:
        raise ex.with_traceback()


if __name__ == "__main__":
    init()
