import process_text
import json

def load_data():
    with open('quotes.json') as f:
        data = json.load(f)

    corpus = []
    for i in data:
        process_data = process_text.ProcessData(i['url'], i['content'])
        corpus.append(process_data)
    return corpus

def save_corpus_tokens(corpus):
    corpus_tokens = [d.tokens for d in corpus]
    flat_tokens = set([ token for tokens in corpus_tokens for token in tokens ])
    with open('corpus_tokens.txt', 'w') as f:
            f.write(' '.join(flat_tokens))
    return flat_tokens

def save_corpus_terms(corpus, flat_tokens):
    corpus_terms = [d.terms for d in corpus]
    terms = set([ term for terms in corpus_terms for term in terms ])
    with open('corpus_terms.txt', 'w') as f:
            f.write(' '.join(terms))
    return terms

def save_corpus_stems(corpus, flat_tokens):
    corpus_stems = [d.stems for d in corpus]
    stems = set([ stem for stems in corpus_stems for stem in stems ])
    with open('corpus_stems.txt', 'w') as f:
            f.write(' '.join(stems))
    return stems



def main():
    corpus = load_data()
    tokens = save_corpus_tokens(corpus)
    terms = save_corpus_terms(corpus, tokens)
    stems = save_corpus_stems(corpus, tokens)
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")



