from section.models import *


# given a Section object, get the Book object that it belongs to
def get_book(section):
    while True:
        try:
            adjacency = Adjacency.objects.get(child=section)
            section = adjacency.parent
        except Adjacency.DoesNotExist:
            return Book.objects.get(root_section=section)
