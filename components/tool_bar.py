from PyQt6.QtWidgets import QToolBar, QLabel, QLineEdit
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QFont


class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setMovable(False)

        self.setStyleSheet("""       
            QToolBar {
                border: none;
                background-color: #22282a;
                padding: 3px;
            }

            QToolButton {
                color: #fff;
                width: 21px;
                height: 21px;
            }

            QLabel,
            QLineEdit,
            QToolButton:hover{
                background-color: #363b3f;
            }

            QLabel {
                padding-left: 5px;
                padding-right: 5px;
                margin-top: 1px;
                margin-left: 5px;
                margin-bottom: 1px;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
            }

            QLineEdit {
                padding-top: 2px;
                padding-right: 10px;
                padding-bottom: 2px;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                color: #fff;
            }
        """)

        self.setIconSize(QSize(14, 14))

        button_back = self.addAction("Back")
        button_back.setIcon(QIcon("assets/icons/arrow-left.svg"))
        button_back.setToolTip("Back")
        button_back.triggered.connect(self.parent.main.back)

        button_forward = self.addAction("Forward")
        button_forward.setIcon(QIcon("assets/icons/arrow-right.svg"))
        button_forward.setToolTip("Forward")
        button_forward.triggered.connect(self.parent.main.forward)

        button_refresh = self.addAction("Refresh")
        button_refresh.setIcon(QIcon("assets/icons/refresh.svg"))
        button_refresh.setToolTip("Refresh")
        button_refresh.triggered.connect(self.parent.main.reload)

        label = QLabel()
        label.setPixmap(QIcon("assets/icons/search.svg").pixmap(QSize(12, 12)))
        self.addWidget(label)

        self.url_edit = QLineEdit()
        self.url_edit.returnPressed.connect(lambda: self.parent.main.navigate(self.url_edit.text()))
        self.url_edit.setPlaceholderText("Search or enter address")

        font = QFont("Poppins", 10)
        font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        # font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

        self.url_edit.setFont(font)
        self.addWidget(self.url_edit)
