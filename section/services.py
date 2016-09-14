def recursive_search(section_dict, section_id):
    if section_dict['id'] == section_id:
        return section_dict
    else:
        for child_section in section_dict['children']:
            result = recursive_search(child_section, section_id)
            if result:
                return result

    return None
