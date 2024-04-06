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
            frame = ScreenFrame(self, screen)
            self.frames[screen] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print(repository.get_current_progress())
        self.show_screen(Screens.LANDING)

    def show_screen(self, screen):
        frame = self.frames[screen]
        frame.pack_propagate(False)
        frame.tkraise()


if __name__ == "__main__":
    app = Application()
    x = app.winfo_screenwidth() // 5
    y = int(app.winfo_screenheight() * 0.1)
    app.geometry('1280x720+' + str(x) + '+' + str(y))
    app.mainloop()