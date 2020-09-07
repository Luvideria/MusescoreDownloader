## MusescoreDowloader
Creates PDFs from musescore's svgs/pngs from url

## Beginner instructions:

![download_zip_git](imgtuto/downloadzip.PNG)

![downloads](imgtuto/downloads.PNG)

Can be somewhere else. Type Ctrl+J in your browser, it's your download page, from here, try to find where the archive is located.

![extract](imgtuto/extract.PNG)

You can also drag and drop or copy paste wherever you want what's inside the archive when you double click it. Just be sure to know where to find it

You need to go in the directory

![powershell](imgtuto/powershell.PNG)

Open the powershell window. Type `python` inside. 

![type_python](imgtuto/type_python.PNG)
Normally, the appstore should pop up:

![install_python](imgtuto/install_python.PNG)

If it doesn't appear, go on the microsoft store yourself and type python3. Select 3.7 or 3.8, it doesn't matter for this script.
Once it is installed, go back to the powershell and type `pip`.
If you see some text, it means it worked. If it doesn't work, or you see red text, close the window and open it again like we did previously. Try to type `pip` again. If it doens't work, either python is not installed (let it finish!), or it is not in the path.
Use your favourite search engine to find how to add python in the Path for windows.

![pip_install](imgtuto/pip_install.PNG)

You should have some downloading going on, let it finish, it should be quick.
Now everything is ready!
Go to musescore and get the link as follows

![musescore_link](imgtuto/tuto.PNG)

Type in your link instead of the example one:

![execute_script](imgtuto/execute_script.PNG)

You can specify in which directory you want your output file(s) after the link.
You can also get the midi file (not always available)
Check below for examples.

## Not-Beginner instructions

To run this program you will need:

`pip install svglib fpdf pypdf2`

or with conda:

`conda install -c conda-forge svglib pypdf2`

sadly fpdf doesn't have a reliable release, but "-c viascience fpdf" looks ok

**Usage**: 
1) go on musescore.com and find the sheet you want

2) Copy the url, this is the inputUrl

3) Use the following command with your inputUrl
### `python musescore.py inputUrl destinationDirectory MidiTrueFalse`

*inputUrl* is the url from musescore
*destinationDirectory* is where the sheet will be written
*MidiTrueFalse* is 1 if the midi file should be downloaded, 0 or empty otherwise
example:

`python ./musescore.py https://musescore.com/user/4609986/scores/1749181`

will put the sheet in the current directory

`python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin`

will put the sheet in the chopin directory. Will be created if does not exist.

`python ./musescore.py https://musescore.com/user/4609986/scores/1749181 chopin 1`

will put the sheet and midi file in the chopin directory, will be created if does not exist. You can use "." (dot) if you want to use the current directory