#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, rich, os
from random import randint
from languageninja.common.auxfcn import parse_word_list_with_stats
from languageninja.models.gptclient import GPTConnector
from languageninja.models.word import Word

#-------------------#
# Static parameters #
#-------------------#
WORDS_FOLDER_PATH     = './data/words'
SENTENCES_FOLDER_PATH = './data/sentences'

#------------------------#
# GPT API Initialisation #
#------------------------#

# Initialize GPT connector
ai_model = "gpt-5"
print(f"Using AI model: {ai_model}")
ai = GPTConnector(model=ai_model)

# GPT prompt for word generation
gpt_prompt_newwords = """
The following is a JSON object representing translations of a word - eg, "she" - in multiple languages.
Specifically, English, French, Spanish, Portuguese, Russian (latin and cyrilic spelling), and Hebrew (latin and hebrew spelling).
{
    "she": {
        "en": "she",
        "fr": "elle",
        "es": "ella",
        "pt": "ela",
        "ru": {
            "cyr": "она",
            "lat": "ona"
        },
        "il": {
            "heb": "היא",
            "lat": "hi"
        }
    }
}
Please generate a JSON list using the same approach for the following comma-separated list of words.
Make sure the list follows the format (using the word "cat" and "dog" as examples):
{
  "result": [
    {
        "cat": {
            "en": "cat",
            "fr": "chat",
            "es": "gato",
            "pt": "gato",
            "ru": {
                "cyr": "кошка",
                "lat": "koshka"
            },
            "il": {
                "heb": "חתול",
                "lat": "chatul"
            }
        }
    },
    {
        "dog": {
            "en": "dog",
            "fr": "chien",
            "es": "perro",
            "pt": "cão",
            "ru": {
                "cyr": "собака",
                "lat": "sobaka"
            },
            "il": {
                "heb": "כלב",
                "lat": "kelev"
            }
        }
    }
  ]
}
Here's your list of words to process:
"""

# GPT prompt for sentence generation
gpt_prompt_newsentences = """
The following is a JSON object representing translations of a word - eg, "have" - in multiple languages.
Specifically, English, French, Spanish, Portuguese, Russian (latin and cyrilic spelling), and Hebrew (latin and hebrew spelling).
{
    "have": {
        "en": "have",
        "fr": "avoir",
        "es": "tener; haber (auxiliary)",
        "pt": "ter",
        "ru": {
            "cyr": "иметь / у меня есть",
            "lat": "imet’ / u menya yest’"
        },
        "il": {
            "heb": "יש לי",
            "lat": "yesh li"
        }
    }
}
Please generate a JSON list of exactly 3 (three) sample sentences using the same approach for the following JSON list of words and translations.
Make sure the list follows the format (using the word "have" as an example):
{
    "result": [
        {
            "have": {
                "en": [
                    "I have a book.",
                    "She has a cat.",
                    "We have time."
                ],
                "fr": [
                    "J'ai un livre.",
                    "Elle a un chat.",
                    "Nous avons du temps."
                ],
                "es": [
                    "Tengo un libro.",
                    "Ella tiene un gato.",
                    "Tenemos tiempo."
                ],
                "pt": [
                    "Tenho um livro.",
                    "Ela tem um gato.",
                    "Temos tempo."
                ],
                "ru": {
                    "cyr": [
                        "У меня есть книга.",
                        "У неё есть кошка.",
                        "У нас есть время."
                    ],
                    "lat": [
                        "U menya yest’ kniga.",
                        "U neyo yest’ koshka.",
                        "U nas yest’ vremya."
                    ]
                },
                "il": {
                    "heb": [
                        "יש לי ספר.",
                        "יש לה חתול.",
                        "יש לנו זמן."
                    ],
                    "lat": [
                        "yesh li sefer.",
                        "yesh la chatul.",
                        "yesh lanu zman."
                    ]
                }
            }
        },
        {...},
        {...},
        ...
    ]
}
Important:
 - make sure that sentence A in position n in the 'en' field is also in position n in the other language fields, 'es', 'fr', etc;
 - make sure that, for the same n, the sentences are exact translations of each other; not different sentences;
 - make sure to use simple sentences, suitable for beginners.
Here's your JSON list of words to process:
"""

