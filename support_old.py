from csv import reader
from os import walk
import pygame

def import_csv_layout(path):  # argument should be the file path
    terrain_map = []  # create list for terrain map
    with open(path) as level_map:  # open the path as level map
        layout = reader(level_map, delimiter=',')  # layout is the reader function on level map with delimiter comma for spacing
        for row in layout:  # for each row in layout (runs through all rows)
            terrain_map.append(list(row))  # append row as a list to the terrain map list creating 2D list
        return terrain_map  # return terrain map

def import_folder(path):  # import folders
    surface_list = []  # create list of surfaces to append surfaces to

    for _, __, img_files in walk(path):  # for 3 parameters in walk function on the path (enables you to walk through a folders content)
        for image in img_files:  # for all the images in image files
            full_path = path + '/' + image  # the full path is equal to the path plus a slash plus the image
            image_surf = pygame.image.load(full_path).convert_alpha()  # image surface is equal to the loaded image of the full path
            surface_list.append(image_surf)  # append the image surface to the surface list

    return surface_list  # return all surfaces in the list

