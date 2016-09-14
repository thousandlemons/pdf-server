import json
import logging
import os

import extractor.html
import extractor.pdf
import extractor.toc
from content.models import Content
from section.models import Section
from section.serializers import SectionInTocSerializer
from version.models import Version

ID = 'id'


def _recursive_extract(node, source, parent_section, previous_section, book):
    logging.info('Processing "{section_title}"'.format(section_title=node['title']))
    print('Processing "{section_title}"'.format(section_title=node['title']))

    # create Section entry
    section = Section.objects.create(book=book, title=node[extractor.toc.TITLE], page=node[extractor.toc.PAGE],
                                     previous=previous_section, has_children=(len(node[extractor.toc.CHILDREN]) != 0))
    section.save()

    # update previous_section.next
    if previous_section is not None:
        previous_section.next = section
        previous_section.save()

    # set parent or update book.root_section
    if parent_section is not None:
        section.parent = parent_section
        section.save()
    else:
        book.root_section = section
        book.save()

    # create Content entry
    version = Version.objects.order_by('id')[0]
    plain_text = extractor.html.extract_plain_text(
        os.path.join(source, node['link'])) if parent_section is not None else ''
    content = Content.objects.create(version=version, section=section, text=plain_text)
    content.save()

    # process all descendants recursively
    previous = section
    for child in node[extractor.toc.CHILDREN]:
        next_ = _recursive_extract(child, source, section, previous, book)
        previous.next = next_
        previous = next_

    return previous


def _reconstruct_tree(book):
    root_section = book.root_section

    root_node = dict()

    _recursive_reconstruct_tree(root_node, root_section)

    book.toc_json = json.dumps(root_node)
    book.save()


def _recursive_reconstruct_tree(current, section):
    if isinstance(current, list):
        node = dict()
        current.append(node)
    else:
        node = current

    node.update(SectionInTocSerializer(section).data)
    node[extractor.toc.CHILDREN] = list()

    if section.has_children:
        children = Section.objects.filter(parent=section)
        for child in children:
            _recursive_reconstruct_tree(node[extractor.toc.CHILDREN], child)


def extract(book):
    # update total number of pages
    book.number_of_pages = extractor.pdf.get_num_of_pages(book.pdf_path)
    book.save()

    # get variables
    source = os.path.dirname(book.toc_html_path)

    # get the toc tree
    toc_tree = extractor.toc.construct_toc_tree(book.title, book.toc_html_path, book.pdf_path)

    # create default version if no entry exists in Version table
    if not Version.objects.all():
        version = Version.objects.create(name='Raw')
        version.save()

    # recursively extract content
    _recursive_extract(toc_tree, source, None, None, book)

    # reconstruct toc tree
    _reconstruct_tree(book)

    # update is_processed flag
    book.is_processed = True
    book.save()