#-----------------------------#
# Class definition: Generator #
#-----------------------------#
class Generator():

    # Class constructor
    def __init__(self, word_list=()):

        # Initialize word list
        self.word_list = word_list

        # Initialise GPT-generated JSON outputs
        self.word_jsonlist_output = None
        self.sentence_jsonlist_output = None

    # Method: Set word list
    def set(self, word_list):
        self.word_list = word_list

    # Static method: Check if word has been already processed
    @staticmethod
    def word_exists(word_key):
        if os.path.exists(os.path.join(WORDS_FOLDER_PATH, f"{word_key}.json")):
            w = Word(key=word_key)
            return w.translations_exist
        else:
            return False

    # Static method: Check if senteces has been already generated
    @staticmethod
    def sentences_exist(word_key):
        w = Word(key=word_key)
        return w.n_samples>0

    # Static method: Remove words that have been already processed
    @staticmethod
    def word_list_clean(word_list, what_to_check='words'):
        cleaned_word_list = []
        if what_to_check=='words':
            for word in word_list:
                if not Generator.word_exists(word):
                    cleaned_word_list.append(word)
        elif what_to_check=='sentences':
            for word in word_list:
                if not Generator.sentences_exist(word):
                    cleaned_word_list.append(word)
        return cleaned_word_list

    # Method: Generate new words
    def generate_words(self, sym_mode=False, verbose=False):

        # Process only words that have not been already generated
        words_to_process = Generator.word_list_clean(self.word_list)

        # Check if there are words to process
        if not words_to_process:
            if verbose:
                print("✅ All words have already been generated.")
            return 0

        # Generate and print full prompt
        full_prompt = f"{gpt_prompt_newwords}{', '.join(words_to_process)}"

        # Print prompt if verbose
        if verbose:
            print('')
            print("-------------------------------------")
            print("Sending request for new words to GPT:")
            print("-------------------------------------")
            print(full_prompt)
            print("--------------------------------------")
        else:
            print(f"⏳ Processing new words with GPT: {', '.join(words_to_process)}")

        # Return if in symulation mode
        if sym_mode:
            print(f"♻️ Running in simulation mode. Words not processed.")
            self.word_jsonlist_output = None
            return 0

        # Execute prompt (function already returns parsed JSON)
        out = ai.send_prompt(full_prompt)

        # Extract 'result' field from output
        word_jsonlist_output = out.get('result', [])

        # Print output if verbose
        if verbose:
            rich.print_json(data=word_jsonlist_output)

        # Assign output to internal variable
        self.word_jsonlist_output = word_jsonlist_output

        # Return number of generated words
        return len(word_jsonlist_output)

    # Method: Generate new words
    def generate_sentences(self, sym_mode=False, verbose=False):

        # Process only words that have not been already generated
        words_to_process = Generator.word_list_clean(self.word_list, what_to_check='sentences')

        # Check if there are words to process
        if not words_to_process:
            if verbose:
                print("✅ All words have already been generated.")
            return 0

        # Generate json input
        json_list = []
        for word_key in words_to_process:
            w = Word(key=word_key)
            json_list += [{word_key: w.langs}]

        # Generate input string
        input_str = json.dumps(json_list, ensure_ascii=False, indent=4)

        # Generate and print full prompt
        full_prompt = f"{gpt_prompt_newsentences}{input_str}"

        # Print prompt if verbose
        if verbose:
            print('')
            print("-----------------------------------------")
            print("Sending request for new sentences to GPT:")
            print("-----------------------------------------")
            print(full_prompt)
            print("--------------------------------------")
        else:
            print(f"⏳ Generating new senteces with GPT for words: {', '.join(words_to_process)}")

        # Return if in symulation mode
        if sym_mode:
            print(f"♻️ Running in simulation mode. Words not processed.")
            self.sentence_jsonlist_output = None
            return 0

        # Execute prompt (function already returns parsed JSON)
        out = ai.send_prompt(full_prompt)

        # Extract 'result' field from output
        sentence_jsonlist_output = out.get('result', [])

        # Print output if verbose
        if verbose:
            rich.print_json(data=sentence_jsonlist_output)

        # Assign output to internal variable
        self.sentence_jsonlist_output = sentence_jsonlist_output

        # Return number of generated words
        return len(sentence_jsonlist_output)

    # Method: Save GPT-generated words to files
    def save_words(self, verbose=False):

        # Check if there is any JSON output to save
        if not self.word_jsonlist_output or self.word_jsonlist_output is None:
            if verbose:
               print("⚠️  No JSON output to save. Please run generate() first.")
            return

        # Iterate over each word entry in the JSON output
        for json_item in self.word_jsonlist_output:

            # Word key is the first (and only) key in the json_item dict
            word_key = list(json_item.keys())[0]

            # Check if word file already exists
            if Generator.word_exists(word_key):
                if verbose:
                    print(f"⚠️ Word '{word_key}' already exists. Skipping.")
                continue

            # Create Word object from JSON entry
            w = Word(key=word_key, verbose=verbose)
            w.langs = json_item[word_key]

            # Save word to file
            w.save(what_to_save='word')

            # Print confirmation
            print(f"✅ Saved word: {word_key}")

    # Method: Save GPT-generated sentences to files
    def save_sentences(self, verbose=False):

        # Check if there is any JSON output to save
        if not self.sentence_jsonlist_output or self.sentence_jsonlist_output is None:
            if verbose:
               print("⚠️  No JSON output to save. Please run generate() first.")
            return

        # Iterate over each word entry in the JSON output
        for json_item in self.sentence_jsonlist_output:

            # Word key is the first (and only) key in the json_item dict
            word_key = list(json_item.keys())[0]

            # Check if sample sentences already exist
            if Generator.sentences_exist(word_key):
                if verbose:
                    print(f"⚠️ Sentences for '{word_key}' already exist. Skipping.")
                continue

            # Create Word object from JSON entry
            w = Word(key=word_key, verbose=verbose)
            w.samples = json_item[word_key]

            # Save word to file
            w.save(what_to_save='sentences')

            # Print confirmation
            print(f"✅ Saved sentences for word: {word_key}")

