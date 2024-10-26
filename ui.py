import sys
import named_entity_tagger
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
from named_entity_tagger import named_entity_summarization, named_entity_summarization_filtered
# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the dataset
        #evaluate_summarizers()
        self.items = []
        self.document = """
            Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans using natural language. The goal is to enable machines to understand, interpret, and generate human language in a way that is meaningful and useful. NLP combines computational linguistics, rule-based modeling of human language, and machine learning to build models that can process large amounts of natural language data. The primary tasks in NLP range from basic text preprocessing to more complex tasks like language generation and understanding. Text preprocessing involves cleaning and preparing the text for analysis, breaking it into manageable units through tokenization, stemming, lemmatization, stopword removal, and part-of-speech tagging. Once text is preprocessed, syntactic and semantic analysis techniques help machines understand the structure and meaning of sentences, including parsing, dependency parsing, named entity recognition, and word sense disambiguation. Language modeling plays a key role in predicting the next word or phrase in a sentence based on the previous words, and this underpins many NLP applications like text generation, speech recognition, and machine translation. Sentiment analysis identifies the sentiment expressed in a text and is widely used in social media monitoring and customer feedback systems. Automatic text summarization reduces large pieces of text to shorter versions while retaining key information, which can be done through extractive summarization (selecting important sentences or phrases) or abstractive summarization (generating a summary in its own words). Question answering systems are designed to answer human questions based on contextual understanding of text, and they are seen in applications such as search engines and virtual assistants. NLP techniques and models have evolved significantly with the rise of deep learning. Bag of Words is a basic technique for converting text into numerical data, while TF-IDF builds on this by weighting words based on their importance in the text corpus. Word embeddings like Word2Vec, GloVe, and FastText create dense vector representations of words that capture semantic relationships between them. However, the real revolution in NLP came with the introduction of Transformer models. Transformers, like BERT and GPT, are neural networks that excel at understanding complex language patterns and are used in tasks such as text generation, sentiment analysis, and machine translation. Recurrent neural networks (RNNs) and Long Short-Term Memory (LSTM) models were previously dominant for sequence-based NLP tasks but have been largely replaced by Transformer architectures due to their superior ability to capture long-range dependencies in text. NLP is used in a wide variety of applications, from search engines and chatbots to healthcare, legal document analysis, and financial services. Despite these advances, NLP faces challenges such as the inherent ambiguity of human language, the diversity of languages and dialects, and the need for better understanding of context in conversations. Ethical concerns also arise, as NLP systems may perpetuate biases present in the training data. Nevertheless, NLP is transforming industries by enabling machines to interact with humans in more intuitive and effective ways.
        """
        summ = named_entity_summarization(self.document)
        print(summ)
        #summ_filtered = named_entity_summarization_filtered(self.document)
        #print(summ_filtered)
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