from typing import Literal, Text, Tuple
from flask import Blueprint, render_template

errors: Blueprint = Blueprint("errors", __name__, template_folder="templates")

@errors.errorhandler(500)
def error_500() -> Tuple[Text, Literal[500]]:
    """Error handler for Internal server error."""
    return render_template("errors/5xx/500.html"), 500
