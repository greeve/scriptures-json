import json
import sys

if len(sys.argv) != 2:
    print("Usage: python scripture_search.py book-of-mormon-flat.json")
    sys.exit(-1)

filename = sys.argv[1]

search_query = str(input('Enter a search query: '))

print('Searching for {}...'.format(search_query))

results = []

data = None

with open(filename, encoding='utf8') as fin:
    data = json.load(fin)

verses = data['verses']

for verse in verses:
    if search_query in verse.get('text'):
        results.append(verse)

print('Finished searching.')

filename = 'search-result_{}.txt'.format(search_query)

heading = '# {}\n\n'

with open(filename, 'w', encoding='utf8') as fout:
    fout.write(heading.format(search_query))
    fout.write('## References\n\n')
    for result in results:
        fout.write('- ' + result.get('reference') + '\n')
    fout.write('\n## Scriptures\n\n')
    for result in results:
        fout.write(result.get('reference') + '\n\n')
        fout.write(result.get('text') + '\n\n')
