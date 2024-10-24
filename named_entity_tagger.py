import spacy
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
nlp = spacy.load('en_core_web_sm')

#An algorithm that naively adds all sentences that contain named entities to the summary
def named_entity_summarization(text, num_sentences=3): 
    
    #Finding the named entities using Spacy and tokenizing the text into sentences
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    doc = nlp(text)
    named_entities = []
    for ent in doc.ents:
        named_entities.append(ent.text)
    sentences = [sent.text for sent in doc.sents]

    #Summarizing the text using LSA
    summarization = LsaSummarizer()(parser.document, num_sentences)
    summarization = "\n".join(str(sentence) for sentence in summarization)

    #Filtering the sentences to only include those that contain named entities
    if any(entity in sentence for entity in named_entities) and sentence not in summarization:
            summarization += sentence
            summarization += " "
    return summarization

#We propose using TextRank scores for the sentences to filter only to include sentences that have a TextRank score above a certain threshold.
def named_entity_summarization_filtered(text, num_sentences=3, threshold=0.1): 
    
    #Finding the named entities using Spacy and tokenizing the text into sentences
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    doc = nlp(text)
    named_entities = []
    for ent in doc.ents:
        named_entities.append(ent.text)
    sentences = [sent.text for sent in doc.sents]

    #Summarizing the text using LSA
    summarization = LsaSummarizer()(parser.document, num_sentences)
    textRank = TextRankSummarizer().rate_sentences(parser.document)
    sentence_scores = {str(sentence): textRank[sentence] for sentence in textRank}
    summarization = "\n".join(str(sentence) for sentence in summarization)

    #Filtering the sentences to only include those that contain named entities and have a TextRank score above the threshold
    for sentence in sentences:
        if any(entity in sentence for entity in named_entities) and sentence not in summarization and sentence_scores[sentence] > threshold:
            summarization += sentence
            summarization += " "
    return summarization
