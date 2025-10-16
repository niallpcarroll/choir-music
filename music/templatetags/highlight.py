from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, search):
    """
    Highlights all occurrences of 'search' in 'text' (case-insensitive)
    by wrapping them in a <span> with class 'highlight'.
    """
    if not search:
        return text
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return mark_safe(
        pattern.sub(lambda m: f'<span class="highlight">{m.group(0)}</span>', text)
    )
