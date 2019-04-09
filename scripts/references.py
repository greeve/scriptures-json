import argparse
import csv
import json
import pathlib
import re

from collections import OrderedDict, defaultdict

VERSE_REGEX = '((\d\s*)?([A-Z]?[a-z]+\.*|[A-Z]&[A-Z]))\s*(\d+)[:-](\d+)?(\s*-\s*\d+)?'


def get_abbreviations(filepath):
  abbrev = OrderedDict()
  with open(filepath, encoding='utf8') as fin:
    reader = csv.reader(fin)
    for row in reader:
      row = [x.replace(u'\xa0', u' ') for x in row]
      row = [x.replace(u'\u2014', u'-') for x in row]
      data = {
        'volume': row[1],
        'volume_slug': row[2],
        'book': row[3],
      }
      abbrev[row[0]] = data
      abbrev[row[3]] = data
      
  return abbrev


def get_references(filepath):
  references = []
  
  with open(filepath) as fin:
    references = fin.readlines()
  
  return references


def parse_reference(reference):
  verses = re.compile(VERSE_REGEX)
  match = verses.search(reference)
  book = match.group(1)
  chapter = match.group(4)
  verse = int(match.group(5))
  range = match.group(6)
  
  verses = []
  verses.append(str(verse))
  
  if range:
    range = int(range.replace('-', ''))
    while verse != range:
      verse += 1
      verses.append(str(verse))
  
  return (book, chapter, verses)

def organize_verses(references, abbrev):
  volumes = defaultdict(list)
  for reference in references:
    print(reference.strip())
    book, chapter, verses = parse_reference(reference)
    volume = abbrev[book]['volume']
    volume_slug = abbrev[book]['volume_slug']
    book = abbrev[book]['book']
    volumes[volume_slug].append((book, chapter, verses))
  return volumes


def get_verses(volume, references):
  data = None
  with open('../reference/' + volume + '-reference.json', encoding='utf8') as fin:
    data = json.load(fin)
  
  texts = {}
  for reference in references:
    book, chapter, verses = reference
    if len(verses) > 1:
      verse_range = '{}-{}'.format(verses[0], verses[-1])
    else:
      verse_range = '{}'.format(verses[0])
    full_reference = '{} {}:{}'.format(book, chapter, verse_range)
    verse_text = []
    for verse in verses:
      if book == 'Doctrine and Covenants':
        verse_text.append(data[chapter][verse])
      else:
        verse_text.append(data[book][chapter][verse])
    texts[full_reference] = '\n\n'.join(verse_text)
  return texts
  

def main():
  
  parser = argparse.ArgumentParser()
  parser.add_argument('references', help='The filepath with scripture references')
  parser.add_argument('abbreviations', help='The filepath with scripture reference abbreviations')
  
  args = parser.parse_args()
  
  abbrev = get_abbreviations(args.abbreviations)
  references = get_references(args.references)
  volumes = organize_verses(references, abbrev)
  verses = {}
  for volume, references in volumes.items():
    verses.update(get_verses(volume, references))
  
  with open('output.txt', 'w', encoding='utf8') as fout:
    for verse, text in verses.items():
      fout.write(verse + '\n\n')
      fout.write(text + '\n\n')


if __name__ == '__main__':
  main()
