import extractor.html
import extractor.pdf

'''
    The resulted toc tree is in a recursive dictionary, for example

    ===============================================================
    {
        "title": "section 1",
        "link": "sample/part1.htm",
        "page": 1,
        "children": [
            {
                "title": "section 1.1",
                "link": "sample/part2.htm",
                "page": 2,
                "children": []
            }
        ]
    }
    ===============================================================

    title:      the title as in the table of the content
    link:       the relative file name of the html page
    page:       the page number of this section
    children:   a list of immediate children of the current heading
'''

# keys in dict
TITLE = 'title'
LEVEL = 'level'
LINK = 'link'
CHILDREN = 'children'
PAGE = 'page'


def _get_list(toc_html_path, pdf_file_path):
    tags = extractor.html.get_toc_tags(toc_html_path)
    bookmarks = extractor.pdf.extract_bookmarks(pdf_file_path)
    array = []
    for tag, bookmark in zip(tags, bookmarks):
        array.append({
            TITLE: tag.text,
            LINK: tag['href'],
            LEVEL: int(tag['class'][0].replace('toc', '')) + 1,
            PAGE: bookmark[PAGE]
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
                PAGE: current[PAGE],
                CHILDREN: []
            })

        if next_level > level + 1:
            _recursive_parse_list(node[CHILDREN][-1], level + 1, array)


def _parse_list(book_title, array):
    root = {
        TITLE: book_title,
        LINK: None,
        PAGE: 1,
        CHILDREN: []
    }
    _recursive_parse_list(root, 0, array)
    return root


def construct_toc_tree(book_title, toc_html_path, pdf_file_path):
    array = _get_list(toc_html_path, pdf_file_path)
    return _parse_list(book_title, array)
