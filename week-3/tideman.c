#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
bool is_valid_lock(int index);
bool is_cycle(int index, int root, int target);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        for (int j = 1; j < pair_count - i; j++)
        {
            if (preferences[pairs[i].winner][pairs[i].loser] < preferences[pairs[j].winner][pairs[j].loser])
            {
                pair aux = pairs[i];
                pairs[i] = pairs[j];
                pairs[j] = aux;
            }
        }
    }

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        printf("Validating lock[%i][%i]...", pairs[i].winner, pairs[i].loser);
        if (is_valid_lock(i))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }

    for (int i = 0; i < pair_count; i++)
    {
        printf("lock[%d][%d]=%i\n", pairs[i].winner, pairs[i].loser, locked[pairs[i].winner][pairs[i].loser]);
    }
    return;
}

bool is_valid_lock(int index)
{
    int root = pairs[index].winner;
    int target = pairs[index].loser;

    return !is_cycle(index, root, target);
}

bool is_cycle(int index, int root, int target)
{
    for (int i = 0; i < pair_count; i++)
    {
        // looks for each pair that has the target as the root and is locked
        printf("target=%i\n", target);
        printf("winner=%i\n", pairs[i].winner);
        printf("locked=%i\n", locked[pairs[i].winner][pairs[i].loser]);
        if (pairs[i].winner == target && locked[pairs[i].winner][pairs[i].loser] && i != index)
        {
            // printf("found %i,%i\n", pairs[i].winner, pairs[i].loser);
            // if the loser is the root and the winner is the target, than it creates a cycle and shouldnt be added
            if (pairs[i].loser == root)
            {
                return true;
            }
            // else check the connections where this target is the root, to trace every possible way
            else
            {
                printf("recursion lock[%i][%i]...", pairs[i].winner, pairs[i].loser);
                return is_cycle(index, root, pairs[i].loser);
            }
        }
    }

    return false;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        // check wether this winner has any edge pointing to they
        bool is_winner = true;

        for (int j = i + 1; j < pair_count; j++)
        {
            if (pairs[j].loser == pairs[i].winner && locked[pairs[j].winner][pairs[j].loser])
            {
                is_winner = false;
            }
        }
        if (is_winner)
        {
            printf("%s\n", candidates[pairs[i].winner]);
            return;
        }
    }
    return;
}
