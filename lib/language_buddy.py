# Import needed classes from models.py
from colorama import Fore
import time
import requests
import json
from lib.models import Session
from datetime import date

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = "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"


class LanguageBuddy:

    source_language = "English"
    target_language = "Russian"
    difficulty = 'C2 (Advanced)'

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
        while True:
            print("Select the language you want to learn")
            self.user_input = input(">>> ")
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
            response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(validate_language_data))

            # Get the JSON response
            response_data = response.json()

            # Extract the sentence
            language_validated = True if response_data['choices'][0]['message']['content'] == 'TRUE' else False
            
            if language_validated:
                self.target_language = self.user_input
                print(f"Your language has been set to {self.target_language}")
                self.main_menu()
                break
            else:
                print("Invalid input. Please select a supported language")

    def view_stats(self):
        print(f"POINTS EARNED:\t\t{Session.total_points_earned()}")
        print(f"POINTS ATTEMPTED:\t{Session.total_points_attempted()}")
        print(f"TOTAL SESSIONS:\t\t{Session.count_sessions()}")
        print(f"TOTAL LANGUAGES: \t{Session.count_distinct_languages()}")
        print(f"ACCURACY:\t\t{(Session.accuracy()*100):.2f}%")
        print(f"HIGH SCORE:\t\t{Session.session_high_score()}")
        self.main_menu()

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
        # Generate a sentence for user to translate:
        # ex., "The cat is on the roof."
        # Then, user inputs translation.
        # Via OpenAI API, we evaluate translation and return comments.

        session = Session(date.today(), self.target_language, self.difficulty, 'translation', 0, 0)
        session.save()

        print(f"""Let's do some translation exercises. 
              EXIT: 'exit'
              RETURN TO MAIN MENU: 'menu'
            """)
        
        self.session_points = 0

        while True:
        
            print(f"Translate the following sentence from {self.target_language} to {self.source_language}")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            get_sentence_data = {
                "model": "gpt-3.5-turbo",
                "messages": [{
                    "role": "user", 
                    "content": f"You are my {self.target_language} language tutor. We are doing a translation exercise. Give me a {self.target_language} sentence to translate into English. The difficulty of this sentence should be {self.difficulty}. Sentences should be creative, expressive, and interesting. Return only the sentence for translation; include no other content."
                }],
                "temperature": 0.7
            }
            # Make the POST request
            response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(get_sentence_data))

            # Get the JSON response
            response_data = response.json()

            # Extract the sentence
            sentence_for_translation = response_data['choices'][0]['message']['content']

            # Print out the model's response
            print(sentence_for_translation)

            user_input = input(">>> ")

            
            if (user_input == "exit"):
                break
            elif (user_input == "menu"):
                self.main_menu()
                break
            else:
                user_translation = user_input

            get_feedback_data = {
                "model": "gpt-3.5-turbo",
                "messages": [{
                    "role": "user", 
                    "content": f"You are my ${self.target_language} language tutor. We are doing a translation exercise. You gave me the following {self.target_language} to translate into {self.source_language}: {sentence_for_translation}. Here is my translation: \"{user_translation}\". Give me concise feedback focusing on errors."
                }],
                "temperature": 0.7
            }
            get_score_data = {
                "model": "gpt-3.5-turbo",
                "messages": [{
                    "role": "user", 
                    "content": f"You are my ${self.target_language} language tutor. We are doing a translation exercise. You gave me the following {self.target_language} to translate into {self.source_language}: {sentence_for_translation}. Here is my translation: {user_translation}. Grade the translation out of 1 point. An incorrect or missing translation should receive 0 points; a partially correct translation should receive 0.5; a nearly correct translation should receive 0.75; and a correct translation should receive 1. Return only the numerical score. Do not return any other text."
                }],
                "temperature": 0.7
            }

            # Make the POST request
            feedback_response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(get_feedback_data))
            score_response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(get_score_data))

            # Get the JSON response
            feedback_response_data = feedback_response.json()
            score_response_data = score_response.json()

            # Extract the sentence
            feedback = feedback_response_data['choices'][0]['message']['content']
            points = int(score_response_data['choices'][0]['message']['content'])
            # self.session_points = self.session_points + points
            session.points_earned = session.points_earned + points
            session.points_possible = session.points_possible + 1
            print(f"POINTS: {points}")
            print(f"FEEDBACK: {feedback}")
            print(f"STATS: {session.points_earned} / {session.points_possible} = {100 * (session.points_earned / session.points_possible):.2f}%")

            session.save()

            play_again = input("Go again (y/n)?\n>>>")
            if play_again == 'y':
                continue
            else: 
                self.view_stats()
                break
        
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

    
