# Imports
import sys


class BPETokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {}

    def _most_common_pair(self, tokens: list[int]):
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

    def _mint_token(self, tokens: list[int], pair_to_replace: tuple[int, int]):
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

    def _build_vocabulary(self) -> dict[int, bytes]:
        vocab = {}
        for i in range(256):
            vocab[i] = bytes([i])

        for (t0, t1), i in self.merges.items():
            vocab[i] = vocab[t0] + vocab[t1]

        return vocab

    def train(self, text: str, vocab_size: int):
        if vocab_size < 256:
            raise ValueError(
                "The desired vocab sixe cannot be smaller than the base byte vocab"
            )

        tokens = list(map(int, text.encode("utf-8")))
        new_tokens = list(tokens)

        merges = {}
        for _ in range(vocab_size - 256):
            if len(new_tokens) < 2:
                break
            try:
                common_pair = self._most_common_pair(new_tokens)
            except StopIteration:
                break

            new_tokens, minted_token = self._mint_token(new_tokens, common_pair)
            merges[common_pair] = minted_token

        self.merges = merges
        self.vocab = self._build_vocabulary()

    def decode(self, tokens: list[int]) -> str:
        # Note: This method uses self.vocab, which is built during training.
        response = []
        for i in tokens:
            response.append(self.vocab[i])

        response = b"".join(response)
        response = response.decode("utf-8", errors="replace")

        return response

    def encode(self, text: str) -> list[int]:
        # Note: This method uses self.merges, which is built during training.
        tokens = text.encode("utf-8")
        tokens = list(map(int, tokens))
        sorted_merges = sorted(self.merges.items(), key=lambda item: item[1])

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

    def save(self):
        merges = {}
        for pair, id in self.merges.items():
            key = f"{pair[0]},{pair[1]}"
            merges[key] = id
        return merges

    def load(self, loaded_merges: dict):
        merges = {}
        for pair, id in loaded_merges.items():
            key = tuple(map(int, pair.split(",")))
            merges[key] = id

        self.merges = merges
        self.vocab = self._build_vocabulary()


def main():
    return 0


if __name__ == "__main__":
    sys.exit(main())

