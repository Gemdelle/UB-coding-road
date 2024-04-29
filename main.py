import tkinter as tk
import pyglet

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_frame import ScreenFrame
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager

# Preload Sounds
sound_manager = SoundManager()
sound_manager.load_sound("background_music", resource_path("assets\\sounds\\background_music.mp3"))
sound_manager.load_sound("correct", resource_path("assets\\sounds\\correct.mp3"))
sound_manager.load_sound("wrong", resource_path("assets\\sounds\\wrong.mp3"))
sound_manager.load_sound("next-level", resource_path("assets\\sounds\\next-level.mp3"))
sound_manager.load_sound("introduction", resource_path("assets\\sounds\\introduction.mp3"))
sound_manager.load_sound("button", resource_path("assets\\sounds\\button.mp3"))
sound_manager.load_sound("win_emblem", resource_path("assets\\sounds\\badge\\win_emblem.mp3"))

pyglet.options['win32_gdi_font'] = True
# Preload Fonts
pyglet.font.add_file(resource_path("assets\\font\\ModerneFraktur.ttf"))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UB Coding Road")
        repository = UserProgressRepository()

        self.frames = {}
        for screen in Screens:
            frame = ScreenFrame(self, screen, change_screen=self.show_screen)
            self.frames[screen] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print(repository.get_current_progress())
        self.show_screen(Screens.SPLASH)

    def show_screen(self, screen):
        print(f"SHOWING SCREEN: {screen}")
        frame = self.frames[screen]
        frame.draw()
        frame.tkraise()
def toggle_fullscreen(app, event=None):
    if app.attributes("-fullscreen"):
        exit_fullscreen(app, event=None)
    else:
        go_full_screen(app)

def go_full_screen(app):
    app.attributes("-fullscreen", True)
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    aspect_ratio = 1280 / 720
    if screen_width / screen_height > aspect_ratio:
        width = int(screen_height * aspect_ratio)
        height = screen_height
    else:
        width = screen_width
        height = int(screen_width / aspect_ratio)
    app.geometry(f"{width}x{height}")


def exit_fullscreen(app, event=None):
    app.attributes("-fullscreen", False)
    x = app.winfo_screenwidth() // 5
    y = int(app.winfo_screenheight() * 0.1)
    app.geometry('1280x720+' + str(x) + '+' + str(y))

if __name__ == "__main__":
    app = Application()

    #app.bind("<F11>", lambda event: toggle_fullscreen(app, event))
    #app.bind("<Escape>", lambda event: exit_fullscreen(app, event))

    app.attributes("-fullscreen", False)
    x = app.winfo_screenwidth() // 5
    y = int(app.winfo_screenheight() * 0.1)
    app.geometry('1280x720+' + str(x) + '+' + str(y))
    app.resizable(False, False)
    app.mainloop()