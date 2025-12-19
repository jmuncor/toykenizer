# Imports
import sys

# Constants
PATH_TO_FILE = "text.txt"
VOCAB_SIZE = 276


# Read file and encode text into the UTF-8 bytes
def get_tokens(path: str):
    file = open(path, "r")
    content = file.read()
    tokens = content.encode("utf-8")
    return list(map(int, tokens))


# Find the most common pair out of a list of utf-8 character ids
def most_common_pair(tokens: list[int]):
    freq_counts = {}
    for pair in zip(tokens, tokens[1:]):
        if pair in freq_counts:
            freq_counts[pair] += 1
        else:
            freq_counts[pair] = 1
    freq_counts = dict(
        sorted(freq_counts.items(), key=lambda item: item[1], reverse=True)
    )
    return next(iter(freq_counts))


# Mint the new token based on the most common pair
def mint_token(tokens: list[int], pair_to_replace: tuple[int, int]):
    minted_token = max(tokens + [255]) + 1
    new_tokens = []

    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == pair_to_replace:
            new_tokens.append(minted_token)
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1

    return new_tokens, minted_token


#  Create the tokenizer and build it to a specific vocab_size
def create(path: str = PATH_TO_FILE, vocab_size: int = VOCAB_SIZE):
    if VOCAB_SIZE < 256:
        raise ValueError(
            "The desired vocab sixe cannot be smaller than the base byte vocab"
        )

    tokens = get_tokens(path)
    new_tokens = list(tokens)

    merges = {}
    for _ in range(vocab_size - 256):
        common_pair = most_common_pair(new_tokens)
        new_tokens, minted_token = mint_token(new_tokens, common_pair)
        merges[common_pair] = minted_token

    return merges


# Function to generate the full vocab using a dictionary of the new tokens
def build_vocabulary(merges: dict[tuple[int, int], int]) -> dict[int, bytes]:
    vocab = {}
    for i in range(256):
        vocab[i] = bytes([i])

    for (t0, t1), i in merges.items():
        vocab[i] = vocab[t0] + vocab[t1]

    return vocab


# Decode function using a vocabulary dict and a list of tokens
def decode(tokens: list[int], vocab: dict[int, bytes]) -> str:
    response = []
    for i in tokens:
        response.append(vocab[i])

    response = b"".join(response)
    response = response.decode("utf-8", errors="replace")

    return response


# Encode
def encode(text: str, merges: dict[tuple[int, int], int]) -> list[int]:
    tokens = text.encode("utf-8")
    tokens = list(map(int, tokens))
    sorted_merges = sorted(merges.items(), key=lambda item: item[1])

    for pair, id in sorted_merges:
        new_tokens = []
        j = 0
        while j < len(tokens):
            if j + 1 < len(tokens) and (tokens[j], tokens[j + 1]) == pair:
                new_tokens.append(id)
                j += 2
            else:
                new_tokens.append(tokens[j])
                j += 1
        tokens = new_tokens

    return tokens


def main():
    minted_tokens = create(PATH_TO_FILE, VOCAB_SIZE)
    print(build_vocabulary(minted_tokens))

    return 1


if __name__ == "__main__":
    sys.exit(main())
