import tkinter as tk
from tkinter import YES, BOTH

from PIL import Image, ImageTk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from core.user_progress_status import UserProgressStatus
from ui.components.gif_image import AnimatedGIF
from utils.resource_path_util import resource_path
from utils.sound_manager import play_button_sound, play_win_emblem_sound

output_container_width = 200
output_container_height = 200
output_container_x = 550
output_container_y = 380

def resize_and_center_image(image):
    img_width, img_height = image.size
    scale = min(output_container_width / img_width, output_container_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    resized_image = image.resize((new_width, new_height))

    x = (output_container_width - new_width) // 2
    y = (output_container_height - new_height) // 2

    return resized_image, x, y

def draw(frame, change_screen):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()
    play_win_emblem_sound()
    emblem_found = None
    module_level = 0
    for key, value in user_progress.items():
        if value["status"] == UserProgressStatus.COMPLETED.value:
            emblem_found = module_level
        module_level += 1

    if emblem_found is None:
        change_screen(Screens.LANDING)
    else:
        canvas = tk.Canvas(frame, bg="black", width=1280, height=720)
        canvas.pack(fill=BOTH, expand=YES)

        image = Image.open(resource_path("assets\\images\\backgrounds\\background-badge-0.png"))
        image = image.resize((1280, 720))
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

        image_next_arrow = Image.open(resource_path("assets\\images\\back_arrow.png"))
        image_next_arrow = image_next_arrow.resize((75, 42))
        image_next_arrow_tk = ImageTk.PhotoImage(image_next_arrow)
        def on_image_next_arrow_click(event):
            play_button_sound()
            change_screen(Screens.LANDING)
            canvas.destroy()

        def on_image_next_arrow_enter(event):
            canvas.config(cursor="hand2")

        def on_image_next_arrow_leave(event):
            canvas.config(cursor="")

        setattr(canvas, f"image_next_arrow_tk", image_next_arrow_tk)
        next_arrow_button = canvas.create_image(1160, 640, anchor=tk.NW, image=image_next_arrow_tk)
        canvas.tag_bind(next_arrow_button, '<Button-1>', on_image_next_arrow_click)
        canvas.tag_bind(next_arrow_button, "<Enter>", on_image_next_arrow_enter)
        canvas.tag_bind(next_arrow_button, "<Leave>", on_image_next_arrow_leave)

        emblem_image = Image.open(resource_path("assets\\images\\emblems\\0.png"))
        resized_image, x, y = resize_and_center_image(emblem_image)
        emblem_image_tk = ImageTk.PhotoImage(resized_image)
        setattr(canvas, f"emblem_unlocked_image_tk", emblem_image_tk)
        canvas.create_image(output_container_x + x, output_container_y + y, anchor=tk.W, image=emblem_image_tk)

        AnimatedGIF(canvas, resource_path("assets\\images\\gifs\\win_emblem.gif"), 400, 30)


