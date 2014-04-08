from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    def __init__(self, template_path):
        self._template_env = Environment(loader=FileSystemLoader(template_path))

    def set_globals(self, **kwargs):
        for key, value in kwargs.items():
            self._template_env.globals[key] = value

    def render(self, template_name, **kwargs):
        template = self._template_env.get_template(template_name)
        return template.render(**kwargs)
