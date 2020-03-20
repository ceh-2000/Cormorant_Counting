#Name: Clare Heinbaugh and Emilio Luz-Ricca
#Date: March 19, 2020

from PIL import Image, ImageEnhance
from random import randint
import shutil
import os

global min_bird
global max_bird
global max_num_birds
global filename
global fuzziness


#######################################################################

#####USER CHANGES THESE VALUES

filename = "ex3.jpg" #name of the image to count birds
min_bird = 30 #minimum number of pixels that make up a bird
fuzziness = 200

#########################################################################


























max_bird = int(min_bird*2.5) #maximum number of pixels that make up a bird

def bird_color(color_tup):
    #sets the lower and upper RGB bounds for a bird
    thresh_red_lower = 0
    thresh_green_lower = 0
    thresh_blue_lower = 0
    thresh_red_upper = 80
    thresh_green_upper = 80
    thresh_blue_upper = 80
    
    #check color_tup against threshold values established above 
    if (color_tup[0] >= thresh_red_lower and color_tup[1] >= thresh_green_lower and color_tup[2] >= thresh_blue_lower and color_tup[0] < thresh_red_upper and color_tup[1] < thresh_green_upper and color_tup[2] < thresh_blue_upper):
        return True
    return False

def recur_bird(x, y, new_color, old_color):
    #base case if you reach an edge or something that is not part of a bird
    if (pix[x,y] != old_color or x < 0 or y < 0 or x >= width - 1 or y >= height - 1):
        return 0

    pix[x,y] = new_color #yes this pixel has been checked

    #recursion for all 4 directions
    return 1 + recur_bird(x + 1, y, new_color, old_color) + recur_bird(x - 1, y, new_color, old_color) + recur_bird(x, y + 1, new_color, old_color) + recur_bird(x, y - 1, new_color, old_color)


def check_bird(im3, my_counter):
    #increase image contrast so birds are more visible
    im4 = ImageEnhance.Contrast(im3).enhance(5)
    im4.save('step_2.jpeg')
    
    im = Image.open('step_2.jpeg')
    
    #establish image properties like pix, size, width, and height
    global pix
    pix = im.load()
    global size_of_image
    size_of_image = im.size
    global width
    width = size_of_image[0]
    global height
    height = size_of_image[1]

    #set starting values like a bird count, a count of continous red blobs that are not birds, and the bird dictionary
    not_birds = 0
    bird_count = 0
    bird_dict = {}

    #populate the bird dictionary with all of the pixels that meet the color requirements to potentially be a bird according to the function "bird_color"
    #recolor all potential bird pixels to black and non-bird pixels white
    for i in range(width):
        for j in range(height):
            color_tup = pix[i, j]
            if (bird_color(color_tup) == False):
                pix[i, j] = (255, 255, 255)
            else:
                pix[i, j] = (0, 0, 0)
                bird_dict[(i, j)] = 0

    #save the image
    im.save('step_3.jpeg')

    #use try-catch block to avoid recursion depth error (i.e. the water produces an error because it is black continously in some places)
    try:
        for x in range(width):
            for y in range(height):
                if (pix[x, y] == (0, 0, 0)):
                    #recolor any black pixel from the bird_dict red and all other black pixels connected to it and get the number of pixels
                    num_pixels = recur_bird(x, y, (255, 0, 0), (0, 0, 0))
                    #check to see if the number of pixels in the current blob exceeds the minimum number of pixels needed to be a bird
                    if (num_pixels > min_bird):
                        #recolor the blob blue to signify a bird has likely been found
                        recur_bird(x, y, (0, 0, 255), (255, 0, 0))
                        
                        #increase the bird count by 1
                        bird_count += 1
                        
                        #account for overlapping birds by dividing the number of pixels in the blob by the maximum number of pixels in a bird and then add the number of overlapping birds to the total number of birds
                        if (num_pixels > max_bird):
                            bird_count += (num_pixels - max_bird) // max_bird
                    else:
                        #keep track of continuous red blobs that are not big enough to be birds and can be used to identify the fuzzier water
                        not_birds += 1
    except RecursionError:
        #this error will be thrown if program tries to identify a large mass of dark water as a bird
        im.save('processed/' + str(my_counter) + '_REC_' + str(bird_count) + '.jpeg')
        return 0

    #if there are lots of collections of pixels that could be birds except that they don't meet the threshold, the image probably contains water and should be disgarded 
    if not_birds > fuzziness:
        im.save('processed/' + str(my_counter) + '_WATER_' + str(bird_count) + '.jpeg')
        return 0

    im.save('step_4.jpeg')
    
    #save the image with the number of birds found in the image and return the number of birds in the current sub-image
    im.save('processed/' + str(my_counter) + '_' + str(bird_count) + '.jpeg')
    return bird_count

def make_white(file_path):
    im = Image.open(file_path)

    #resize image so that it can be divided into neat 100 pixel by 100 pixel cropped images
    t_size = im.size
    t_new_width = ((im.size[0] // 100) * 100) + 100
    t_new_height = ((im.size[1] // 100) * 100) + 100

    #recolor the overhanging space white
    bob = Image.new("RGB", (t_new_width, t_new_height), color = (255, 255, 255))
    pixit = bob.load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pixit[x, y] = im.getpixel((x, y))
            
    return bob


if __name__ == "__main__":
    #make a "processed" folder
    try:
        shutil.rmtree('processed')
    except:
        print('"processed" doesn\'t exist yet')
    os.mkdir('processed')
    
    #make a "check_these" folder
    try:
        shutil.rmtree('check_these')
    except:
        print('"check_these" doesn\'t exist yet')
    os.mkdir('check_these')

    #set up initial image values
    yolo = make_white(filename)
    the_size = yolo.size
    print(the_size)
    x = 1
    
    #THIS IS THE ALL IMPORTANT BIRD COUNT
    num_of_birds = 0
    
    #iterate through all individual 100 by 100 pixel images
    for i in range(0, the_size[0], 100):
        for j in range(0, the_size[1], 100):
            sam = yolo.crop((i, j, i + 100, j + 100))
            sam.save('step_1.jpeg')
            sam.save('check_these/' + str(x) + 'same.jpeg')
            num_of_birds += check_bird(sam, x)
            x+=1

    #print number of birds
    print("Run number %s: %s birds in image" % (x, num_of_birds))
