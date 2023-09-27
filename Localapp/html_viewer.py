import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


def view_html_file(html_file):
    app = QApplication(sys.argv)

    class HTMLViewer(QMainWindow):
        def __init__(self, html_file):
            super().__init__()

            self.setWindowTitle("HTML Viewer")
            self.setGeometry(100, 100, 800, 600)

            central_widget = QWidget(self)
            self.setCentralWidget(central_widget)

            layout = QVBoxLayout(central_widget)

            self.web_view = QWebEngineView()
            layout.addWidget(self.web_view)

            self.load_html(html_file)

        def load_html(self, html_file):
            url = QUrl.fromLocalFile(html_file)
            self.web_view.setUrl(url)

    viewer = HTMLViewer(html_file)
    viewer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python html_viewer.py <path_to_html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    view_html_file(html_file)
