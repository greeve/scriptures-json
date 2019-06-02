import pathlib

import requests
from bs4 import BeautifulSoup

VOLUMES = [
    'bofm',
    'dc-testament',
    'pgp',
]

URL = 'https://www.lds.org/scriptures/{}?lang=hun'


def download_volumes():
    for volume in VOLUMES:
        path = pathlib.Path(volume)
        path.mkdir(exist_ok=True)

        r = requests.get(URL.format(volume))
        filename = '{}/{}.html'.format(volume, volume)
        with open(filename, 'wb') as fout:
            fout.write(r.content)

        # soup = BeautifulSoup(r.content, 'html.parser')
        # title_info = soup.h1
        # print(title_info)
        # primary = soup.find(id='primary')
        # print(primary)


def download_books():
    for volume in VOLUMES:
        print(volume)
        path = pathlib.Path(volume)
        index = path / '{}.html'.format(volume)
        data = None
        soup = None
        with open(index, encoding='utf8') as fin:
            data = fin.read()
            soup = BeautifulSoup(data, 'html.parser')

        frontmatter = soup.find('ul', class_='frontmatter')
        for item in frontmatter.find_all('li'):
            print(item)
            uri = item.a['href']
            if uri.startswith('http'):
                label = item.a.text
                filename = '{}.html'.format(label)
                folder = path / 'frontmatter'
                folder.mkdir(parents=True, exist_ok=True)
                filepath = folder / filename
                r = requests.get(uri)
                with open(filepath, 'wb') as fout:
                    fout.write(r.content)

        books = soup.find_all('ul', class_='books')
        for book in books:
            for item in book.find_all('li'):
                uri = item.a['href']
                if uri.startswith('http'):
                    slug = item['id']
                    label = item.a.text

                    filename = '{}.html'.format(slug)
                    folder = path / 'books'
                    folder.mkdir(parents=True, exist_ok=True)
                    filepath = folder / filename
                    r = requests.get(uri)
                    with open(filepath, 'wb') as fout:
                        fout.write(r.content)


def main():
    download_volumes()
    download_books()


if __name__ == '__main__':
    main()
