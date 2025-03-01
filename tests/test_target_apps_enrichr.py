import unittest

from g2e.target_applications import enrichr
from substrate import Gene, RankedGene


class TestTargetAppsEnrichr(unittest.TestCase):

    def setUp(self):
        self.ranked_genes = [
            RankedGene(Gene('A'), 1),
            RankedGene(Gene('B'), .5),
            RankedGene(Gene('C'), 0),
            RankedGene(Gene('D'), -.5),
            RankedGene(Gene('E'), -1)
        ]

    def test_get_link(self):
        link = enrichr.get_link(self.ranked_genes, '')
        self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in link)

    def test_convert_ranked_genes_to_tuples(self):
        genes = enrichr.convert_ranked_genes_to_tuples(self.ranked_genes)
        self.assertEqual(len(genes), len(self.ranked_genes))
        self.assertTrue(type(genes[0]) is tuple)

    def test_get_genes_as_string(self):
         genes = enrichr.convert_ranked_genes_to_tuples(self.ranked_genes)
         gene_str = enrichr.get_genes_as_string(genes)
         self.assertEqual('A,1\nB,0.5\nC,0\nD,0.5\nE,1', gene_str)
