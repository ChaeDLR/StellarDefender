from pygame import Rect, Surface

class Hud:
    rect: Rect = None

    __components: list = []

    def __init__(self, dims: tuple[int, int]) -> None:
        self.rect = Rect(0.0, 0.0, dims[0], dims[1])

    def get_blitseq(self) -> list[Surface, Rect]:
        """Get a sequence of tuples

        Returns:
            list[Surface, Rect]: _description_
        """
        return [(i.image, i.rect) for i in self.__components]

    def attach(self, *components) -> None:
        """Attach a component to the hud to be updated and drawn

        Args:
            component (any): Class should have
            component.rect: pygame.Rect
            component.image: pygame.Surface
            component.update(): method to update component variables
        """
        for component in components:
            if not (
                hasattr(component, "image")
                and hasattr(component, "rect")
                and hasattr(component, "update")
            ):
                raise Exception(
                    f"Component: {component}\nDoes not have attr image and/or rect."
                )
            self.__components.append(component)

    def update(self) -> None:
        for component in self.__components:
            component.update()
