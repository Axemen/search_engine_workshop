import re
from collections import Counter
from heapq import nlargest
from math import log, sqrt
from typing import Iterable, List

""" 
self.index:
{
    term -> {
        document_id -> term's frequency for that document
    }
}

self.documents:
{
    document_id -> {
        name -> name of the document
        normalizaiton_factor -> The L2 normalization factor for this document
    }
}
"""


class Search:
    def __init__(self) -> None:
        self.index = {}
        self.documents = {}

    def index_document(self, text: str, name: str):
        """ Takes in text and adds indexs in """
        tokens = self.tokenize(text)
        term_frequencies = Counter(tokens)  # Calculate term frequencies
        doc_id = len(self.documents)  # Get document id as newest document

        for term in term_frequencies:
            if term not in self.index:
                self.index[term] = {}
            self.index[term][doc_id] = term_frequencies[term]

        self.documents[doc_id] = {
            "name": name,
            "mag": self.magnitude(term_frequencies.values())
        }

    def search(self, query: str, n=10):
        """ Search the index for the given query and return the top n results """
        query_terms = self.tokenize(query)
        scores = self.calc_cosine_scores(query_terms)

        # return the top N document
        results = nlargest(n, scores.items(), key=lambda x: x[1])
        for i, (doc_id, score) in enumerate(results):
            print(i, self.documents[doc_id], score)

    def calc_cosine_scores(self, query_terms): # Ranking function
        N = len(self.documents)  # Number of document in the corpus
        scores = Counter()

        for term in query_terms:
            df = len(self.index[term])  # document frequency for the term
            idf = log(N/df)  # inverse document frequency for the term

            # tf is the document term frequency
            for doc_id, tf in self.index[term].items():
                scores[doc_id] += (tf * idf)

        # Normalize the score using the normalization factor calculated when a document is indexed
        for doc_id, score in scores.items():
            scores[doc_id] = score / self.documents[doc_id]['mag']

        return scores

    @staticmethod
    def tokenize(text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    @staticmethod
    def magnitude(vec: Iterable) -> float:
        return sqrt(sum([x**2 for x in vec]))


if __name__ == "__main__":
    from pathlib import Path

    from tqdm import tqdm

    s = Search()
    files: List[Path] = list(Path(r"E:\data\opinions").glob("*"))[:100]

    for file in tqdm(files):
        s.index_document(file.read_text(encoding='utf-8'), f"{str(file)}")

    s.search("written contract")
