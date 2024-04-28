import tkinter as tk
from tkinter import YES, BOTH

from PIL import Image, ImageTk, ImageEnhance

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

    def on_image_next_arrow_enter(event):
        canvas.config(cursor="hand2")

    def on_image_next_arrow_leave(event):
        canvas.config(cursor="")

    setattr(canvas, f"image_next_arrow_tk", image_next_arrow_tk)
    next_arrow_button = canvas.create_image(40, 405, anchor=tk.NW, image=image_next_arrow_tk)
    canvas.tag_bind(next_arrow_button, '<Button-1>', on_image_next_arrow_click)
    canvas.tag_bind(next_arrow_button, "<Enter>", on_image_next_arrow_enter)
    canvas.tag_bind(next_arrow_button, "<Leave>", on_image_next_arrow_leave)

    create_programme(canvas)
    create_notes(canvas)
    create_library(canvas)
    create_toggle_sound(canvas)

    row_index = 0
    row_offset = 50
    emblems_offset = 63
    for key, value in user_progress.items():
        if row_index >= 5 and row_index <= 6:
            column_offset = 40
            #capitalized_module_name = [word.capitalize() for word in key.split('_')]
            #output_capitalized_module_name = " ".join(capitalized_module_name)
            #canvas.create_text(150, 100 + row_offset, text=f"{row_index}. {output_capitalized_module_name}", fill="#e8e8e3", font=("Georgia", 15, "bold"), anchor="nw")

            if value["status"] != "LOCKED":
                image_book = Image.open(resource_path("assets\\images\\books\\"+str(row_index)+".png"))
                image_book = image_book.resize((50, 70))
                image_book_tk = ImageTk.PhotoImage(image_book)
                setattr(canvas, f"image_book_{row_index}", image_book_tk)
                canvas.create_image(500, 160 + row_offset, anchor=tk.NW, image=image_book_tk)

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
                button = canvas.create_image(560 + column_offset, 165 + row_offset, anchor=tk.NW, image=image_level_tk)
                if state != "LOCKED":
                    canvas.tag_bind(button, "<Enter>", on_image_enter)
                    canvas.tag_bind(button, "<Leave>", on_image_leave)
                    canvas.tag_bind(button, '<Button-1>', on_image_click)

                emblem_image = Image.open(resource_path("assets\\images\\emblems\\" + str(row_index) + ".png"))
                emblem_image = emblem_image.resize((65, 85))

                if value["status"] == "LOCKED":
                    emblem_image_enhance = ImageEnhance.Brightness(emblem_image)
                    emblem_image_unlocked = emblem_image_enhance.enhance(0.2)
                    emblem_image_tk = ImageTk.PhotoImage(emblem_image_unlocked)
                else:
                    emblem_image_tk = ImageTk.PhotoImage(emblem_image)

                setattr(canvas, f"emblem_image_tk_{row_index}", emblem_image_tk)
                canvas.create_image(580 + column_offset + emblems_offset, 155 + row_offset, anchor=tk.NW, image=emblem_image_tk)

                column_offset += 63

            row_offset += 95
        row_index += 1

