import tkinter as tk
from network import request
from html_parser import extract_text

WIDTH, HEIGHT = 800, 600


class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My Scratch Browser")

        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        # Load first page
        self.load_page("https://example.com")

        self.window.mainloop()

    def load_page(self, url):
        html = request(url)
        text = extract_text(html)

        self.canvas.delete("all")

        # Draw text on canvas
        self.canvas.create_text(
            10, 10,
            anchor="nw",
            text=text,
            width=WIDTH - 20,
            font=("Arial", 14),
            fill="black"
        )


Browser()
