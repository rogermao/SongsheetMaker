from collections import defaultdict
import argparse
import re

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
import xml.etree.ElementTree as ET

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

    doc = Document('basic')
    for song_num in args.song_names:
        song_name = numbers[int(song_num)]
        with doc.create(Section(song_name)):
            for verse in songs[song_name]:
                doc.append(verse + "\n")

    doc.generate_pdf("songs")
    doc.generate_tex()

if __name__ == '__main__':
    main()
