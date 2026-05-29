class SimpleVocab:
    def __init__(self, token_counts, specials=None):
        specials = list(specials or [])
        tokens = specials + [token for token in token_counts.keys() if token not in specials]
        self.itos = list(tokens)
        self.stoi = {token: index for index, token in enumerate(self.itos)}
        self.default_index = None

    def __len__(self):
        return len(self.itos)

    def __getitem__(self, token):
        if self.default_index is None:
            return self.stoi[token]
        return self.stoi.get(token, self.default_index)

    def __call__(self, tokens):
        return self.lookup_indices(tokens)

    def set_default_index(self, index):
        self.default_index = index

    def lookup_indices(self, tokens):
        return [self[token] for token in tokens]

    def lookup_token(self, index):
        return self.itos[int(index)]

    def lookup_tokens(self, indices):
        return [self.lookup_token(index) for index in indices]

    def get_itos(self):
        return list(self.itos)

    def get_stoi(self):
        return dict(self.stoi)
