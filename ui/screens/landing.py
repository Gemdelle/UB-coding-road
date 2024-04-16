import tkinter as tk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.clickable_image import ClickableImage
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager

levels=["a","b","c","d","e","f","g","h","i","j","k", "l"]

def play_background_music():
    sound_manager = SoundManager()
    # if not sound_manager.is_playing("background_music"):
    sound_manager.set_volume("background_music", 0.2)
    sound_manager.play_sound("background_music")

def draw(frame, change_screen):
    global levels
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    play_background_music()

    title_frame = tk.Frame(frame, bg=frame.cget('bg'))
    title_frame.grid(row=0, column=0, columnspan=8)

    title_label = WhiteStormLabel(title_frame, text=f"Coding Road Map", foreground="#e8e8e3", font_size=35, bg=frame.cget('bg'))
    title_label.grid(row=0, column=0, sticky=tk.W,padx=(300, 0), pady=(0, 0))

    body_frame = tk.Frame(frame, bg=frame.cget('bg'))
    body_frame.grid(row=1, column=0, columnspan=8)

    row_index = 0
    for key, value in user_progress.items():
        label = WhiteStormLabel(body_frame, text=f"{row_index}. {key.capitalize()}", foreground="#e8e8e3", font_size=20, bg=frame.cget('bg'))
        label.grid(row=row_index, column=0, padx=(40, 40), pady=(0, 0), sticky=tk.W)

        if value["status"] != "LOCKED":
            book_image = ClickableImage(body_frame, image_path=resource_path("assets\\images\\books\\"+str(row_index+1)+".png"),
                                        bg=frame.cget('bg'), image_size=(60, 80))
            book_image.grid(row=row_index, column=1, sticky='w', padx=(0, 20),
                            pady=(20, 10))

        for i in range(value["total"]):
            state = "LOCKED" if value["status"] == "LOCKED" else "IN_PROGRESS" if i == value["current"] else "LOCKED" if i > value["current"] else "COMPLETED"
            screen_to_change = Screens[f'{key}_{i}'.upper()]
            levels_image_path = None
            if state == "IN_PROGRESS":
                levels_image_path = resource_path("assets\\images\\levels\\"+levels[row_index]+"-current.png")
            elif state == "LOCKED":
                levels_image_path = resource_path("assets\\images\\levels\\locked.png")
            elif state == "COMPLETED":
                levels_image_path = resource_path("assets\\images\\levels\\"+levels[row_index]+"-passed.png")
            button = ClickableImage(body_frame, image_path=levels_image_path, image_size=(60, 100), bg=frame.cget('bg'), highlightthickness=0, callback=lambda screen=screen_to_change, state=state: change_screen(screen) if state != "LOCKED" else None)
            button.grid(row=row_index, column=2 + i, padx=(5, 5), pady=(20, 0), sticky=tk.W)

        # test_stats = value["test"]
        # rhombus_button = RombusButton(body_frame, width=20, height=20, text=f"{test_stats['actual']}/{test_stats['total']}")
        # rhombus_button.grid(row=row_index, column=2 + value["total"] + 1, padx=10, pady=10, sticky=tk.W)

        row_index += 1