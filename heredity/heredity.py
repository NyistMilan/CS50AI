import csv
import itertools
from operator import ge
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1
    for person in people:
        sum = 1
        # Find out what group the person is in [one_gene or two_gene or None], [have_trait or None]
        person_trait = True if person in have_trait else False
        person_mutated_gene = 2 if person in two_genes else 1 if person in one_gene else 0

        # Prob of the trait being True or False based on number of mutated genes
        sum *= PROBS["trait"][person_mutated_gene][person_trait]

        # If person doesn't have parents in the dataset
        mother = people[person]["mother"]
        father = people[person]["father"]

        if not mother and not father:
            sum *= PROBS["gene"][person_mutated_gene]
        # If person has parents find out the probability of getting mutated genes
        else:
            mother_mutated_gene = 2 if mother in two_genes else 1 if mother in one_gene else 0
            father_mutated_gene = 2 if father in two_genes else 1 if father in one_gene else 0
            mother_prob = 0
            father_prob = 0

            # Mutated gene will transfer with a prob of 1.0, but it can mutate with a prob of PROBS["mutation"]
            if mother_mutated_gene == 2:
                mother_prob = 1 - PROBS["mutation"]
            # Either a mutated gene is transfered or a healthy one
            elif mother_mutated_gene == 1:
                mother_prob = 0.5
            else:
            # All genes are healthy so the only way to get a mutated one is for it to mutate (PROBS["mutation"])
                mother_prob = PROBS["mutation"]
            
            # Same for the father gene
            if father_mutated_gene == 2:
                father_prob = 1 - PROBS["mutation"]
            elif father_mutated_gene == 1:
                father_prob = 0.5
            else:
                father_prob = PROBS["mutation"]
            
            # Person inheriting two mutated genes
            if person_mutated_gene == 2:
                sum *= mother_prob * father_prob
            # Person inheriting one mutated gene
            elif person_mutated_gene == 1:
                sum *= (1 - father_prob) * (mother_prob) + (1 - mother_prob) * (father_prob)
            # Person inheriting no mutated gene
            else:
                sum *= (1 - mother_prob) * (1 - father_prob)
        
        probability *= sum

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        person_mutated_gene = 2 if person in two_genes else 1 if person in one_gene else 0
        probabilities[person]["gene"][person_mutated_gene] += p

        person_trait = True if person in have_trait else False
        probabilities[person]["trait"][person_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalizing Trait values...
        trait_sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / trait_sum
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / trait_sum

        # Normalizing Gene values...
        gene_sum = probabilities[person]["gene"][2] + probabilities[person]["gene"][1] + probabilities[person]["gene"][0]
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / gene_sum
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / gene_sum
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / gene_sum


if __name__ == "__main__":
    main()