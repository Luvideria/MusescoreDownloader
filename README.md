## MusescoreDowloader
Creates PDFs from musescore's svgs/pngs from url

To run this program you will need to do:

`pip install svglib fpdf pypdf2`

or with conda:

`conda install -c conda-forge svglib pypdf2`

sadly fpdf doesn't have a reliable release, but "-c viascience fpdf" looks ok

**Usage**: go on musescore and find the sheet you want
Copy the url, this is the inputUrl

## `python musescore.py inputUrl destinationDirectory MidiTrueFalse`

*inputUrl* is the url from musescore
*destinationDirectory* is where the sheet will be written
*MidiTrueFalse* is 1 if the midi file should be downloaded, 0 or empty otherwise
example:

`python ./musescore.py https://musescore.com/user/4609986/scores/1749181`

will put the sheet in the current directory

`python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin`

will put the sheet in the chopin directory. Will be created if does not exist.

`python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin 1`

will put the sheet and midi file in the chopin directory, will be created if does not exist.