from src.funcs import verify_mnt, remove_imgs_list, get_imgs_name

source = '/home/matheus/gdrive'
verify_mnt(source)
source += '/Legendas'

remove_imgs_list(get_imgs_name(source))
print(get_imgs_name(source))
