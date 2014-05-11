#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 20, 2014

@author: connieschibber
'''
import urllib2
import os
import csv
import StringIO
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.converter import TextConverter
#import nltk
#from nltk.corpus import stopwords
#import string
#import logging
#from io import open
import codecs
import string
import collections


def link_to_pdf(url):
    """Read a website and extract PDF - Code will pass if the website doesn't work"""
    try:
        page = urllib2.urlopen(url)
        page_object = StringIO.StringIO(page.read())
        page.close()        
        return page_object
    except urllib2.URLError, e: 
        print e.args
        pass
    except urllib2.HTTPError, e: 
        print e.code
        pass

def pdf_to_text(page_object):
    """Parse PDF and return text"""
    parser = PDFParser(page_object)
    #Create a PDF document object that stores the document structure
    doc = PDFDocument(parser)
    # Connect the parser and document objects.
    parser.set_document(doc)
    doc.initialize('')
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF page aggregator object
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    text_content = []
    ### i = page number #without this it doesn't work
    ### page are items in page
    for i, page in enumerate(PDFPage.create_pages(doc)):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        for object in layout:
            if isinstance(object, LTTextBox) or isinstance(object, LTTextLine):
                trial = []
                trial.append(object.get_text())
                for word in trial:
                    text_content.append(word)                    
    return text_content

def write_file (folder, filename, filedata, flags='w'):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False
    if os.path.isdir(folder):
        try:
            file_obj = codecs.open(os.path.join(folder, filename), encoding='utf-16', mode='w', errors='ignore')
            for item in filedata:
                file_obj.write("%s\n" % item)
            file_obj.close()
            result = True
        except IOError:
            print "ERROR WRITE FILE"
            pass
    return result


def clean_Spanish_letters(myname):
    'clean Spanish text -- re.match and re.search often dont work with some characters'
    myname = str(myname)
    myname = re.sub('á', 'a', myname)
    myname = re.sub('Á', 'A', myname)
    myname = re.sub('é', 'e', myname)
    myname = re.sub('É', 'E', myname)
    myname = re.sub('í', 'i', myname)
    myname = re.sub('í', 'I', myname)
    myname = re.sub('Ó', 'O', myname)
    myname = re.sub('ó', 'o', myname)
    myname = re.sub('ú', 'u', myname)
    myname = re.sub('Ú', 'U', myname)
    myname = re.sub('ñ', 'n', myname)
    myname = re.sub('Ñ', 'N', myname)
    return(myname)

##Use the following If you are using PDF files 
## comment URL info and function and FEED folder w/PDFS ###

#url = "http://www.camara.cl/pdf.aspx?prmID=4803+&prmTIPO=TEXTOSESION"
#  files here
#path_save = "/Users/connieschibber/RDirectory/Dissertation/"
#filename = "PRUEBACHILE3.txt"
#try: 
#    page = link_to_pdf(url)
#    print 'url read'
#    page_pdf = pdf_to_text(page)
#    print 'pdf transformed'
#    new_text = [] 
#    # clean text - erase - and substitute some characters
#    for word in page_pdf:
#        word = re.sub('-', '', word) 
#        word = clean_Spanish_letters(word)
#        new_text.append(word)   
#    write_file(folder=path_save, filename=filename, filedata=new_text)
#    print "ready"
#    print '------'
#except PDFSyntaxError:
#    print "Error - NOT A PDF"  
#    print "------"
#    pass           

##### 
 # Here open TEXT file just saved -- You do not have to save text file -- This is an example
 #####
f = codecs.open("/Users/connieschibber/RDirectory/Dissertation/PRUEBACHILE3.txt", encoding='utf-16', errors='ignore')
text = f.read()
text.strip() # strip all extra spaces
#print text
trial = []
trial2 = []
# example 1 - phrase 'votacion forma economica'
for voto in re.finditer(r'vota*\w+', text):
    n = int(voto.end())
#    print n
    texit = text[(n - 4):(n + 30)]
    texit = re.sub(r'\s+', '', texit) #erase all spaces
    if re.findall(r'formaeco*', texit): 
        trial.append(text[n:(n + 30)])
    else:
        pass
print 'example 1'    
print trial
# example 2 -phrase 'Votaron por la afirmativa los siguientes' (Step 2 in Instructions)
# Since we stripped spaces it turns as below
for voto in re.finditer(r'Votar*', text):  ## Capital letter is IMPORTANT
    n = int(voto.end())
#    print n
    texit = text[(n - 4):(n + 30)]
    texit = re.sub(r'\s+', '', texit)
#    print texit
    if re.findall(r'porlaafirmativa*', texit): 
        trial2.append(text[n:(n + 30)])
    else:
        pass
print 'example 2'    
print trial2



print '----- The End -----'
