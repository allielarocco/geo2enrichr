"""Transforms user input to SOFT file.
"""

import time

from g2e import database
from g2e.endpoints.request_utils import get_param_as_list
from substrate import CustomDataset, GeoDataset, SoftFile, SoftFileSample
from . import parser, cleaner, file_manager, eutils


def from_geo(args):
    """Constructs a SoftFile
    """
    accession = args['dataset']

    if not file_manager.file_exists(accession):
        file_manager.download(accession)

    dataset = database.get_geo_dataset(accession)
    if not dataset:
        platform = args['platform']
        if platform.index('GPL') == 0:
            platform = platform[3:]

        title = args.get('title')
        summary = args.get('summary')
        if not title or not summary:
            title, summary = eutils.get_title_and_summary(accession)
            print('Fetched title and summary from EUtils API: %s, %s' % (title, summary))

        dataset = GeoDataset(
            accession=accession,
            platform=platform,
            organism=args['organism'],
            title=title,
            summary=summary
        )
    else:
        print('Dataset %s already exists!') % accession

    a_cols = get_param_as_list(args, 'A_cols')
    b_cols = get_param_as_list(args, 'B_cols')

    # Use get_or_create to track GSMs. We don't do this for custom files.
    control = [database.get_or_create(SoftFileSample,
                                      name=sample,
                                      is_control=True) for sample in a_cols]
    experimental = [database.get_or_create(SoftFileSample,
                                           name=sample,
                                           is_control=False) for sample in b_cols]
    samples = control + experimental

    genes, a_vals, b_vals, selections, stats = parser.parse(accession,
                                                            True,
                                                            dataset.platform,
                                                            samples)

    if 'normalize' not in args or args['normalize'] == 'True':
        normalize = True
    else:
        normalize = False

    genes, a_vals, b_vals = cleaner.clean(genes, a_vals, b_vals, normalize)

    text_file = file_manager.write(accession, dataset.platform, normalize,
                                   genes, a_vals, b_vals, samples, selections,
                                   stats)

    return SoftFile(
        samples, dataset, text_file,
        genes, a_vals, b_vals,
        stats=stats, normalize=normalize
    )


def from_file(file_obj, args):
    """Constructs a SoftFile from a user uploaded file.
    """
    # We support name and title for historical reasons, i.e. Firefox
    # support since we won't be releasing new versions of the add on.
    if 'name' in args and args['name'] != '':
        title = args['name']
    elif 'title' in args and args['title'] != '':
        title = args['title']
    else:
        title = str(time.time())[:10]

    text_file = file_manager.save(title, file_obj)
    genes, a_vals, b_vals, samples = parser.parse(title, is_geo=False)

    control = [SoftFileSample(x[0], True) for x in samples if x[1] == '0']
    experimental = [SoftFileSample(x[0], False) for x in samples if x[1] == '1']
    samples = control + experimental

    organism = args['organism'] if 'organism' in args else None

    dataset = CustomDataset(
        title=title,
        organism=organism
    )
    return SoftFile(samples, dataset, text_file, genes, a_vals, b_vals)
