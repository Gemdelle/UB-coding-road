import tkinter as tk
from tkinter import YES, BOTH

from PIL import Image, ImageTk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager, play_background_music, play_button_sound


def draw(frame, change_screen):
    global levels
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    canvas = tk.Canvas(frame, bg="black", width=1280, height=720)
    canvas.pack(fill=BOTH, expand=YES)

    image = Image.open(resource_path("assets\\images\\backgrounds\\background-main-2.png"))
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

    setattr(canvas, f"image_next_arrow_tk", image_next_arrow_tk)
    next_arrow_button = canvas.create_image(120, 330, anchor=tk.NW, image=image_next_arrow_tk)
    canvas.tag_bind(next_arrow_button, '<Button-1>', on_image_next_arrow_click)

    row_index = 0
    row_offset = 50
    for key, value in user_progress.items():
        if row_index >= 5:
            column_offset = 40
            #capitalized_module_name = [word.capitalize() for word in key.split('_')]
            #output_capitalized_module_name = " ".join(capitalized_module_name)
            #canvas.create_text(150, 100 + row_offset, text=f"{row_index}. {output_capitalized_module_name}", fill="#e8e8e3", font=("Georgia", 15, "bold"), anchor="nw")

            if value["status"] != "LOCKED":
                image_book = Image.open(resource_path("assets\\images\\books\\"+str(row_index+1)+".png"))
                image_book = image_book.resize((40, 50))
                image_book_tk = ImageTk.PhotoImage(image_book)
                setattr(canvas, f"image_book_{row_index}", image_book_tk)
                canvas.create_image(600, 80 + row_offset, anchor=tk.NW, image=image_book_tk)

            for i in range(value["total"]):
                state = "LOCKED" if value["status"] == "LOCKED" else "IN_PROGRESS" if i == value["current"] else "LOCKED" if i > value["current"] else "COMPLETED"
                screen_to_change = Screens[f'{key}_{i}'.upper()]
                levels_image_path = None
                if state == "IN_PROGRESS":
                    levels_image_path = resource_path("assets\\images\\levels\\"+str(row_index)+"-current.png")
                elif state == "LOCKED":
                    levels_image_path = resource_path("assets\\images\\levels\\locked.png")
                elif state == "COMPLETED":
                    levels_image_path = resource_path("assets\\images\\levels\\"+str(row_index)+"-passed.png")

                image_level = Image.open(levels_image_path)
                image_level = image_level.resize((50, 90))
                image_level_tk = ImageTk.PhotoImage(image_level)

                def on_image_click(event, screen=screen_to_change):
                    change_screen(screen)
                    canvas.destroy()

                def on_image_enter(event):
                    canvas.config(cursor="hand2")

                def on_image_leave(event):
                    canvas.config(cursor="")

                setattr(canvas, f"image_level_tk_{row_index}_{i}", image_level_tk)
                button = canvas.create_image(640 + column_offset, 70 + row_offset, anchor=tk.NW, image=image_level_tk)
                if state != "LOCKED":
                    canvas.tag_bind(button, "<Enter>", on_image_enter)
                    canvas.tag_bind(button, "<Leave>", on_image_leave)
                    canvas.tag_bind(button, '<Button-1>', on_image_click)

                column_offset += 60

            row_offset += 95
        row_index += 1
