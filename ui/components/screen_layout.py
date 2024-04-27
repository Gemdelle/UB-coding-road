from tkinter import BOTH, YES

import tkinter as tk
from PIL import Image, ImageTk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager
from utils.sound_manager import play_button_sound

output_container_width = 500
output_container_height = 534
output_container_x = 730
output_container_y = 122

def resize_and_center_image(image):
    img_width, img_height = image.size
    scale = min(output_container_width / img_width, output_container_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    resized_image = image.resize((new_width, new_height))

    x = (output_container_width - new_width) // 2
    y = (output_container_height - new_height) // 2

    return resized_image, x, y

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
        image = Image.open(resource_path(f"assets\\images\\backgrounds\\background-levels.png"))
        image = image.resize((1280, 720))
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)
        # End Background #

        # Start Title and Subtitle #
        canvas.create_text(45, 40, text=self.title_text, fill="#e8e8e3", font=("Georgia", 25, "bold"), anchor="w")
        canvas.create_text(45, 75, text=self.subtitle_text, fill="#e8e8e3",
                           font=("Georgia", 16, "bold"), anchor="w")
        # End Title and Subtitle #

        # Start Levels Images #
        levels_image_path = None
        image_width = 55
        offset_between_images = 10

        total_width = (user_progress[self.level_name]["total"] - 1) * offset_between_images + user_progress[self.level_name]["total"] * image_width

        x_start = 1230 - total_width
        for i in range(user_progress[self.level_name]["total"]):
            state = "LOCKED" if user_progress[self.level_name]["status"] == "LOCKED" else "IN_PROGRESS" if i == user_progress[self.level_name]["current"] else "LOCKED" if i > user_progress[self.level_name]["current"] else "COMPLETED"
            if state == "IN_PROGRESS":
                levels_image_path = resource_path(f"assets\\images\\levels\\{self.module_number}-current.png")
            elif state == "LOCKED":
                levels_image_path = resource_path("assets\\images\\levels\\locked.png")
            elif state == "COMPLETED":
                levels_image_path = resource_path(f"assets\\images\\levels\\{self.module_number}-passed.png")

            image_level = Image.open(levels_image_path)
            image_level = image_level.resize((image_width, 95))
            image_level_tk = ImageTk.PhotoImage(image_level)

            setattr(canvas, f"image_level_tk_{i}", image_level_tk)
            x_coordinate = x_start + i * (image_width + offset_between_images)
            canvas.create_image(x_coordinate, 75, anchor="w", image=image_level_tk)
        # End Levels Images #

        # Start Task #
        frame_image = Image.open(resource_path(f"assets\\images\\frames\\instructions-background.png"))
        frame_image = frame_image.resize((680, 200))
        frame_image_tk = ImageTk.PhotoImage(frame_image)
        setattr(canvas, f"frame_image_tk", frame_image_tk)
        canvas.create_image(25, 200, anchor="w", image=frame_image_tk)
        canvas.create_text(120, 160, justify="left", text=self.task_text, fill="black", font=("Georgia", 8, "bold"), anchor="w")
        # End Task #

        # Start Code Area #
        text_area = tk.Text(canvas, wrap="word", width=75, height=22)
        canvas.create_window(55, 500, window=text_area, anchor="w")
        # End Code Area #

        if user_completed_stage:
            text_area.insert("1.0", self.correct_code_text)
            self.correct_excercise_state(canvas, text_area)
        else:
            text_area.insert("1.0", self.incorrect_code_text)
            self.incorrect_output(canvas)

        if not user_completed_stage:
            # Start Run Button #
            run_button_canvas = tk.Canvas(self.frame, bg="white", width=100, height=72, highlightthickness=0)
            run_button_window = canvas.create_window(540, 640, window=run_button_canvas, anchor="w")
            run_button_image = Image.open(resource_path("assets\\images\\buttons\\run-button.png"))
            run_button_image = run_button_image.resize((96, 70))
            run_button_image_tk = ImageTk.PhotoImage(run_button_image)

            def on_run_button_click(event):
                self.process_input(text_area, run_button_window, canvas,
                                   lambda: (self.correct_excercise_state(canvas, text_area)),
                                   lambda: (self.incorrect_output(canvas), self.show_wrong_message(canvas)))

            def on_image_enter(event):
                run_button_canvas.config(cursor="hand2")

            def on_image_leave(event):
                run_button_canvas.config(cursor="")

            setattr(run_button_canvas, f"run_button_image_tk", run_button_image_tk)
            run_button = run_button_canvas.create_image(5, 34, anchor="w", image=run_button_image_tk)
            run_button_canvas.tag_bind(run_button, "<Enter>", on_image_enter)
            run_button_canvas.tag_bind(run_button, "<Leave>", on_image_leave)
            run_button_canvas.tag_bind(run_button, '<Button-1>', on_run_button_click)
            # End Run Button #

            # Start Tooltip Button #
            tooltip_button_image = Image.open(resource_path("assets\\images\\tooltip\\light-tooltip.png"))
            tooltip_button_image = tooltip_button_image.resize((50, 60))
            tooltip_button_image_tk = ImageTk.PhotoImage(tooltip_button_image)

            tooltip_off_button_image = Image.open(resource_path("assets\\images\\tooltip\\dark-tooltip.png"))
            tooltip_off_button_image = tooltip_off_button_image.resize((50, 60))
            tooltip_off_button_image_tk = ImageTk.PhotoImage(tooltip_off_button_image)

            def on_tooltip_button_enter(button_id):
                canvas.config(cursor="hand2")
                self.correct_output(canvas)
                setattr(canvas, "tooltip_button_image_tk", tooltip_button_image_tk)
                canvas.itemconfig(button_id, image=tooltip_button_image_tk)

            def on_tooltip_button_leave(button_id):
                canvas.config(cursor="")
                self.incorrect_output(canvas)
                setattr(canvas, "tooltip_button_image_tk", tooltip_off_button_image_tk)
                canvas.itemconfig(button_id, image=tooltip_off_button_image_tk)

            setattr(canvas, "tooltip_button_image_tk", tooltip_off_button_image_tk)
            tooltip_button = canvas.create_image(1080, 665, anchor="w", image=tooltip_off_button_image_tk)
            canvas.tag_bind(tooltip_button, "<Enter>", lambda event: on_tooltip_button_enter(tooltip_button))
            canvas.tag_bind(tooltip_button, "<Leave>", lambda event: on_tooltip_button_leave(tooltip_button))
            # End Tooltip Button #

            self.incorrect_output(canvas)
        else:
            text_area.config(state=tk.DISABLED, cursor="arrow")

        # Start Back Arrow #
        back_arrow_image = Image.open(resource_path("assets\\images\\back_arrow.png"))
        back_arrow_image = back_arrow_image.resize((59, 33))
        back_arrow_image_tk = ImageTk.PhotoImage(back_arrow_image)

        def on_back_arrow_click(event):
            play_button_sound()
            self.back_screen()
            canvas.destroy()

        def on_arrow_click_image_enter(event):
            canvas.config(cursor="hand2")

        def on_arrow_click_image_leave(event):
            canvas.config(cursor="")

        setattr(canvas, f"back_arrow_image_tk_{i}", back_arrow_image_tk)
        back_arrow_button = canvas.create_image(1141, 666, anchor="w", image=back_arrow_image_tk)
        canvas.tag_bind(back_arrow_button, "<Enter>", on_arrow_click_image_enter)
        canvas.tag_bind(back_arrow_button, "<Leave>", on_arrow_click_image_leave)
        canvas.tag_bind(back_arrow_button, '<Button-1>', on_back_arrow_click)
        # End Back Arrow #

        # Start Book #
        book_image_image = Image.open(resource_path(f"assets\\images\\books\\{self.module_number}.png"))
        book_image_image = book_image_image.resize((40, 63))
        book_image_image_tk = ImageTk.PhotoImage(book_image_image)

        setattr(canvas, f"book_image_tk_{i}", book_image_image_tk)
        canvas.create_image(1213, 665, anchor="w", image=book_image_image_tk)
        # End Book #

    def incorrect_output(self, output_canvas):
        if self.incorrect_output_image_path is not None:
            music_sheet_image = Image.open(self.incorrect_output_image_path)
            resized_image, x, y = resize_and_center_image(music_sheet_image)
            music_sheet_image_tk = ImageTk.PhotoImage(resized_image)

            setattr(output_canvas, f"music_sheet_image_tk_wrong", music_sheet_image_tk)
            output_canvas.create_image(output_container_x + x, output_container_y + y, anchor='nw', image=music_sheet_image_tk)

    def correct_output(self, canvas):
        music_sheet_image = Image.open(self.correct_output_image_path)
        resized_image, x, y = resize_and_center_image(music_sheet_image)
        music_sheet_image_tk = ImageTk.PhotoImage(resized_image)
        setattr(canvas, f"music_sheet_image_tk_right", music_sheet_image_tk)
        canvas.create_image(output_container_x + x, output_container_y + y, anchor='nw', image=music_sheet_image_tk)

    def correct_excercise_state(self, canvas, input_area):
        self.correct_output(canvas)

        # Start Next Button #
        next_button_canvas = tk.Canvas(canvas, bg="white", width=200, height=110, highlightthickness=0)
        canvas.create_window(450, 620, window=next_button_canvas, anchor="w")
        next_button_image = Image.open(resource_path("assets\\images\\buttons\\next.png"))
        next_button_image = next_button_image.resize((200, 110))
        next_button_image_tk = ImageTk.PhotoImage(next_button_image)

        def on_next_button_click(event):
            self.next_screen()
            play_button_sound()

        def on_image_enter(event):
            next_button_canvas.config(cursor="hand2")

        def on_image_leave(event):
            next_button_canvas.config(cursor="")

        setattr(next_button_canvas, f"next_button_image_tk", next_button_image_tk)
        next_button = next_button_canvas.create_image(3, 60, anchor="w", image=next_button_image_tk)
        next_button_canvas.tag_bind(next_button, "<Enter>", on_image_enter)
        next_button_canvas.tag_bind(next_button, "<Leave>", on_image_leave)
        next_button_canvas.tag_bind(next_button, '<Button-1>', on_next_button_click)
        # End Next Button #

        # Start Pet #
        # pet_canvas = tk.Canvas(canvas, bg="white", width=70, height=50, highlightthickness=0)
        # canvas.create_window(500, 630, window=pet_canvas, anchor="w")
        # pet_image = Image.open(resource_path("assets\\images\\pet.png"))
        # pet_image = pet_image.resize((70, 50))
        # pet_image_tk = ImageTk.PhotoImage(pet_image)
        #
        # setattr(pet_canvas, f"pet_image_tk_right", pet_image_tk)
        # pet_canvas.create_image(0, 30, anchor='w', image=pet_image_tk)
        # End Pet #

        input_area.config(state=tk.DISABLED, cursor="arrow")

    # def show_right_message(self, code_frame):
    #     right_feedback_canvas = tk.Canvas(self.frame, bg="white", width=104, height=100, highlightthickness=0)
    #     right_feedback_window = code_frame.create_window(440, 620, window=right_feedback_canvas, anchor="w")
    #     right_feedback_image = Image.open(resource_path("assets\\images\\code-feedback\\nice-message-feedback.png"))
    #     right_feedback_image = right_feedback_image.resize((83, 80))
    #     right_feedback_tk = ImageTk.PhotoImage(right_feedback_image)
    #
    #     setattr(right_feedback_canvas, f"right_feedback_tk", right_feedback_tk)
    #     right_feedback_canvas.create_image(20, 60, anchor="w", image=right_feedback_tk)
    #
    #     set_timeout_manager = SetTimeoutManager()
    #     set_timeout_manager.setTimeout(lambda: code_frame.delete(right_feedback_window), 2)

    def show_wrong_message(self, code_frame):
        wrong_feedback_image = Image.open(resource_path("assets\\images\\code-feedback\\try-again-message-feedback.png"))
        wrong_feedback_image = wrong_feedback_image.resize((83, 80))
        wrong_feedback_tk = ImageTk.PhotoImage(wrong_feedback_image)

        setattr(code_frame, f"wrong_feedback_tk", wrong_feedback_tk)
        wrong_feedback_id = code_frame.create_image(640, 655, anchor="w", image=wrong_feedback_tk)

        set_timeout_manager = SetTimeoutManager()
        set_timeout_manager.setTimeout(lambda: code_frame.delete(wrong_feedback_id), 2)
