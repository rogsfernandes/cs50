#include <stdio.h>
#include <regex.h>
#include <string.h>
#include <cs50.h>

bool isNumberOnly(string digits);
string isValid(string digits);
bool validateWithLuhn(string digits);
bool isMasterCard(string digits);
bool isVisa(string digits);
bool isAmex(string digits);

int main(void)
{
    string digits = get_string("Number: ");

    while (isNumberOnly(digits) != 0)
    {
        digits = get_string("Number: ");
    }

    printf("%s\n", isValid(digits));
}

bool isNumberOnly(string digits)
{
    regex_t regex;
    regcomp(&regex, "[^A-Za-z\\-]", 0);
    return regexec(&regex, digits, 0, NULL, 0);
}

string isValid(string digits)
{
    if (strlen(digits) < 13)
    {
        return "INVALID";
    }

    bool valid = validateWithLuhn(digits);
    if (!valid)
    {
        return "INVALID";
    }

    if (isVisa(digits))
    {
        return "VISA";
    }

    if (isAmex(digits))
    {
        return "AMEX";
    }

    if (isMasterCard(digits))
    {
        return "MASTERCARD";
    }

    return "INVALID";
}

bool validateWithLuhn(string digits)
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

bool isMasterCard(string digits)
{
    return digits[0] == '5' && (digits[1] == '1' || digits[1] == '2' || digits[1] == '3' || digits[1] == '4' || digits[1] == '5');
}

bool isAmex(string digits)
{
    return digits[0] == '3' && (digits[1] == '4' || digits[1] == '7');
}

bool isVisa(string digits)
{
    return digits[0] == '4';
}