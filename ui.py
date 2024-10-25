import sys

from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import (
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
        self.setWindowTitle("SummarizerGUI")
        self.model = QStringListModel(items)

        # Create main layout
        main_layout = QVBoxLayout()

        # Sample document section
        sample_button = QPushButton("Summarize sample doc")
        sample_button.clicked.connect(self.the_button_was_clicked)
        main_layout.addWidget(sample_button)

        # File summarization section
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Enter file name")
        file_button = QPushButton("Summarize text file")
        file_button.clicked.connect(self.summarize_file)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)
        main_layout.addLayout(file_layout)

        # URL summarization section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter link url")
        url_button = QPushButton("Summarize link content")
        url_button.clicked.connect(self.summarize_url)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(url_button)
        main_layout.addLayout(url_layout)

        # Results display
        self.list = QListView()
        self.list.setModel(self.model)
        main_layout.addWidget(self.list)

        # Set up central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def the_button_was_clicked(self):
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

    def return_pressed(self):
        print("Return pressed!")
        summaries = summarize_from_file(self.current_file_text, 3)
        for name, summary in summaries.items():
            print(f"\n{name} Summary:")
            print(summary)
            items.append(name + ":\n" + summary)
        self.model.setStringList(items)
        self.list.scrollToBottom()
        
    

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)
        self.current_file_text = s

    def return_pressed2(self):
        print("Return pressed!")
        #self.centralWidget().setText("BOOM!")

    def selection_changed2(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed2(self, s):
        print("Text changed...")
        print(s)

    def text_edited2(self, s):
        print("Text edited...")
        print(s)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()