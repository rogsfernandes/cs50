#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

string alphabet = "abcdefghijklmnopqrstuvwxyz";

int guard(int argc, string argv[]);
char encrypt(int key, char c);

int main(int argc, string argv[])
{
    if (guard(argc, argv))
        return 1;

    int key = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");
    string ciphertext = plaintext;

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            ciphertext[i] = encrypt(key, plaintext[i]);
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    printf("ciphertext: %s\n", ciphertext);
}

char encrypt(int key, char c)
{
    if (isupper(c))
    {
        int alphabet_index = c - 'A';
        return toupper(alphabet[(alphabet_index + key) % 26]);
    }
    else
    {
        int alphabet_index = c - 'a';
        return tolower(alphabet[(alphabet_index + key) % 26]);
    }
}

int guard(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key");
        return 1;
    }

    for (int j = 0; j < strlen(argv[1]); j++)
    {
        if (!isdigit(argv[1][j]))
        {
            printf("Usage: ./caesar key");
            return 1;
        }
    }

    return 0;
}