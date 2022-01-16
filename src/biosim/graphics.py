import os
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns

# pip install moviepy. Må pip installeres i environmentet du jobber i
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.video.io.ImageSequenceClip


@dataclass
class GraphicsParams:
    ymax_animals: int
    cmax_animals_herbivore: int = 50
    cmax_animals_carnivore: int = 50

    img_dir: str = 'C:/'
    img_base: str = 'BioSim'
    img_fmt: str = 'png'

    age_max: float = 60
    age_delta: float = 2
    weight_max: float = 60
    weight_delta: float = 2
    fitness_max: float = 1
    fitness_delta: float = 0.05

    codes_for_landscape_types: str = 'WLHD'

    def code_landscape(self, value):  # Finn mer beskrivende funksjonsnavn
        # TODO: Funksjonen må oppdateres med å sjekke at input value er lovlig.
        plot_values_for_landscape_types = '0123'
        # Vurder å ha de som parametere, sånn at de kan brukes globalt
        if value in self.codes_for_landscape_types:
            replacement_values = list(zip(self.codes_for_landscape_types, plot_values_for_landscape_types))
            for letter, number in replacement_values:
                if value == letter:
                    return int(number)


class Graphics(GraphicsParams):

    def __init__(self, base_map, hist_specs: dict,
                 ymax_animals: int, cmax_animals: dict,
                 vis_years: int, img_dir, img_base,
                 img_fmt, img_years):
        """
        numpy_island_map er base_map fra World.
        """
        #self._island_plot = self._make_plot_map(numpy_island_map)
        self._base_map = base_map
        self._set_histogram_specs(hist_specs)
        self.ymax_animals = ymax_animals
        self._set_cmax_animals(cmax_animals)
        self._vis_years = vis_years
        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt

        if not img_years:
            self._img_years = vis_years
        else:
            self._img_years = img_years

    def _plot_island_map(self, ax:object)->object:
        """
        Lager numpy array (kartet) som brukes for å plotte verdenskartet.
        Plotter verdenskartet
        """
        # Konveterer en numpy array med bokstaver (str) til en numpy array med tall 0, 1, 2 og 3.
        island_map_plot = np.copy(self._base_map)
        vcode_landscape = np.vectorize(self.code_landscape) # Gjør det mulig at fx kan benyttes celle for celle.
        island_map_plot[:, :] = vcode_landscape(island_map_plot) # Bruker fx celle for celle på island_map_plot
        island_map_plot = np.array(island_map_plot, dtype=int) # Konverterer fra siffer (tall som str) til tall (int).

        row, col = island_map_plot.shape
        colormap = colors.ListedColormap(['blue', 'darkgreen', 'lightgreen', 'yellow'])

        ax.imshow(island_map_plot, cmap=colormap, extent=[1, col + 1, row + 1, 1])
        ax.set_xticks(range(1, col + 1))
        ax.set_yticks(range(1, row + 1))
        ax.set_xticklabels(range(1, col + 1), rotation=90)
        ax.set_yticklabels(range(1, row + 1))
        ax.set(title='Island map')

        return ax

    def _set_cmax_animals(self, cmax_animals: dict):
        """{'Herbivore': 50, 'Carnivore': 20}"""

        if cmax_animals is None:
            return True

        for key, value in cmax_animals.items():
            if key == 'Herbivore':
                self.cmax_animals_herbivore = value
            if key == 'Carnivore':
                self.cmax_animals_carnivore = value

    def _plot_heatmap(self, data: object, species: str, ax:object, year: int)->object:
        """Plotter heatmap"""
        if species == 'Herbivore':
            title = 'Herbivore distribution'
            cmap = 'Greens'
            center = self.cmax_animals_herbivore
        elif species == 'Carnivore':
            title = 'Carnivore distribution'
            cmap = 'Reds'
            center = self.cmax_animals_carnivore
        else:
            raise ValueError('Species mus be Herbivore or Carnivore')

        ax = sns.heatmap(data[year, :, :], cmap=cmap, ax=ax,
                         center=center, xticklabels=[x for x in range(1, data.shape[2] + 1)],
                         yticklabels=[x for x in range(1, data.shape[1] + 1)])
        ax.set_title(title)

        return ax

    def _plot_population_size(self, herb_data: object, carn_data: object, ax: object, year)->object:
        """
        Brukes til å plotte population size over tid
        Data er np array, med en sum per år i simuleringen
        """

        ax.plot(herb_data[0:year], color='green', label='Herbivore')
        ax.plot(carn_data[0:year], color='red', label='Carnivore')
        ax.set_title('Population size', loc='left')
        ax.set_xlabel('Years')
        ax.set_ylabel('Number of animals')
        ax.legend(loc='upper left')
        if self.ymax_animals:
            ax.set(ylim=(0, self.ymax_animals))

        return ax

    def _set_histogram_specs(self, hist_specs: dict):
        """Setting the parameters for plotting histograms"""
        for key, value in hist_specs.items():
            if key == 'fitness':
                self.fitness_max = value['max']
                self.fitness_delta = value['delta']
            if key == 'age':
                self.age_max = value['max']
                self.age_delta = value['delta']
            if key == 'weight':
                self.weight_max = value['max']
                self.weight_delta = value['delta']

    def _plot_histogram(self, hist_herb_data: list, hist_carn_data: list,
                        ax_age, ax_weight, ax_fitness,
                        year: int) -> object:
        """Plotting the histograms for age, weight and fitness"""
        # Setting colors for Herbivores, Carnivores
        hist_colors = ['green', 'red']

        yearly_herb_data = hist_herb_data[year]
        yearly_carn_data = hist_carn_data[year]

        if yearly_carn_data.shape == (0,):
            yearly_carn_data = np.zeros(shape=(1, 3))
        if yearly_herb_data.shape == (0,):
            yearly_herb_data = np.zeros(shape=(1, 3))

        # Fitness
        ax_fitness.hist([yearly_herb_data[:, 2], yearly_carn_data[:, 2]],
                        bins=int(self.fitness_max / self.fitness_delta),
                        range=(0, self.fitness_max),
                        histtype='step',
                        stacked=False,
                        fill=False,
                        color=hist_colors,
                        label=['Herbivore', 'Carnivore'])
        ax_fitness.legend(bbox_to_anchor=(1.01, 1))
        ax_fitness.set(xlim=(0, self.fitness_max),
                       title='Fitness')

        # Age
        ax_age.hist([yearly_herb_data[:, 0], yearly_carn_data[:, 0]],
                    bins=int(self.age_max / self.age_delta),
                    range=(0, self.age_max),
                    histtype='step',
                    stacked=False,
                    fill=False,
                    color=hist_colors,
                    label=['Herbivore', 'Carnivore'])
        ax_age.set(xlim=(0, self.age_max),
                   title='Age')

        # Weight
        ax_weight.hist([yearly_herb_data[:, 1], yearly_carn_data[:, 1]],
                       bins=int(self.weight_max / self.weight_delta),
                       range=(0, self.weight_max),
                       histtype='step',
                       stacked=False,
                       fill=False,
                       color=hist_colors,
                       label=['Herbivore', 'Carnivore'])
        ax_weight.set(xlim=(0, self.weight_max),
                      title='Weight')

        return ax_age, ax_weight, ax_fitness

    def _make_grid(self, data_heat_herb, data_heat_carn,
                   herb_data, carn_data,
                   hist_herb_data, hist_carn_data, year):
        plot_year = year
        year -= 1  # Må ta -1 fordi dataene er null-basert (første index er 0)

        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(str(f'Year: {plot_year:.0f}'), fontsize=36, x=0.15, y=0.95)

        grid = plt.GridSpec(10, 14, wspace=0.75, hspace=1.5)

        map_ax = plt.subplot(grid[0:3, 0:4])
        self._plot_island_map(map_ax)

        herb_heatax = plt.subplot(grid[0:3, 4:9])
        self._plot_heatmap(data_heat_herb, 'Herbivore', herb_heatax, year=year)

        carn_heatax = plt.subplot(grid[0:3, 9:14])
        self._plot_heatmap(data_heat_carn, 'Carnivore', carn_heatax, year=year)

        pop_ax = plt.subplot(grid[4:10, 0:5])
        self._plot_population_size(herb_data, carn_data, pop_ax, year=year)

        age_ax = plt.subplot(grid[6:8, 6:13])
        weight_ax = plt.subplot(grid[8:10, 6:13])
        fitness_ax = plt.subplot(grid[4:6, 6:13])
        self._plot_histogram(hist_herb_data, hist_carn_data, age_ax, weight_ax, fitness_ax, year)

        return fig

    def _save_grid(self, fig: object, year: int):
        fig.savefig(f'{self.img_dir}/{self.img_base}_{year:05d}.{self.img_fmt}', format=self.img_fmt)

    def show_grid(self, data_heat_herb, data_heat_carn,
                  herb_data, carn_data,
                  hist_herb_data, hist_carn_data,
                  pause, year, show: bool, save: bool):
        fig = self._make_grid(data_heat_herb, data_heat_carn,
                              herb_data, carn_data,
                              hist_herb_data,
                              hist_carn_data, year)
        if show:
            plt.pause(pause)

        if save:
            self._save_grid(fig, year)

        plt.close(fig)

    def make_movie_from_files(self):
        fps = 1
        image_files = [os.path.join(self.img_dir, img)
                       for img in os.listdir(self.img_dir)
                       if img.endswith("." + self.img_fmt)]  # Lager en liste over alle filene
        image_files.sort()

        filename = f'{self.img_dir}/{self.img_base}_video.mp4'
        # Går gjennom et og et bilde og bygger opp video-kuben.
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile(filename)  # Lager det om til en videofil.
