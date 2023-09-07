# Import needed classes from models.py
from colorama import Fore, Style
import time
import textwrap
import requests
import json
from sys import exit
from lib.models import Session
from datetime import date

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = ""
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def BLUE(str):
    return f"{Fore.BLUE}" + str + f"{Fore.RESET}"
def LIGHTRED(str):
    return f"{Fore.LIGHTRED_EX}" + str + f"{Fore.RESET}"
def GREEN(str):
    return f"{Fore.GREEN}" + str + f"{Fore.RESET}"
def RED(str):
    return f"{Fore.RED}" + str + f"{Fore.RESET}"
def MAGENTA(str):
    return f"{Fore.MAGENTA}" + str + f"{Fore.RESET}"
def BRIGHT(str):
    return f"{Style.BRIGHT}" + str + f"{Style.RESET_ALL}"

CARROTS = LIGHTRED(">>> ")
RED_EXIT = RED("Exit") + f"{Fore.BLUE}"
BLUE_SELECT_OPTION = BLUE("\nSelect an option:\n")
INVALID_INPUT = BRIGHT(RED("\nInvalid input. Please try again.\n"))
GO_AGAIN = BLUE("""
        -----------------------------    
        Go again? (y/n)
        -----------------------------
""")

class LanguageBuddy:

    source_language = "English"
    target_language = "Spanish"
    difficulty = 'A1 (Beginner)'
    custom_instructions = "Sentences should be creative, expressive, interesting, and unlikely to repeat."
    vocab_custom_instructions = "Pick words that are interesting, creative, and unlikely to repeat."
    feedback_custom_instructions = "Give me concise feedback focusing on errors. Do not include unnecessary praise or fluff."

    def run(self):
        WELCOME = """
        -----------------------------------
            Welcome to Language Buddy!
        -----------------------------------
        """

        print(BRIGHT(MAGENTA(WELCOME)))
        self.main_menu()

    def exit_language_buddy(self):
        EXIT_TEXT = """
        
        -----------------------------
        Bye! ¡Adiós! 再见! Au revoir! 
        Ciao! Tschüss! Пока! さようなら!
        -----------------------------

        """
        print(BRIGHT(MAGENTA(EXIT_TEXT)))
        exit()

    def main_menu(self):
        MAIN_MENU_OPTIONS = {
            "1": self.settings,
            "settings": self.settings,
            "2": self.view_stats,
            "view stats": self.view_stats,
            "3": self.training_menu,
            "train": self.training_menu,
            "4": self.exit_language_buddy,
            "exit": self.exit_language_buddy

        }
        MAIN_MENU_TEXT = f"""

        ----------MAIN MENU----------
        1. Settings
        2. View Stats
        3. Train
        4. {RED_EXIT}
        -----------------------------

        """

        while True:
            print(BLUE_SELECT_OPTION)
            print(BLUE(MAIN_MENU_TEXT))
            self.user_input = input(CARROTS).lower()
            if self.user_input in MAIN_MENU_OPTIONS:
                break
            else:
                print(INVALID_INPUT)

        try:
            MAIN_MENU_OPTIONS[self.user_input]()
        except:
            pass

    def settings(self):
        SETTINGS_MENU_TEXT = f"""

        ----------SETTINGS----------
        1. Set Language
        2. Set Level
        3. Return to Main Menu
        4. {RED_EXIT}
        -----------------------------
        
        """
        SETTINGS_MENU_OPTIONS = {
            "1": self.select_language,
            "2": self.set_level,
            "3": self.main_menu,
            "4": self.exit_language_buddy
        }

        print(BLUE(SETTINGS_MENU_TEXT))
        while True:
            print(BLUE_SELECT_OPTION)
            self.user_input = input(CARROTS).lower()
            if self.user_input in SETTINGS_MENU_OPTIONS:
                break
            else:
                print(INVALID_INPUT)

        SETTINGS_MENU_OPTIONS[self.user_input]()

    def set_level(self):
        LEVELS_TEXT = f"""

        ---------SET LEVELS---------
        A1. Beginner
        A2. Pre-Intermediate
        B1. Intermediate
        B2. Upper Intermediate
        C1. Advanced
        C2. Advanced / Fluent

        0. Return to Settings
        1. Return to Main Menu
        2. {RED_EXIT}
        -----------------------------

        """
        LEVELS_OPTIONS = {
            "a1": "A1 (Beginner)",
            "a2": "A2 (Pre-Intermediate)",
            "b1": "B1 (Intermediate)",
            "b2": "B2 (Upper Intermediate)",
            "c1": "C1 (Advanced)",
            "c2": "C2 (Advanced / Fluent)",
            "0": self.settings,
            "1": self.main_menu,
            "2": self.exit_language_buddy
        }

        print(BLUE(LEVELS_TEXT))
        while True:
            print(BLUE_SELECT_OPTION)
            self.user_input = input(CARROTS).lower()
            if self.user_input in LEVELS_OPTIONS:
                if self.user_input in {'0', '1', '2'}:
                    LEVELS_OPTIONS[self.user_input]()
                else:
                    self.difficulty = LEVELS_OPTIONS[self.user_input]
                    print(BLUE(f"\nYour level has been set to {self.difficulty}\n"))
                    self.settings()
            else:
                print(INVALID_INPUT)

    def select_language(self):
        LANGUAGE_TEXT = """

        ------SELECT LANGUAGE-------
        Enter the language you want to practice. 
        Language Buddy uses gpt-3.5-turbo, which 
        provides support for Spanish, Portuguese, 
        Russian, Mandarin, and French, among others. 
        -----------------------------

        """
        print(BLUE(LANGUAGE_TEXT))
        while True:
            
            self.user_input = input(CARROTS)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            validate_language_data = {
                "model": "gpt-3.5-turbo",
                "messages": [{
                    "role": "user",
                    "content": f"Does gpt-3.5-turbo support the following language: {self.user_input}? Return 'TRUE' or 'FALSE'. Do not return any other text."
                }],
                "temperature": 0.7
            }
            # Make the POST request
            response = requests.post(
                API_ENDPOINT, headers=headers, data=json.dumps(validate_language_data))

            # Get the JSON response
            response_data = response.json()

            # Extract the sentence
            language_validated = True if response_data['choices'][0]['message']['content'] == 'TRUE' else False

            if language_validated:
                self.target_language = self.user_input
                print(BLUE(f"\nYour language has been set to {self.target_language}\n"))
                self.settings()
                break
            else:
                print(INVALID_INPUT)

    def view_stats(self):

        STATS = BLUE(f"""

        ------------STATS------------
        POINTS EARNED:\t\t{Session.total_points_earned()}
        POINTS ATTEMPTED:\t{Session.total_points_attempted()}
        TOTAL SESSIONS:\t\t{Session.count_sessions()}
        TOTAL LANGUAGES: \t{Session.count_distinct_languages()}
        ACCURACY:\t\t{(Session.accuracy()*100):.2f}%
        HIGH SCORE:\t\t{Session.session_high_score()}
        -----------------------------

        Hit 'Enter' to return to main menu.
        
        """)

        print(STATS)

        self.input = input(CARROTS)
        
        self.main_menu()

    def training_menu(self):
        TRAINING_OPTIONS = {
            "1": self.translation_menu,
            "translate": self.translation_menu,
            "2": self.vocab_game,
            "vocab game": self.vocab_game,
            "3": self.flashcard_review,
            "flashcards": self.flashcard_review,
            "4": self.main_menu,
            "return to main menu": self.main_menu,
            "5": self.exit_language_buddy,
            "exit": self.exit_language_buddy,
        }
        TRAINING_MENU_TEXT = BLUE(f"""

        --------TRAINING MENU--------
        1. Translate
        2. Vocab Game
        3. Flashcards
        4. Return to Main Menu
        5. {RED_EXIT}
        -----------------------------

        """)

        print(TRAINING_MENU_TEXT)
        while True:
            print(BLUE_SELECT_OPTION)
            self.user_input = input(CARROTS).lower()
            if self.user_input in TRAINING_OPTIONS:
                break
            else:
                print(INVALID_INPUT)

        try:
            TRAINING_OPTIONS[self.user_input]()
        except:
            pass

    def translation_menu(self):
        TRANSLATION_MENU_TEXT = BLUE("""
              
        ---------TRANSLATION---------
        1. Start New Session               
        2. Set Custom Instructions
        3. Return to Training Menu
        4. Return to Main Menu
        5. Exit
        -----------------------------
              
        """)

        TRANSLATION_MENU_OPTIONS = {
            "1": self.translation_session,
            "2": self.set_custom_instructions,
            "3": self.training_menu,
            "4": self.main_menu,
            "5": self.exit_language_buddy,
        }

        print(TRANSLATION_MENU_TEXT)

        while True:
            print(BLUE_SELECT_OPTION)
            self.user_input = input(CARROTS)
            if self.user_input in TRANSLATION_MENU_OPTIONS:
                break

        TRANSLATION_MENU_OPTIONS[self.user_input]()
       
    def set_custom_instructions(self):
        INSTRUCTIONS = BLUE("""
              
        -----------------------------
        Enter custom instructions. For best results, use full sentences beginning "I want to practice ... ",
        "Sentences should ...", "Feedback should ...", etc
            Ex., "I want to practice food vocabulary."
            Ex., "I want to practice questions with interrogative pronouns."
            Ex., "Sentences should use advanced computer science vocabulary."
            Ex., "Sentences should be at least 20 words in length."
            Ex., "Feedback should rhyme."
        -----------------------------

        Enter custom instructions for sentences:  
                  
        """)
        print(INSTRUCTIONS)
        self.custom_instructions = input(CARROTS)
        FEEDBACK_INSTRUCTIONS = BLUE("""
                                     
        Enter custom instructions for feedback:
                                     
        """)
        print(FEEDBACK_INSTRUCTIONS)
        self.feedback_custom_instructions = input(CARROTS)
        print(BLUE("Custom instructions have been set!"))

        self.translation_menu()

    def translation_session(self):

        # Generate a sentence for user to translate:
        # ex., "The cat is on the roof."
        # Then, user inputs translation.
        # Via OpenAI API, we evaluate translation and return comments.

        session = Session(date.today(), self.target_language, self.difficulty, 'translation', 0, 0)
        session.save()

        INSTRUCTIONS = BLUE(f"""

        -----------------------------
        Translate the following sentence 
        from {self.target_language} to {self.source_language}
        -----------------------------

        """)

        while True:
            print(INSTRUCTIONS)

            gpt_sentence = self.get_sentence_for_translation()
            formatted_gpt_sentence = BRIGHT(MAGENTA("\n" + self.format_text(gpt_sentence) + "\n"))
            print(formatted_gpt_sentence)

            user_translation = input(CARROTS)
            feedback = self.get_feedback_for_translation(gpt_sentence, user_translation)
            points = self.get_points_for_translation(gpt_sentence, user_translation) * 0.01

            
            session.points_earned = session.points_earned + points
            session.points_possible = session.points_possible + 1
            print(f"\nPOINTS: {points}\n")
            FORMATTED_FEEDBACK = BRIGHT(MAGENTA(f"""
FEEDBACK:
{self.format_text(feedback)}

"""))
            print(FORMATTED_FEEDBACK)
            print(
                f"STATS: {session.points_earned} / {session.points_possible} = {100 * (session.points_earned / session.points_possible):.2f}%")

            session.save()

            print(GO_AGAIN)
            play_again = input(CARROTS)
            if play_again == 'y':
                continue
            else:
                break
        self.translation_menu()

    def get_sentence_for_translation(self):

        get_sentence_data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": f"You are my {self.target_language} language tutor. We are doing a translation exercise. Give me a {self.target_language} sentence to translate into English. The difficulty of this sentence should be {self.difficulty}. {self.custom_instructions} Return only the sentence for translation; include no other content."
            }],
            "temperature": 0.7
        }
        # Make the POST request
        response = requests.post(
            API_ENDPOINT, headers=HEADERS, data=json.dumps(get_sentence_data))
        # Get the JSON response
        response_data = response.json()
        # Extract the sentence
        sentence_for_translation = response_data['choices'][0]['message']['content']
        return sentence_for_translation

    def get_feedback_for_translation(self, gpt_sentence, user_translation):
        get_feedback_data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": f"You are my ${self.target_language} language tutor. We are doing a translation exercise. You gave me the following {self.target_language} to translate into {self.source_language}: {gpt_sentence}. Here is my translation: \"{user_translation}\". {self.feedback_custom_instructions}"
            }],
            "temperature": 0.7
        }

        feedback_response = requests.post(API_ENDPOINT, headers=HEADERS, data=json.dumps(get_feedback_data))
        feedback_response_data = feedback_response.json()
        feedback = feedback_response_data['choices'][0]['message']['content']
        return feedback

    def get_points_for_translation(self, gpt_sentence, user_translation):
        get_score_data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": f"You are my ${self.target_language} language tutor. We are doing a translation exercise. You gave me the following {self.target_language} to translate into {self.source_language}: {gpt_sentence}. Here is my translation: {user_translation}. Grade the translation out of 100 points, where 100 is perfect. A nonsensical or very incorrect translation should always receive 0 points. Return only the numerical score. Do not return any other text."
            }],
            "temperature": 0.7
        }

        # Make the POST request

        score_response = requests.post(
            API_ENDPOINT, headers=HEADERS, data=json.dumps(get_score_data))

        # Get the JSON response
        score_response_data = score_response.json()
        points = int(score_response_data['choices'][0]['message']['content'])
        return points

    def vocab_game(self):
        # We could get words from word list and have OpenAI API provide definitions;
        # Or, we could just have the OpenAI API pick the word
        # #

        session = Session(date.today(), self.target_language, self.difficulty, 'vocab_game', 0, 0)
        session.save()

        INSTRUCTIONS = BLUE("""

        -----------------------------
        Read the clue and guess the word!
        -----------------------------
        
        """)

        print(INSTRUCTIONS)

        while True:
            # Get a clue from gpt
            # While user has not guessed word, allow free back-and-forth with gpt
            # If gpt says 'correct', user gets point
            # If user gives up or guesses incorrectly three times, 
            # user doesn't get point, answer is revealed, and we move on
            self.vocab_exercise()
            session.points_earned = session.points_earned + 1
            session.points_possible = session.points_possible + 1
            print(f"\nTOTAL POINTS: {session.points_earned}\n")
            session.save()
            self.user_input = input(GO_AGAIN)
            if self.user_input == 'n':
                self.training_menu()

    def vocab_exercise(self):
        conversation = []
        prompt = (""
        f"You are my {self.target_language} tutor and we are playing a vocabulary game. "
        f"You give me a clue in  describing a word; I guess the word. "
        f"Your clue should be 3-5 sentences long and appropriate for a learner at the {self.difficulty} level. "
        f"You must use ONLY {self.target_language}. Return ONLY the clue; include no other text."
        f"{self.vocab_custom_instructions}"
        "")
        get_data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": f"{prompt}"
            }],
            "temperature": 0.7
        }
        response = requests.post(
            API_ENDPOINT, headers=HEADERS, data=json.dumps(get_data))

        # Get the JSON response
        data = response.json()
        gpt_response = data['choices'][0]['message']['content']
        print(BRIGHT(MAGENTA("\n" + self.format_text(gpt_response) + "\n")))

        self.user_input = input(CARROTS)

        prompt = (
            f"You are my {self.target_language} tutor and we are playing a vocabulary game. "
            f"You gave me the following clue: {gpt_response} "
            f"Here is my guess: {self.user_input}"
            f"Is this guess correct? Give feedback in {self.target_language}. If my answer is wrong, tell me the correct answer and its English translation."
            f"Feedback must be appropriate for level {self.difficulty}. No English should be used except to translate the correct answer."
        )
        get_data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": f"{prompt}"
            }],
            "temperature": 0.7
        }
        response = requests.post(
            API_ENDPOINT, headers=HEADERS, data=json.dumps(get_data))

        # Get the JSON response
        data = response.json()
        gpt_response = data['choices'][0]['message']['content']
        print(BRIGHT(MAGENTA("\n" + self.format_text(gpt_response) + "\n")))

    # TODO 9/7 KEVAL -- implement flashcard review game
    def flashcard_review(self):
        # We query flashcards from db for selected lang (/level?) 
        # User reviews flashcards -- can flip between sides 
        pass

    # TODO 9/7 HALLIE -- implement add flashcard & integrate into translate, vocab exercises
    def add_flashcard(self):
        # Users can add words to flashcards from any app stage. Words are stored
        # in sqlite db and can be reviewed via flashcards.
        # We may pull definitions in via a dictionary API or via OpenAI#
        pass
    # This function was generated by ChatGPT
    def format_text(self, text, width=80):
        """Formats text for terminal display with a given width."""
        wrapper = textwrap.TextWrapper(width=width)
        formatted_text = wrapper.fill(text)
        return formatted_text
