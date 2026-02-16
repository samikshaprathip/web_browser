import tkinter as tk
from network import request
from layout import LayoutEngine

WIDTH, HEIGHT = 900, 650
TOPBAR_HEIGHT = 55
TABBAR_HEIGHT = 40
SCROLL_STEP = 50


class Tab:
    def __init__(self, url="home://"):
        self.url = url
        self.title = "New Tab 💖"
        self.scroll_y = 0
        self.page_height = 0
        self.display_list = []
        self.links = []

        self.history = []
        self.history_index = -1


class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pinkie Browser 💖")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.configure(bg="#ffd6e8")

        # Tabs
        self.tabs = []
        self.current_tab_index = 0
        self.bookmarks = []

        # ------------------- TAB BAR -------------------
        self.tab_bar = tk.Frame(self.window, bg="#ff77b7", height=TABBAR_HEIGHT)
        self.tab_bar.pack(fill="x")

        self.tab_frames = []

        self.new_tab_btn = tk.Button(
            self.tab_bar,
            text="➕",
            bg="#ff4fa3",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.new_tab
        )
        self.new_tab_btn.pack(side="right", padx=6, pady=6)

        # ------------------- TOP BAR -------------------
        self.top_bar = tk.Frame(self.window, bg="#ff9ecb", height=TOPBAR_HEIGHT)
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

        self.bookmark_btn = tk.Button(
            self.top_bar,
            text="⭐",
            bg="#ff4fa3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.add_bookmark
        )
        self.bookmark_btn.pack(side="left", padx=6)

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

        # ------------------- MAIN FRAME -------------------
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.scrollbar_move)
        self.scrollbar.pack(side="right", fill="y")

        # ------------------- LOADING BAR -------------------
        self.loading_frame = tk.Frame(self.window, bg="#ffd6e8", height=10)
        self.loading_frame.pack(fill="x")

        self.loading_bar = tk.Canvas(self.loading_frame, height=8, bg="#ffd6e8", highlightthickness=0)
        self.loading_bar.pack(fill="x")

        self.loading_progress = 0
        self.loading_active = False

        # Bindings
        self.window.bind("<MouseWheel>", self.on_scroll)
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)

        self.url_entry.bind("<Return>", self.go_to_url)
        self.canvas.bind("<Button-1>", self.on_click)

        # Start with 1 tab
        self.new_tab()

        self.window.mainloop()

    # ------------------- CURRENT TAB -------------------
    def current_tab(self):
        return self.tabs[self.current_tab_index]

    # ------------------- HOME PAGE -------------------
    def home_page_html(self):
        bookmarks_html = ""

        if self.bookmarks:
            bookmarks_html += "<h2>⭐ Your Bookmarks</h2>"
            for link in self.bookmarks:
                bookmarks_html += f'<p><a href="{link}">{link}</a></p>'
        else:
            bookmarks_html += "<p>No bookmarks yet 😭</p>"

        return f"""
        <html>
        <body>
        <h1>🌸 Welcome to Pinkie Browser 💖</h1>
        <p>Hello Samiksha 👑</p>

        <p>This is your own Python browser built from scratch.</p>

        <h2>Try these websites:</h2>

        <p><a href="https://example.com">Example Domain</a></p>
        <p><a href="https://httpbin.org/html">HttpBin HTML</a></p>
        <p><a href="https://info.cern.ch">First Website Ever</a></p>

        {bookmarks_html}

        <p>Made with 💕</p>
        </body>
        </html>
        """

    def add_bookmark(self):
        tab = self.current_tab()

        if tab.url not in self.bookmarks and tab.url != "home://":
            self.bookmarks.append(tab.url)

        self.load_page("home://", add_to_history=False)

    def extract_title(self, html):
        import re

        match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if match:
            title = match.group(1).strip()
            title = re.sub(r"\s+", " ", title)
            return title

        return "Untitled Page"

    def start_loading(self):
        self.loading_active = True
        self.loading_progress = 0
        self.title_label.config(text="🌸 Loading...")
        self.animate_loading()

    def stop_loading(self):
        self.loading_active = False
        self.loading_bar.delete("all")
        self.title_label.config(text="🌸 Pinkie Browser")

    def animate_loading(self):
        if not self.loading_active:
            return

        self.loading_bar.delete("all")

        width = self.window.winfo_width()
        self.loading_progress += 30

        if self.loading_progress > width:
            self.loading_progress = 0

        self.loading_bar.create_rectangle(
            0, 0,
            self.loading_progress, 8,
            fill="#ff4fa3",
            outline=""
        )

        self.window.after(50, self.animate_loading)

    # ------------------- LOAD PAGE -------------------
    def load_page(self, url, add_to_history=True):
        tab = self.current_tab()

        try:
            self.start_loading()

            if url == "home://":
                html = self.home_page_html()
            else:
                html = request(url)

            tab.title = self.extract_title(html)
            engine = LayoutEngine(html)
            tab.display_list, tab.links = engine.parse()

            if tab.display_list:
                max_y = max(item[1] for item in tab.display_list)
                tab.page_height = max_y + 100
            else:
                tab.page_height = 0

            self.stop_loading()

        except Exception as e:
            tab.display_list = [(20, 20, f"❌ Error loading page:\n\n{e}", "red", False, ("Arial", 14))]
            tab.links = []
            tab.page_height = 0
            self.stop_loading()

        tab.scroll_y = 0
        tab.url = url
        self.window.title(f"Pinkie Browser 💖 - {tab.title}")

        self.update_scrollbar()
        self.render()

        if add_to_history:
            if tab.history_index < len(tab.history) - 1:
                tab.history = tab.history[: tab.history_index + 1]

            tab.history.append(url)
            tab.history_index += 1

        self.refresh_tabs()

    # ------------------- TAB SYSTEM -------------------
    def new_tab(self):
        tab = Tab("home://")
        self.tabs.append(tab)
        self.current_tab_index = len(self.tabs) - 1
        self.load_page("home://")
        self.refresh_tabs()

    def close_tab(self, index):
        # if only one tab, don't close fully
        if len(self.tabs) == 1:
            self.tabs[0] = Tab("home://")
            self.current_tab_index = 0
            self.load_page("home://")
            self.refresh_tabs()
            return

        # delete the tab
        del self.tabs[index]

        # adjust current tab index
        if self.current_tab_index >= len(self.tabs):
            self.current_tab_index = len(self.tabs) - 1

        self.switch_tab(self.current_tab_index)

    def switch_tab(self, index):
        self.current_tab_index = index
        tab = self.current_tab()

        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, tab.url)

        self.update_scrollbar()
        self.render()
        self.refresh_tabs()

    def refresh_tabs(self):
        for frame in self.tab_frames:
            frame.destroy()

        self.tab_frames = []

        for i, tab in enumerate(self.tabs):
            title = "Home 💕" if tab.url == "home://" else tab.title
            if len(title) > 14:
                title = title[:14] + "..."

            bg_color = "#ff4fa3" if i == self.current_tab_index else "#ffb3d9"

            tab_frame = tk.Frame(self.tab_bar, bg=bg_color)
            tab_frame.pack(side="left", padx=4, pady=6)

            tab_button = tk.Button(
                tab_frame,
                text=title,
                bg=bg_color,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                command=lambda i=i: self.switch_tab(i)
            )
            tab_button.pack(side="left", padx=4)

            close_button = tk.Button(
                tab_frame,
                text="❌",
                bg=bg_color,
                fg="white",
                font=("Arial", 9, "bold"),
                relief="flat",
                command=lambda i=i: self.close_tab(i)
            )
            close_button.pack(side="left", padx=2)

            self.tab_frames.append(tab_frame)

    # ------------------- SCROLLBAR -------------------
    def update_scrollbar(self):
        tab = self.current_tab()
        visible_height = HEIGHT - TOPBAR_HEIGHT - TABBAR_HEIGHT

        if tab.page_height <= visible_height:
            self.scrollbar.set(0, 1)
            return

        start = tab.scroll_y / tab.page_height
        end = (tab.scroll_y + visible_height) / tab.page_height

        if end > 1:
            end = 1

        self.scrollbar.set(start, end)

    def scrollbar_move(self, *args):
        tab = self.current_tab()
        visible_height = HEIGHT - TOPBAR_HEIGHT - TABBAR_HEIGHT

        if tab.page_height <= visible_height:
            return

        if args[0] == "moveto":
            fraction = float(args[1])
            tab.scroll_y = int(fraction * tab.page_height)

        elif args[0] == "scroll":
            amount = int(args[1])
            tab.scroll_y += amount * SCROLL_STEP

        self.limit_scroll()
        self.update_scrollbar()
        self.render()

    def limit_scroll(self):
        tab = self.current_tab()
        visible_height = HEIGHT - TOPBAR_HEIGHT - TABBAR_HEIGHT

        if tab.scroll_y < 0:
            tab.scroll_y = 0

        max_scroll = tab.page_height - visible_height
        if max_scroll < 0:
            max_scroll = 0

        if tab.scroll_y > max_scroll:
            tab.scroll_y = max_scroll

    # ------------------- NAVIGATION -------------------
    def go_to_url(self, event=None):
        url = self.url_entry.get().strip()
        if url == "":
            return

        if not url.startswith("http") and url != "home://":
            url = "https://" + url

        self.load_page(url)

    def go_home(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "home://")
        self.load_page("home://")

    def go_back(self):
        tab = self.current_tab()

        if tab.history_index > 0:
            tab.history_index -= 1
            url = tab.history[tab.history_index]

            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

            self.load_page(url, add_to_history=False)

    def go_forward(self):
        tab = self.current_tab()

        if tab.history_index < len(tab.history) - 1:
            tab.history_index += 1
            url = tab.history[tab.history_index]

            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

            self.load_page(url, add_to_history=False)

    # ------------------- RENDER -------------------
    def render(self):
        tab = self.current_tab()
        self.canvas.delete("all")

        for x, y, word, color, underline, font in tab.display_list:
            draw_y = y - tab.scroll_y

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

    # ------------------- LINK CLICK -------------------
    def on_click(self, event):
        tab = self.current_tab()
        click_x = event.x
        click_y = event.y + tab.scroll_y

        for x1, y1, x2, y2, url in tab.links:
            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, url)
                self.load_page(url)
                return

    # ------------------- SCROLL EVENTS -------------------
    def on_scroll(self, event):
        tab = self.current_tab()

        if event.delta < 0:
            tab.scroll_y += SCROLL_STEP
        else:
            tab.scroll_y -= SCROLL_STEP

        self.limit_scroll()
        self.update_scrollbar()
        self.render()

    def scroll_down(self, event=None):
        tab = self.current_tab()
        tab.scroll_y += SCROLL_STEP

        self.limit_scroll()
        self.update_scrollbar()
        self.render()

    def scroll_up(self, event=None):
        tab = self.current_tab()
        tab.scroll_y -= SCROLL_STEP

        self.limit_scroll()
        self.update_scrollbar()
        self.render()


Browser()
