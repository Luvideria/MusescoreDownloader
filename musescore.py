import sys, os, io
import urllib.request
from pathlib import Path
from svglib.svglib import svg2rlg #for svg to pdf
from reportlab.graphics import renderPDF #for svg to pdf
from fpdf import FPDF #for png to pdf
from PIL import Image #for png to pdf
from PyPDF2 import PdfFileMerger # for merging pdfs (svg side)

'''
To run this program you will need to do:

pip install svglib fpdf pypdf2

or with conda:

conda install -c conda-forge svglib pypdf2
sadly fpdf doesn't have a reliable release, but "-c viascience fpdf" looks ok

Usage: go on musescore and find the sheet you want
Copy the url, this is the inputUrl

python musescore.py inputUrl destinationDirectory MidiTrueFalse

inputUrl is the url from musescore
destinationDirectory is where the sheet will be written
MidiTrueFalse is 1 if the midi file should be downloaded, 0 or empty otherwise
example:
python ./musescore.py https://musescore.com/user/4609986/scores/1749181

will put the sheet in the current directory

python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin

will put the sheet in the chopin directory. Will be created if does not exist.

python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin 1

will put the sheet and midi file in the chopin directory, will be created if does not exist.
'''

def makePdf(pdfFileName, listPages,ext=".png"):
    # got this code from https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
    
    cover = Image.open(str(listPages[0]) + ext)
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(str(page) + ext, 0, 0)

    pdf.output( pdfFileName + ".pdf", "F")
if __name__ == "__main__":
    try:
        urlin=sys.argv[1]
    except:
        print('''
To run this program you will need to do:

pip install svglib fpdf pypdf2

or with conda:

conda install -c conda-forge svglib pypdf2
sadly fpdf doesn't have a reliable release, but "-c viascience fpdf" looks ok

Usage: go on musescore and find the sheet you want
Copy the url, this is the inputUrl

python musescore.py inputUrl destinationDirectory MidiTrueFalse

inputUrl is the url from musescore
destinationDirectory is where the sheet will be written
MidiTrueFalse is 1 if the midi file should be downloaded, 0 or empty otherwise
example:
python ./musescore.py https://musescore.com/user/4609986/scores/1749181

will put the sheet in the current directory

python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin

will put the sheet in the chopin directory. Will be created if does not exist.

python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin 1

will put the sheet and midi file in the chopin directory, will be created if does not exist.''')
        exit()
    try:
        dirscore=sys.argv[2]
    except:    
        dirscore="."
    try:
        midi=sys.argv[3]
    except:
        midi=""
    print("URL chosen: " + urlin)
    if dirscore==".":
        print("Output will be in current directory")
    else:
        print("Output will be in the directory: " + dirscore)
    
    fp = urllib.request.urlopen(urlin)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    nametext='<meta property="og:title" content="'

    namestart=mystr.find(nametext)+len(nametext)
    nameend=mystr.find('">\n',namestart)
    name=mystr[namestart:nameend]
    print("score found: " + name)

    # text to find in the source html to extract the correct url
    svgtext='<link type="image/svg+xml" href="'
    pngtext='<link type="image/png" href="'
    jpgtext='<link type="image/jpg" href="'
    svgext='.svg'
    pngext='.png'
    jpgext='.jpg'
    midiext="score.mid"
    scoreext=svgext

    # find() returns the position of the start of the sequence, need to add lenght
    page=mystr.find(svgtext)+len(svgtext)

    # check if find has found something
    if page == len(svgtext)-1:
        scoreext=pngext
        page=mystr.find(pngtext)+len(pngtext)
    if page == len(pngtext)-1:
        scoreext=jpgext
        page=mystr.find(jpgtext)+len(jpgtext)
    # the matching value is always score_0.png or .svg 
    endpage=mystr.find("score_0"+scoreext,page)

    # the midi, if available, is always score.mid
    url=mystr[page:endpage]
    midurl=url+midiext
    if not midi=="":
        test=urllib.request.urlretrieve(midurl, "/".join([dirscore,name+".mid"]))
    
    # create the destination directory if it does not exist
    Path(dirscore).mkdir(parents=True, exist_ok=True)

    i=0
    # downloads the file sheet pages one by one
    # iterates until code 404
    while True:
        iteri="score_"+str(i)+scoreext
        cururl=url+iteri
        
        try:
            test=urllib.request.urlretrieve(cururl, "/".join([dirscore,iteri]))
        except urllib.request.HTTPError as e:
            print(str(i)+" pages found")
            break
        i+=1

    Npages=i
    # simply contains dirscore/score_0, dirscore/score_1 ...
    listpages=[dirscore+"/score_"+str(n) for n in range(Npages)]

    if scoreext==".svg":
        # creates a file merger to concatenate pdf files (we don't have any yet)
        merger = PdfFileMerger()
        i=0
        listpdf=[]

        for p in listpages:
            drawing = svg2rlg(p+".svg") # this creates a temporary structure needed to create the pdf
            f=io.BytesIO() # uses BytesIO instead of actual file because it's temporary
            renderPDF.drawToFile(drawing, f) # this creates the pdf from the svg and saves it in f
            merger.append(f) # queue for the merge
            # hopefully we don't need to close the bytesio

        output = open(dirscore+"/"+name+".pdf", "wb")
        merger.write(output) # creates the final pdf
        [os.remove(f+".svg") for f in listpages] # removes the temporary svg we downloaded
        output.close() # close the output file (otherwise it will be condsidered open)

    else:
    #use the makePdf function defined at the beginning for png and jpg
        makePdf(dirscore+"/"+name+".pdf",listpages, scoreext)
