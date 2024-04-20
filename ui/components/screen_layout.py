from tkinter import BOTH, YES

import tkinter as tk
from PIL import Image, ImageTk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from utils.resource_path_util import resource_path
from utils.sound_manager import play_button_sound


class ScreenLayout:
    def __init__(self, frame, back_screen, next_screen, process_input, level_name, level_number, module_number, background_image_path, correct_output_image_path, incorrect_output_image_path, title_text, subtitle_text, task_text, correct_code_text, incorrect_code_text):
        self.frame = frame
        self.level_name = level_name
        self.level_number = level_number
        self.module_number = module_number
        self.back_screen = back_screen
        self.next_screen = next_screen
        self.process_input = process_input
        self.background_image_path = background_image_path
        self.correct_output_image_path = correct_output_image_path
        self.incorrect_output_image_path = incorrect_output_image_path
        self.title_text = title_text
        self.subtitle_text = subtitle_text
        self.task_text = task_text
        self.correct_code_text = correct_code_text
        self.incorrect_code_text = incorrect_code_text

    def draw(self):
        repository = UserProgressRepository()
        user_progress = repository.get_current_progress()
        user_completed_stage = user_progress[self.level_name]["current"] > self.level_number

        canvas = tk.Canvas(self.frame, bg="black", width=1280, height=720)
        canvas.pack(fill=BOTH, expand=YES)

        def on_image_enter(event):
            canvas.config(cursor="hand2")

        def on_image_leave(event):
            canvas.config(cursor="")

        # Start Background #
        image = Image.open(self.background_image_path)
        image = image.resize((1280, 720))
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)
        # End Background #

        # Start Title and Subtitle #
        canvas.create_text(70, 50, text=self.title_text, fill="#e8e8e3", font=("Georgia", 25, "bold"), anchor="w")
        canvas.create_text(70, 100, text=self.subtitle_text, fill="#e8e8e3",
                           font=("Georgia", 16, "bold"), anchor="w")
        # End Title and Subtitle #

        # Start Levels Images #
        levels_image_path = None
        column_offset = 50
        for i in range(user_progress[self.level_name]["total"]):
            state = "LOCKED" if user_progress[self.level_name]["status"] == "LOCKED" else "IN_PROGRESS" if i == user_progress[self.level_name]["current"] else "LOCKED" if i > user_progress[self.level_name]["current"] else "COMPLETED"
            if state == "IN_PROGRESS":
                levels_image_path = resource_path(f"assets\\images\\levels\\{self.level_number}-current.png")
            elif state == "LOCKED":
                levels_image_path = resource_path("assets\\images\\levels\\locked.png")
            elif state == "COMPLETED":
                levels_image_path = resource_path(f"assets\\images\\levels\\{self.level_number}-passed.png")

            image_level = Image.open(levels_image_path)
            image_level = image_level.resize((45, 80))
            image_level_tk = ImageTk.PhotoImage(image_level)

            setattr(canvas, f"image_level_tk_{i}", image_level_tk)
            canvas.create_image(320 + column_offset, 60, anchor="w", image=image_level_tk)
            column_offset += 60
        # End Levels Images #

        # Start Back Arrow #
        back_arrow_image = Image.open(resource_path("assets\\images\\back_arrow.png"))
        back_arrow_image = back_arrow_image.resize((87, 46))
        back_arrow_image_tk = ImageTk.PhotoImage(back_arrow_image)

        def on_back_arrow_click(event):
            play_button_sound()
            self.back_screen()
            canvas.destroy()

        setattr(canvas, f"back_arrow_image_tk_{i}", back_arrow_image_tk)
        back_arrow_button = canvas.create_image(1100, 60, anchor="w", image=back_arrow_image_tk)
        canvas.tag_bind(back_arrow_button, "<Enter>", on_image_enter)
        canvas.tag_bind(back_arrow_button, "<Leave>", on_image_leave)
        canvas.tag_bind(back_arrow_button, '<Button-1>', on_back_arrow_click)
        # End Back Arrow #

        # Start Book #
        book_image_image = Image.open(resource_path(f"assets\\images\\books\\{self.level_number}.png"))
        book_image_image = book_image_image.resize((60, 80))
        book_image_image_tk = ImageTk.PhotoImage(book_image_image)

        setattr(canvas, f"book_image_tk_{i}", book_image_image_tk)
        canvas.create_image(1200, 60, anchor="w", image=book_image_image_tk)
        # End Book #

        # Start Task #
        task_canvas = tk.Canvas(self.frame, bg="#e8e8e3", width=600, height=160)
        canvas.create_window(70, 200, window=task_canvas, anchor="w")
        task_canvas.create_text(20, 80, justify="left", text=self.task_text, fill="black", font=("Georgia", 8, "bold"), anchor="w")
        # End Task #

        # Start Code Area #
        text_area = tk.Text(canvas, wrap="word", width=75, height=22)
        canvas.create_window(70, 480, window=text_area, anchor="w")
        # End Code Area #

        if user_completed_stage:
            text_area.insert("1.0", self.correct_code_text)
            self.correct_excercise_state(canvas, text_area)
        else:
            text_area.insert("1.0", self.incorrect_code_text)
            self.incorrect_output(canvas)

        if not user_completed_stage:
            # Start Run Button #
            run_button_canvas = tk.Canvas(self.frame, bg="red", width=60, height=30)
            run_button_window = canvas.create_window(600, 630, window=run_button_canvas, anchor="w")
            run_button_image = Image.open(resource_path("assets\\images\\back_arrow.png"))
            run_button_image = run_button_image.resize((87, 46))
            run_button_image_tk = ImageTk.PhotoImage(run_button_image)

            def on_run_button_click(event):
                self.process_input(text_area, run_button_window, canvas,
                              lambda: self.correct_excercise_state(canvas, text_area),
                              lambda: self.incorrect_output(canvas))

            def on_image_enter(event):
                run_button_canvas.config(cursor="hand2")

            def on_image_leave(event):
                run_button_canvas.config(cursor="")

            setattr(run_button_canvas, f"run_button_image_tk", run_button_image_tk)
            run_button = run_button_canvas.create_image(10, 10, anchor="w", image=run_button_image_tk)
            run_button_canvas.tag_bind(run_button, "<Enter>", on_image_enter)
            run_button_canvas.tag_bind(run_button, "<Leave>", on_image_leave)
            run_button_canvas.tag_bind(run_button, '<Button-1>', on_run_button_click)
            # End Run Button #

            # Start Tooltip Button #
            tooltip_button_image = Image.open(resource_path("assets\\images\\levels\\0-current.png"))
            tooltip_button_image = tooltip_button_image.resize((46, 46))
            tooltip_button_image_tk = ImageTk.PhotoImage(tooltip_button_image)

            def on_tooltip_button_enter(event):
                canvas.config(cursor="hand2")
                self.correct_output(canvas)

            def on_tooltip_button_leave(event):
                canvas.config(cursor="")
                self.incorrect_output(canvas)

            setattr(canvas, "tooltip_button_image_tk", tooltip_button_image_tk)
            tooltip_button = canvas.create_image(1150, 680, anchor="w", image=tooltip_button_image_tk)
            canvas.tag_bind(tooltip_button, "<Enter>", on_tooltip_button_enter)
            canvas.tag_bind(tooltip_button, "<Leave>", on_tooltip_button_leave)
            # End Tooltip Button #

            self.incorrect_output(canvas)
        else:
            text_area.config(state=tk.DISABLED, cursor="arrow")

    def incorrect_output(self, output_canvas):
        music_sheet_image = Image.open(self.incorrect_output_image_path)
        music_sheet_image = music_sheet_image.resize((307, 534))
        music_sheet_image_tk = ImageTk.PhotoImage(music_sheet_image)

        setattr(output_canvas, f"music_sheet_image_tk_wrong", music_sheet_image_tk)
        output_canvas.create_image(800, 120, anchor='nw', image=music_sheet_image_tk)

    def correct_output(self, canvas):
        music_sheet_image = Image.open(self.correct_output_image_path)
        music_sheet_image = music_sheet_image.resize((307, 534))
        music_sheet_image_tk = ImageTk.PhotoImage(music_sheet_image)
        setattr(canvas, f"music_sheet_image_tk_right", music_sheet_image_tk)
        canvas.create_image(800, 120, anchor='nw', image=music_sheet_image_tk)

    def correct_excercise_state(self, canvas, input_area):
        self.correct_output(canvas)

        # Start Next Button #
        next_button_canvas = tk.Canvas(canvas, bg="white", width=60, height=30, highlightthickness=0)
        canvas.create_window(600, 630, window=next_button_canvas, anchor="w")
        next_button_image = Image.open(resource_path("assets\\images\\book.jpg"))
        next_button_image = next_button_image.resize((87, 46))
        next_button_image_tk = ImageTk.PhotoImage(next_button_image)

        def on_next_button_click(event):
            self.next_screen()
            play_button_sound()

        def on_image_enter(event):
            next_button_canvas.config(cursor="hand2")

        def on_image_leave(event):
            next_button_canvas.config(cursor="")

        setattr(next_button_canvas, f"next_button_image_tk", next_button_image_tk)
        next_button = next_button_canvas.create_image(10, 10, anchor="w", image=next_button_image_tk)
        next_button_canvas.tag_bind(next_button, "<Enter>", on_image_enter)
        next_button_canvas.tag_bind(next_button, "<Leave>", on_image_leave)
        next_button_canvas.tag_bind(next_button, '<Button-1>', on_next_button_click)
        # End Next Button #

        # Start Pet #
        pet_canvas = tk.Canvas(canvas, bg="white", width=70, height=50, highlightthickness=0)
        canvas.create_window(500, 630, window=pet_canvas, anchor="w")
        pet_image = Image.open(resource_path("assets\\images\\pet.png"))
        pet_image = pet_image.resize((70, 50))
        pet_image_tk = ImageTk.PhotoImage(pet_image)

        setattr(pet_canvas, f"pet_image_tk_right", pet_image_tk)
        pet_canvas.create_image(0, 30, anchor='w', image=pet_image_tk)
        # End Pet #

        input_area.config(state=tk.DISABLED, cursor="arrow")