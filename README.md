# Advanced Python Browser

This project is a first step toward building a custom web browser using Python and PyQt5. It uses `QWebEngineView` to render web pages and adds basic browser features like tabs, history, bookmarks, downloads, and a URL/search bar.

## What It Does Today

- Multi-tab browsing with a tab bar.
- Back, forward, reload, and home navigation.
- URL bar that supports direct URLs and search queries.
- History tracking saved in `history.json`.
- Bookmarks saved in `bookmarks.json`.
- Download handling with a save dialog.
- Simple right-click context menu (back/forward/reload/copy URL).
- Optional dark mode styling.
- Step 1 completed: raw socket networking with HTTPS to fetch HTML.
- Step 2 completed: separate HTTP headers from the body.
- Step 3 completed: basic GUI window with a Tkinter canvas.
- Step 4 completed: basic HTML tag stripping to extract text.
- Step 5 completed: real HTML parser with DOM tree structure.
- Step 6 completed: styling system with mini CSS support.
- Step 7 completed: layout engine to calculate text positions and line breaks.
- Step 8 completed: rendering engine to draw the display list to the screen.
- Step 9 completed: scrolling system for navigating long pages.
- Step 10 completed: link clicking with clickable area detection.
- Step 11 completed: address bar for typing and navigating to URLs.
- Step 12 completed: history tracking for back/forward navigation.
- Step 13 completed: bookmarks saved to a JSON file.
- Step 14 completed: image support using Pillow and Tkinter.
- Step 15 completed: permanent bookmarks with JSON load/save and delete links.
- Step 16 completed: permanent browsing history saved to JSON.

## Files

- `advanced_browser.py`: Main application code.
- `network.py`: Step 1 networking proof of concept (raw sockets + HTTPS).
- `html_parser.py`: Step 2 response parsing (headers vs body).
- `browser.py`: Step 3 GUI window with a drawing canvas.
- `test_browser.py`: Step 4 quick test to print extracted text.
- `dom_parser.py`: Step 5 DOM tree builder (tokenization + tree structure).
- `style_engine.py`: Step 6 styling engine (applies font size, bold, italic, color).
- `layout_engine.py`: Step 7 layout engine (calculates coordinates and line breaks).
- `layout.py`: Combined layout and rendering logic.
- `history.json`: Stored browsing history.
- `bookmarks.json`: Stored bookmarks.

## Step Highlights

- Step 1: Connect via raw sockets, send GET, receive HTML.
- Step 2: Split headers and body at `\r\n\r\n`.
- Step 3: Use Tkinter `Canvas` as a drawing surface.
- Step 4: Strip HTML tags to get plain text.
- Step 5: Build a DOM tree using tokenization + stack.
- Step 6: Apply simple styles (font size, bold, italic, color).
- Step 7: Flow layout with line wrapping and spacing.
- Step 8: Render display list to pixels on canvas.
- Step 9: Scroll by adjusting viewport offset.
- Step 10: Detect link clicks using stored rectangles.
- Step 11: Address bar for typing URLs and navigation.
- Step 12: Back/forward history stack per tab.
- Step 13: Basic bookmarks list.
- Step 14: Image support via Pillow + ImageTk.
- Step 15: Persist bookmarks to `bookmarks.json` with delete links.
- Step 16: Persist history to `history.json` with `history://` page.

## Run It

```bash
python advanced_browser.py
```

```bash
python network.py
```

```bash
python html_parser.py
```

```bash
python browser.py
```

```bash
python test_browser.py
```

```bash
python dom_parser.py
```

```bash
python style_engine.py
```

```bash
python layout_engine.py
```

## Notes

This is a learning project and can be expanded step by step as new features are added.
