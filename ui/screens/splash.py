from core.screens import Screens
from ui.components.clickable_image import ClickableImage
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager


def draw(frame, change_screen):
    splash_image = ClickableImage(frame, image_path=resource_path("assets\\images\\splash.png"), image_size=(1280, 720), bg=frame.cget('bg'))
    splash_image.pack()

    set_timeout_manager = SetTimeoutManager()
    set_timeout_manager.setTimeout(lambda: change_screen(Screens.LANDING), 3)
