import os
import re
import csv
import string
from num2words import num2words
from nltk.tokenize import sent_tokenize, word_tokenize

# Define all necessary functions

def replace_british_spelling(text):
    # Dictionary mapping British spelling to American spelling
    british_to_american = {
        'favourite': 'favorite',
        'flavour': 'flavor',
        'colour': 'color',
        'humour': 'humor',
        'labour': 'labor',
        'neighbour': 'neighbor',
        'apologise': 'apologize',
        'organise': 'organize',
        'recognise': 'recognize',
        'analyse': 'analyze',
        'paralyse': "paralyze",
        'travelled': 'travaled',
        'manoeuvre': 'maneuver'

        # Add more pairs as needed
    }
    for british, american in british_to_american.items():
        text = text.replace(british, american)
    return text

def replace_non_ascii(text):
    return text.encode('ascii', 'replace').decode('ascii')

def remove_punctuation_except_periods(text):
    # Replace end-of-sentence periods with " PERIOD"
    text = re.sub(r'\.(?=\s|$)', ' PERIOD', text)
    # Remove all other punctuation (except periods not at the end of a sentence)
    text = re.sub(r'[{}]+'.format(re.escape(string.punctuation.replace('.', ''))), '', text)
    return text

def replace_numerals(text):
    # Replace ordinal numbers with words
    text = re.sub(r'\b(\d+)(st|nd|rd|th)\b', lambda m: num2words(int(m.group(1)), to='ordinal'), text)
    # Remove all other numerals
    text = re.sub(r'\b\d+\b', '', text)
    return text

def lowercase_first_letter(text):
    sentences = sent_tokenize(text)
    return ' '.join(sentence[0].lower() + sentence[1:] if sentence else '' for sentence in sentences)

def is_article_long_enough(text):
    return len(word_tokenize(text)) >= 10

def process_content(content):
    content = re.sub(r'"[^"]*"', '', content)  # Remove direct quotes
    content = replace_british_spelling(content)
    content = replace_non_ascii(content)
    content = remove_punctuation_except_periods(content)
    content = replace_numerals(content)
    content = lowercase_first_letter(content)
    return content if is_article_long_enough(content) else ''

def process_csv_file(input_path, output_path, num_articles=10000):
    with open(input_path, mode='r', encoding='utf-8') as infile, \
            open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for article in reader:
            article['content'] = process_content(article['content'])
            if article['content']:  # Only write articles that are long enough
                writer.writerow(article)
                count += 1

            if count >= num_articles:
                break
