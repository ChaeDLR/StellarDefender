from abc import ABCMeta

# Everything a screen needs to operate in the game loop
class ScreenBase(metaclass=ABCMeta):
    """
    Store all of the code every screen in the game will need access to
    """

    # bool to tell the main loop to reassign the active screen
    change_screen: bool = False
    # next active screen's key | First active screen is main menu
    # screen's key will be the file name of the screen without ".py"
    new_screen: str = "main_menu"

    # check that the required methods have been added to the subclass
    # more information at "https://realpython.com/python-interface/#formal-interfaces"
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "check_events")
            and callable(subclass.check_events)
            and hasattr(subclass, "update")
            and callable(subclass.update)
        )
