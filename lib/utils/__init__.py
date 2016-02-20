

def file_contents(filename=None, content=None):
    """
    Just return the contents of a file as a string or write if content
    is specified. Returns the contents of the filename either way.

    :param content:
    :param filename:
    """
    if content:
        f = open(filename, 'w')
        f.write(content)
        f.close()

    try:
        f = open(filename, 'r')
        text = f.read()
        f.close()
    except:
        text = None

    return text
