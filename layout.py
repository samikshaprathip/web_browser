import re
import tkinter.font as tkfont


class LayoutEngine:
    def __init__(self, html):
        self.html = html
        self.display_list = []
        self.links = []

        self.x = 20
        self.y = 20

        self.line_height = 26
        self.max_width = 860

        self.current_link = None
        self.current_font = ("Arial", 14)
        self.current_color = "black"
        self.current_underline = False

    def clean_html(self):
        html = re.sub(r"<script.*?>.*?</script>", "", self.html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
        return html

    def new_line(self, extra_space=0):
        self.x = 20
        # Use font size to determine line height
        font_size = self.current_font[1] if len(self.current_font) > 1 else 14
        line_height = int(font_size * 1.5)  # 1.5x font size for good spacing
        self.y += line_height + extra_space

    def draw_word(self, word):
        # Use actual Tkinter font measurement for accurate width
        try:
            font_obj = tkfont.Font(family=self.current_font[0], size=self.current_font[1])
            if len(self.current_font) > 2:
                font_obj.configure(weight=self.current_font[2])
            word_width = font_obj.measure(word)
        except:
            # Fallback if font measurement fails
            word_width = len(word) * 10

        # Add space between words
        space_width = 8

        if self.x + word_width > self.max_width:
            self.new_line()

        # Store drawing instruction
        self.display_list.append((
            self.x,
            self.y,
            word,
            self.current_color,
            self.current_underline,
            self.current_font
        ))

        # Store link clickable area
        if self.current_link:
            self.links.append((
                self.x,
                self.y,
                self.x + word_width,
                self.y + 20,
                self.current_link
            ))

        self.x += word_width + space_width

    def parse_tag(self, tag):
        tag = tag.lower().strip()

        # Paragraph breaks
        if tag.startswith("<p") or tag.startswith("</p"):
            self.new_line(extra_space=10)

        # Line break
        elif tag.startswith("<br"):
            self.new_line()

        # Headings
        elif tag.startswith("<h1"):
            self.new_line(extra_space=10)
            self.current_font = ("Arial", 22, "bold")

        elif tag.startswith("</h1"):
            self.current_font = ("Arial", 14)
            self.new_line(extra_space=10)

        elif tag.startswith("<h2"):
            self.new_line(extra_space=8)
            self.current_font = ("Arial", 18, "bold")

        elif tag.startswith("</h2"):
            self.current_font = ("Arial", 14)
            self.new_line(extra_space=8)

        # Bold tag
        elif tag.startswith("<b") or tag.startswith("<strong"):
            self.current_font = ("Arial", 14, "bold")

        elif tag.startswith("</b") or tag.startswith("</strong"):
            self.current_font = ("Arial", 14)

        # Link start
        elif tag.startswith("<a "):
            match = re.search(r'href="([^"]+)"', tag, flags=re.IGNORECASE)
            if match:
                self.current_link = match.group(1)
                self.current_color = "blue"
                self.current_underline = True

        # Link end
        elif tag.startswith("</a"):
            self.current_link = None
            self.current_color = "black"
            self.current_underline = False

    def parse(self):
        html = self.clean_html()

        tokens = re.split(r"(<[^>]+>)", html)

        for token in tokens:
            if token.startswith("<"):
                self.parse_tag(token)
            else:
                words = token.split()
                for word in words:
                    self.draw_word(word)

        return self.display_list, self.links
