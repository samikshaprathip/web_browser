import tkinter as tk
from network import request
from html_parser import extract_text

WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 40


class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My Scratch Browser")

        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.scroll_y = 0
        self.page_text = ""

        # Bind scroll + keys
        self.window.bind("<MouseWheel>", self.on_scroll)
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)

        # Load first page
        self.load_page("https://example.com")

        self.window.mainloop()

    def load_page(self, url):
        html = request(url)
        self.page_text = extract_text(html)

        self.scroll_y = 0
        self.render()

    def render(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            10, 10 - self.scroll_y,
            anchor="nw",
            text=self.page_text,
            width=WIDTH - 20,
            font=("Arial", 14),
            fill="black"
        )

    def on_scroll(self, event):
        if event.delta < 0:
            self.scroll_y += SCROLL_STEP
        else:
            self.scroll_y -= SCROLL_STEP

        if self.scroll_y < 0:
            self.scroll_y = 0

        self.render()

    def scroll_down(self, event=None):
        self.scroll_y += SCROLL_STEP
        self.render()

    def scroll_up(self, event=None):
        self.scroll_y -= SCROLL_STEP

        if self.scroll_y < 0:
            self.scroll_y = 0

        self.render()


Browser()
