import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from dataclasses import dataclass
from world import BioSim
import seaborn as sns

@dataclass
class Graphics_param:
    codes_for_landscape_types: str = 'WLHD'

    def code_landscape(self, value): # Finn mer beskrivende funksjonsnavn
        # Funksjonen må oppdateres med å sjekke at input value er lovlig.
        plot_values_for_landscape_types = '0123'
        # Vurder å ha de som parametere, sånn at de kan brukes globalt
        if value in self.codes_for_landscape_types:
            replacement_values = list(zip(self.codes_for_landscape_types, plot_values_for_landscape_types))
            for letter,number in replacement_values:
                if value == letter:
                    return int(number)


class Graphics(Graphics_param):
    """Denne klassen skal spørre BioSim, om data og fremstille det grafisk"""

    def __init__(self, numpy_island_map):
        self._island_plot = self.make_plot_map(numpy_island_map)



    @property
    def island_plot(self):
        return self._island_plot

    def make_plot_map(self, numpy_island_map):
        """Lager numpy array (kartet) som brukes for å plotte verdenskartet."""
        island_map_plot = np.copy(numpy_island_map) # Lager intern kopi, for å unngå å ødelegge opprinnelig array. Hadde bare blitt et view om man ikke hadde gjort det.
        vcode_landscape = np.vectorize(self.code_landscape) # Vektoriserer funksjonen. Funksjonen kan da benyttes celle for celle i arrayen (eller et utvalg av arrayen).
        island_map_plot[:, :] = vcode_landscape(island_map_plot) # Bruker den vektoriserte funksjonen element for element i slicen som er laget (her alle celler).
        island_map_plot = np.array(island_map_plot, dtype=int)  # Konverterer fra siffer (tall som str) til tall (int).

        return island_map_plot
        # Returnerer np array med verdiene 0 til 3, som kan brukes til plotting.

    def plot_island_map(self, plot_map=None, scale = 3):
        """Plotter verdenskartet"""
        if plot_map == None:
            plot_map = self.island_plot
        row, col = plot_map.shape
        with plt.style.context('seaborn-whitegrid'): # Konfigurerbar? Skal dette være en input?
            colormap = colors.ListedColormap(['blue', 'darkgreen', 'lightgreen', 'yellow']) # Skal dette være en input
            fig, ax = plt.subplots(figsize=(col / scale, row / scale))
            ax.imshow(plot_map, cmap=colormap, extent=[1, col + 1, row + 1, 1])
            ax.set_xticks(range(1, col + 1))
            ax.set_yticks(range(1, row + 1))
            ax.set_xticklabels(range(1, col + 1))
            ax.set_yticklabels(range(1, row + 1))
            plt.show()

        return ax # Returnerer grafen


    def plotting_population_count(self, herb_data:object, carn_data: object, ax: object):
        """Brukes til å plotte population size over tid"""
        """Data er np array, med en sum per år i simuleringen"""
        with plt.style.context('default'):
            #fig, ax = plt.subplots()
            ax.plot(herb_data, linestyle = 'dashed', color = 'green', label='herbs')
            ax.plot(carn_data, color = 'red', label = 'carns')
            ax.set_title('Population size', loc='left')
            ax.set_xlabel('Years')
            ax.set_ylabel('Number of animals')
            leg = ax.legend(loc='center left')
            #plt.show()
            # fig.savefig('Test_plot.pdf')
            return ax

    def plot_heatmap(self, data: object, species: str, ax, square = True, year: int = -1):
        """Plotter heatmap"""
        #fig, ax = plt.subplots() # Midlertidig siden heatmap ikke vil inn i panelet.
        if species == 'herbivore':
            title = 'Herbivore distribution'
            cmap = 'Greens'
        elif species == 'carnivore':
            title = 'Carnivore distribution'
            cmap = 'Reds'
        else:
            raise ValueError('Feil')
        with plt.style.context('default'):
            ax = sns.heatmap(data[year, :, :], annot=True, cmap=cmap, ax = ax)
            ax.set_title(title)
            ax.set_xticklabels(range(1, data.shape[2] + 1))
            ax.set_yticklabels(range(1, data.shape[1] + 1))

            #plt.show()
            return ax

    def plot_histogram(self, hist_herb_data:object, hist_carn_data:object, ax_age, ax_weight, ax_fitness, year: int = -1)-> object:
        """
        """
        colors = ['green', 'red']
        age, weight, fitness = (0, 1, 2)
        max_age, delta_age = (60, 2) #TODO: Skal leses inn som parametere når BioSim objektet instansieres
        max_weight, delta_weight = (60, 2)
        max_fitness, delta_fitness = (1, 0.05)

        #fig, ax = plt.subplots(nrows=3, ncols=1, figsize = (12, 18))
        yearly_herb_data = hist_herb_data[year]
        yearly_carn_data = hist_carn_data[year]


        # Age
        ax_age.set_title('Age')
        ax_age.hist([yearly_herb_data[:, 0],yearly_carn_data[:,0]], bins=int(max_age/delta_age),
                     range=(0,max_age), histtype= 'step', stacked=False, fill=False, color=colors, label=['Herbivore', 'Carnivore'])
        leg = ax_age.legend()

        # Weight
        ax_weight.set_title('Weight')
        ax_weight.hist([yearly_herb_data[:, 1], yearly_carn_data[:, 1]], bins=int(max_weight / delta_weight),
                     range=(0, max_weight), histtype='step', stacked=False, fill=False, color=colors)

        # Fitness
        ax_fitness.set_title('Fitness')
        ax_fitness.hist([yearly_herb_data[:, 2], yearly_carn_data[:, 2]], bins=int(max_fitness / delta_fitness),
                        range=(0, max_fitness), histtype='step', stacked=False, fill=False, color=colors)

        plt.show()
        return ax_age, ax_weight, ax_fitness

    def heat(self, ax):
        #ax = sns.heatmap(np.random.rand(13, 21), square=True, ax=ax)
        ax=sns.histplot([1,2,3,4,5], ax=ax)
        return ax

    def show_panel(self, herb_data:object, carn_data: object, data: object, species: str, hist_herb_data, hist_carn_data, year = -1): #TODO: Gjør ferdig panel
        # TODO: Lag data objekt i biosim, som pakker alle dataene inn i f.eks. en dict. Da kan man sende hele dicten inn i her
        fig = plt.figure(figsize=(18, 12))
        if year == -1:
            year_title = len(herb_data)
        else:
            year_title = year
        fig.suptitle(str(f'Year: {year_title}'), fontsize=16, x=0.5, y=0.95)  # Bytt år

        grid = plt.GridSpec(12, 18, wspace = 0.1, hspace=1)

        population_size_ax = plt.subplot(grid[0:3, 0:3])
        self.plotting_population_count(herb_data, carn_data, population_size_ax)

        age_property_ax = plt.subplot(grid[5:8, 0:3])
        weight_property_ax = plt.subplot(grid[5:8, 6:9])
        fitness_property_ax = plt.subplot(grid[5:8, 12:15])
        self.plot_histogram(hist_herb_data, hist_carn_data, age_property_ax, weight_property_ax, fitness_property_ax,
                            year)

        heatmap_herbs_ax = plt.subplot(grid[8:, 15:])
        self.heat(heatmap_herbs_ax)

        plt.show()

    def heat(self, ax):
        ax = sns.heatmap(np.random.rand(13, 21), square=True, ax=ax)
        return ax

    def population(self, ax):
        ax = ax.plot(np.random.rand(20))
        return ax

    def hist_prop(self, ax):
        ax = ax.hist(np.random.normal(15, 5, 30), histtype='step')
        return ax

    def make_grid(self, year):
        scale = 1.6
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(str(f'Year: {(year + 1):.0f}'), fontsize=36, x=0.08, y=0.95)

        grid = plt.GridSpec(10, 14, wspace=0.5, hspace=1)

        #map_ax = plt.subplot(grid[0:3, 0:4])
        #self.showbasemap(self.base_map(), map_ax)

        herb_heatax = plt.subplot(grid[0:3, 4:9])
        self.heat(herb_heatax)

        carn_heatax = plt.subplot(grid[0:3, 9:14])
        self.heat(carn_heatax)

        pop_ax = plt.subplot(grid[4:10, 0:5])
        self.population(pop_ax)

        fitness_ax = plt.subplot(grid[4:6, 5:13])
        self.hist_prop(fitness_ax)

        age_ax = plt.subplot(grid[6:8, 5:13])
        self.hist_prop(age_ax)

        weight_ax = plt.subplot(grid[8:10, 5:13])
        self.hist_prop(weight_ax)

        return fig

