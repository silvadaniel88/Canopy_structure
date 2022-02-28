#  ISODATA Compute global image threshold using iterative isodata method.
#   LEVEL = ISODATA(I) computes a global threshold (LEVEL) that can be
#   used to convert an intensity image to a binary image with IM2BW. LEVEL
#   is a normalized intensity value that lies in the range [0, 1].
#   This iterative technique for choosing a threshold was developed by Ridler and Calvard .
#   The histogram is initially segmented into two parts using a starting threshold value such as 0 = 2B-1, 
#   half the maximum dynamic range. 
#   The sample mean (mf,0) of the gray values associated with the foreground pixels and the sample mean (mb,0) 
#   of the gray values associated with the background pixels are computed. A new threshold value 1 is now computed 
#   as the average of these two sample means. The process is repeated, based upon the new threshold, 
#   until the threshold value does not change any more.

#   Reference :T.W. Ridler, S. Calvard, Picture thresholding using an iterative selection method, 
#            IEEE Trans. System, Man and Cybernetics, SMC-8 (1978) 630-632.

# Developed by Daniel Augusto da Silva (danielaugusto@furb.br) with the help of Artur Ricardo Bizon for the Global LAI Project

import numpy as np
import os
import fnmatch
from skimage import img_as_ubyte
from skimage import io

#INFORM THE MAIN FOLDER WHERE THE SUBFOLDERS WITH THE HP ARE LOCATED (use foward slash "/")
Folder = 'follder'


#  START ISODATA THRESHOLD
def isodata ():
# Makes a copy of the original file, extracts the blue channel and its histogram    
    image_tresh = img.copy()
    blue = image_tresh[:,:,2]
    hist,bins = np.histogram (blue,256,[0,256])

# Set the initial mean bin (T)
    T = round(sum(map(np.prod, zip(bins, hist)))/sum(hist))
    T = int(T)
    T2 = 0
    newT = T
# Set the mean bin bellow T and above T and creates the new mean bin
    while T != T2:
        T = newT
        mu2 = sum(hist[0:newT])
        hist2 = hist[0:newT]
        MBT = round(sum(map(np.prod, zip(bins,hist2)))/mu2)

        mu3 = sum(hist[newT:256])
        hist3 = hist[newT:256]
        MAT = round(sum(map(np.prod, zip(bins,hist3)))/mu3)+T
        T2 = round(int((MAT + MBT)/2))
        newT = T2
        
# Applies the threshold (T) to the grayscale image         
        
    blue[blue > T] = 255     #set the pixels above the threshold to DN = 255
    blue[blue<255] = 0       #set the pixels below the threshold to DN = 0
    blue[blue == 255] = 100  #set the pixels above the threshold to DN = 100 to suit the standard of CAN_EYE V6.494  
    
    return (blue)
    
# END ISODATA


# Loop all sub-folders and apply the isodata algorithm (as described above) 
#   to all .jpg images in the folders
    
subfolders = os.listdir (Folder)
print ('These are your folders', subfolders)    
    
def walk_depth(folder, depth=0):
    '''Walk within folder with depth constraint'''
    folder = folder.rstrip(os.path.sep)
    assert os.path.isdir(folder)
    sep_count = folder.count(os.path.sep)
   
    for root, dirs, files in os.walk(folder):
        yield root, dirs, files
        sep_counter = root.count(os.path.sep)
        if sep_count + depth <= sep_counter:
            del dirs[:]
   
for root, dirs, files in walk_depth(Folder):
    for d in dirs:
        os.makedirs(os.path.join(Folder,d+"_Thresh"))
for root, dirs, files in os.walk(Folder):
    for d in dirs:
        if d+'_Thresh' in dirs:
            dirs.remove(d+'_Thresh')
        else:
            for file in files:
                if fnmatch.fnmatch(file, '*.JPG'):
                    print ('processing image\n','file = %s' % file)
                    img = io.imread (os.path.join(root, file))
                    cs = isodata()
                    io.imsave( os.path.join(root+"_Thresh", file)+"_tresh.TIFF", img_as_ubyte(cs)) 
                          
                    
    