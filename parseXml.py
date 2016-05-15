from collections import defaultdict
import re
import pdb
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
def main():
    tree = ET.parse('Songbook.xml')

    root = tree.getroot()

    pages = root.findall('page')
    pages = pages[4:]

    songs = defaultdict(list)

    for page in pages:
        currentSong = "contents"
        verseCount = 0
        emptyLine = False
        for text in page.findall('text'):
            #Then song title
            if text.find('b') is not None:
                currentSong = text.find('b').text
                verseCount = 0
                emptyLine = True
            #Then
            else:
                if text.text != None and check_chords(text.text):
                    songs[currentSong].append(text.text)
    for song in songs:
        print song
        for verse in songs[song]:
            print verse
        print "\n\n"

if __name__ == '__main__':
    main()
