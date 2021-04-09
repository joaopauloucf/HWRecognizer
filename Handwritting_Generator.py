# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:51:29 2020

@author: jleite
"""

from PIL import Image, ImageDraw, ImageFont, ImageTk, features
import os,random
import sys
import configparser
import cv2
import csv
import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
import Augmentor
import datetime
import warnings


def parse_input_file(path):
    filename = path
    
    label_text = []
    label = []
    target_text = []
    
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        label_text = next(csvreader)
        for row in csvreader:
            target_text.append(row)
            
    label_text = label_text[0].split("\t")
    print(label_text)
    
    return label_text,target_text

def parse_ini_file():
    config = configparser.ConfigParser()
 

    # parse existing file
    config.read('Config.ini')

    # read values from a section
    inputpath = config.get('CONFIG', 'inputpath')
    num_to_generate = config.getint('CONFIG', 'num_to_generate')
    savetype = config.get('CONFIG', 'save_as_type')
    distortion_variation = config.getint('CONFIG', 'distortion_variation')
    num_of_each = config.getint('CONFIG', 'num_var')
    
    return num_to_generate,num_of_each,savetype,inputpath,distortion_variation 
    

def get_target_text(target_text):
    text = random.choice(target_text)

    return text[0].replace('\t', '')

def select_random_font(path):
    
    font = random.choice(os.listdir(path)) #change dir name to whatever
    font = path + "\\" + font

    return font

def create_new_image(text):
    font = ImageFont.truetype(select_random_font("C:\John\FONT\FONT_TYPE"),  random.randint(40,70))
    text_width, text_height = font.getsize(text)
    snippet_width = text_width + 100
    snippet_height = text_height + 70

    text_image = Image.new('RGB', (snippet_width, snippet_height), (255,255,255))
    text_draw = ImageDraw.Draw(text_image)
    text_image,vertspace = draw_text(text_image,text_draw,text, font)
    
    return text_image,font,vertspace

def draw_background(input_image,label_text,vertspace):
    
    background_font = ImageFont.truetype(select_random_font("C:\John\FONT\LABEL_FONT"), 30)
    background_draw = ImageDraw.Draw(input_image)
    snippet_width,snippet_height = input_image.size

    background = random.randint(0,4)
    line_height = vertspace - random.randint(7,15)
    
    #returns normal image with no background
    if background == 0:
        input_image = input_image
    #returns image with line on the bottom
    elif background == 1:
        background_draw.line((0, snippet_height-line_height,snippet_width,snippet_height-line_height) ,fill=(0, 0, 0),width=random.randint(4,7))
    #returns iamge with boarder around the entire image
    elif background == 2:
        background_draw.line((0, snippet_height-line_height,snippet_width,snippet_height-line_height) ,fill=(0, 0, 0),width=random.randint(4,7))
        background_draw.line((0, 0,snippet_width,0) ,fill=(0, 0, 0),width=random.randint(4,7))
        background_draw.line((0, 0,0,snippet_height) ,fill=(0, 0, 0),width=random.randint(4,7))
        background_draw.line((snippet_width, 0,snippet_width,snippet_height) ,fill=(0, 0, 0),width=random.randint(4,7))

    
    if random.randint(0,1) == 1:
        background_draw.text((2, -4), get_label(label_text), font=background_font,fill=(0, 0, 0))
        
    input_image = sp_noise(np.array(input_image),random.uniform(-.05, .09))
    
    return input_image

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def draw_text(image,draw,text,font):
    charspace = random.uniform(-.5,.5)
    vertspace = random.randint(25,50)
    vertspace2 = vertspace
    horiznumber = random.randint(-4, 0)
    
    # use a truetype font
    for char in text:


        text_width, text_height = font.getsize(char)
        vertnumber = random.uniform(-float(text_height*.1), float(text_height*.05))
        horiznumber = horiznumber + random.uniform(-.5,.75)
        if char == ' ':
            horiznumber = horiznumber + 1


        draw.text((20+charspace, vertspace), char, font=font,fill=(0, 0, 0))
        charspace = charspace + text_width + horiznumber - float(text_width*.15)
        vertspace = vertspace + vertnumber
        
    return image, vertspace2
    

def get_label(label_text):

    return random.choice(label_text)

def generate_base_samples(x,num_of_each,savetype,path,variation):
    
    images =[]
    labels = []
    label_text = []
    target_text = []
    label_text,target_text =parse_input_file(path)

    for y in range(0,x):  

        images =[]
        labels = []
        frames = []
        
        unicode_text = get_target_text(target_text)
        text_image, font,vertspace = create_new_image(unicode_text)
        text_image = draw_background(text_image,label_text,vertspace)
        
        open_cv_image = np.array(text_image) 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        images.append(open_cv_image)
        labels.append(unicode_text)
        
        outx,outy = Augementation_Pipeline(images,labels,num_of_each,variation)
   
        for z in range(0,len(outy)):
            im = Image.fromarray(outx[z])
            open_cv_image = np.array(im) 
            # Convert RGB to BGR 
            open_cv_image = open_cv_image[:, :, ::-1].copy() 
         

  
            # Taking a matrix of size 5 as the kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4))
  
            img_erosion = cv2.erode(open_cv_image, kernel, iterations=1)
            img_dilation = cv2.dilate(open_cv_image, kernel, iterations=1)
            opening = cv2.morphologyEx(open_cv_image, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(open_cv_image, cv2.MORPH_CLOSE, kernel)
            gradient = cv2.morphologyEx(open_cv_image, cv2.MORPH_GRADIENT, kernel)

            frames.append(im)
            if savetype.upper() == "PNG":
                name = str(font.getname()[0]) + "_" + outy[z] + "_" +str(z) +"_" + str(y)
                cv2.imwrite(name + "_ORIG" + ".png", open_cv_image)
                #cv2.imwrite(name + "_EROS" + ".png", img_erosion)
                #cv2.imwrite(name + "_DILA" + ".png", img_dilation)
                #cv2.imwrite(name + "_OPEN" + ".png", opening)
                #cv2.imwrite(name + "_CLOS" + ".png", closing)
                #cv2.imwrite(name + "_GRAD" + ".png", gradient)
            
        if savetype == "GIF":
            name = outy[z] + "_" +str(y)+ ".gif"

            frames[0].save(name, format='GIF', append_images=frames[1:], save_all=True, duration=num_of_each, loop=0)
        
    return outx,outy
    
def Augementation_Pipeline(images,labels,size,variation):

    p = Augmentor.Pipeline()
    p.random_distortion(probability=.75, grid_width=random.randint(6+variation,8+variation), grid_height=random.randint(4+variation,7+variation), magnitude=random.randint(6+variation,9+variation))
    p.shear(.75, 2+(variation*.2), 2+(variation*.2))
    p.skew(.5,.1+(variation*.025))
    print("Start Set: " + str(datetime.datetime.now()))
    g = p.keras_generator_from_array(images,labels , scaled=False,batch_size=size)
    outx, outy = next(g)
    print("End Set: " + str(datetime.datetime.now()))
    return outx,outy


num_to_generate,num_of_each,savetype,inputpath,distortion_variation = parse_ini_file()

if num_to_generate > 10000:
    warnings.warn("Large number of samples are set to be generated, this operation may take some time")
if savetype not in ("PNG", "GIF"):
    warnings.warn("Improper Save As set, check Config.ini")
    sys.exit(0) # this exits your program with exit code 0
if os.path.exists(inputpath) == False:
    warnings.warn("Input Path does not exist, check Config.ini")
    sys.exit(0) # this exits your program with exit code 0
if distortion_variation > 3:
    warnings.warn("Distortion is very aggressive, expect poor sample output")

images =[]
labels = []

print("Start: " + str(datetime.datetime.now()))
generate_base_samples(num_to_generate,num_of_each,savetype,inputpath,distortion_variation)
print("End: " + str(datetime.datetime.now()))


 # You can also use np.reshape()
#print(images.shape)

#cv.imshow('Test', outx[0])
#cv.imshow('Test2', outx[1])
#cv.imshow('Test3', outx[2])
#cv.imshow('Test4', outx[3])


#p = Augmentor.DataPipeline(images,list(unicode_text))
#p.random_distortion(probability=.9, grid_width=4, grid_height=4, magnitude=8)
#p.shear(.6, 3, 3)
#p.skew(.6,.15)
#aumented_images,labels = p.sample(10)

