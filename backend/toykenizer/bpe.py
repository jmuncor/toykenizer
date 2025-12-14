# Imports
from os import replace
import sys

# Constants
PATH_TO_FILE = "text.txt"


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
    new_token = max(tokens + [255]) + 1
    new_tokens = []

    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == pair_to_replace:
            new_tokens.append(new_token)
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1

    return new_tokens


# Main function
def main():
    tokens = get_tokens(PATH_TO_FILE)
    common_pair = most_common_pair(tokens)
    print(mint_token(tokens, common_pair))
    return 1


if __name__ == "__main__":
    sys.exit(main())
