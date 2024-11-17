import re
from markdown2 import Markdown
from difflib import get_close_matches
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def markdown_md(title):
    mark = Markdown()
    tit, enc = get_entry(title)
    enc = mark.convert(enc)
    return tit, enc


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename.lower())
                       for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def del_entry(title):
    filename = f"entries/{title}.md"
    default_storage.delete(filename)


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        # capitalize title
        title = str(title).lower()
        titles = list_entries()

        # check for query of search
        if title not in titles:
            if closest_matches := get_close_matches(title, titles, n=1):
                title = closest_matches[0]
        # ...
        f = default_storage.open(f"entries/{title}.md")
        return title, f.read().decode("utf-8")
    except FileNotFoundError:
        return None
