import os
import json
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
from tqdm import tqdm

#ocr 
def recognize_text(img_path):
    #load and recognize text
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)

#load annotated data into datalist
f = open('data.json')
datalist = json.load(f)

def testing():
    result = 0
    totaliter = 0
    wrongconfs = []
    # iterate through each image for testing 
    for image in tqdm(os.listdir('images')):
        #manipulate image name to match annotated data id
        img_path = 'images/' + image 
        print (image + "\n")
        image = image.replace("_image", "")
        image = image.replace(".png", "")
        annotatedtext=""
        for data in datalist:
            if (data['id'] == image):
                annotatedtext = data['text']
                break
       #run ocr on the image
        resultdata = recognize_text(img_path)
        resulttext = ""
        resultconf = 0
        textnum = 0
        for data in resultdata:
            #concat all the text detected by OCR and add up the whole confidence level
            resulttext += data[1]
            #for testing confidence, take average confidence per text in the image
            resultconf += data[2]
            textnum += 1
        annotatedtext = annotatedtext.replace('\n','')
        annotatedtext = annotatedtext.replace(' ','')
        resulttext = resulttext.replace(' ','')
        #average resultconf
        avgconf = resultconf/textnum
        if (resulttext==annotatedtext):
            result+=1
        else:
            result-=1
            wrongconfs.append(avgconf)
        totaliter+=1
    if (len(wrongconfs)==0): 
        print('WOW perfect!')
    else:
        allmisses = ""
        for misses in wrongconfs:
            allmisses = allmisses + str(misses) + ','
        print ('Misses at: ' + allmisses)
    return result/totaliter * 100
result = testing()
print(result)


#split annotateddata/resultdata into list of characters





# result = recognize_text(im6)

# test contextual spell check
# postprocessing
# import contextualSpellCheck
# import spacy
# nlp = spacy.load("en_core_web_trf")
# contextualSpellCheck.add_to_pipe(nlp)



#  result will be a list of words as follows:
# (coordinates = [(top_left), (top_right), (bottom_right), (bottom_left)])
# (word)
# (confidence)

# print (result)



