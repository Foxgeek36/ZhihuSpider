import os

files = os.listdir()
files.remove('merge.py')

foo = open('core ability.md', 'a+', encoding='utf8')

for file in files:
    foo.write(open(file, 'r', encoding='utf8').read())
    foo.write('\n\n')
print('finish')
