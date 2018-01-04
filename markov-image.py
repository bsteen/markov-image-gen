from PIL import Image
from random import randint
import sys
# Only works with images encoded with 3-layer color (RGB)

# Contains a pixel's value and its neighbors
class Pixel():
    def __init__(self, rgb_val):
        self.rgb_value = rgb_val
        self.neighbors = []     # Contains all pixel data (RGB values) that has been seen around this give pixel
                                # Each time an instance of this pixel is found, its 8 neighboring pixels are
                                # added to this list

    def get_rand_neighbor(self):
        max_index = len(self.neighbors) - 1
        
        if max_index == -1:
            return
        else:
            index = randint(0, max_index)
            return self.neighbors[index]

# Manages the list of pixels; Has functions to manipulate the list
class Manage_Pixels():
    def __init__(self):
        self.pixel_list = []    # List containing only unique pixels and thier neighbors
        
    # Returns index in pixel_list if rgb_val is already present
    def find_pixel_index(self, rgb_val):
        for i in range(0, len(self.pixel_list)):
            if rgb_val == self.pixel_list[i].rgb_value:
                return i
        return -1
        
    # Inserts a pixel into pixel_list; If an identical pixel (has same rgb_value) is already in
    # the list, just add to the neighboring values;
    # Otherwise, create a new entry and then add the neighbors
    def insert_pixel(self, rgb_val, nb):
        index = self.find_pixel_index(rgb_val)
        
        if index == -1:
            px = Pixel(rgb_val)
            self.pixel_list.append(px)
            index = len(self.pixel_list) - 1    # Put new pixel entry at end of the list
            
        for i in range(0, len(nb)):
            self.pixel_list[index].neighbors.append(nb[i])
    
    # Get a random rgb value from the pixel list
    # Used to start the creation of a new image
    def get_rand_pixel_rgb_value(self):
        index = randint(0, len(self.pixel_list) - 1)
        return self.pixel_list[index].rgb_value
    
    # Given a previous RGB value, return an RGB value that is likely to appear
    # next to it
    def get_next_rgb_value(self, prev_rgb_val):
        index = self.find_pixel_index(prev_rgb_val)
        
        if index == -1:
            print("Pixel", prev_rgb_val ,"not found; returning random RGB value")
            return self.get_rand_pixel_rgb_value()
        else:
            return self.pixel_list[index].get_rand_neighbor()

if __name__== "__main__":
    
    if len(sys.argv) != 2:
        print("Provide image file name (python3 markov-image.py <file>)")
        exit(1)
    else:
        file_name = str(sys.argv[1])
        
    try:
        image = Image.open(file_name)
    except OSError:
        print("Image", file_name, "was not found")
        exit(1)
        
    width, height = image.size
    mp = Manage_Pixels()
    
    print("Reading in image...")
    # Record all data in the image
    for y in range(0, height):
        if y % 10 == 0:
            print(y , "/", height, "rows proccessed")
            
        for x in range(0, width):
            
            nb = [] # List of 8 neighbors around a pixel
            
            if x == 0:
                nb.append(image.getpixel((x,y)))    # Out of bounds indexes will just be replaced with the current pixel
                nb.append(image.getpixel((x,y)))
                nb.append(image.getpixel((x,y)))
            else:
                if y == 0:
                    nb.append(image.getpixel((x,y)))
                else:    
                    nb.append(image.getpixel((x-1,y-1)))
                
                if y == height - 1:
                    nb.append(image.getpixel((x,y)))
                else:
                    nb.append(image.getpixel((x-1,y+1)))
                
                nb.append(image.getpixel((x-1,y)))
            
            if x == width - 1:
                nb.append(image.getpixel((x,y)))
                nb.append(image.getpixel((x,y)))
                nb.append(image.getpixel((x,y)))
            else:
                if y == 0:
                    nb.append(image.getpixel((x,y)))
                else:
                    nb.append(image.getpixel((x+1,y-1)))
                
                if y == height - 1:
                    nb.append(image.getpixel((x,y)))
                else:
                    nb.append(image.getpixel((x+1,y+1)))

                nb.append(image.getpixel((x+1,y)))  
            
            if y == 0:
                nb.append(image.getpixel((x,y)))
            else:
                nb.append(image.getpixel((x,y-1)))
            
            if y == height - 1:
                nb.append(image.getpixel((x,y)))
            else:
                nb.append(image.getpixel((x,y+1)))
            
            mp.insert_pixel(image.getpixel((x,y)), nb)
    
    print("Proccesing new image...")
    new_image = Image.new("RGB", image.size)
    for y in range(0, height):
        for x in range(0, width):
            if x == 0:
                new_image.putpixel((x,y), mp.get_rand_pixel_rgb_value())
            else:
                prev_rgb_val = new_image.getpixel((x-1, y))
                next_rgb_val = mp.get_next_rgb_value(prev_rgb_val)
                new_image.putpixel((x,y), next_rgb_val)
    
    new_image.save("output.jpg")
    print("Done")