from section.models import *


def get_children(section):
    return [adjacency.child for adjacency in Adjacency.objects.filter(parent=section)]


def get_parent(section):
    try:
        return Adjacency.objects.get(child=section)
    except Adjacency.DoesNotExist:
        return None


def recursive_search(section_dict, section_id):
    if section_dict['id'] == section_id:
        return section_dict
    else:
        for child_section in section_dict['children']:
            result = recursive_search(child_section, section_id)
            if result:
                return result

    return None
