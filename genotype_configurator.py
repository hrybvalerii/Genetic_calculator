import tkinter as tk
from tkinter import ttk
from config import FONT_NAME, MAX_PHEN_LEN, ALLELES_RANGE, GENE_RANGE
import math
import json


class ConfigWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title('Genotype_configurator')
        self.window.geometry('900x700')

        self.genotype_label = tk.Label(self.window, text='Genotype', font=(FONT_NAME, 12))
        self.genotype_label.grid(row=0, column=1, padx=5)
        self.phenotype_label = tk.Label(self.window, text='Phenotype', font=(FONT_NAME, 12))
        self.phenotype_label.grid(row=0, column=2, padx=5)

        self.genes_menubutton = ttk.Menubutton(self.window, text='Number of genes')
        self.genes_menubutton.grid(row=0, column=0, padx=(0, 5))
        self.genes_sub_num = tk.Menu(self.genes_menubutton)
        for num in GENE_RANGE:
            self.genes_sub_num.add_command(label=str(num), command=lambda opt=num: self.add_locus(opt))

        self.genes_menubutton.configure(menu=self.genes_sub_num)

        self.set_button = tk.Button(self.window, text='set', font=(FONT_NAME, 10), height=1, width=15,
                                    command=lambda: self.read_entries())
        self.set_button.grid(row=0, column=5, padx=10, pady=10)

        self.locuses = []
        self.info = {}

        self.add_locus(1)

        self.window.bind('<Button-1>', self.lose_focus)

    def add_locus(self, number):
        """
        Adds to the window a specified number of Generow objects which consists of
        :param number:
        :return:
        """
        Generow.number_of_row = 0
        for locus in self.locuses:
            locus.destroy()
        self.locuses = []
        for locus_num in range(number):
            self.locuses.append(Generow(self.window, 1 + 10 * locus_num))

    def read_entries(self):
        if all(loccus.check_valid() for loccus in self.locuses):
            self.info = {}
            for locus in self.locuses:
                for allel in locus.alleles:
                    if allel.genotype_field.get() and allel.phenotype_field.get():
                        self.info[allel.genotype_field.get()] = allel.phenotype_field.get()
                        allel.genotype_field.delete(0, 'end')
                        allel.phenotype_field.delete(0, 'end')

            with open('genotypes.json', 'w') as f:
                json.dump(self.info, f)
            self.window.destroy()

    def lose_focus(self, press):
        if 100 < press.x > 450:
            self.window.focus_set()


class Generow:
    number_of_row = 0

    def __init__(self, window, start):
        self.window = window
        Generow.number_of_row += 1
        self.start_position = start

        self.gene_label = (tk.Label(self.window, text=f'Gene{self.number_of_row}'))
        self.allele_menu = ttk.Menubutton(self.window, text='Number of alleles')
        self.sub = tk.Menu(self.allele_menu)

        for option in ALLELES_RANGE:
            self.sub.add_command(label=str(option), command=lambda opt=option: self.add_alleles(opt))

        self.allele_menu.configure(menu=self.sub)
        self.allele_menu.grid(row=self.start_position, column=5)

        self.gene_label.grid(row=self.start_position, column=0)
        self.alleles = []
        self.add_alleles(2,)

    def check_valid(self):
        return all(a.check_valid() for a in self.alleles)

    def add_alleles(self, n_alleles):
        self.clear_alleles()
        possible_genotypes = n_alleles + math.comb(n_alleles, 2)
        for gene_comb in range(possible_genotypes):
            self.alleles.append(GenotypePhenotypeEntry(self.window))
            self.alleles[gene_comb].genotype_field.grid(row=gene_comb + self.start_position, column=1)
            self.alleles[gene_comb].phenotype_field.grid(row=gene_comb + self.start_position, column=2)
            self.alleles[gene_comb].message.grid(row=gene_comb + self.start_position, column=3)
        self.alleles[-1].genotype_field.grid_configure(pady=(0, 10))
        self.alleles[-1].phenotype_field.grid_configure(pady=(0, 10))
        self.gene_label.grid_configure(rowspan=possible_genotypes)
        self.allele_menu.grid_configure(rowspan=possible_genotypes)

    def clear_alleles(self):
        for entry in self.alleles:
            entry.delete()
            self.alleles = []

    def destroy(self):
        self.gene_label.grid_forget()
        self.allele_menu.grid_forget()
        self.clear_alleles()


class GenotypePhenotypeEntry:
    def __init__(self, window):
        self.window = window
        self.genotype_field = tk.Entry(self.window, width=12, font=(FONT_NAME, 14), validate='focusout',
                                       validatecommand=self.gen_validation)
        self.phenotype_field = tk.Entry(self.window, width=12, font=(FONT_NAME, 14), validate='focusout',
                                        validatecommand=self.phen_validation)

        self.message = tk.Label(self.window, width=25, text='', fg='red', wraplength=200,
                                font=(FONT_NAME, 10), justify='left')
        self.warnings = ['', '']

    def gen_validation(self):
        """
        Validates the genotype entry field(should contain 2 letters)
        Appends tick to the warning attribute if content is valid and error message if not
        :return:
        """
        input_gen = self.genotype_field.get()
        if len(input_gen) == 2:
            self.warnings[0] = '\u2713'
            if self.check_valid():
                self.display_warn()
            return True
        else:
            self.warnings[0] = 'Genotype length should be 2 characters long'
            self.display_warn()
            return False

    def phen_validation(self):
        """
        Validates the phenotype entry field(should contain no more than 15 characters)
        Appends tick to the warning attribute if content is valid and error message if not
        :return:
        """
        input_gen = self.phenotype_field.get()
        if 0 < len(input_gen) <= MAX_PHEN_LEN:
            self.warnings[1] = '\u2713'
            if self.check_valid():
                self.display_warn()
            return True
        else:
            self.warnings[1] = 'Phenotype description should range from 1 to 15 characters'
            self.display_warn()
            return False

    def display_warn(self):
        self.message.config(text=max(self.warnings, key=len))

    def check_valid(self):
        return set(self.warnings) == {'\u2713'}

    def delete(self):
        self.genotype_field.grid_forget()
        self.phenotype_field.grid_forget()
        self.message.grid_forget()
