import logging
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

logger = logging.getLogger(__name__)

class XMLRenderer:
    def __init__(self, template_dir: str = "templates"):
        """
        Initializes the XMLRenderer with the specified template directory.

        :param template_dir: Directory where Jinja2 templates are stored.
        """
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Renders a Jinja2 template with the given context.

        :param template_name: Name of the template file.
        :param context: Dictionary containing context variables for the template.
        :return: Rendered template as a string.
        """
        try:
            template: Template = self.env.get_template(template_name)
            return template.render(context)
        except Exception as e:
            logger.error(f"Error rendering template '{template_name}': {e}")
            raise
