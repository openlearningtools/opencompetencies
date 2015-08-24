from random import randint, choice

with open('/srv/projects/opencompetencies/development_resources/lorem_ipsum.txt') as f:
    lines = f.readlines()

all_lines = ''
for line in lines:
    all_lines += line.strip()

#print(all_lines)

lines = all_lines.split('.')
lines = [line.lstrip() + '.' for line in lines]
#for line in lines:
#    print(line)

def get_paragraph(num_lines):
    """Get a certain number of sentences."""
    # Get a random set of lines.
    return_lines = ''
    for line_num in range(num_lines):
        return_lines += lines[randint(0, len(lines)-1)] + ' '
    return return_lines

def get_paragraphs(num_paragraphs):
    """Get a certain number of paragraphs."""
    return_paragraphs = ''
    for par_num in range(num_paragraphs):
        return_paragraphs += get_paragraph(randint(3,7)) + '\n\n'
    return return_paragraphs

def get_words(num_words):
    """Get a certain number of words."""
    return_words = ''
    for word_num in range(num_words):
        # Get a random line, pull a random word.
        line = choice(lines)
        return_words += choice(line.split()).strip(',. ') + ' '
    return return_words
