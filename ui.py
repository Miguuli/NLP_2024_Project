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
from nltk_proj import (
    summarize_text, summarize_from_file, summarize_from_url, evaluate_summarizers,
)
# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the dataset
        #evaluate_summarizers()
        self.items = []
        self.document = """
            Natural language processing is a subfield of artificial intelligence (AI) focused on the interaction between computers and humans through natural language. The ultimate objective of NLP is to enable computers to understand, interpret, and generate human languages in a way that is both valuable and meaningful. NLP is used to apply algorithms to identify and extract the natural language rules such that the unstructured language data is converted into a form that computers can understand.
        """

        self.current_file_text = ""
        self.current_url_text = ""
        self.setWindowTitle("SummarizerGUI")
        self.model = QStringListModel(self.items)

        # Buttons
        summ_sample_doc_button = QPushButton("Summarize sample doc")
        summ_sample_doc_button.clicked.connect(self.summarize_sample_doc_clicked)

        summ_file_doc_button = QPushButton("Summarize text file")
        summ_file_doc_button.clicked.connect(self.summarize_file_doc_clicked)

        summ_link_content_button = QPushButton("Summarize link content")
        summ_link_content_button.clicked.connect(lambda: asyncio.ensure_future(self.summarize_url_clicked()))

        # Text boxes
        file_input_text_box = QLineEdit()
        file_input_text_box.setMaxLength(100)
        file_input_text_box.setPlaceholderText("Enter file name")
        file_input_text_box.returnPressed.connect(self.file_text_return_pressed)
        #file_input_text_box.selectionChanged.connect(self.file_text_selection_changed)
        file_input_text_box.textChanged.connect(self.file_text_changed)
        file_input_text_box.textEdited.connect(self.file_text_edited)

        url_input_text_box = QLineEdit()
        url_input_text_box.setMaxLength(100)
        url_input_text_box.setPlaceholderText("Enter link url")
        url_input_text_box.returnPressed.connect(self.url_text_return_pressed)
        #url_input_text_box.selectionChanged.connect(self.url_text_selection_changed)
        url_input_text_box.textChanged.connect(self.url_text_changed)
        url_input_text_box.textEdited.connect(self.url_text_edited)

        # Results content loaded to list view from model
        self.list = QListView()
        self.list.setModel(self.model)
        # Results display
        self.scrollArea = QScrollArea()
        self.scrollBar = QScrollBar()
        self.scrollArea.setWidget(self.scrollBar)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.viewport().setUpdatesEnabled(True)
        self.scrollArea.setWidget(self.list)

        # Create main layout
        layout = QVBoxLayout()
        # Add all ui components to main layout
        layout.addWidget(summ_sample_doc_button)
        layout.addWidget(file_input_text_box)
        layout.addWidget(summ_file_doc_button)
        layout.addWidget(url_input_text_box)
        layout.addWidget(summ_link_content_button)
        layout.addWidget(self.scrollArea)

        # Add main layout to main widget
        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    def display_summaries(self, summaries):
        self.items.clear()  # Clear previous items
        for name, summary in summaries.items():
            self.items.append(f"{name}:\n{summary}")
        self.model.setStringList(self.items)
        self.list.scrollToBottom()

    def summarize_sample_doc_clicked(self):
        summaries = summarize_text(self.document)
        self.display_summaries(summaries)

    def summarize_file_doc_clicked(self):
        file_path = self.current_file_text
        if file_path:
            summaries = summarize_from_file(self.current_file_text, 3)
            self.display_summaries(summaries)

    async def summarize_url_clicked(self):
        await asyncio.sleep(1)
        summaries = summarize_from_url(self.current_url_text, 3)
        self.display_summaries(summaries)

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

# Print results
#for name, scores in results.items():
    #print(f"{name} Summarizer:")
    #print(f"  ROUGE-1: {scores['ROUGE-1']:.4f}")
    #print(f"  ROUGE-2: {scores['ROUGE-2']:.4f}")
    #print(f"  ROUGE-L: {scores['ROUGE-L']:.4f}")
    #print()

# Analysis and comments
#print("Analysis:")
#print("1. Performance Comparison:")
#best_rouge1 = max(results, key=lambda x: results[x]['ROUGE-1'])
#best_rouge2 = max(results, key=lambda x: results[x]['ROUGE-2'])
#best_rougel = max(results, key=lambda x: results[x]['ROUGE-L'])
#print(f"   - Best ROUGE-1 performance: {best_rouge1}")
#print(f"   - Best ROUGE-2 performance: {best_rouge2}")
#print(f"   - Best ROUGE-L performance: {best_rougel}")