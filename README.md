# Cormorant_Counting

This is a project for the William and Mary Center for Geospatial Analysis. It counts the black Cormorant birds in the image. The code begins by dividing the inputted image into smaller 100 pixel by 100 pixel sub images. Then it increases the contrast, recolors the dark pixels (likely birds) black then red. The birds that are counted are recolored blue. The number of birds in each sub image are added to get the total number of birds in the original image. We will proceed to explain the code by defining each function and how it interacts with the other functions to count the number of birds in the image. 

An example of an original 100 by 100 pixel subimage and a processed subimage with bird total in the image name are provided (called 769same.jpeg and 769_5.jpeg). 

See PDF for a detailed guide of how to use code and how code works. 
