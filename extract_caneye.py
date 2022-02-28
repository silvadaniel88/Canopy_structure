
# coding: utf-8

# In[2]:


import os
import fnmatch
import codecs 
from bs4 import BeautifulSoup as soup
import pandas as pd

#INFORM THE MAIN FOLDER WHERE THE SUBFOLDERS WITH THE .HTML ARCHIVES ARE LOCATED (use foward slash "/")
Folder = 'folder'


# In[181]:


def variables_extraction ():
    basefile = codecs.open(file, 'r')
    out_soup = soup(basefile, "html.parser")
    tables = out_soup.find_all('table')


    for i in tables:
        #print(i.text)
        # remove linhas em branco
        linhas = i.text.split("\n\n\n")
        #print(linhas)
        #print("\n")
        # itera pelo conteudo restante
        for index, palavra in enumerate(linhas):
            #caso o conteudo inicie com "Gap"
            if palavra.startswith("Gap"):
                # Remove caracteres indesejados
                CO.append (float(palavra[4:-2]))
            
            if palavra.startswith("PAI"):
               # Remove caracteres indesejados
               linhaDoValor = linhas[index + 1]
               value = (float(linhaDoValor[7:12]))
               LAI.append (value)
               
            if palavra.startswith("ALA"):
               # Remove caracteres indesejados
               linhaDoValor = linhas[index + 1]
               value = (float(linhaDoValor[7:12]))
               ALA.append (value) 
               
            if palavra.startswith("\n\nMEASURED FAPAR"):
                # Remove caracteres indesejados
                FAPAR.append (float(palavra[22:27]))
                
            if palavra.startswith("PAI\nEffective"):
            # Remove caracteres indesejados
                LAIef.append (float(palavra[13:18]))
    
    
    
# In[ ]:


subfolders = os.listdir (Folder)
print ('These are your folders', subfolders)

# creating the dataframe
SampleUnits = []
CO = []
LAI = []
FAPAR = []
ALA = []
LAIef = []
    
for root, dirs, files, in os.walk(Folder):
    for file in files:
        if fnmatch.fnmatch(file,'*.html'):
            print ("Extracting values from: ", 'file = %s' %file)
            file = (os.path.join(root,file))
            variables_extraction()
for su in subfolders:
    su = su[8:]
    SampleUnits.append(su)
CanopyData = pd.DataFrame(index = (SampleUnits))
CanopyData['CO'] = CO
CanopyData['LAI'] = LAI
CanopyData['FAPAR'] = FAPAR
CanopyData['ALA'] = ALA
CanopyData['LAIef'] = LAIef

CanopyData.to_csv('your_folder')
            

      


