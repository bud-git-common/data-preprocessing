import json
import string
from nltk import ngrams
from datasketch import MinHashLSH, MinHash

def concatenate_texts(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        texts = [entry['text'] for entry in data]
        concatenated_text = ' text '.join(texts)
        return texts, concatenated_text

def generate_ngrams(text, n):
    tokens = text.split()
    ngram_list = list(ngrams(tokens, n))
    return ngram_list

def apply_minhash(ngram_list, num_perm):
    minhash_list = []
    for ngram in ngram_list:
        minhash = MinHash(num_perm=num_perm)
        for word in ngram:
            minhash.update(word.encode('utf8'))
        minhash_list.append(minhash)
    return minhash_list

def group_texts(minhash_list, texts, threshold):
    lsh = MinHashLSH(threshold=threshold, num_perm=len(minhash_list[0].hashvalues))
    for i, minhash in enumerate(minhash_list):
        lsh.insert(i, minhash)

    grouped_texts = []
    grouped_indices = set()
    for minhash in minhash_list:
        neighbors = lsh.query(minhash)
        group_indices = [idx for idx in neighbors if idx < len(texts)]
        if group_indices and set(group_indices) not in grouped_indices:
            grouped_text = [texts[idx] for idx in group_indices]
            grouped_texts.append(grouped_text)
            grouped_indices.add(frozenset(group_indices))
    return grouped_texts

def remove_similar_texts(grouped_texts, threshold, num_perm):
    cleaned_groups = []
    unique_sentences = set()
    for group in grouped_texts:
        unique_group = []
        for text in group:
            minhash = MinHash(num_perm=num_perm)
            for word in text.split():
                minhash.update(word.encode('utf8'))
            unique = True
            for sentence in unique_sentences:
                other_minhash = MinHash(num_perm=num_perm)
                for word in sentence.split():
                    other_minhash.update(word.encode('utf8'))
                similarity = minhash.jaccard(other_minhash)
                if similarity >= threshold:
                    unique = False
                    break
            if unique:
                unique_sentences.add(text)
                unique_group.append(text)
        if unique_group:
            cleaned_groups.append(unique_group)
    return cleaned_groups

# Example usage
json_file_path = '../data.json'  # Replace with the actual path to your JSON file

# Concatenate texts
texts, concatenated_text = concatenate_texts(json_file_path)

# Remove punctuations
translator = str.maketrans('', '', string.punctuation)
cleaned_text = concatenated_text.translate(translator)

# Generate n-grams
n = 3  # Specify the desired value of n for n-grams
ngram_list = generate_ngrams(cleaned_text, n)

# Apply MinHash
num_perm = 128  # Number of permutations for MinHash
minhash_list = apply_minhash(ngram_list, num_perm)

# Apply MinHash LSH and group similar texts
threshold = 0.8  # Specify the Jaccard similarity threshold for LSH
grouped_texts = group_texts(minhash_list, texts, threshold)

# Remove similar texts within groups and save only the first occurrence
cleaned_groups = remove_similar_texts(grouped_texts, threshold, num_perm)

# Save cleaned groups as a JSON file
output_file_path = '../cleaned_groups.json'  # Specify the output file path
with open(output_file_path, 'w') as output_file:
    json.dump(cleaned_groups, output_file, indent=4)

print("Cleaned groups saved as JSON:", output_file_path)
