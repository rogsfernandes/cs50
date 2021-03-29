from cs50 import get_string


def main():
    text = get_string('Text: ')
    # computes the grade based on Coleman-Liau formula
    grade = compute_grade(text)
    # generates message based on the grade
    message = generate_message(grade)

    print(message)


def compute_grade(text):
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # L is the average number of letters per 100 words
    l = (letters * 100) / words
    # S is the average number of sentences per 100 words
    s = (sentences * 100) / words
    # Coleman-Liau index
    index = round((0.0588 * l) - (0.296 * s) - 15.8)

    return index


def count_letters(text):
    return len([c for c in text if c.isalpha()])


def count_words(text):
    return len([s for s in text if s.isspace()]) + 1


def count_sentences(text):
    punctiations = ['!', '.', '?']
    return len([p for p in text if p in punctiations])


def generate_message(grade):
    message = "Grade " + str(grade)

    # Changes message if grade is greater than 16
    if grade >= 16:
        message = "Grade 16+"
    # Changes message if grade is lesser than 16
    if grade < 1:
        message = "Before Grade 1"

    return message


if __name__ == '__main__':
    main()
