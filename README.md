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

## Files

- `advanced_browser.py`: Main application code.
- `network.py`: Step 1 networking proof of concept (raw sockets + HTTPS).
- `html_parser.py`: Step 2 response parsing (headers vs body).
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

## Next Steps (Ideas)

- Custom homepage and theme.
- Better incognito support with a separate profile.
- Improved downloads UI and progress tracking.
- Better search engine selection.
- Favicon and page title handling per tab.

## Notes

This is a learning project and can be expanded step by step as new features are added.
