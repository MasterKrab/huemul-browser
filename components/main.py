from PyQt6.QtWidgets import QTabWidget, QPushButton
from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
import validators


class Main(QTabWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        with open("homepage/index.html", "r") as file:
            self.homepage = file.read()
            self.homepage_path = "file:///homepage/index.html"
            self.homepage_url = QUrl(self.homepage_path)

        self.setStyleSheet("""
            QPushButton,
            QTabBar::tab{
                color: #fff;
            }
        
            QPushButton {
                background-color: transparent;
                border: none;
            }
            
            QTabWidget::pane {  
                border: none;
            }

            QPushButton:hover,
            QTabBar::tab,
            QTabBar{
                background-color: #363b3f;
            }

            QTabBar::tab:selected {
                background-color: #22282a;
            }
            
            QTabBar::close-button {
                image: url(assets/icons/close.svg);
                padding: 3px;
                margin-bottom: 1px;
           }
            
            QTabBar QToolButton,
            QTabBar QToolButton:selected {
                background-color: transparent;
                color: #fff;
            }
        """)

        self.setFont(QFont("Poppins", 10))

        self.add_tab_button = QPushButton("+", clicked=self.open_tab)
        self.add_tab_button.setFixedSize(QSize(25, 24))
        self.add_tab_button.setFont(QFont("Poppins", 12))

        self.add_tab_button.setParent(self)

        self.tabBarClicked.connect(self.select_tab)
        self.tabCloseRequested.connect(self.close_tab)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setDocumentMode(True)

        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)

    def change_url(self):
        url = self.currentWidget().url().toString()
        self.parent.tool_bar.url_edit.setText("" if url == self.homepage_path else url)

    def change_title(self, tab, title):
        self.setTabText(self.indexOf(tab), title)
        self.move_add_tab_button()

    def change_icon(self, tab, icon):
        self.setTabIcon(self.indexOf(tab), icon)
        self.move_add_tab_button()

    def resizeEvent(self, event):
        self.move_add_tab_button()

    def move_add_tab_button(self):
        tap_bar = self.tabBar()
        tap_bar.setFixedWidth(0)

        tabs_width = 0

        for i in range(tap_bar.count()):
            tabs_width += tap_bar.tabRect(i).width()

        tap_bar.setFixedWidth(tabs_width)

        tab_bar_width = tap_bar.width()

        self.add_tab_button.move(tab_bar_width, 0)

        width = self.width()
        button_width = self.add_tab_button.width()
        difference = width - button_width

        if self.add_tab_button.x() > difference:
            tap_bar.setFixedWidth(difference)
            self.add_tab_button.move(width - self.add_tab_button.width(), 0)

    def select_tab(self, index):
        self.setCurrentIndex(index)
        self.change_url()

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
            self.move_add_tab_button()
        else:
            self.parent.close()

    def open_tab(self):
        self.add_tab()
        self.move_add_tab_button()

    def add_tab(self, url=None):
        tab = QWebEngineView()

        if url:
            tab.setUrl(QUrl(url))
        else:
            tab.setHtml(self.homepage, self.homepage_url)

        tab.urlChanged.connect(self.change_url)
        tab.titleChanged.connect(lambda title: self.change_title(tab, title))
        tab.iconChanged.connect(lambda icon: self.change_icon(tab, icon))

        self.addTab(tab, "New Tab")
        self.setCurrentWidget(tab)

    def back(self):
        self.currentWidget().back()

    def forward(self):
        self.currentWidget().forward()

    def reload(self):
        self.currentWidget().reload()

    def navigate(self, url):
        if validators.url(url):
            normalized_url = url
        elif validators.domain(url):
            normalized_url = f"http://{url}"
        else:
            normalized_url = f"https://duckduckgo.com/?q={url}"

        self.currentWidget().setUrl(QUrl(normalized_url))
