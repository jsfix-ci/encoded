from pyramid.response import Response
from pyramid.view import view_config
from ..contentbase import Item, embed
from pyramid.httpexceptions import HTTPFound
from collections import OrderedDict


def getTrack(file_json):
    data = OrderedDict([
        ('visibility', 'full'),
        ('color', '128,0,0'),
        ('long_label', file_json['accession']),
        ('short_label', file_json['accession']),
        ('bigDataUrl', 'http://encodedcc.sdsc.edu/warehouse/' + file_json['download_path']),
        ('type', file_json['file_format']),
        ('track', file_json['accession']),
    ])
    return data


def getGenomeTxt(properties):
    genome = OrderedDict([('trackDb', 'trackDb.txt'), ('genome', 'hg19')])
    if properties['replicates'][0]['library']['biosample']['organism']['name'] != 'human':
        genome['genome'] = 'mm9'
    genome_array = []
    for i in range(len(genome)):
        temp = list(genome.popitem())
        str1 = ' '.join(temp)
        genome_array.append(str1)
    return genome_array


def getHubTxt():
    hub = OrderedDict([
        ('email', 'jseth@stanford.edu'),
        ('genomesFile', 'genomes.txt'),
        ('longLabel', 'ENCODE Data Coordination Center Data Hub'),
        ('shortLabel', 'ENCODE DCC Hub'),
        ('hub', 'DCC_Hub')
    ])
    hub_array = []
    for i in range(len(hub)):
        temp = list(hub.popitem())
        str1 = ' '.join(temp)
        hub_array.append(str1)
    return hub_array


def getTrackDbTxt(files_json):
    tracks = []
    for file_json in files_json:
        if file_json['file_format'] in ['bigWig', 'bigBed']:
            track = getTrack(file_json)
            for i in range(len(track)):
                temp = list(track.popitem())
                str1 = ' '.join(temp)
                tracks.append(str1)
            tracks.append('')
    return tracks


@view_config(name='visualize', context=Item, request_method='GET',
             permission='view')
def visualize(context, request):
    hub_url = (request.url).replace('@@visualize', '@@hub')
    UCSC_url = 'http://genome.ucsc.edu/cgi-bin/hgTracks?udcTimeout=1&db-hg19' + \
        '&hubUrl=' + hub_url + '/hub.txt'
    print UCSC_url
    return HTTPFound(location=UCSC_url)


@view_config(name='hub', context=Item, request_method='GET',
             permission='view')
def hub(context, request):

    embedded = embed(request, request.resource_path(context))
    files_json = embedded.get('files', None)
    if files_json is not None:
        url_ret = (request.url).split('@@hub')
        if url_ret[1] == '/hub.txt':
            return Response('\n'.join(getHubTxt()), content_type='text/plain')
        elif url_ret[1] == '/genomes.txt':
            return Response('\n'.join(getGenomeTxt(embedded)), content_type='text/plain')
        elif url_ret[1] == '/trackDb.txt':
            return Response('\n'.join(getTrackDbTxt(files_json)), content_type='text/plain')
    return ''
