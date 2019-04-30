from os.path import dirname, relpath
import jinja2


class template_function(object):
    def __init__(self, template_path):
        self.template_path = template_path

    def __call__(self, template_name: str, **params) -> str:
        template_loader = jinja2.FileSystemLoader(searchpath=self.template_path)
        env = jinja2.Environment(loader=template_loader)
        template = env.get_template(template_name)
        return template.render(**params)