#================#
# Main execution #
#================#
if __name__ == "__main__":

    # What to process?
    what_to_process = 'words'

    # Get list of words to process from file with list of most common words
    word_list = parse_word_list_with_stats()

    #===============================#
    # Process in batches of N words #
    #===============================#

    # Processing parameters
    batch_size = 5
    max_num_iterations = 100000
    iter_counter = 0
    verbose = False
    sym_mode = False

    # Loop over words list
    for i,b in enumerate(range(0, len(word_list), batch_size)):

        # Get current batch of words
        batch_words = tuple(word_list[b:b+batch_size])

        # Keep only words that exist
        if what_to_process=='words':
            batch_words = tuple([word_key for word_key in word_list[b:b+batch_size] if Generator.sentences_exist(word_key) and not Generator.word_exists(word_key)])
        elif what_to_process=='sentences':
            batch_words = tuple([word_key for word_key in word_list[b:b+batch_size] if Generator.word_exists(word_key)])

        # Create Generator object for the batch
        gen = Generator(word_list=batch_words)

        # What to generate?
        # -> Words
        if what_to_process=='words':

            # Generate new words
            n_generated = gen.generate_words(sym_mode=sym_mode, verbose=verbose)

            # Save generated words
            if not sym_mode:
                gen.save_words(verbose=verbose)

        # -> Sentences
        elif what_to_process=='sentences':

            # Generate new sentences
            n_generated = gen.generate_sentences(sym_mode=sym_mode, verbose=verbose)

            # Save generated sentences
            if not sym_mode:
                gen.save_sentences(verbose=verbose)

        # Check if it counts as an effective iteration
        iter_counter += int(n_generated>0)

        # Stop after max number of iterations
        if iter_counter==max_num_iterations:
            break
