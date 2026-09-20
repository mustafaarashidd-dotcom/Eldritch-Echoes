from settings import *
from os.path import join
from os import walk

# game functions
def check_connections(radius, entity, target, tolerance = 30):  # this check connections is to see if player and character are within the right radius
    relation = vector(target.rect.center) - vector(entity.rect.center)  # create the relation being the difference between their vectors (distance between them in vector form)
    if relation.length() < radius:  # if the magnitude or length of the relation vector is less than the radius then
        if abs(relation.y) < tolerance:  # check if the absolute value for relations y component is less than the tolerance
            return True
            # all conditions met then return true so we can manipulate check connections function in if statements for the dialog tree class

def import_image(*path, alpha = True, format = 'png'):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

def import_tilemap(cols, rows, *path):
    frames = {}
    surf = import_image(*path)
    cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
    for col in range(cols):
        for row in range(rows):
            cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
            cutout_surf = pygame.Surface((cell_width, cell_height))
            cutout_surf.fill('green')
            cutout_surf.set_colorkey('green')
            cutout_surf.blit(surf, (0,0), cutout_rect)
            frames[(col, row)] = cutout_surf
    return frames

def import_folder_dict(*path):
    frames = {}
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames[image_name.split('.')[0]] = surf
    return frames

def attack_importer(*path):
    attack_dict = {}
    for folder_path, _, image_names in walk(join(*path)):
        for image in image_names:
            image_name = image.split('.')[0]
            attack_dict[image_name] = list(import_tilemap(4, 1, folder_path, image_name).values())
    return attack_dict

def audio_importer(*path):
    files = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            files[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)
    return files