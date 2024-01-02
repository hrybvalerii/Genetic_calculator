import tkinter as tk
from genotype_configurator import ConfigWindow
from genetic_operations import Specimen, Generation, hybridize
from config import BG_COLOR, FONT_NAME


class GUI:
    def __init__(self):
        """
        Initialize the GUI window and set up the initial interface elements.
        """
        self.current_generation = None
        self.generation_number = 1

        self.root = tk.Tk()
        self.root.configure(background=BG_COLOR)
        self.root.geometry('800x600')
        self.root.tk.call('tk', 'scaling', 1.5)
        self.root.title("Genetic calculator")
        self.icon = tk.PhotoImage(file="Icon.png")
        self.root.iconphoto(False, self.icon)

        self.label = tk.Label(self.root, text='Parents genotypes:', font=(FONT_NAME, 16), background=BG_COLOR)
        self.label.grid(row=0, column=0, columnspan=4, pady=10, padx=5)

        self.venera_mirror = tk.Label(self.root, text='P: ' + '\u2640', font=(FONT_NAME, 14), background=BG_COLOR)
        self.venera_mirror.grid(row=1, column=0, padx=5)
        self.mars_spear = tk.Label(self.root, text='x  ' + '\u2642', font=(FONT_NAME, 14), background=BG_COLOR)
        self.mars_spear.grid(row=1, column=2, padx=5)

        self.entry1 = tk.Entry(self.root, width=12, font=(FONT_NAME, 14))
        self.entry1.grid(row=1, column=1, padx=5)
        self.entry2 = tk.Entry(self.root, width=12, font=(FONT_NAME, 14))
        self.entry2.grid(row=1, column=3, padx=5)

        self.calc_button = tk.Button(text='calculate Gen1', font=(FONT_NAME, 10), height=1, width=15, state=tk.DISABLED,
                                     command=self.calculate_results)
        self.calc_button.grid(row=1, column=4, padx=5, pady=0)

        self.parent_phenotype1 = tk.Label(text='...', font=(FONT_NAME, 14), background=BG_COLOR)
        self.parent_phenotype2 = tk.Label(text='...', font=(FONT_NAME, 14), background=BG_COLOR)
        self.parent_phenotype1.grid(row=2, column=1, padx=5, pady=20)
        self.parent_phenotype2.grid(row=2, column=3, padx=5, pady=20)

        self.generation = tk.Label(self.root, text=f'Gen{self.generation_number}: ', font=(FONT_NAME, 14),
                                   background=BG_COLOR)
        self.generation.grid(row=3, column=0, padx=5, pady=20)

        self.offspring = tk.Label(self.root, text='', font=(FONT_NAME, 14,), wraplength=550, background=BG_COLOR,
                                  fg="black")
        self.offspring.grid(row=3, column=1, padx=5, columnspan=4)

        self.config_button = tk.Button(text='Set genotypes/phenotypes', font=(FONT_NAME, 10), height=1, width=20,
                                       command=ConfigWindow)
        self.config_button.grid(row=1, column=5)

        self.next_gen_button = tk.Button(text='Next generation', font=(FONT_NAME, 10), height=1, width=20,
                                         state=tk.DISABLED, command=self.display_next_gen)
        self.next_gen_button.grid(row=2, column=5)
        self.check_parent_genotypes()
        self.root.mainloop()

    def calculate_results(self):
        """
        This function displays (self.offspring label) the result of hybridization
        between genotypes entered in entry fields
        :return: None
        """
        genotype1 = Specimen(self.entry1.get())
        genotype2 = Specimen(self.entry2.get())
        self.current_generation = Generation(hybridize(genotype1, genotype2))
        self.next_gen_button['state'] = tk.ACTIVE
        txt = ''
        for key, item in self.current_generation.phenotypes_dict.items():
            txt += f'{key}: {item}\n\n'
        self.offspring.config(text=txt, justify="left")
        self.generation_number = 1
        self.generation.config(text=f'F{self.generation_number}: ')

    def check_parent_genotypes(self):
        """
        Check the validity of the genotypes entered in the entry fields.
        Enable or disable the calculate button based on the presence of valid genotypes.
        Also displays parent phenotype in parent phenotype label
        :return:
        """
        button_active = False
        for field, parent_phen in zip((self.entry1, self.entry2), (self.parent_phenotype1, self.parent_phenotype2)):
            if field.get():
                try:
                    genotype = Specimen(field.get())
                    parent_phen.config(text=genotype.phenotype)
                except (IndexError, KeyError):
                    parent_phen.config(text='Unknown genotype')
                    break
            else:
                parent_phen.config(text='...')

                break
        else:
            button_active = True

        if button_active:
            self.calc_button['state'] = tk.ACTIVE

        else:
            self.calc_button['state'] = tk.DISABLED

        self.root.after(1000, self.check_parent_genotypes)

    def display_next_gen(self):
        """
        displays the result of hybridization between current generation specimen
        :return:
        """
        self.current_generation = self.current_generation.next_generation()
        txt = ''
        for key, item in self.current_generation.phenotypes_dict.items():
            txt += f'{key}: {item}\n'
        self.offspring.config(text=txt, justify="left")
        self.generation_number += 1
        self.generation.config(text=f'F{self.generation_number}: ')


if __name__ == '__main__':
    GUI()
