import tkinter as tk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_frame import ScreenFrame


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
        self.show_screen(Screens.LANDING)

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