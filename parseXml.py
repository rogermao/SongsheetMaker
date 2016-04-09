import xml.etree.ElementTree as ET

tree = ET.parse('Songbook.xml')

root = tree.getroot()

pages = root.findall('page')
pages = pages[4:]

songs = {}

for page in pages:
    song = {}
    currentSong = ""
    verseCount = 0
    emptyLine = False
    for text in pages.findall('text'):
        #Then song title
        if text.find('b') is not None:
            songs[currentSong] = song
            song = {}
            currentSong = text.find('b').text
            verseCount = 0
            emptyLine = True
        #Then 
        elif text.text is None:
            if emptyLine:
                
            else:
                emptyLine = True
