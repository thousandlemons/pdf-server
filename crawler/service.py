import base64
import json
import os
from io import BytesIO

from wordcloud import WordCloud

from crawler.json_file import save_json
from crawler.page_text_extractor import extract_plain_text
from crawler.toc_tree import *
from section.models import *

NO_CONTENT_BASE64 = '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'

ID = 'id'


def recursive_extract(node, source, target, parent_section, book):
    print('[Info] Processing "' + node['title'] + '"')

    accumulated_text = ''

    # check if has children
    has_children = len(node[CHILDREN]) != 0

    # create Section entry
    section = Section.objects.create(book=book, title=node[TITLE], slugified=node[SLUGIFIED],
                                     has_children=has_children)
    section.save()

    # create Adjacency entry
    if parent_section is not None:
        adjacency = Adjacency.objects.create(parent=parent_section, child=section)
        adjacency.save()
    else:
        section.title = book.title
        section.save()
        book.root_section = section
        book.save()

    # if the current node have children
    if has_children:

        target = os.path.join(target, node[SLUGIFIED])

        # create target directory
        if not os.path.exists(target):
            os.mkdir(target)

        # loop through children and do recursion
        for child in node[CHILDREN]:
            child_text = recursive_extract(child, source, target, section, book)
            accumulated_text += child_text

    # save content of the current node
    with open(os.path.join(target, node[SLUGIFIED] + '.txt'), 'w+') as file:
        plain_text = extract_plain_text(os.path.join(source, node['link']))
        file.write(plain_text)

    # create base64 encoded word cloud image in Adjacency entry
    accumulated_text += plain_text
    if accumulated_text != '':
        wordcloud = WordCloud(width=1024, height=768).generate(accumulated_text)
        image = wordcloud.to_image()
        buffered = BytesIO()
        image.save(buffered, format='JPEG')
        base64_encoded = base64.b64encode(buffered.getvalue())
        section.word_cloud_base64 = str(base64_encoded, 'ascii')
    else:
        section.word_cloud_base64 = NO_CONTENT_BASE64
    section.save()

    # return accumulated text
    return accumulated_text


def reconstruct_tree(book):
    root_section = book.root_section

    root_node = dict()
    root_node[TITLE] = book.title

    recursive_reconstruct_tree(root_node, root_section, True)

    book.toc_json = json.dumps(root_node)
    book.save()


def recursive_reconstruct_tree(current, section, is_root):
    if isinstance(current, list):
        node = dict()
        current.append(node)
    else:
        node = current

    if is_root:
        is_root = False
    else:
        node[TITLE] = section.title

    node[SLUGIFIED] = slugify(node[TITLE])
    node[ID] = section.id
    node[CHILDREN] = list()

    if section.has_children:
        adjacencies = Adjacency.objects.filter(parent=section)
        for adjacency in adjacencies:
            recursive_reconstruct_tree(node[CHILDREN], adjacency.child, is_root)


def extract(book):
    source = os.path.dirname(book.toc_html_path)
    title = ntpath.basename(book.toc_html_path).replace('.html', '')
    target = book.target_dir_path

    # get the toc tree
    toc_tree = construct_toc_tree(title, os.path.join(source, title + '.html'))

    # create the target directory
    if not os.path.exists(target):
        os.mkdir(target)

    # save the toc tree in json format
    save_json(os.path.join(target, title + '.json'), toc_tree)

    # extract content
    recursive_extract(toc_tree, source, target, None, book)

    # reconstruct toc tree
    reconstruct_tree(book)

    # save is_processed flag
    book.is_processed = True
    book.save()
