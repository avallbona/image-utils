#!/usr/bin/python
import shutil
from os import listdir, remove, mkdir
from os.path import isfile, join

from PIL import Image, ImageOps


def pad_counter(value: int, total_digits=2):
    return format(value, '0{}'.format(total_digits))


def get_files(path: str):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles.sort()
    return onlyfiles


def create_output_dir(outdir: str):
    try:
        shutil.rmtree(outdir)
    except FileNotFoundError:
        pass
    mkdir(outdir)


def generate_filename(path: str, file_prefix: str, counter: str):
    return f'{path}/{file_prefix}{counter}.jpg'


def remove_file(filename: str):
    try:
        remove(filename)
    except OSError:
        pass


# initial values
my_path = '/home/avallbona/Desktop/puerto_cala_figuera/novesfotos'
out_dir_name = 'out'
path_out = f'{my_path}/{out_dir_name}'
prefix = 'puerto4_'
prefix_mini = 'minipuerto4_'
new_width = 800
new_height = 600
new_width_mini = 150
new_height_mini = 150
# new_width_mini = 125
# new_height_mini = 101


def main():
    print('Starting...')
    print(f'Creating output dir {path_out}')
    create_output_dir(path_out)

    for i, item in enumerate(get_files(my_path), start=1):
        origin = f'{my_path}/{item}'
        try:
            im = Image.open(origin)
            w, h = im.size

            str_counter = pad_counter(i)
            new_name = generate_filename(path_out, prefix, str_counter)
            new_name_mini = generate_filename(path_out, prefix_mini, str_counter)

            remove_file(new_name)
            remove_file(new_name_mini)

            print(f'Generating: {new_name}')

            if w > h:
                # horitzontal
                new_size = (new_width, new_height)
            else:
                # vertical
                new_size = (new_height, new_width)
            new_size_mini = (new_width_mini, new_height_mini)

            # gran
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(new_name, 'JPEG')

            im = ImageOps.fit(im, new_size_mini, method=Image.ANTIALIAS)
            im.save(new_name_mini, 'JPEG')

        except Exception as e:
            print(e)

    print('End of the proces')


if __name__ == '__main__':
    main()
