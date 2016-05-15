from collections import defaultdict
import re
import pdb
import argparse
import subprocess
import os

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
import xml.etree.ElementTree as ET
template_start = """
\\documentclass{article}
\\usepackage[margin=0.2in]{geometry}
\\begin{document}
"""
template_end = """
\\end{document}
"""

def check_chords(line):
    if len(line) < 1:
        return False
    wordsplit = re.findall(r"[\w]+", line)
    if len(wordsplit) < 1:
        return False
    elif max([len(word) for word in wordsplit]) < 4 or any([bool(re.search(r"[A-Z]sus", word)) for word in wordsplit]):
        return False
    else:
        return True
def parse_songs(filename):
    tree = ET.parse(filename)

    root = tree.getroot()

    pages = root.findall('page')
    pages = pages[4:]

    songs = defaultdict(list)
    numbers = {}
    for page in pages:
        currentSong = "contents"
        verseCount = 0
        emptyLine = False
        for text in page.findall('text'):
            #Then song title
            if text.find('b') is not None:
                currentSong = text.find('b').text
                reg = re.compile(r"([0-9]+)\.\s+(.+)$")
                matches = reg.search(currentSong)
                if matches != None:
                    numbers[int(matches.group(1))] = currentSong
                verseCount = 0
                emptyLine = True
            #Then
            else:
                if text.text != None and check_chords(text.text):
                    songs[currentSong].append(text.text)
    return songs, numbers

def main():
    parser = argparse.ArgumentParser(description = "Script to parse the songbook xml and generate song sheets")
    parser.add_argument('song_names', nargs='*')
    args = parser.parse_args()


    songs, numbers = parse_songs('Songbook.xml')

    with open('songs.tex', 'w') as f:
        f.write(template_start)
        f.write('\\begin{flushleft}\\begin{tabular}{p{3.935in} p{3.935in}}')
        for i in xrange(4):
            for song_num in args.song_names:
                song_name = numbers[int(song_num)]
                f.write('\\textbf{%s} & \\textbf{%s} \\\\ \n' % (song_name, song_name))
                for verse in songs[song_name]:
                    f.write('%s & %s \\\\\n' % (verse,verse))
                f.write('\\vspace{0.01cm} & \\vspace{0.01cm} \\\\\n')
            f.write('\\vspace{0.01cm} & \\vspace{0.01cm} \\\\\n')
        f.write('\\end{tabular}\\end{flushleft}')
        f.write(template_end)


    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'songs.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

    retcode = proc.returncode
    if not retcode == 0:
        os.unlink('songs.pdf')
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 



if __name__ == '__main__':
    main()
