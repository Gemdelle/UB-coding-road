import tkinter as tk


class CircleButton(tk.Canvas):
    def __init__(self, master=None, status=None, width=0, height=0, screen_to_change=None, on_click=None, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.status = status
        self.width = width
        self.height = height
        self.on_click = on_click
        self.screen_to_change = screen_to_change
        self.draw_circle()
        if status == "IN_PROGRESS" and on_click is not None:
            self.bind("<Button-1>", self.button_click)

    def button_click(self, event):
        self.on_click(self.screen_to_change)
    def draw_circle(self):
        self.delete("all")
        cell_width = self.winfo_reqwidth()
        cell_height = self.winfo_reqheight()

        if self.status == "IN_PROGRESS":
            color = "blue"
        elif self.status == "LOCKED":
            color = "grey"
        elif self.status == "COMPLETED":
            color = "green"
        else:
            raise ValueError("Invalid state")

        # Calculate coordinates to center the circle in the cell
        x0 = (cell_width - self.width) / 2
        y0 = (cell_height - self.height) / 2
        x1 = x0 + self.width
        y1 = y0 + self.height

        # Draw the circle
        self.create_oval(x0, y0, x1, y1, fill=color, outline="black")