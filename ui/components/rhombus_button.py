import tkinter as tk


class RombusButton(tk.Canvas):
    def __init__(self, master=None, width=0, height=0, text="", **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.text = text
        self.draw_rhombus()

    def draw_rhombus(self):
        self.delete("all")
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        # Calculate coordinates of the four corners
        x0 = canvas_width / 2
        y0 = 0
        x1 = canvas_width
        y1 = canvas_height / 2
        x2 = x0
        y2 = canvas_height
        x3 = 0
        y3 = y1

        # Draw lines connecting the corners
        self.create_line(x0, y0, x1, y1, fill="black")
        self.create_line(x1, y1, x2, y2, fill="black")
        self.create_line(x2, y2, x3, y3, fill="black")
        self.create_line(x3, y3, x0, y0, fill="black")

        # Calculate the center coordinates of the rhombus
        center_x = (x0 + x1 + x2 + x3) / 4
        center_y = (y0 + y1 + y2 + y3) / 4

        # Create the text item
        text_item = self.create_text(center_x, center_y, text=self.text)

        # Calculate the bounding box of the text item
        text_bbox = self.bbox(text_item)

        if text_bbox is not None:
            # Calculate the width and height of the text
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate the anchor point for the text to center it horizontally and vertically
            anchor_x = center_x - text_width / 2
            anchor_y = center_y - text_height / 2

            # Move the text item to the centered position
            self.move(text_item, anchor_x - text_bbox[0], anchor_y - text_bbox[1])
