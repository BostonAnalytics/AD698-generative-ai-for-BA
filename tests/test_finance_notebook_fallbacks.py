"""Execute the notebook's fallback cells without downloading or training."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch


ROOT = Path(__file__).resolve().parents[1] / "help-code/4-nlp-finance"


def code_cells(name):
    notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


class EmbeddingFallbackTests(unittest.TestCase):
    def setUp(self):
        cells = code_cells("S9.4 - RNN Sentiment Analysis.ipynb")
        self.lookup = next(c for c in cells if c.startswith("pretrained_embedding = None"))
        self.install = next(c for c in cells if c.startswith("if pretrained_embedding is not None:"))
        self.model = SimpleNamespace(embedding=torch.nn.Embedding(3, 4))
        self.scope = {"torch": torch, "rnn": self.model,
                      "vocabulary": SimpleNamespace(get_itos=lambda: ["a", "b", "c"])}

    def test_missing_vectors_reset_stale_value_and_keep_parameter(self):
        weight = self.model.embedding.weight
        before = weight.detach().clone()
        self.scope.update(pretrained_vectors=None, pretrained_embedding=torch.ones(3, 4))
        exec(self.lookup, self.scope)
        exec(self.install, self.scope)
        self.assertIsNone(self.scope["pretrained_embedding"])
        self.assertIs(weight, self.model.embedding.weight)
        self.assertTrue(torch.equal(before, weight))

    def test_loaded_vectors_preserve_optimizer_parameter(self):
        weight = self.model.embedding.weight
        optimizer = torch.optim.SGD(self.model.embedding.parameters(), lr=0.1)
        self.scope["pretrained_vectors"] = SimpleNamespace(get_vecs_by_tokens=lambda _: torch.ones(3, 4))
        exec(self.lookup, self.scope)
        exec(self.install, self.scope)
        self.assertTrue(torch.equal(weight, torch.ones(3, 4)))
        self.assertIs(optimizer.param_groups[0]["params"][0], weight)

    def test_wrong_shape_fails_without_changing_weights(self):
        before = self.model.embedding.weight.detach().clone()
        self.scope["pretrained_vectors"] = SimpleNamespace(get_vecs_by_tokens=lambda _: torch.ones(2, 4))
        exec(self.lookup, self.scope)
        with self.assertRaisesRegex(ValueError, "does not match"):
            exec(self.install, self.scope)
        self.assertTrue(torch.equal(before, self.model.embedding.weight))

    def test_blank_spacy_pipeline_segments_sentences(self):
        import spacy
        cells = code_cells("S9.3 - Data Preparation LM SA.ipynb")
        setup = next(c for c in cells if "nlp.has_pipe" in c)
        # Execute the exact guard with a blank pipeline, without loading models.
        guard = next(n for n in ast.parse(setup).body if isinstance(n, ast.If))
        nlp = spacy.blank("en")
        exec(compile(ast.Module(body=[guard], type_ignores=[]), "notebook", "exec"), {"nlp": nlp})
        self.assertEqual(len(list(nlp("One sentence. Another sentence.").sents)), 2)


if __name__ == "__main__":
    unittest.main()
