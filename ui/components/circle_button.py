import tkinter as tk


class CircleButton(tk.Canvas):
    def __init__(self, master=None, state=None, width=0, height=0, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.state = state
        self.width = width
        self.height = height
        self.draw_circle()

    def draw_circle(self):
        self.delete("all")
        cell_width = self.winfo_reqwidth()
        cell_height = self.winfo_reqheight()

        if self.state == "IN_PROGRESS":
            color = "grey"
        elif self.state == "COMPLETED":
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