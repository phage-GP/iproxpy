'''
refs：
    https://www.iprox.cn/proxi/swagger-ui.html
    https://www.ibm.com/docs/en/ahts/4.4?topic=line-ascp-command-reference
'''


import os
import multiprocessing
from multiprocessing import Pool
from joblib import Parallel, delayed
import requests


def get_file_urls(URL, identifier: str = ''):
    '''
    input:
        iprox url
        dataset identifier: PXD043774
    output:
        file download url list
    '''
    re = requests.get(URL)
    # print(re.status_code)
    if re.status_code == 200:
        dict(re.json()).keys()
        # >>> dict_keys(['accession', 'title', 'contacts', 'instruments', 'species', 'publications', 'summary', 'modifications', 'keywords', 'datasetLink', 'dataFiles'])
        print(f"{dict(re.json())['accession']['name']}: {dict(re.json())['accession']['value']}") # accession
        print(f"Title: {dict(re.json())['title']}") # Title
        # print(f"instruments: {dict(re.json())['instruments']['name']}") # Instruments list
        print(f"Summary: {dict(re.json())['summary']}") # summary
        print(f"DatasetLink: {dict(re.json())['datasetLink']['value']}") # datasetLink
        print(f"File Counts: {len(dict(re.json())['dataFiles'])}")

        file_url_list = [file_dict['value'] for file_dict in dict(re.json())['dataFiles']]

    return file_url_list
    

def download(file_url, username='guests', password='guests', path='./', engine='wget'):
    '''
    function:
        download data in file url
        # https://download.iprox.org/IPX0005194000/IPX0005194001/Exp115081_UCT_Plasma_HFX_F1_R1.raw
    input:
        file_url: file url
        path: path to save file 

    output:
        None
    '''
    print(f"Downloading {file_url.split('/')[-1]}")
    if engine == 'wget':
        os.system(f"wget -c {file_url} –output-file={file_url.split('/')[-1]} --no-check-certificate")
    if engine == 'aspera':
        os.putenv('ASPERA_SCP_PASS',password)
        os.system(f"ascp -d -QT -l1000m -P 33001 --file-manifest=text -k 2 -o Overwrite=diff {username}@download.iprox.cn:{file_url.replace('https://download.iprox.org','')} {path}")


def batch_download(file_url_list:list = [], username='guests', password='guests',path = "./", engine = 'wget',processes_num:int = multiprocessing.cpu_count() // 2 ):
    '''
    function:
        download data in file url list
    input:
        file_url_list: file url list
        username='guests'
        password='guests'
        path = "./"
        engine = 'wget'
        processes_num

    output:
        None
    '''

    # multiprocessing
    # with Pool(processes = processes_num) as p:
    #     p.map(download, file_url_list) # (file_url,path=path)

    # joblib
    Parallel(n_jobs=processes_num)(delayed(download)(file_url, username=username, password=password, path=path, engine=engine) for file_url in file_url_list)

if __name__ == '__main__':

    identifier = 'PXD043774'
    URL = f'https://www.iprox.cn/proxi/datasets/{identifier}'
    file_url_list = get_file_urls(URL,identifier=identifier)[:4]
    batch_download(file_url_list,
                   engine = 'aspera',
                   path='~/',
                   processes_num=4)