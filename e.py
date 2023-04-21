import os
import re
from collections import Counter
import click
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize


def read_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text


def analyze_text(text):
    # Tokenize sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Calculate statistics
    word_count = len(words)
    char_count = len(text)
    sentence_count = len(sentences)
    avg_word_len = round(sum(len(word) for word in words) / len(words), 2)

    # Generate word cloud
    word_freq = dict(Counter(words).most_common(10))
    plt.bar(word_freq.keys(), word_freq.values())
    plt.savefig('word_cloud.png')
    plt.clf()

    # Return results
    return {
        'word_count': word_count,
        'char_count': char_count,
        'sentence_count': sentence_count,
        'avg_word_len': avg_word_len,
        'word_freq': word_freq
    }


def display_results(results):
    for key, value in results.items():
        if key == 'word_freq':
            print(f'Most common words: {list(value.keys())}')
        else:
            print(f'{key.capitalize()}: {value}')


def save_results(results, stats_out, word_cloud_out):
    with open(stats_out, 'w') as f:
        for key, value in results.items():
            if key == 'word_freq':
                f.write(f'Most common words: {list(value.keys())}\n')
            else:
                f.write(f'{key.capitalize()}: {value}\n')

    plt.bar(results['word_freq'].keys(), results['word_freq'].values())
    plt.savefig(word_cloud_out)
    plt.clf()


@click.command()
@click.option('--input', default='text.txt', help='Input file for text analysis')
@click.option('--output', default='out.txt', help='Output file for text statistics')
def main(input, output):
    text = read_file(input)
    results = analyze_text(text)
    display_results(results)
    save_results(results, output, 'word_cloud.png')
    print(f'Text statistics saved to {output}.')


if __name__ == '__main__':
    main()
