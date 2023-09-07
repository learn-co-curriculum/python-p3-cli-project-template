from lib.models import Session, Flashcard
from lib.language_buddy import HEADERS, LanguageBuddy
import textwrap

from colorama import Fore, Style

def format_text(text, width=80):
    """Formats text for terminal display with a given width."""
    wrapper = textwrap.TextWrapper(width=width)
    formatted_text = wrapper.fill(text)
    return formatted_text

flashcard_1 = Flashcard("Textbook A", "2023-09-07", "Spanish", "Beginner", "hola", "hello", "A greeting", "¡Hola, Juan!", 1)
flashcard_2 = Flashcard("Textbook A", "2023-09-07", "Spanish", "Beginner", "comer", "to eat", "To consume food", "Voy a comer una manzana.", 2)
flashcard_3 = Flashcard("Textbook A", "2023-09-07", "Spanish", "Beginner", "bailar", "to dance", "To move rhythmically to music", "Ella le encanta bailar salsa.", 3)
flashcard_4 = Flashcard("Textbook B", "2023-09-07", "Russian", "Beginner", "кот", "cat", "A domesticated feline", "Это мой кот, Миша.", 4)
flashcard_5 = Flashcard("Textbook B", "2023-09-07", "Russian", "Beginner", "бассейн", "pool", "A place for swimming", "Дети играют в бассейне.", 5)


app = LanguageBuddy()

import ipdb; ipdb.set_trace()

