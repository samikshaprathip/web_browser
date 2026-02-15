import tkinter as tk
from network import request
from html_parser import extract_text

WIDTH, HEIGHT = 900, 650
SCROLL_STEP = 40


class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pinkie Browser 💖")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.configure(bg="#ffd6e8")  # light pink background

        self.scroll_y = 0
        self.page_text = ""

        # ------------------- TOP BAR -------------------
        self.top_bar = tk.Frame(self.window, bg="#ff9ecb", height=50)
        self.top_bar.pack(fill="x")

        self.title_label = tk.Label(
            self.top_bar,
            text="🌸 Pinkie Browser",
            bg="#ff9ecb",
            fg="white",
            font=("Comic Sans MS", 14, "bold")
        )
        self.title_label.pack(side="left", padx=10)

        self.url_entry = tk.Entry(
            self.top_bar,
            font=("Arial", 13),
            width=50,
            bd=2,
            relief="solid"
        )
        self.url_entry.pack(side="left", padx=10, pady=10)

        self.go_button = tk.Button(
            self.top_bar,
            text="Go 💕",
            bg="#ff4fa3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.go_to_url
        )
        self.go_button.pack(side="left", padx=5)

        # ------------------- CANVAS -------------------
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT - 50, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Scroll bindings
        self.window.bind("<MouseWheel>", self.on_scroll)
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)

        # Enter key loads URL
        self.url_entry.bind("<Return>", self.go_to_url)

        # Load default home page
        self.url_entry.insert(0, "https://example.com")
        self.load_page("https://example.com")

        self.window.mainloop()

    # ------------------- PAGE LOADING -------------------
    def load_page(self, url):
        try:
            html = request(url)
            self.page_text = extract_text(html)

        except Exception as e:
            self.page_text = f"❌ Error loading page:\n\n{e}"

        self.scroll_y = 0
        self.render()

    def go_to_url(self, event=None):
        url = self.url_entry.get().strip()

        if not url.startswith("http"):
            url = "https://" + url

        self.load_page(url)

    # ------------------- RENDERING -------------------
    def render(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            20, 20 - self.scroll_y,
            anchor="nw",
            text=self.page_text,
            width=WIDTH - 40,
            font=("Arial", 14),
            fill="black"
        )

    # ------------------- SCROLLING -------------------
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
