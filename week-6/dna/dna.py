import sys
import csv


def main():
    # validates program arguments
    validate_arguments()
    # reads in DNA samples from possible matches
    persons = read_persons()
    # reads in the DNA sequence to be tested against the samples
    sequence = read_sequence()
    # test the sequence with the samples to find a match
    person = dna_match(persons, sequence)
    # print the result
    print(person['name'] if person != None else "No match")


def read_persons():
    persons = []
    filename = sys.argv[1]

    # open file
    with open(filename) as csvfile:
        # read csv as dictionary
        reader = csv.DictReader(csvfile)
        # adds each row to persons list
        for row in reader:
            persons.append(row)

    return persons


def read_sequence():
    sequence = ''
    filename = sys.argv[2]

    with open(filename) as file:
        sequence = file.read()

    return sequence


def dna_match(persons, sequence):
    # create a list with the patterns to seach in the DNA sequence. sample: ['AGATC', 'AATG', 'TATC']
    patterns = extract_pattern(persons)
    # count the patterns appearances in sequence.txt file and based on the same index as [12, 13, 15]
    apperances = count_appearances(patterns, sequence)
    # search for a person who has the same amount of STRs appearances
    person = find_person(patterns, apperances, persons)

    return person


def extract_pattern(data):
    patterns = []

    for key in data[0]:
        if key != 'name':
            patterns.append(key)

    return patterns


def count_appearances(patterns, sequence):
    appearances = []

    for pattern in patterns:
        continous_appearances = coumpute_biggest_continuous_appearances(
            pattern, sequence)
        appearances.append(continous_appearances)

    return appearances


def coumpute_biggest_continuous_appearances(pattern, sequence):
    count = 1

    # look for contecutives patterns and stops when found the biggest continuous sequence
    while True:
        if pattern * count in sequence:
            count += 1
        else:
            count -= 1
            break

    return count


def find_person(patterns, appearances, persons):
    for person in persons:
        found = True
        for i in range(len(patterns)):
            if person[patterns[i]] != str(appearances[i]):
                found = False
                break
        if found:
            return person


def validate_arguments():
    if len(sys.argv) != 3:
        sys.exit('Usage: python dna.py <database.csv> <sequence.txt>')


if __name__ == '__main__':
    main()
