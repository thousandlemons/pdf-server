from section.models import *


def get_children(section):
    return [adjacency.child for adjacency in Adjacency.objects.filter(parent=section)]


def get_parent(section):
    try:
        return Adjacency.objects.get(child=section)
    except Adjacency.DoesNotExist:
        return None
