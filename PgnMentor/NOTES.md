wget 'https://www.pgnmentor.com/files.html'

```
import re

f = open('files.html', 'r').read()
for part in re.findall('(players/[A-Z][a-zA-Z]+.zip)', f):
  print(f'https://www.pgnmentor.com/{part}')
