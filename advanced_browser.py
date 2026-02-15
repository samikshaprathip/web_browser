import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction,
    QLineEdit, QTabWidget, QMenu, QFileDialog, QMessageBox,
    QListWidget, QDockWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl


HISTORY_FILE = "history.json"
BOOKMARKS_FILE = "bookmarks.json"


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


class AdvancedBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced Python Browser")
        self.setGeometry(100, 100, 1400, 850)

        # Load history & bookmarks
        self.history = load_data(HISTORY_FILE)
        self.bookmarks = load_data(BOOKMARKS_FILE)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Toolbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction("⬅ Back", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction("➡ Forward", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction("🔄 Reload", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction("🏠 Home", self)
        home_btn.triggered.connect(self.go_home)
        navbar.addAction(home_btn)

        navbar.addWidget(self.url_bar)

        new_tab_btn = QAction("➕ Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_btn)

        incognito_btn = QAction("🕶 Incognito", self)
        incognito_btn.triggered.connect(self.add_incognito_tab)
        navbar.addAction(incognito_btn)

        bookmark_btn = QAction("⭐ Bookmark", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_btn)

        history_btn = QAction("📜 History", self)
        history_btn.triggered.connect(self.show_history)
        navbar.addAction(history_btn)

        bookmarks_btn = QAction("📌 Bookmarks", self)
        bookmarks_btn.triggered.connect(self.show_bookmarks)
        navbar.addAction(bookmarks_btn)

        download_btn = QAction("⬇ Downloads", self)
        download_btn.triggered.connect(self.show_downloads)
        navbar.addAction(download_btn)

        dark_mode_btn = QAction("🌙 Dark Mode", self)
        dark_mode_btn.triggered.connect(self.toggle_dark_mode)
        navbar.addAction(dark_mode_btn)

        # Download list dock
        self.download_list = QListWidget()
        self.download_dock = QDockWidget("Downloads", self)
        self.download_dock.setWidget(self.download_list)
        self.addDockWidget(2, self.download_dock)
        self.download_dock.hide()

        # History dock
        self.history_list = QListWidget()
        self.history_dock = QDockWidget("History", self)
        self.history_dock.setWidget(self.history_list)
        self.addDockWidget(1, self.history_dock)
        self.history_dock.hide()

        # Bookmarks dock
        self.bookmarks_list = QListWidget()
        self.bookmarks_dock = QDockWidget("Bookmarks", self)
        self.bookmarks_dock.setWidget(self.bookmarks_list)
        self.addDockWidget(1, self.bookmarks_dock)
        self.bookmarks_dock.hide()

        self.dark_mode = False

        # Add default tab
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or isinstance(qurl, bool):
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))
        browser.loadFinished.connect(lambda _, browser=browser:
            self.tabs.setTabText(self.tabs.indexOf(browser), browser.page().title())
        )

        browser.page().profile().downloadRequested.connect(self.handle_download)

        browser.urlChanged.connect(lambda qurl: self.save_history(qurl.toString()))

        browser.setContextMenuPolicy(3)
        browser.customContextMenuRequested.connect(lambda pos, b=browser: self.show_context_menu(pos, b))

    def add_incognito_tab(self):
        profile = QWebEngineProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)

        browser = QWebEngineView()
        browser.setPage(browser.page())
        browser.setUrl(QUrl("https://www.google.com"))

        i = self.tabs.addTab(browser, "Incognito")
        self.tabs.setCurrentIndex(i)

        browser.page().profile().downloadRequested.connect(self.handle_download)

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url_bar(qurl, self.tabs.currentWidget())

    def navigate_to_url(self):
        url = self.url_bar.text().strip()

        if " " in url:
            search_url = "https://www.google.com/search?q=" + url.replace(" ", "+")
            self.tabs.currentWidget().setUrl(QUrl(search_url))
            return

        if not url.startswith("http") and "." not in url:
            search_url = "https://www.google.com/search?q=" + url
            self.tabs.currentWidget().setUrl(QUrl(search_url))
            return

        if not url.startswith("http"):
            url = "https://" + url

        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url_bar(self, qurl, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def go_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    # ---------------- HISTORY ----------------
    def save_history(self, url):
        if url and url not in self.history:
            self.history.append(url)
            save_data(HISTORY_FILE, self.history)

    def show_history(self):
        self.history_list.clear()
        for item in reversed(self.history):
            self.history_list.addItem(item)

        self.history_list.itemClicked.connect(lambda item: self.open_url_from_list(item.text()))
        self.history_dock.show()

    # ---------------- BOOKMARKS ----------------
    def add_bookmark(self):
        url = self.tabs.currentWidget().url().toString()
        if url and url not in self.bookmarks:
            self.bookmarks.append(url)
            save_data(BOOKMARKS_FILE, self.bookmarks)
            QMessageBox.information(self, "Bookmark", "Bookmarked Successfully!")

    def show_bookmarks(self):
        self.bookmarks_list.clear()
        for item in self.bookmarks:
            self.bookmarks_list.addItem(item)

        self.bookmarks_list.itemClicked.connect(lambda item: self.open_url_from_list(item.text()))
        self.bookmarks_dock.show()

    def open_url_from_list(self, url):
        self.tabs.currentWidget().setUrl(QUrl(url))

    # ---------------- DOWNLOADS ----------------
    def handle_download(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if path:
            download.setPath(path)
            download.accept()
            self.download_list.addItem(f"Downloading: {path}")

    def show_downloads(self):
        self.download_dock.show()

    # ---------------- DARK MODE ----------------
    def toggle_dark_mode(self):
        if not self.dark_mode:
            self.setStyleSheet("""
                QMainWindow { background-color: #121212; color: white; }
                QToolBar { background-color: #1e1e1e; }
                QLineEdit { background-color: #2a2a2a; color: white; padding: 5px; }
                QListWidget { background-color: #1e1e1e; color: white; }
            """)
            self.dark_mode = True
        else:
            self.setStyleSheet("")
            self.dark_mode = False

    # ---------------- RIGHT CLICK MENU ----------------
    def show_context_menu(self, pos, browser):
        menu = QMenu()

        back_action = menu.addAction("Back")
        forward_action = menu.addAction("Forward")
        reload_action = menu.addAction("Reload")
        copy_url_action = menu.addAction("Copy Page URL")

        action = menu.exec_(browser.mapToGlobal(pos))

        if action == back_action:
            browser.back()
        elif action == forward_action:
            browser.forward()
        elif action == reload_action:
            browser.reload()
        elif action == copy_url_action:
            QApplication.clipboard().setText(browser.url().toString())


app = QApplication(sys.argv)
window = AdvancedBrowser()
window.show()
sys.exit(app.exec_())
