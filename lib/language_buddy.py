# Import needed classes from models.py
from colorama import Fore
import time


class LanguageBuddy:

    def run(self):
        print("Welcome to Language Buddy!")
        self.main_menu()

    def main_menu(self):
        MAIN_MENU_OPTIONS = {
            "1": self.select_language,
            "select language": self.select_language,
            "2": self.view_stats,
            "view stats": self.view_stats,
            "3": self.train,
            "train": self.train,
            "4": None,
            "exit": None

        }
        MAIN_MENU_TEXT = """
        1. Select Language
        2. View Stats
        3. Train
        4. Exit
        """

        while True:
            print("Select an option:")
            print(MAIN_MENU_TEXT)
            self.user_input = input('>>> ').lower()
            if self.user_input in MAIN_MENU_OPTIONS:
                break
            else:
                print("Invalid input.")

        try:
            MAIN_MENU_OPTIONS[self.user_input]()
        except:
            pass

    def select_language(self):
        pass

    def view_stats(self):
        pass

    def train(self):
        TRAINING_OPTIONS = {
            "1": self.translate,
            "translate": self.translate,
            "2": self.vocab_game,
            "vocab game": self.vocab_game,
            "3": self.flashcards,
            "flashcards": self.flashcards,
            "4": self.main_menu,
            "return to main menu": self.main_menu
        }
        TRAINING_MENU_TEXT = """
        1. Translate
        2. Vocab Game
        3. Flashcards
        4. Return to Main Menu
        """

        while True:
            print("Select an option:")
            print(TRAINING_MENU_TEXT)
            self.user_input = input('>>> ').lower()
            if self.user_input in TRAINING_OPTIONS:
                break
            else:
                print("Invalid input.")

        try:
            TRAINING_OPTIONS[self.user_input]()
        except:
            pass

    def translate(self):
        # Generate a source-language sentence for user to translate: 
        # ex., "The cat is on the roof." 
        # Then, user inputs translation. 
        # Via OpenAI API, we evaluate translation and return comments.
        # Comments may include praise ("Great job!"), corrections 
        # ("Not quite -- a better translation is ..."), encouragement ("You've translated 10 sentences today!").
        # As long as user doesn't press i.e., 'Quit', we keep going
        # Store sentence and translation in db, or store points in db
        # Ideas: show accuracy percentage; show progress towards goal
        # #
        pass


    def vocab_game(self):
        # We could get words from word list and have OpenAI API provide definitions;
        # Or, we could just have the OpenAI API pick the word
        # #

        pass

    def flashcards(self):
        # Users can add words to flashcards from any app stage. Words are stored
        # in sqlite db and can be reviewed via flashcards. 
        # We may pull definitions in via a dictionary API or via OpenAI#
        pass