# Pythono3 code to rename multiple  
# files in a directory or folder 
  
# importing os module 
import os

# Function to rename multiple files in the format
# friendlyship_##_skin_#_Normal@2x.png
# to ship_##_apex_#.png
def emojirenamefunc():
    for filename in os.listdir():
        tokens = filename.split('_')
        if len(tokens) == 5: #i want to try to make this into regex later
            newname = 'ship_'+ tokens[1] +'_apex_'+ tokens[3] + '.png'
        elif len(tokens) == 3:
            newname = 'ship_' + tokens[1] + '.png'
        else:
            newname = filename
        os.rename(filename,newname)
        
emojirenamefunc()

        # rename() function will 
        # rename all the files 
        #os.rename(src, dst) 
