import unittest
import numpy as np

from g2e.signature_factory.soft_file_factory.cleaner import average_duplicates


class TestSoftFileAverageDuplicateGenes(unittest.TestCase):

    def setUp(self):
        self.genes = np.array(['A', 'C', 'C', 'B', 'A'])
        self.vals = np.array([
            [2.0, 2.0, 9.0, 9.0],
            [3.0, 3.0, 3.0, 3.0],
            [8.0, 8.0, 2.0, 2.0],
            [4.0, 4.0, 4.0, 3.0],
            [1.0, 1.0, 1.0, 1.0]
        ])

    def test_output_length(self):
        genes, vals = average_duplicates(self.genes, self.vals)
        self.assertEqual(len(vals), 3)
        self.assertEqual(len(vals), len(genes))

    def test_reduced_matrix(self):
        genes_ans = np.array(['A', 'B', 'C'])
        vals_ans = np.array([
            [1.5, 1.5, 5.0, 5.0],
            [4.0, 4.0, 4.0, 3.0],
            [5.5, 5.5, 2.5, 2.5]
        ])

        genes, vals = average_duplicates(self.genes, self.vals)
        self.assertTrue(np.array_equal(vals, vals_ans))
        self.assertTrue(np.array_equal(genes, genes_ans))
