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
    # ext in case jpg is needed, so far not
    
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
        print('''pip install svglib fpdf pypdf2

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
    print(urlin)
    print("dir: " + dirscore)
    
    fp = urllib.request.urlopen(urlin)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    nametext='<meta property="og:title" content="'

    namestart=mystr.find(nametext)+len(nametext)
    nameend=mystr.find('">\n',namestart)
    name=mystr[namestart:nameend]

    svgtext='<link type="image/svg+xml" href="'
    svgext='.svg'
    pngext='.png'
    midiext="score.mid"
    pngtext='<link type="image/png" href="'
    scoreext=svgext

    #find returns the position of the start of the sequence, add lenght of sequence to get the pos after
    page=mystr.find(svgtext)+len(svgtext)

    #check if find has found something
    if page == len(svgtext)-1:
        scoreext=pngext
        page=mystr.find(pngtext)+len(pngtext)
    endpage=mystr.find("score_0"+scoreext,page)

    url=mystr[page:endpage]
    midurl=url+midiext
    if not midi=="":
        test=urllib.request.urlretrieve(midurl, "/".join([dirscore,name+".mid"]))
    
    
    Path(dirscore).mkdir(parents=True, exist_ok=True)

    i=0
    while True:
        iteri="score_"+str(i)+scoreext
        cururl=url+iteri
        i+=1

        try:
            test=urllib.request.urlretrieve(cururl, "/".join([dirscore,iteri]))
        except urllib.request.HTTPError as e:
            i-=1
            print(str(i)+" pages found")
            break
    Npages=i
    if scoreext==".png":
        listpages=[dirscore+"/score_"+str(n) for n in range(i)]
        makePdf(dirscore+"/"+name+".pdf",listpages)

    elif scoreext==".svg":
        listpages=[dirscore+"/score_"+str(n) for n in range(Npages)]
        merger = PdfFileMerger()
        inputs=[]
        i=0
        listpdf=[]
        for p in listpages:
            drawing = svg2rlg(p+".svg")
            f=io.BytesIO()
            renderPDF.drawToFile(drawing, f)
            merger.append(f)
            inputs.append(f)

        output = open(dirscore+"/"+name+".pdf", "wb")
        merger.write(output)
        [f.close() for f in inputs]
        [os.remove(f+".svg") for f in listpages]
        output.close()
