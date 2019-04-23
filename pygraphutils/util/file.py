import os


def mkdir(dir: str) -> bool:
    try:
        os.makedirs(dir)
        return True
    except OSError:
        return False


def basename(filename):
    return os.path.basename(os.path.splitext(filename)[0])


def ext(filename):
    return filename.split(".")[-1]


def get_filenames(path, ext=""):
    files = []
    for file in os.listdir(path):
        if not ext or file.endswith(".%s" % ext):
            files.append(os.path.join(path, file))
    return sorted(files)
