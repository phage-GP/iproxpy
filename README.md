## Introduction
[iprox](https://www.iprox.cn/) is an integrated proteome resources center in China, which is built to accelerate the worldwide data sharing in proteomics. 

iproxpy is an unofficial Python package for data queries and downloads of iprox database.

## Home Page
https://github.com/phage-GP/iproxpy/

## Dependencies
**aspera-cli**

```bash
conda install -c hcc aspera-cli
```

## Useage

**Installation**
```bash
pip install iproxpy
```

**Example**
```python
import iproxpy

identifier = 'PXD043774'
URL = f'https://www.iprox.cn/proxi/datasets/{identifier}'
file_url_list = iproxpy.get_file_urls(URL,identifier=identifier)
```

```python
iproxpy.download(file_url_list[0],engine = 'aspera',path='~/')
```

```python
iproxpy.batch_download(file_url_list[:4],
                engine = 'aspera',
                path='~/',
                processes_num=4)
```

## Refs
> https://www.iprox.cn/page/helpApi.html

> https://www.ibm.com/docs/en/ahts/4.4?topic=line-ascp-command-reference