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
        self.window.configure(bg="#ffd6e8")

        self.scroll_y = 0
        self.page_text = ""

        # History system
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

        # Buttons
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

        # URL bar
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

        # Scroll + keys
        self.window.bind("<MouseWheel>", self.on_scroll)
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)

        # Enter loads URL
        self.url_entry.bind("<Return>", self.go_to_url)

        # Load Home Page
        self.go_home()

        self.window.mainloop()

    # ------------------- CUSTOM HOME PAGE -------------------
    def home_page_html(self):
        return f"""
        <html>
        <head><title>Pinkie Browser Home</title></head>
        <body>
        <h1>🌸 Welcome to Pinkie Browser 💖</h1>
        <p>Hello Samiksha 👑</p>
        <p>This is your own browser made from scratch in Python.</p>
        <p>Try typing:</p>
        <p>example.com</p>
        <p>httpbin.org/html</p>
        <p>info.cern.ch</p>
        <p>Made with 💕 in Python</p>
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

            self.page_text = extract_text(html)

        except Exception as e:
            self.page_text = f"❌ Error loading page:\n\n{e}"

        self.scroll_y = 0
        self.render()

        # Add to history
        if add_to_history:
            if self.history_index < len(self.history) - 1:
                self.history = self.history[: self.history_index + 1]

            self.history.append(url)
            self.history_index += 1

    # ------------------- URL NAVIGATION -------------------
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

    # ------------------- BACK / FORWARD -------------------
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
