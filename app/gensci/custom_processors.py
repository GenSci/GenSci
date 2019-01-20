"""
gensci.context_processors - Custom designed context processors.

These context processors handle setting additional context variables
in the Django request/response cycle.

Processors:
    debug_var - This sends the DEBUG setting value to the template context as the `testing_env` variable.
"""

from gensci.settings import DEBUG

def debug_var(request):
    """
    A context processor to pass the DEBUG value to all templates.  This will help indentify testing environments.
    """
    return {'testing_env': DEBUG}
