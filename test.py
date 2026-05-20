import os

path = '/Users/Player3/Desktop/Zombies/Sprites'


print(os.listdir(path))

for folder in os.listdir(path):

    parentdir = folder
    path_to_dir = os.path.join(path,folder)

    # while 'png' not in os.listdir(path_to_dir):
    
    #     subdirs = os.listdir(path_to_dir)


print(12%6)