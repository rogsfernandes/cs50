#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);
int get_score(char letter);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!");
    }
    else
    {
        printf("Tie!");
    }
    printf("\n");
}

int compute_score(string word)
{
    int score = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        score += get_score(word[i]);
    }

    return score;
}

int get_score(char letter)
{
    int index = 0;
    int ascii = (int)letter;

    if (ispunct(ascii) || isdigit(ascii) || isspace(ascii))
    {
        return 0;
    }

    index = ascii - (isupper(ascii) ? 'A' : 'a');

    return POINTS[index];
}