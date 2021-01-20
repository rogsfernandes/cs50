#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <cs50.h>

int compute_grade(string text);
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
bool is_sentence_end(char letter);

int main(void)
{
    string text = get_string("Text: ");

    int grade = compute_grade(text);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }
}

int compute_grade(string text)
{
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // L is the average number of letters per 100 words
    float L = (float)(letters * 100) / words;
    // S is the average number of sentences per 100 words
    float S = (float)(sentences * 100) / words;
    //  Coleman-Liau index
    int index = round((0.0588 * L) - (0.296 * S) - 15.8);

    return index;
}

int count_letters(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        count += isalpha(text[i]) ? 1 : 0;
    }

    return count;
}

int count_words(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        count += isspace(text[i]) ? 1 : 0;

        if (i == strlen(text) - 1)
            count++;
    }

    return count;
}

int count_sentences(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        count += is_sentence_end(text[i]) ? 1 : 0;
    }

    return count;
}

bool is_sentence_end(char letter)
{
    return letter == '.' || letter == '!' || letter == '?';
}