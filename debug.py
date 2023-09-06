from lib.models import Session
import textwrap

from colorama import Fore, Style

def format_text(text, width=80):
    """Formats text for terminal display with a given width."""
    wrapper = textwrap.TextWrapper(width=width)
    formatted_text = wrapper.fill(text)
    return formatted_text

import ipdb; ipdb.set_trace()

