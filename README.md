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

## Files

- `advanced_browser.py`: Main application code.
- `history.json`: Stored browsing history.
- `bookmarks.json`: Stored bookmarks.

## How It Works (High Level)

1. The app starts a `QMainWindow` and adds a `QTabWidget` as the main area.
2. Each tab is a `QWebEngineView` that loads a URL.
3. The URL bar reads input and decides whether to navigate or perform a search.
4. History and bookmarks are stored as JSON for quick loading on startup.

## Run It

```bash
python advanced_browser.py
```

## Next Steps (Ideas)

- Custom homepage and theme.
- Better incognito support with a separate profile.
- Improved downloads UI and progress tracking.
- Better search engine selection.
- Favicon and page title handling per tab.

## Notes

This is a learning project and can be expanded step by step as new features are added.
