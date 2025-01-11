import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import mistune

class MarkdownViewer(QMainWindow):
    def __init__(self, markdown_text):
        super().__init__()

        self.setWindowTitle("Markdown Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a QWebEngineView to display the rendered Markdown
        self.web_view = QWebEngineView()

        # Parse Markdown to HTML using mistune's create_markdown function
        # which returns a function that accepts Markdown text and returns HTML
        md = mistune.create_markdown()  # Default configuration includes table rendering
        html_text = md(markdown_text)

        # Set the HTML content to QWebEngineView
        self.web_view.setHtml(html_text)

        # Add QWebEngineView to layout
        layout.addWidget(self.web_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Sample Markdown text with a table
    markdown_text = """
    # Sample Table

    | Header1 | Header2 | Header3 |
    | --- | --- | --- |
    | Row1Col1 | Row1Col2 | Row1Col3 |
    | Row2Col1 | Row2Col2 | Row2Col3 |
    | Row3Col1 | Row3Col2 | Row3Col3 |
    """

    viewer = MarkdownViewer(markdown_text)
    viewer.show()

    sys.exit(app.exec_())