import os

from PIL import Image


class HelloPhoto(object):

    def __init__(self):
        pass

    @staticmethod
    def transfer_jpg_to_webp(path):

        def _do(path_file):
            print('transfer_jpg_to_webp', path_file)
            try:
                Image.open(path_file).convert("RGB").save(path_file + '.webp', 'WEBP')
            except Exception as e:
                print("cannot convert", path_file, e)

        # file
        if os.path.isfile(path):
            _do(path)
            return

        # folder
        if os.path.isdir(path):
            for f in os.listdir(path):
                _do(os.path.join(path, f))
            return

        # link or other
        print('path: %s is a link or other file' % path)
        return

    @staticmethod
    def create_thumbnail(path, size=(640, 360)):

        def _do(_path_file):
            print('create_thumbnail', _path_file)
            try:
                im = Image.open(_path_file)
                width, height = im.size

                width_16_9 = width
                height_16_9 = int(width_16_9 / 16.0 * 9.0)
                _size = (
                    0,
                    int((height - height_16_9) / 2),
                    width_16_9,
                    int((height - height_16_9) / 2) + height_16_9
                )
                region = im.crop(_size)
                # region.resize(size)
                region.thumbnail(size)
                region.save(_path_file + '.webp', 'WEBP')
            except Exception as e:
                print("cannot convert", _path_file, e)

        # file
        if os.path.isfile(path):
            _do(path)
            return

        # folder
        if os.path.isdir(path):
            for f in os.listdir(path):
                _do(os.path.join(path, f))
            return

        # link or other
        print('path: %s is a link or other file' % path)
        return

    @staticmethod
    def create_markdown(path):
        pass

    @staticmethod
    def renew_home_page(self):
        pass


if __name__ == '__main__':
    HelloPhoto.transfer_jpg_to_webp('/home/z04014/Pictures')
    # HelloPhoto.create_thumbnail('/home/Pictures')
