

class ReferenceAnalyzer:

    def generate_ngrams_for_variation_reference(self, reference):
        ngram_size = 3
        reference_words = reference.split()

        possible_ngrams = ['']
        for i in range(len(reference_words)):
            for j in range(i, i + 1 + ngram_size):
                ngram = " ".join(reference_words[i:j])
                if ngram not in possible_ngrams:
                    possible_ngrams.append(ngram)

        return possible_ngrams
