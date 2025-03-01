import json
import time
import unittest

from g2e import app


unittest.TestCase.maxDiff = None


def get_gene_value(genelist, gene):
    for gv in genelist:
        if gv[0] == gene:
            return gv[1]
    return None


class TestRoundTrip(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # This should be multiple unit tests but it is annoyingly slow to run.
    def test_extraction_endpoint_chdir(self):

        s = time.time()

        self.resp = self.app.post('/g2e/api/extract/geo', data=dict(
            is_geo = True,
            dataset = 'GDS5077',
            platform = 'GPL10558',
            organism = 'Homo sapiens',
            normalize = True,
            A_cols = ['GSM1071454', 'GSM1071455'],
            B_cols = ['GSM1071457', 'GSM1071456']
        ))
        self.resp_dict = json.loads(self.resp.data.decode())
        self.assertEquals(self.resp.status_code, 200)
        self.assertTrue('extraction_id' in self.resp_dict)
        extraction_id = self.resp_dict['extraction_id']
        resp = self.app.get('/g2e/api/extract/' + str(extraction_id))
        resp_dict = json.loads(resp.data.decode())

        # Test response from round-trip.
        self.assertTrue(resp_dict['required_metadata']['diff_exp_method'] == 'chdir')
        self.assertTrue(resp_dict['required_metadata']['cutoff'] == 500)
        self.assertTrue(resp_dict['soft_file']['accession'] == 'GDS5077')
        self.assertTrue(resp_dict['soft_file']['title'] == 'Transmembrane protein 88 depletion effect on stem cell cardiac differentiation in vitro')
        self.assertTrue('static/softfile/clean/GDS5077_' in resp_dict['soft_file']['text_file'])
        self.assertTrue(resp_dict['soft_file']['platform'] == 'GPL10558')
        self.assertTrue(resp_dict['soft_file']['organism'] == 'Homo sapiens')
        self.assertTrue(resp_dict['soft_file']['normalize'] == True)
        self.assertTrue(resp_dict['soft_file']['is_geo'])

        for gl in resp_dict['gene_lists']:
            self.assertTrue('direction' in gl)
            self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in gl['target_apps']['enrichr'])
            if gl['direction'] == 0:
                self.assertTrue('http://amp.pharm.mssm.edu/L1000CDS2' in gl['target_apps']['l1000cds2'])
                self.assertTrue('http://amp.pharm.mssm.edu/PAEA' in gl['target_apps']['paea'])

        genelist = resp_dict['gene_lists'][2]['ranked_genes']
        self.assertTrue(get_gene_value(genelist, 'HBE1') == -0.0939582)
        self.assertTrue(get_gene_value(genelist, 'EOMES') == 0.0866544)
        self.assertTrue(get_gene_value(genelist, 'SRPK1') == -0.0222528)
        self.assertTrue(get_gene_value(genelist, 'MYH6') == -0.0327115)
        print(time.time() - s)

    # This should be multiple unit tests but it is annoyingly slow to re-run.
    def test_extraction_endpoint_ttest(self):

        s = time.time()

        self.resp = self.app.post('/g2e/api/extract/geo', data=dict(
            is_geo = 'True',
            dataset = 'GDS5077',
            organism = 'Homo sapiens',

            # Both of these arguments are misnamed--or haven't been updated
            # because I don't want to release a new version of the extensions
            # just to support this. They should be changed in the future.
            diffexp_method = 'ttest',
            correction_metrequired_metadatahod = 'BH',

            threshold = 0.05,
            normalize = True,
            platform = 'GPL10558',
            A_cols = ['GSM1071454', 'GSM1071455'],
            B_cols = ['GSM1071457', 'GSM1071456']
        ))
        self.resp_dict = json.loads(self.resp.data.decode())
        self.assertEquals(self.resp.status_code, 200)
        self.assertTrue('extraction_id' in self.resp_dict)
        extraction_id = self.resp_dict['extraction_id']

        resp = self.app.get('/g2e/api/extract/' + str(extraction_id))
        resp_dict = json.loads(resp.data.decode())

        self.assertTrue(resp_dict['required_metadata']['diff_exp_method'] == 'ttest')
        self.assertTrue(resp_dict['required_metadata']['ttest_correction_method'] == 'BH')
        self.assertTrue(resp_dict['required_metadata']['threshold'] == 0.05)

        self.assertTrue(resp_dict['soft_file']['accession'] == 'GDS5077')
        self.assertTrue(resp_dict['soft_file']['title'] == 'Transmembrane protein 88 depletion effect on stem cell cardiac differentiation in vitro')
        self.assertTrue('static/softfile/clean/GDS5077_' in resp_dict['soft_file']['text_file'])
        self.assertTrue(resp_dict['soft_file']['platform'] == 'GPL10558')
        self.assertTrue(resp_dict['soft_file']['organism'] == 'Homo sapiens')
        self.assertTrue(resp_dict['soft_file']['is_geo'])

        for gl in resp_dict['gene_lists']:
            self.assertTrue('direction' in gl)
            self.assertTrue('http://amp.pharm.mssm.edu/Enrichr/enrich?dataset' in gl['target_apps']['enrichr'])

        genelist = resp_dict['gene_lists'][2]['ranked_genes']
        self.assertTrue(get_gene_value(genelist, 'HBE1') == -0.00469161)
        self.assertTrue(get_gene_value(genelist, 'PTPRN2') == 0.00486001)
        self.assertTrue(get_gene_value(genelist, 'GNG11') == -0.04072)
        self.assertTrue(get_gene_value(genelist, 'PDZRN3') == -0.0375523)
        print(time.time() - s)

    def test_file_upload(self):
        self.resp = self.app.post('/g2e/api/extract/upload_soft_file', data=dict(
            file = (file('tests/data/example_input.txt'), 'test.txt'),
            title = 'ExampleData',
            cutoff = 'none'
        ))

        self.resp_dict = json.loads(self.resp.data.decode())
        self.assertEquals(self.resp.status_code, 200)
        self.assertTrue('extraction_id' in self.resp_dict)
        extraction_id = self.resp_dict['extraction_id']
        resp = self.app.get('/g2e/api/extract/' + str(extraction_id))
        resp_dict = json.loads(resp.data.decode())

        self.assertTrue(resp_dict['soft_file']['title'], 'ExampleData')
        genelist = resp_dict['gene_lists'][2]['ranked_genes']
        self.assertTrue(get_gene_value(genelist, 'MBTPS1') == -0.0185085)
        self.assertTrue(get_gene_value(genelist, 'SPRED2') == 0.0537715)
        self.assertTrue(get_gene_value(genelist, 'ZNF274') == -0.00367804)
        self.assertTrue(get_gene_value(genelist, 'CLIC4') == 0.00194543)
