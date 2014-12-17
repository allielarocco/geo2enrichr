"""This module identifies differentially expressed genes. It delegates to the
appropriate method depending on user options and defaults to the
characteristic direction.

__authors__ = "Gregory Gundersen, Axel Feldmann, Kevin Hu"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


from scipy import stats

import chdir
from log import pprint


def analyze(A, B, genes, config, filename=''):
	"""Identifies differentially expressed genes, delegating to the correct
	helper function based on client or default configuration.
	"""

	# Default to the characteristic direction with a cutoff of 500.
	if config['method'] == 'ttest':
		gene_pvalues = ttest(A, B, genes, config['cutoff'])
	else:
		pprint('Calculating the characteristic direction.')
		genes, pvalues = chdir.chdir(A, B, genes.tolist())

	# sort pvalues and genes by the absolute values pvalues in descending order.
	grouped = zip([abs(item) for item in pvalues], genes, pvalues)
	grouped = sorted(grouped, key=lambda x: x[0], reverse=True)
	return [(item[1], item[2]) for item in grouped]


def ttest(A, B, genes):
	"""Performs a standard T-test.
	"""

	pvalues = []
	for i in range(len(A)):
		ttest_results = stats.ttest_ind(A[i], B[i])
		# TODO: Ask Andrew if I should use `all()` or `any()`.
		signed_pvalue = ttest_results[1] if (ttest_results[0] > 0).all() else (ttest_results[1] * -1)
		pvalues.append((genes[i], signed_pvalue))

	# TODO: This should also handle a cutoff.
	return pvalues