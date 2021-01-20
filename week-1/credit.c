#include <stdio.h>
#include <regex.h>
#include <string.h>
#include <cs50.h>

bool is_number(string digits);
string is_valid(string digits);
bool validate_luhn_algorithm(string digits);
bool is_mastercard(string digits);
bool is_visa(string digits);
bool is_amex(string digits);

int main(void)
{
    string digits = get_string("Number: ");

    while (is_number(digits) != 0)
    {
        digits = get_string("Number: ");
    }

    printf("%s\n", is_valid(digits));
}

bool is_number(string digits)
{
    regex_t regex;
    regcomp(&regex, "[^A-Za-z\\-]", 0);
    return regexec(&regex, digits, 0, NULL, 0);
}

string is_valid(string digits)
{
    if (strlen(digits) < 13)
    {
        return "INVALID";
    }

    bool valid = validate_luhn_algorithm(digits);
    if (!valid)
    {
        return "INVALID";
    }

    if (is_visa(digits))
    {
        return "VISA";
    }

    if (is_amex(digits))
    {
        return "AMEX";
    }

    if (is_mastercard(digits))
    {
        return "MASTERCARD";
    }

    return "INVALID";
}

bool validate_luhn_algorithm(string digits)
{
    int sum = 0;
    for (int i = strlen(digits) - 2; i < strlen(digits); i = i - 2)
    {
        int digit = (digits[i] - 48) * 2;
        if (digit > 9)
        {
            sum += (int)(digit / 10);
            sum += digit % 10;
        }
        else
        {
            sum += (int)digit;
        }
    }
    for (int k = strlen(digits) - 1; k < strlen(digits); k = k - 2)
    {
        sum += digits[k] - 48;
    }

    if (sum % 10 == 0)
    {
        return true;
    }

    return false;
}

bool is_mastercard(string digits)
{
    return digits[0] == '5' && (digits[1] == '1' || digits[1] == '2' || digits[1] == '3' || digits[1] == '4' || digits[1] == '5');
}

bool is_amex(string digits)
{
    return digits[0] == '3' && (digits[1] == '4' || digits[1] == '7');
}

bool is_visa(string digits)
{
    return digits[0] == '4';
}