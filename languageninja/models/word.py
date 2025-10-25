#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, rich, os
from random import randint

#-------------------#
# Static parameters #
#-------------------#
WORDS_FOLDER_PATH     = './data/words'
SENTENCES_FOLDER_PATH = './data/sentences'

#------------------------#
# Class definition: Word #
#------------------------#
class Word():

    # Class constructor
    def __init__(self, key=None):

        # Set English name
        self.key = key

        # Initialise translations
        self.langs = {
            'en' : self.key,
            'fr' : None,
            'es' : None,
            'pt' : None,
            'ru' : {
                'cyr': None,
                'lat': None
            },
            'il' : {
                'heb': None,
                'lat': None
            }
        }

        # Initialise sample sentences
        self.samples = {
            'en' : [],
            'fr' : [],
            'es' : [],
            'pt' : [],
            'ru' : {
                'cyr': [],
                'lat': []
            },
            'il' : {
                'heb': [],
                'lat': []
            }
        }

    # Method: Load word JSON from file (if exists)
    def load(self):

        # Generate word file path
        word_file_path = f"{WORDS_FOLDER_PATH}/{self.langs['en']}.json"

        # Load JSON data from file (if exists)
        try:
            with open(word_file_path, 'r') as f:
                data = json.load(f)
                self.langs.update(data[self.key])
        except FileNotFoundError:
            print(f"File not found: {word_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {word_file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Generate sentences file path
        sentences_file_path = f"{SENTENCES_FOLDER_PATH}/{self.langs['en']}.json"

        # Load JSON data from file (if exists)
        try:
            with open(sentences_file_path, 'r') as f:
                data = json.load(f)
                self.samples.update(data[self.key])
        except FileNotFoundError:
            print(f"File not found: {sentences_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {sentences_file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Method: Say the word or sentence using MacOS text-to-speech
    # The 'sentence' parameter can be the index or "random" to select a sample sentence
    def say(self, lang='en', sentence=None, rate=None, save_to=None):

        # Randomly select or index a sentence to speak
        if sentence == 'random':
            sentence = randint(0, len(self.samples[lang]) - 1) if self.samples[lang] else None

        # Determine text to speak
        # Use Switch/ case:
        match lang:
            case 'en' | 'fr' | 'es' | 'pt':
                text_to_print = text_to_speak = self.samples[lang][sentence] if isinstance(sentence, int) else self.langs[lang]
            case 'ru':
                text_to_speak = self.samples['ru']['cyr'][sentence] if isinstance(sentence, int) else self.langs['ru']['cyr']
                text_to_print = self.samples['ru']['lat'][sentence] + ' / ' + text_to_speak if isinstance(sentence, int) else self.langs['ru']['lat']
            case 'il':
                text_to_speak = self.samples['il']['heb'][sentence] if isinstance(sentence, int) else self.langs['il']['heb']
                text_to_print = self.samples['il']['lat'][sentence] + ' / ' + text_to_speak if isinstance(sentence, int) else self.langs['il']['lat']
            case _:
                print(f"Unsupported language code: {lang}")
                return

        # Map language codes to MacOS voice names
        voice_map = {
            "en": "Samantha",
            "fr": "Thomas",
            "es": "Mónica",
            "pt": "Joana",
            "ru": "Milena",
            "il": "Carmit",
        }
        voice = voice_map[lang]

        # Rate defaults
        if rate is None or rate == 'normal':
            rate = {
                "en": 130,
                "fr": 130,
                "es": 90,
                "pt": 160,
                "ru": 120,
                "il": 100,
            }[lang]
        elif rate == 'slow':
            rate = {
                "en": 80,
                "fr": 70,
                "es": 40,
                "pt": 90,
                "ru": 60,
                "il": 50,
            }[lang]

        # Optional rate flag (words per minute)
        rate_flag = f"-r {int(rate)} " if isinstance(rate, (int, float)) else ""

        # Execute MacOS say command
        if save_to:
            file_name = f"{self.langs['en']}_{lang}.aiff"
            print(f'Saving speech to {file_name} in {lang} ({voice}): {text_to_print}')
            os.system(f'say -v {voice} {rate_flag}-o {file_name} "{text_to_speak}"')
        else:
            print(f'Speaking in {lang} ({voice}): {text_to_print}')
            os.system(f'say -v {voice} {rate_flag}"{text_to_speak}"')

if __name__ == "__main__":

    # Pick random word from data/words folder
    word_files = [f for f in os.listdir(WORDS_FOLDER_PATH) if f.endswith('.json')]
    random_word_file = word_files[randint(0, len(word_files) - 1)]
    random_word_key = os.path.splitext(random_word_file)[0]

    # Example usage
    word = Word(key=random_word_key)
    word.load()
    rich.print_json(data=word.langs)
    rich.print_json(data=word.samples)

    # Randomly select or index a sentence to speak
    k = randint(0,2)

    # en
    word.say(lang='en')
    word.say(lang='en', sentence=k)
    # fr
    word.say(lang='fr')
    word.say(lang='fr', sentence=k)
    # es
    word.say(lang='es')
    word.say(lang='es', sentence=k)
    # pt
    word.say(lang='pt')
    word.say(lang='pt', sentence=k)
    # ru
    word.say(lang='ru')
    word.say(lang='ru', sentence=k)
    # il
    word.say(lang='il')
    word.say(lang='il', sentence=k)