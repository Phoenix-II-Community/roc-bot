# Pythono3 code to rename multiple  
# files in a directory or folder 
  
# importing os module 
import os 
import json
from pathlib import Path
# Function to rename multiple files 
home_dir = Path.home()
emojiname_json = open(('{hd}/scripts/apex-bot/res/shipemojiname.json').format(hd=home_dir))
emojiname_data = json.load(emojiname_json)


def emojirenamefunc():    
    for filename in os.listdir(): 
        print(filename)
        #if filename == 
        #dst ="Hostel" + str(i) + ".jpg"
        #src ='xyz'+ filename 
        #dst ='xyz'+ dst 
            
        # rename() function will 
        # rename all the files 
        #os.rename(src, dst) 
