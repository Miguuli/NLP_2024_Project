import sys
import nltk_proj
from nltk_proj import summarize_text
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Example usage
document = """
Natural language processing is a subfield of artificial intelligence (AI) focused on the interaction between computers and humans through natural language. The ultimate objective of NLP is to enable computers to understand, interpret, and generate human languages in a way that is both valuable and meaningful. NLP is used to apply algorithms to identify and extract the natural language rules such that the unstructured language data is converted into a form that computers can understand.
"""


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SummarizerGUI")
        layout = QVBoxLayout()
        button = QPushButton("Summarize sample doc")
        #button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        button2 = QPushButton("Summarize text file")

        button3 = QPushButton("Summarize link content")

        line_edit = QLineEdit()
        line_edit.setMaxLength(10)
        line_edit.setPlaceholderText("Enter file name")
        line_edit.returnPressed.connect(self.return_pressed)
        line_edit.selectionChanged.connect(self.selection_changed)
        line_edit.textChanged.connect(self.text_changed)
        line_edit.textEdited.connect(self.text_edited)

        line_edit2 = QLineEdit()
        line_edit2.setMaxLength(100)
        line_edit2.setPlaceholderText("Enter link url")
        line_edit2.returnPressed.connect(self.return_pressed2)
        line_edit2.selectionChanged.connect(self.selection_changed2)
        line_edit2.textChanged.connect(self.text_changed2)
        line_edit2.textEdited.connect(self.text_edited2)

        layout.addWidget(button)
        layout.addWidget(line_edit)
        layout.addWidget(button2)
        layout.addWidget(line_edit2)
        layout.addWidget(button3)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    def the_button_was_clicked(self):
        summaries = summarize_text(document)
        for name, summary in summaries.items():
            print(f"\n{name} Summary:")
            print(summary)

    def return_pressed(self):
        print("Return pressed!")
        #self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)

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