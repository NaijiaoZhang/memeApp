

import os

text_file = open("output.txt", "w")
indir = 'static/media/faces_02'
memeid = 853

for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        text_file.write("INSERT INTO Meme VALUES(%i, '%s','../static/media/faces_02/%s','%s');"%(memeid, f[0:-4], f, f) + '\n')
        memeid += 1
        
