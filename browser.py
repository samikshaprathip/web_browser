import tkinter as tk
from network import request
from layout import LayoutEngine

WIDTH, HEIGHT = 900, 650
SCROLL_STEP = 40


class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pinkie Browser 💖")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.configure(bg="#ffd6e8")

        self.scroll_y = 0

        self.display_list = []
        self.links = []

        self.history = []
        self.history_index = -1

        # ------------------- TOP BAR -------------------
        self.top_bar = tk.Frame(self.window, bg="#ff9ecb", height=55)
        self.top_bar.pack(fill="x")

        self.title_label = tk.Label(
            self.top_bar,
            text="🌸 Pinkie Browser",
            bg="#ff9ecb",
            fg="white",
            font=("Comic Sans MS", 14, "bold")
        )
        self.title_label.pack(side="left", padx=10)

        self.back_btn = tk.Button(
            self.top_bar,
            text="⬅️",
            bg="#ff4fa3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.go_back
        )
        self.back_btn.pack(side="left", padx=3)

        self.forward_btn = tk.Button(
            self.top_bar,
            text="➡️",
            bg="#ff4fa3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.go_forward
        )
        self.forward_btn.pack(side="left", padx=3)

        self.home_btn = tk.Button(
            self.top_bar,
            text="🏠",
            bg="#ff4fa3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.go_home
        )
        self.home_btn.pack(side="left", padx=8)

        self.url_entry = tk.Entry(
            self.top_bar,
            font=("Arial", 13),
            width=45,
            bd=2,
            relief="solid"
        )
        self.url_entry.pack(side="left", padx=10, pady=12)

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
        self.canvas = tk.Canvas(self.window, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Bindings
        self.window.bind("<MouseWheel>", self.on_scroll)
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        self.url_entry.bind("<Return>", self.go_to_url)

        # Link click binding
        self.canvas.bind("<Button-1>", self.on_click)

        # Load home
        self.go_home()

        self.window.mainloop()

    # ------------------- HOME PAGE -------------------
    def home_page_html(self):
        return f"""
        <html>
        <body>
        <h1>🌸 Welcome to Pinkie Browser 💖</h1>
        <p>Hello Samiksha 👑</p>
        <p>This is your browser built from scratch.</p>

        <p>Try these websites:</p>
        <p><a href="https://example.com">Example Domain</a></p>
        <p><a href="https://httpbin.org/html">HttpBin HTML</a></p>
        <p><a href="https://info.cern.ch">First Website Ever</a></p>

        <p>Made with 💕</p>
        </body>
        </html>
        """

    # ------------------- LOAD PAGE -------------------
    def load_page(self, url, add_to_history=True):
        try:
            if url == "home://":
                html = self.home_page_html()
            else:
                html = request(url)

            engine = LayoutEngine(html)
            self.display_list, self.links = engine.parse()

        except Exception as e:
            self.display_list = [(20, 20, f"❌ Error loading page:\n\n{e}", "red", False)]
            self.links = []

        self.scroll_y = 0
        self.render()

        if add_to_history:
            if self.history_index < len(self.history) - 1:
                self.history = self.history[: self.history_index + 1]

            self.history.append(url)
            self.history_index += 1

    # ------------------- NAVIGATION -------------------
    def go_to_url(self, event=None):
        url = self.url_entry.get().strip()

        if url == "":
            return

        if not url.startswith("http"):
            url = "https://" + url

        self.load_page(url)

    def go_home(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "home://")
        self.load_page("home://")

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            url = self.history[self.history_index]
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.load_page(url, add_to_history=False)

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            url = self.history[self.history_index]
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.load_page(url, add_to_history=False)

    # ------------------- RENDER -------------------
    def render(self):
        self.canvas.delete("all")

        for x, y, word, color, underline, font in self.display_list:
            draw_y = y - self.scroll_y

            text_id = self.canvas.create_text(
                x, draw_y,
                anchor="nw",
                text=word,
                font=font,
                fill=color
            )

            if underline:
                bbox = self.canvas.bbox(text_id)
                if bbox:
                    x1, y1, x2, y2 = bbox
                    self.canvas.create_line(x1, y2, x2, y2, fill=color)

    # ------------------- CLICK LINKS -------------------
    def on_click(self, event):
        click_x = event.x
        click_y = event.y + self.scroll_y

        for x1, y1, x2, y2, url in self.links:
            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, url)
                self.load_page(url)
                return

    # ------------------- SCROLL -------------------
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
