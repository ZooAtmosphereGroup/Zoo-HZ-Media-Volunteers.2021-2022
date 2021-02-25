import os

from PIL import Image


class HelloPhoto(object):
    url_home = 'https://zooatmospheregroup.github.io/Zoo-HZ-Media-Volunteers'

    def __init__(self):
        pass

    @staticmethod
    def mkdir_if_not_exist(path):
        if os.path.exists(path) and os.path.isdir(path):
            return
        os.makedirs(path)

    @classmethod
    def transfer_jpg_to_webp(cls, path_in, path_out):
        cls.mkdir_if_not_exist(path_out)

        def _do(_path_file):
            print('transfer_jpg_to_webp', _path_file)
            try:
                _, _f = os.path.split(_path_file)
                _path = os.path.join(path_out, _f)
                Image.open(_path_file).convert("RGB").save(_path + '.webp', 'WEBP')
            except Exception as e:
                print("cannot convert", _path_file, e)

        # file
        if os.path.isfile(path_in):
            _do(path_in)
            return

        # folder
        if os.path.isdir(path_in):
            for f in os.listdir(path_in):
                _do(os.path.join(path_in, f))
            return

        # link or other
        print('path: %s is a link or other file' % path_in)
        return

    @classmethod
    def create_thumbnail(cls, path_in, path_out, size=(640, 360)):
        cls.mkdir_if_not_exist(path_out)

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
                _, _f = os.path.split(_path_file)
                _path = os.path.join(path_out, _f)
                region.save(_path + '.webp', 'WEBP')
            except Exception as e:
                print("cannot convert", _path_file, e)

        # file
        if os.path.isfile(path_in):
            _do(path_in)
            return

        # folder
        if os.path.isdir(path_in):
            for f in os.listdir(path_in):
                _do(os.path.join(path_in, f))
            return

        # link or other
        print('path: %s is a link or other file' % path_in)
        return

    @classmethod
    def resize_with_the_same_ratio(cls, path_in, path_out, size_max=3200):
        cls.mkdir_if_not_exist(path_out)

        def _do(_path_file):
            print('resize_with_the_same_ratio', _path_file)
            try:
                im = Image.open(_path_file)
                width, height = im.size

                if width >= height:
                    height = int(height / (width / size_max))
                    width = size_max
                else:
                    width = int(width / (height / size_max))
                    height = size_max

                _, _f = os.path.split(_path_file)
                _path = os.path.join(path_out, _f)
                im.resize((width, height)).save(_path + '.%s.webp' % size_max, 'WEBP')
            except Exception as e:
                print("cannot convert", _path_file, e)

        # file
        if os.path.isfile(path_in):
            _do(path_in)
            return

        # folder
        if os.path.isdir(path_in):
            for f in os.listdir(path_in):
                _do(os.path.join(path_in, f))
            return

        # link or other
        print('path: %s is a link or other file' % path_in)
        return

    @classmethod
    def render_markdown(cls, path_in):
        path_out = path_in.replace('/static/images/', '/mds/')
        path_out_head, tail = os.path.split(path_out)
        cls.mkdir_if_not_exist(path_out_head)

        if not os.path.exists(path_in) or not os.path.isdir(path_in):
            print('path: %s is not exist or is not dir' % path_in)
            return

        md_head = """---
layout: default
---
### render for path: %s

""" % path_in
        md_item = """### {size}, {name}, {message}
![{name}]({path})

"""
        md = ''
        md += md_head
        for f in os.listdir(path_in):
            # /home/xxx/static/images/webp/zzz/a.webp
            path_abs_f = os.path.join(path_in, f)
            size = round(os.path.getsize(path_abs_f) / 1024 / 1024, 2)
            size_str = 'size: %sM' % size

            # url_home/static/images/webp/zzz/a.webp
            path_relative_f = path_abs_f[path_abs_f.find('/static/images/'):]
            path = cls.url_home + path_relative_f
            item = md_item.format(size=size_str, name=f, path=path, message='')
            md += item

        with open(os.path.join(path_out_head, tail + '.md'), 'w') as f:
            f.write(md)
        return

    @classmethod
    def render_home_page(cls, path_in):
        pass


if __name__ == '__main__':
    # HelloPhoto.transfer_jpg_to_webp(
    #     r'C:\-C\Zoo-HZ-Media-Volunteers\static\images\raw\202005\20200520',
    #     r'C:\-C\Zoo-HZ-Media-Volunteers\static\images\webp\202005\20200520',
    # )
    HelloPhoto.resize_with_the_same_ratio(
        r'C:\-C\Zoo-HZ-Media-Volunteers\static\images\webp\202005\20200520',
        r'C:\-C\Zoo-HZ-Media-Volunteers\static\images\webp-resize-2000\202005\20200520',
        size_max=2000
    )
    HelloPhoto.render_markdown(
        r'C:/-C/Zoo-HZ-Media-Volunteers/static/images/webp-resize-2000/202005/20200520',
    )
    # HelloPhoto.render_markdown(
    #     '/home/Desktop/Cloud/Zoo-HZ-Media-Volunteers.2021-2022/static/images/webp/202102/test')
    # HelloPhoto.render_markdown(
    #     '/home/Desktop/Cloud/Zoo-HZ-Media-Volunteers.2021-2022/static/images/webp-resize-3200/202102/test')
    # HelloPhoto.create_thumbnail('/home/Pictures')
