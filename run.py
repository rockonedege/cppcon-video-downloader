import requests
from pathlib import Path
import re

def download_command(url, name):
  return f'wget {url} -O {name}_high.mp4'

def get_one(index):
  index = f'{index:03d}'
  url = f'https://channel9.msdn.com/Events/GoingNative/CppCon-2017/{index}'
  r = requests.get(url)

  title = re.findall(r'<title>(.+)</title>?', r.text)[0]
  title = re.sub(r'(&#?\w+;)|([)(\s:?<>|"\\/*]+)', '-', title)
  title = re.sub('-+', '-', title)

  url = re.findall(r'rel="Mp4High?" href="([^_]+?_high\.mp4)"?', r.text)
  if not url:
    url = re.findall(r'rel="Mp4?" href="([^_]+?\.mp4)"?', r.text)
    
  return download_command(url[0], title)
      
def main():
  for i in range(1, 138):
    print(get_one(i))

if __name__ == '__main__':
  main()
