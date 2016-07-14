import os

from section.models import *


# given a Section object, get the Book object that it belongs to
def get_book(section):
    while True:
        try:
            adjacency = Adjacency.objects.get(child=section)
            section = adjacency.parent
        except Adjacency.DoesNotExist:
            return Book.objects.get(root_section=section)


# get the absolute file path of the extracted content of this section on the local file system
def get_file_path(section):
    steps = list()
    steps.append(section.slugified + '.txt')

    if section.has_children:
        steps.append(section.slugified)

    current = section
    while True:
        try:
            adjacency = Adjacency.objects.get(child=current)
            current = adjacency.parent
            steps.append(current.slugified)
        except Adjacency.DoesNotExist:
            break
    result = Book.objects.get(root_section=current).target_dir_path
    steps.reverse()
    for path in steps:
        result = os.path.join(result, path)
    return result


# get the extracted content of a section (excl. any sub section)
def get_content(section):
    with open(get_file_path(section)) as file:
        return file.read()


# get the extracted content of a section and all its sub sections
def get_content_aggregate(section):
    result = ''
    if section.has_children:
        for path, subdirs, files in os.walk(os.path.dirname(get_file_path(section))):
            for filename in files:
                file = os.path.join(path, filename)
                with open(file) as f:
                    result += f.read() + ' '

    else:
        with open(get_file_path(section)) as f:
            result = f.read()

    return result



