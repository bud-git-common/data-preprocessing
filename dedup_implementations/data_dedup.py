import string
from nltk import ngrams
from datasketch import MinHash

def clean_text(file_path, output_path):
    # Read the text file with 'latin-1' encoding
    with open(file_path, 'r', encoding='latin-1') as file:
        text = file.read()

    # Remove punctuation and special characters
    cleaned_text = ''.join(char for char in text if char not in string.punctuation)

    # Write the cleaned text to a new file
    with open(output_path, 'w', encoding='latin-1') as file:
        file.write(cleaned_text)

    print("Text cleaned and saved successfully.")




def apply_minhash(input_file, n):
    # Read the cleaned text file
    with open(input_file, 'r', encoding='latin-1') as file:
        text = file.read()

    # Tokenize the text into n-grams
    tokens = text.split()
    ngram_tokens = list(ngrams(tokens, n))

    # Apply MinHash to the n-grams
    minhashes = []
    for ngram in ngram_tokens:
        minhash = MinHash()
        for word in ngram:
            minhash.update(word.encode('latin-1'))
        minhashes.append(minhash)

    # Save the hashed n-grams
    output_file = input_file.replace('.txt', f'_minhash_{n}.txt')
    with open(output_file, 'w', encoding='latin-1') as file:
        for minhash in minhashes:
            file.write(str(minhash) + '\n')

    print(f"MinHash hashed n-grams saved to {output_file}.")

# Example usage
input_file = '../data.json'
output_file = '../output_file.txt'
n = 3  # Change this to the desired n-gram size
clean_text(input_file, output_file)
apply_minhash(input_file, n)



