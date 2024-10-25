import sys

from PySide6 import QtAsyncio
from PySide6.QtAsyncio import asyncio
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QScrollBar,
    QListView,
    QSplitter,
    QHBoxLayout
)
from nltk_proj import summarize_text, summarize_from_file, summarize_from_url

# Example usage
document = """
Natural language processing is a subfield of artificial intelligence (AI) focused on the interaction between computers and humans through natural language. The ultimate objective of NLP is to enable computers to understand, interpret, and generate human languages in a way that is both valuable and meaningful. NLP is used to apply algorithms to identify and extract the natural language rules such that the unstructured language data is converted into a form that computers can understand.
"""

items = []
# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_text = ""
        self.current_url_text = ""
        self.setWindowTitle("SummarizerGUI")
        self.model = QStringListModel(items)

        # Results display
        self.list = QListView()
        self.list.setModel(self.model)

        layout = QVBoxLayout()
        button = QPushButton("Summarize sample doc")
        button.clicked.connect(self.summarize_sample_doc_clicked)

        button2 = QPushButton("Summarize text file")
        button2.clicked.connect(self.summarize_file_doc_clicked)

        button3 = QPushButton("Summarize link content")
        button3.clicked.connect(lambda: asyncio.ensure_future(self.summarize_url_clicked()))

        line_edit = QLineEdit()
        line_edit.setMaxLength(100)
        line_edit.setPlaceholderText("Enter file name")
        line_edit.returnPressed.connect(self.file_text_return_pressed)
        #line_edit.selectionChanged.connect(self.file_text_selection_changed)
        line_edit.textChanged.connect(self.file_text_changed)
        line_edit.textEdited.connect(self.file_text_edited)

        line_edit2 = QLineEdit()
        line_edit2.setMaxLength(100)
        line_edit2.setPlaceholderText("Enter link url")
        line_edit2.returnPressed.connect(self.url_text_return_pressed)
        #line_edit2.selectionChanged.connect(self.url_text_selection_changed)
        line_edit2.textChanged.connect(self.url_text_changed)
        line_edit2.textEdited.connect(self.url_text_edited)

        self.scrollArea = QScrollArea()
        self.scrollBar = QScrollBar()
        self.scrollArea.setWidget(self.scrollBar)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.viewport().setUpdatesEnabled(True)
        self.scrollArea.setWidget(self.list)

        layout.addWidget(button)
        layout.addWidget(line_edit)
        layout.addWidget(button2)
        layout.addWidget(line_edit2)
        layout.addWidget(button3)
        layout.addWidget(self.scrollArea)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    def summarize_sample_doc_clicked(self):
        summaries = summarize_text(document)
        self.display_summaries(summaries)

    def summarize_file(self):
        file_path = self.file_input.text()
        if file_path:
            summaries = summarize_from_file(file_path)
            self.display_summaries(summaries)

    def summarize_url(self):
        url = self.url_input.text()
        if url:
            summaries = summarize_from_url(url)
            self.display_summaries(summaries)

    def display_summaries(self, summaries):
        items.clear()  # Clear previous items
        for name, summary in summaries.items():
            print(f"\n{name} Summary:")
            print(summary)
            items.append(f"{name}:\n{summary}")
        self.model.setStringList(items)
        self.list.scrollToBottom()

    def summarize_file_doc_clicked(self):
        summaries = summarize_from_file(self.current_file_text, 3)
        for name, summary in summaries.items():
            print(f"\n{name} Summary:")
            print(summary)
            items.append(name + ":\n" + summary)
        self.model.setStringList(items)
        self.list.scrollToBottom()
        
    

    async def summarize_url_clicked(self):
        await asyncio.sleep(1)
        summaries = summarize_from_url(self.current_url_text, 3)
        for name, summary in summaries.items():
            print(f"\n{name} Summary:")
            print(summary)
            items.append(name + ":\n" + summary)
        self.model.setStringList(items)
        self.list.scrollToBottom()

    def file_text_return_pressed(self):
        pass

    def file_text_changed(self, s):
        self.current_file_text = s

    def file_text_edited(self, s):
        pass

    def url_text_return_pressed(self):
        pass

    def url_text_changed(self, s):
        self.current_url_text = s

    def url_text_edited(self, s):
        pass

app = QApplication(sys.argv)

window = MainWindow()
window.show()
QtAsyncio.run(handle_sigint=True)

app.exec()
