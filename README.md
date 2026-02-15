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

## Step 1 Completed: Networking (Raw Sockets + HTTPS)

The `network.py` script proves the browser can connect to a real server, negotiate HTTPS, send an HTTP GET request, and parse the response to extract the HTML body. This is the foundation for building a renderer later.

What it does:

- Connects to a website server (example.com).
- Uses SSL for HTTPS encryption.
- Sends a valid HTTP GET request.
- Receives the response and extracts the HTML body.

## Step 2 Completed: Separate Headers and Body

Server responses contain HTTP headers and the HTML body in the same payload. The browser must split them so it can read metadata (headers) and then render the actual HTML (body).

How it works:

- HTTP headers end with a blank line: `\r\n\r\n`.
- Split the response once at that marker to separate headers and body.

Example:

```python
headers, body = response.split("\r\n\r\n", 1)
```

## Step 3 Completed: Create a Window (GUI)

A browser needs a window to render content. For this step, a Tkinter `Canvas` acts like a whiteboard where the browser can draw text and shapes, which is a step toward rendering HTML as pixels.

Why Canvas:

- Lets us draw text, rectangles, lines, and images.
- Provides a simple way to think about converting HTML into pixels.

Example:

```python
canvas.create_text(100, 50, text="Hello")
```

## Step 4 Completed: Remove HTML Tags (Basic Parsing)

HTML contains tags like `<h1>` and `<p>`, but the user should see only the text. This step implements a simple parser that scans the HTML character-by-character, ignores everything inside `<` and `>`, and keeps only the visible text.

How it works:

- When `<` is found, start ignoring characters.
- When `>` is found, stop ignoring and resume collecting text.
- Output is plain text that can be drawn to the canvas.

This is a beginner-friendly approach and not enough for complex pages, but it proves the core idea.

## Step 5 Completed: Build a Real HTML Parser (DOM Tree)

Simple tag stripping loses structure. HTML is a tree, so the browser must build a **DOM (Document Object Model)** to know which elements are nested, which text is bold, and how to apply styles.

Why DOM is needed:

```html
<p>Hello <b>Samiksha</b></p>
```

Stripping gives `Hello Samiksha`, but the browser must know "Samiksha" is bold and both are inside a paragraph.

DOM tree looks like:

```
p
 ├── text("Hello")
 └── b
      └── text("Samiksha")
```

How DOM is built:

1. **Tokenization**: Split HTML into tokens (opening tags, closing tags, text).
2. **Tree building**: Use a stack to track open elements and build parent-child relationships.

Example:

- `<p>` → push node to stack
- `Hello` → add as child of `<p>`
- `<b>` → push node to stack
- `Samiksha` → add as child of `<b>`
- `</b>` → pop node from stack
- `</p>` → pop node from stack

## Step 6 Completed: Styling (Mini CSS Support)

HTML defines content structure, but styling defines how it looks. The browser must apply visual properties like font size, bold, italic, and color to each element.

What styling does:

- `<h1>` → large bold font
- `<b>` → bold text
- `<i>` → italic text
- `<p>` → normal paragraph

How it works:

The browser walks through the DOM tree and assigns style properties to each node based on its tag:

```python
if node.tag == "h1":
    node.font_size = 32
    node.bold = True
```

Each node now has:

- Text content
- Font size
- Font weight (bold/normal)
- Font style (italic/normal)
- Color

This prepares the DOM for rendering, where the browser can draw each element with the correct visual properties.

## Step 7 Completed: Layout Engine (Calculate Positions)

Styling tells the browser *how* elements should look, but the layout engine determines *where* to place them on the screen. It calculates exact coordinates for every piece of text and handles line breaks.

Why layout is needed:

- Determine where text goes (x, y coordinates)
- Handle line wrapping when text reaches the window edge
- Add spacing between paragraphs
- Calculate vertical positioning

How it works:

The browser uses a flow layout system:

1. Text flows left to right
2. When text reaches the window width → wrap to next line
3. Block elements (like `<p>`) add vertical spacing

Example:

```
Window width = 500px
Text: "Hello welcome to my browser project"
```

If "browser project" doesn't fit on the same line, it wraps to the next line.

Layout output (display list):

```python
[("Hello", x=10, y=10, font="normal"),
 ("Samiksha", x=70, y=10, font="bold"),
 ("Welcome", x=10, y=40, font="normal")]
```

Now every piece of text has exact pixel coordinates, ready for rendering.

## Step 8 Completed: Rendering Engine (Drawing)

The rendering engine takes the display list from the layout engine and draws it to the screen using the Tkinter canvas.

What rendering does:

- Loops through the display list
- Draws each text element at its calculated (x, y) position
- Applies the correct font, color, and underline styles

Example:

```python
canvas.create_text(x, y, text=word, font=font, fill=color)
```

Now the webpage becomes visible on screen.

Real browser concept:

- Chrome uses the **Blink** rendering engine
- Firefox uses **Gecko**
- Our browser uses a simplified mini renderer

The render function in `browser.py` handles scrolling and redraws the canvas whenever needed (on scroll, page load, etc.).

## How It Works (High Level)

1. The app starts a `QMainWindow` and adds a `QTabWidget` as the main area.
2. Each tab is a `QWebEngineView` that loads a URL.
3. The URL bar reads input and decides whether to navigate or perform a search.
4. History and bookmarks are stored as JSON for quick loading on startup.

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

## Next Steps (Ideas)

- Custom homepage and theme.
- Better incognito support with a separate profile.
- Improved downloads UI and progress tracking.
- Better search engine selection.
- Favicon and page title handling per tab.

## Notes

This is a learning project and can be expanded step by step as new features are added.
