import requests
from bs4 import BeautifulSoup
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer


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
        text = ' '.join(text.split()[:10000])
        
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