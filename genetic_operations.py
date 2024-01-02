from math import gcd
from functools import reduce
import json


class Specimen:
    def __init__(self, genotype_str: str):
        self.genotype = []
        self.calculate_genotype(genotype_str)
        self.gamets = self.get_gamets()
        with open('genotypes.json', 'r') as f:
            phenotypes = json.load(f)
        self.phenotype = tuple([phenotypes[locus] for locus in self.genotype])

    def __repr__(self):
        return f'{"".join(self.genotype)}({", ".join(self.phenotype)})'

    def __eq__(self, spec2):
        return self.genotype == spec2.genotype

    def __hash__(self):
        return hash(''.join(self.genotype))

    def calculate_genotype(self, genotype_str: str):

        while genotype_str:
            self.genotype += [genotype_str[:2]]
            genotype_str = genotype_str[2:]

    def get_gamets(self):
        result = []
        for i in range(2 ** len(self.genotype)):
            bin_num = str(bin(i)[2:])
            bin_num = bin_num.rjust(len(self.genotype), '0')
            elem = ''
            for ind, character in enumerate(bin_num):
                elem += self.genotype[ind][int(character)]
            result.append(elem)
        return result


def hybridize(genotype1: Specimen, genotype2: Specimen) -> list:
    """
    The function takes 2 arguments Specimen objects and returns list of all their offspring with a corresponding ratio.
    List is filled with specimen objects.
    :param genotype1: Specimen object
    :param genotype2: Specimen object
    :return: list with all children
    """
    with open('genotypes.json', 'r') as f:
        phenotypes = json.load(f)
    offspring = []
    for gam1 in genotype1.gamets:
        for gam2 in genotype2.gamets:
            child = ''.join([allele1 + allele2 if allele1 + allele2 in phenotypes else allele2 + allele1
                             for allele1, allele2 in zip(gam1, gam2)])
            offspring.append(Specimen(child))
    return offspring


class Generation:
    def __init__(self, offspring):
        self.offspring = offspring
        self.phenotypes_dict = {}
        self.get_phen_dist()

    def get_phen_dist(self):
        """
        Calculates and displays distribution of phenotypes(percenatage of each phenotype and genotype)
        result is stored in phenotypes_dict attribute.
        :return:
        """
        phenotypes_list = [specimen.phenotype for specimen in self.offspring]
        phenotypes_set = set(phenotypes_list)
        for phenotype in phenotypes_set:
            phenotype_percentage = round(phenotypes_list.count(phenotype) / len(phenotypes_list) * 100, 2)
            genotype_list = []
            for child in set(self.offspring):
                if child.phenotype == phenotype:
                    genotype_percentage = round(self.offspring.count(child) / len(self.offspring) * 100, 2)
                    genotype_list.append(f"{''.join(child.genotype)}_{genotype_percentage}%")
            self.phenotypes_dict[f"{' '.join(phenotype)} {phenotype_percentage}%"] = f"({', '.join(genotype_list)})"

    def next_generation(self):
        next_gen_list = []
        for specimen1 in self.offspring:
            for specimen2 in self.offspring:
                next_gen_list.extend(hybridize(specimen1, specimen2))
        return Generation(optimize(next_gen_list))


def optimize(lst: list) -> list:
    """
    Takes any not empty list, counts occurence of each element and divides number of occurences by the gcd
    :param lst: not empty list
    :return: list where the amount of elements is less or the same but their ratio is constant
    """
    count_dict = {elem: lst.count(elem)for elem in set(lst)}
    gcd_for_amounts = reduce(gcd, count_dict.values())
    optimized_list = []
    for elem, amount in count_dict.items():
        for ind in range(int(amount / gcd_for_amounts)):
            optimized_list.append(elem)
    return optimized_list



