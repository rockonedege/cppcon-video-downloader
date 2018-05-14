import requests
from pathlib import Path
import re
# from pprint import pprint as print

output_folder = Path('output')
output_folder.mkdir(exist_ok=True)    


def make_cmd(url, name, tool = 'wget'):
    '''tool can be wget, curl or aria2'''
    return f'{tool} {url} -O {name}'

def clean(s):
    s = s.strip()
    s = re.sub(r'(&#?\w+;)|([^+\w]+)', '-', s)
    s = re.sub('-+', '-', s.strip())
    return s

def get_one_year(year, url):

    r = requests.get(url)

    (output_folder / f'ch9-{year}.xml').write_text(r.text, encoding='utf-8')


    import xml.etree.ElementTree as ET  

    ns = dict(dc="http://purl.org/dc/elements/1.1/", media="http://search.yahoo.com/mrss/")

    root = ET.fromstring(r.text).find('channel')

    all_ = []
    for item in root.findall('item'):
        title = item.find('title').text       
        link = item.find('link').text.rsplit('/')[-1]        

        author = item.findall('dc:creator', ns)[0].text

        url = item.find('enclosure').get('url')

        all_.append(dict(title=clean(title), link = link, author = author, url = url))

    return all_

def run():

    for name, url in [
        ('build-2018', 'https://s.ch9.ms/Events/Build/2018/RSS/mp4high'),
        ('cppcon-2017', 'https://s.ch9.ms/Events/GoingNative/CppCon-2017/RSS/mp4high'),
        ('cppcon-2016', 'https://s.ch9.ms/Events/CPP/CppCon-2016/RSS/mp4high'),
        ('cppcon-2015', 'https://s.ch9.ms/Events/CPP/CppCon-2015/RSS/mp4high'),
        ('cppcon-2014', 'https://s.ch9.ms/Events/CPP/C-PP-Con-2014/RSS/mp4high'),
        ('cppcon-2013', 'https://s.ch9.ms/Events/GoingNative/2013/RSS/mp4high'),
        ('cppcon-2012', 'https://s.ch9.ms/Events/GoingNative/GoingNative-2012/RSS/mp4high')
        ]:
        
        print(f'processing {name} ...')
        cmds = []
        for a in get_one_year(name, url):
            url = a['url']
            ext = url.rsplit('.')[-1]
            cmds.append(make_cmd(url, f'{a["title"]}_high.{ext}'))

        (output_folder / f'{name}.sh').write_text('\n'.join(cmds), encoding='utf-8')
        

if __name__ == '__main__':
    run()
