from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tarfile
import io
import json
from rouge import Rouge
import numpy as np
import spacy
import nltk


nltk.download('punkt', quiet=True)

def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    summarizers = {
        "Edmundson": EdmundsonSummarizer(),
        "LSA": LsaSummarizer(),
        "KL": KLSummarizer(),
        "LexRank": LexRankSummarizer()
    }
    
    results = {}
    
    for name, summarizer in summarizers.items():
        if name == "Edmundson":
            summarizer.bonus_words = ["NLP", "language", "algorithms", "AI", "natural"]
            summarizer.stigma_words = ["is", "the", "a", "of", "and", "to", "in"]
            summarizer.null_words = ["and", "or", "but", "if", "then", "with", "so", "on"]
        
        summary = summarizer(parser.document, num_sentences)
        results[name] = "\n".join(str(sentence) for sentence in summary)
    
    return results

def summarize_from_url(url, num_sentences=3):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        # Limit the text to the first 1000 words for faster processing
        text = ' '.join(text.split()[:1000])
        
        return summarize_text(text, num_sentences)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {"Error": f"Failed to fetch URL: {str(e)}"}
    except Exception as e:
        print(f"Error summarizing URL: {e}")
        return {"Error": f"Failed to summarize URL: {str(e)}"}
    
# Function to summarize from a file
def summarize_from_file(file_path, num_sentences=3):
    with open(file_path, 'r') as file:
        text = file.read()
    return summarize_text(text, num_sentences)



# Example usage
#document = """
#Natural language processing is a subfield of artificial intelligence (AI) focused on the interaction between computers and humans through natural language. The ultimate objective of NLP is to enable computers to understand, interpret, and generate human languages in a way that is both valuable and meaningful. NLP is used to apply algorithms to identify and extract the natural language rules such that the unstructured language data is converted into a form that computers can understand.
#"""

#summaries = summarize_text(document)

#for name, summary in summaries.items():
    #print(f"\n{name} Summary:")
    #print(summary)

# Example usage for file and URL
#file_path = "/home/t/Desktop/koulu/nltk/proj/test.in"
#file_summaries = summarize_from_file(file_path)

#url = "https://en.wikipedia.org/wiki/Natural_language_processing"
#url_summaries = summarize_from_url(url)

#print("\nFile Summaries:")
#for name, summary in file_summaries.items():
    #print(f"\n{name} Summary:")
    #print(summary)

#print("\nURL Summaries:")
#for name, summary in url_summaries.items():
    #print(f"\n{name} Summary:")
    #print(summary)

# Initialize ROUGE
rouge = Rouge()

# Initialize summarizers
edmundson = EdmundsonSummarizer()
edmundson.bonus_words = ["important", "significant", "key", "central", "crucial"]
edmundson.stigma_words = ["trivial", "minor", "unimportant", "insignificant"]
edmundson.null_words = ["the", "a", "an", "in", "on", "at", "for", "of", "with"]

summarizers = {
    "Edmundson": edmundson,
    "LSA": LsaSummarizer(),
    "KL": KLSummarizer(),
    "LexRank": LexRankSummarizer()
}

def generate_summary(text, summarizer, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

def evaluate_summarizer(summarizer, data):
    rouge_1_scores = []
    rouge_2_scores = []
    rouge_l_scores = []
    
    for _, row in data.iterrows():
        full_text = row['summary']
        reference_summary = row['title'] + ". " + " ".join(full_text.split()[:30])  # Use title and first 30 words as reference
        generated_summary = generate_summary(full_text, summarizer)
        
        scores = rouge.get_scores(generated_summary, reference_summary)[0]
        rouge_1_scores.append(scores['rouge-1']['f'])
        rouge_2_scores.append(scores['rouge-2']['f'])
        rouge_l_scores.append(scores['rouge-l']['f'])
    
    return np.mean(rouge_1_scores), np.mean(rouge_2_scores), np.mean(rouge_l_scores)

# Load the Wikipedia Summary Dataset
def load_wiki_summary_data(file_path, num_samples=10000):
    with tarfile.open(file_path, "r:gz") as tar:
        txt_file = [f for f in tar.getmembers() if f.name.endswith('.txt')][0]
        with tar.extractfile(txt_file) as f:
            content = io.TextIOWrapper(f, encoding='utf-8')
            data = []
            for i, line in enumerate(content):
                if i >= num_samples:
                    break
                title, summary = line.strip().split('|||')
                data.append({'title': title.strip(), 'summary': summary.strip()})
    return pd.DataFrame(data)

# Load the dataset
#data = load_wiki_summary_data('raw.tar.gz', num_samples=10000)
#print(f"Loaded {len(data)} samples from the dataset.")

# Evaluate each summarizer
#results = {}
#for name, summarizer in summarizers.items():
    #print(f"Evaluating {name} summarizer...")
    #rouge_1, rouge_2, rouge_l = evaluate_summarizer(summarizer, data)
    #results[name] = {'ROUGE-1': rouge_1, 'ROUGE-2': rouge_2, 'ROUGE-L': rouge_l}

# Print results
#for name, scores in results.items():
    print(f"{name} Summarizer:")
    print(f"  ROUGE-1: {scores['ROUGE-1']:.4f}")
    print(f"  ROUGE-2: {scores['ROUGE-2']:.4f}")
    print(f"  ROUGE-L: {scores['ROUGE-L']:.4f}")
    print()

# Analysis and comments
#print("Analysis:")
#print("1. Performance Comparison:")
#best_rouge1 = max(results, key=lambda x: results[x]['ROUGE-1'])
#best_rouge2 = max(results, key=lambda x: results[x]['ROUGE-2'])
#best_rougel = max(results, key=lambda x: results[x]['ROUGE-L'])
#print(f"   - Best ROUGE-1 performance: {best_rouge1}")
#print(f"   - Best ROUGE-2 performance: {best_rouge2}")
#print(f"   - Best ROUGE-L performance: {best_rougel}")

