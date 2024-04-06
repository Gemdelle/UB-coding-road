import tkinter as tk

from PIL import Image, ImageTk

from utils.resource_path_util import resource_path


def draw(frame):
    # Load and resize the image
    image = Image.open(resource_path("assets\\images\\background.jpg"))
    image = image.resize((1280, 720), Image.LANCZOS)

    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(frame, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label = tk.Label(frame, text="Splash Screen", font=("Helvetica", 20))
    label.pack(pady=20)