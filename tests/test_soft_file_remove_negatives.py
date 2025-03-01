import unittest
import numpy as np

from g2e.signature_factory.soft_file_factory.cleaner import _remove_negatives


class TestSoftFileRemoveNegatives(unittest.TestCase):

    def setUp(self):
        self.genes = np.array(['A', 'B', 'C', 'D', 'E'])
        self.vals = np.array([
            [2.0, 2.0],
            [-3.0, 3.0],
            [8.0, -8.0],
            [4.0, 4.0],
            [1.0, 1.0]
        ])

    def test_remove_negatives(self):
        genes, vals = _remove_negatives(self.genes, self.vals)
        ans_vals = np.array([[2.0, 2.0], [4.0, 4.0], [1.0, 1.0]])
        ans_genes = np.array(['A', 'D', 'E'])
        self.assertTrue((vals == ans_vals).all())
        self.assertTrue((genes == ans_genes).all())

    def test_output_length(self):
        genes, vals = _remove_negatives(self.genes, self.vals)
        self.assertEqual(len(vals), 3)
        self.assertEqual(len(genes), len(vals))
