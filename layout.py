import re

class LayoutEngine:
    def __init__(self, html):
        self.html = html
        self.display_list = []   # stores what to draw
        self.links = []          # stores clickable link areas

    def parse(self):
        html = re.sub(r"<script.*?>.*?</script>", "", self.html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<style.*?>.*?</style>", "", self.html, flags=re.DOTALL | re.IGNORECASE)

        tokens = re.split(r"(<[^>]+>)", html)

        x, y = 20, 20
        line_height = 28
        max_width = 820

        current_link = None

        for token in tokens:
            if token.startswith("<"):
                tag = token.lower()

                # Line breaks
                if tag.startswith("<br") or tag.startswith("</p") or tag.startswith("</h1") or tag.startswith("</div"):
                    x = 20
                    y += line_height

                # Heading style
                if tag.startswith("<h1"):
                    y += 10

                # Detect <a href="">
                if tag.startswith("<a "):
                    match = re.search(r'href="([^"]+)"', token, flags=re.IGNORECASE)
                    if match:
                        current_link = match.group(1)

                # Detect closing </a>
                if tag.startswith("</a"):
                    current_link = None

            else:
                words = token.split()
                for word in words:
                    word_width = len(word) * 9  # rough width estimate

                    if x + word_width > max_width:
                        x = 20
                        y += line_height

                    color = "blue" if current_link else "black"
                    underline = True if current_link else False

                    self.display_list.append((x, y, word, color, underline))

                    if current_link:
                        self.links.append((x, y, x + word_width, y + 20, current_link))

                    x += word_width + 10

        return self.display_list, self.links
