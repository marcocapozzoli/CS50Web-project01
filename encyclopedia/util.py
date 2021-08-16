import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Retorna uma lista de todos os nomes de entradas da enciclopédia.
    filenames = é a lista de todos os arquivos listados na pasta entries
    re.sub(...) = substitui o ".md" por ""
    sorted = cria uma lista a partir de um iterável, que o filename
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
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


def get_entry(title):
    """
    Recupera uma entrada da enciclopédia por seu título. Se essa entrada não existir,
    a função retornará Nenhum.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None