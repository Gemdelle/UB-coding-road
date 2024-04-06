import tkinter as tk
from PIL import ImageTk, Image

from core.user_progress_repository import UserProgressRepository
from ui.components.circle_button import CircleButton
from ui.components.rhombus_button import RombusButton
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path

def draw(frame):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    image = Image.open(resource_path("assets\\images\\book.jpg"))
    resized_image = image.resize((20, 20))
    tk_image = ImageTk.PhotoImage(resized_image)

    # Crear un marco para el título y la cuadrícula
    title_frame = tk.Frame(frame)
    title_frame.grid(row=0, column=0, columnspan=8)  # Establecer el marco encima de la cuadrícula

    # Colocar el título en el marco del título y centrarlo vertical y horizontalmente
    title_label = WhiteStormLabel(title_frame, text=f"CODING ROAD MAP", font_size=10, bg="#3d6466")
    title_label.pack(side='right',padx=(500, 0),pady=(10,10))  # Ajustar el relleno vertical y extender horizontalmente

    row_index = 0
    for key, value in user_progress.items():
        label = WhiteStormLabel(frame, text=f"{row_index}. {key}", font_size=10)
        label.grid(row=row_index+1, column=0, padx=10, pady=10, sticky=tk.W)

        if value["status"] != "LOCKED":
            book_image = tk.Label(frame, image=tk_image)
            book_image.image = tk_image
            book_image.grid(row=row_index+1, column=1, padx=10, pady=10, sticky=tk.W)

        for i in range(value["total"] + 1):
            state = "IN_PROGRESS" if value["status"] == "LOCKED" else "IN_PROGRESS" if value["current"] < i else "COMPLETED"
            button = CircleButton(frame, state=state, width=20, height=20)
            button.grid(row=row_index+1, column=2 + i, padx=10, pady=10, sticky=tk.W)

        test_stats = value["test"]
        rhombus_button = RombusButton(frame, width=20, height=20, text=f"{test_stats['actual']}/{test_stats['total']}")
        rhombus_button.grid(row=row_index+1, column=2 + value["total"] + 1, padx=10, pady=10, sticky=tk.W)

        row_index += 1

    # Configure column widths
    for i in range(8):  # Todas las columnas
        frame.columnconfigure(i, weight=1)

if __name__ == "__main__":
    app = tk.Tk()
    frame = tk.Frame(app)
    frame.pack(fill=tk.BOTH, expand=True)
    draw(frame)
    app.mainloop()
