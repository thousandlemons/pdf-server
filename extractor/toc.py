import re

from bs4 import BeautifulSoup

'''
    The resulted toc tree is in a recursive dictionary, for example

    ===============================================================
    {
        "title": "section 1",
        "link": "sample/part1.htm"
        "children": [
            {
                "title": "section 1.1",
                "link": "sample/part2.htm"
                "children": []
            }
        ]
    }
    ===============================================================

    title:      the title as in the table of the content
    link:       the relative file name of the html page
    children:   a list of immediate children of the current heading
    '''

# keys in dict
TITLE = 'title'
LEVEL = 'level'
LINK = 'link'
CHILDREN = 'children'

SLUGIFIED = 'slugified'


def _get_list_from_html(book_title, toc_html_path):
    file = open(toc_html_path, 'r', encoding='utf-8')
    html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all(attrs={
        'class': re.compile('toc\d+')
    })
    array = [{
        TITLE: book_title,
        LINK: toc_html_path,
        LEVEL: 0
    }]
    for tag in tags:
        array.append({
            TITLE: tag.text,
            LINK: tag['href'],
            LEVEL: int(tag['class'][0].replace('toc', '')) + 1
        })
    return array


def _recursive_parse_list(node, level, array):
    while True:
        if not array:
            break

        next_level = array[0][LEVEL]

        if next_level < level + 1:
            break

        if next_level == level + 1:
            current = array.pop(0)
            node[CHILDREN].append({
                TITLE: current[TITLE],
                LINK: current[LINK],
                CHILDREN: []
            })

        if next_level > level + 1:
            _recursive_parse_list(node[CHILDREN][-1], level + 1, array)


def _parse_list(array):
    root = {
        TITLE: array[0][TITLE],
        LINK: array[0][LINK],
        CHILDREN: []
    }
    _recursive_parse_list(root, 0, array[1:])
    return root


def construct_toc_tree(book_title, toc_html_path):
    array = _get_list_from_html(book_title, toc_html_path)
    return _parse_list(array)