def create_toggle_sound(canvas):
    sound_manager = SoundManager()
    toggle_sound_button_image = Image.open(resource_path("assets\\images\\buttons\\header\\music-on-button.png"))
    toggle_sound_button_image = toggle_sound_button_image.resize((115, 71))
    toggle_sound_button_image_tk = ImageTk.PhotoImage(toggle_sound_button_image)

    toggle_sound_off_button_image = Image.open(resource_path("assets\\images\\buttons\\header\\music-off-button.png"))
    toggle_sound_off_button_image = toggle_sound_off_button_image.resize((115, 71))
    toggle_sound_off_button_image_tk = ImageTk.PhotoImage(toggle_sound_off_button_image)

    def on_tooltip_button_enter(event):
        canvas.config(cursor="hand2")

    def on_tooltip_button_leave(event):
        canvas.config(cursor="")

    def on_tooltip_button_click(button_id):
        canvas.config(cursor="hand2")
        sound_manager.toggle_sound()
        toggle_sound_image_tk_changed = toggle_sound_off_button_image_tk if sound_manager.is_muted else toggle_sound_button_image_tk
        setattr(canvas, "toggle_sound_button_image_tk", toggle_sound_image_tk_changed)
        canvas.itemconfig(button_id, image=toggle_sound_image_tk_changed)

    toggle_sound_image_tk = toggle_sound_off_button_image_tk if sound_manager.is_muted else toggle_sound_button_image_tk
    setattr(canvas, "toggle_sound_button_image_tk", toggle_sound_image_tk)
    tooltip_button = canvas.create_image(500, 90, anchor="w", image=toggle_sound_image_tk)
    canvas.tag_bind(tooltip_button, '<Button-1>', lambda event: on_tooltip_button_click(tooltip_button))
    canvas.tag_bind(tooltip_button, "<Enter>", on_tooltip_button_enter)
    canvas.tag_bind(tooltip_button, "<Leave>", on_tooltip_button_leave)

def create_programme(canvas):
    programme_button_image = Image.open(resource_path("assets\\images\\buttons\\header\\programme-button.png"))
    programme_button_image = programme_button_image.resize((85, 40))
    programme_button_image_tk = ImageTk.PhotoImage(programme_button_image)

    def on_programme_button_enter(event):
        canvas.config(cursor="hand2")

    def on_programme_button_leave(event):
        canvas.config(cursor="")

    def on_programme_button_click(button_id):
        canvas.config(cursor="hand2")

    setattr(canvas, "programme_button_image_tk", programme_button_image_tk)
    programme_button = canvas.create_image(200, 90, anchor="w", image=programme_button_image_tk)
    canvas.tag_bind(programme_button, '<Button-1>', lambda event: on_programme_button_click(programme_button))
    canvas.tag_bind(programme_button, "<Enter>", on_programme_button_enter)
    canvas.tag_bind(programme_button, "<Leave>", on_programme_button_leave)

def create_notes(canvas):
    notes_button_image = Image.open(resource_path("assets\\images\\buttons\\header\\notes-button.png"))
    notes_button_image = notes_button_image.resize((65, 50))
    notes_button_image_tk = ImageTk.PhotoImage(notes_button_image)

    def on_notes_button_enter(event):
        canvas.config(cursor="hand2")

    def on_notes_button_leave(event):
        canvas.config(cursor="")

    def on_notes_button_click(button_id):
        canvas.config(cursor="hand2")

    setattr(canvas, "notes_button_image_tk", notes_button_image_tk)
    notes_button = canvas.create_image(320, 90, anchor="w", image=notes_button_image_tk)
    canvas.tag_bind(notes_button, '<Button-1>', lambda event: on_notes_button_click(notes_button))
    canvas.tag_bind(notes_button, "<Enter>", on_notes_button_enter)
    canvas.tag_bind(notes_button, "<Leave>", on_notes_button_leave)

def create_library(canvas):
    library_button_image = Image.open(resource_path("assets\\images\\buttons\\header\\library-button.png"))
    library_button_image = library_button_image.resize((70, 50))
    library_button_image_tk = ImageTk.PhotoImage(library_button_image)

    def on_library_button_enter(event):
        canvas.config(cursor="hand2")

    def on_library_button_leave(event):
        canvas.config(cursor="")

    def on_library_button_click(button_id):
        canvas.config(cursor="hand2")

    setattr(canvas, "library_button_image_tk", library_button_image_tk)
    library_button = canvas.create_image(410, 90, anchor="w", image=library_button_image_tk)
    canvas.tag_bind(library_button, '<Button-1>', lambda event: on_library_button_click(library_button))
    canvas.tag_bind(library_button, "<Enter>", on_library_button_enter)
    canvas.tag_bind(library_button, "<Leave>", on_library_button_leave)
