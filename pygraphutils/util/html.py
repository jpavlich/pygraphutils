import re
from os.path import dirname
from urllib.parse import urlparse
from urllib.request import urlopen


def include_tags_in_html(in_html_str: str, base_path: str = None) -> str:

    # https://stackoverflow.com/a/8357518
    def is_absolute(url):
        return bool(urlparse(url).netloc)

    def open_file(url) -> str:
        if is_absolute(url) and base_path:
            with urlopen(url) as f:
                return f.read().decode("utf-8")
        else:
            url = "%s/%s" % (base_path, url)
            with open(url) as f:
                return f.read()

    def replace_tag(m):
        out_tag = m.group(1)
        included_file_url = m.group(2)
        included_file_str = open_file(included_file_url)
        return "<%s>%s" % (out_tag, included_file_str)

    script_regex = r'\s+<(script)[^>]*src="([^"]*)"[^>]*>'
    link_regex = r'\s+<(link)[^>]*href="([^"]*)"[^>]*>'

    tag_pattern = re.compile("|".join([script_regex, link_regex]))

    # tag_pattern = re.compile(script_regex)

    return re.sub(tag_pattern, replace_tag, in_html_str)
