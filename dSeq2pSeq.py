import requests
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import sys

#dSeq2pSeq v0.0
#Created by P.D.M.Dilan
#2020/05/01


banner=(r"""

  __  ____                       ___           ____                        
 /\ \/\  _`\                   /'___`\        /\  _`\                      
 \_\ \ \,\L\_\     __     __  /\_\ /\ \  _____\ \,\L\_\     __     __      
 /'_` \/_\__ \   /'__`\ /'__`\\/_/// /__/\ '__`\/_\__ \   /'__`\ /'__`\    
/\ \L\ \/\ \L\ \/\  __//\ \L\ \  // /_\ \ \ \L\ \/\ \L\ \/\  __//\ \L\ \   
\ \___,_\ `\____\ \____\ \___, \/\______/\ \ ,__/\ `\____\ \____\ \___, \  
 \/__,_ /\/_____/\/____/\/___/\ \/_____/  \ \ \/  \/_____/\/____/\/___/\ \ 
                             \ \_\         \ \_\                      \ \_\
                              \/_/          \/_/                       \/_/

~~ Nucleotide (DNA/RNA) sequence to a protein sequence translation tool ~~
                    ~~ dSeq2pSeq version 0.0 ~~

        ~~ Select .fasta file or text file for translation ~~

                """)

print(banner)
print('\n')

try:
    #graphical window open
    Tk().withdraw() 
    filename = askopenfilename( title='Choose a file') 

    if not filename:
        print("Cancelled")
        sys.exit()

    #read DNA sequence    
    sequences = []
    if filename.endswith('.fasta'):
        with open(filename, "r") as f:
            ls = f.readlines()[1:]
            for i in ls:
                sequences.append(i.rstrip("\n"))
    elif filename.endswith('.txt'):
        with open(filename, "r") as f:
            ls = f.readlines()
            for i in ls:
                sequences.append(i.rstrip("\n"))
    else:
        print("File extension is not a .fasta or .txt !")
        sys.exit()



    print('Starting the process :\n')

    #get data from https://web.expasy.org API
    url='https://web.expasy.org/cgi-bin/translate/dna2aa.cgi?dna_sequence=%s&output_format=%s' % (sequences,'fasta')

    data=requests.get(url)
    sData=(data.content).decode('utf-8')
    cleanedSdata=re.sub(r'\>.*?\:', '', sData)

    #save data to text file
    if filename.endswith('.txt'):
        filename=re.sub(r'\.*?', '', filename)+'out'
        filenameSave =Path(filename).with_suffix('.txt')
    else:
        filenameSave =Path(filename).with_suffix('.txt')

    with open(filenameSave, "w") as text_file:
        text_file.write(cleanedSdata)

    #print data 
    print(cleanedSdata)
    print('Finished !')

except (requests.HTTPError , requests.ConnectionError):
    print('Please check your internet connection !\n')
    exit()