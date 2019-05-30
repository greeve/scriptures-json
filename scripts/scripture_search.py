import json

search_query = str(input('Enter a search query: '))

print('Searching for {}...'.format(search_query))

results = []

data = None

with open('book-of-mormon-flat.json', encoding='utf8') as fin:
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
    for result in results:
        fout.write(result.get('reference') + '\n\n')
        fout.write(result.get('text') + '\n\n')