#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

string encrypt_text(string key, string plaintext);
char encrypt_char(string key, char c);
bool validate_key(string key);

    int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if (!validate_key(key))
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext = encrypt_text(key, plaintext);

    printf("ciphertext: %s\n", ciphertext);
}

string encrypt_text(string key, string plaintext)
{
    string ciphertext = plaintext;

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            ciphertext[i] = encrypt_char(key, plaintext[i]);
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    return ciphertext;
}

char encrypt_char(string key, char c)
{
    char encrypted;

    if (isupper(c))
    {
        // getting the key by converting char from ASCII index to alphabetical index
        encrypted = toupper(key[(c - 'A')]);
    }
    else
    {
        encrypted = tolower(key[(c - 'a')]);
    }

    return encrypted;
}

bool validate_key(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }

    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        if (i + 1 == strlen(key))
        {
            break;
        }

        if (key[i] == key[i + 1])
        {
            return false;
        }
    }

    return true;
}