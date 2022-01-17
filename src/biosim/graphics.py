import os
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.video.io.ImageSequenceClip
from biosim.base_logger import logger




@dataclass
class GraphicsParams:
    ymax_animals: int
    cmax_animals_herbivore: int = 50
    cmax_animals_carnivore: int = 50

    age_max: float = 60
    age_delta: float = 2
    weight_max: float = 60
    weight_delta: float = 2
    fitness_max: float = 1
    fitness_delta: float = 0.05

    codes_for_landscape_types: str = 'WLHD'
    plot_values_for_landscape_types: str = '0123'
    island_map_colors: tuple = ('blue', 'darkgreen', 'lightgreen', 'yellow')

    def transform_landscape_type_from_str_to_int(self, value):
        """

        Parameters
        ----------
        value: `{'L', 'H', 'D', W'}`
            Landscape letter

        Returns
        -------
        `int`
        """
        if value in self.codes_for_landscape_types:
            replacement_values = list(zip(self.codes_for_landscape_types, self.plot_values_for_landscape_types))
            for letter, number in replacement_values:
                if value == letter:
                    return int(number)


class Graphics(GraphicsParams):

    def __init__(self, base_map, hist_specs: dict,
                 ymax_animals: int, cmax_animals: dict,
                 vis_years: int, img_dir, img_base,
                 img_fmt, img_years):

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
        """ Plots the map of the island
        Parameters
        ----------
        ax: `object`
            The axes for the plot

        Returns
        -------
        ax: `object`
            The axes with the plot
        """
        colormap = ['blue']
        if 'L' in self._base_map:
            colormap.append('darkgreen')
        if 'H' in self._base_map:
            colormap.append('lightgreen')
        if 'D' in self._base_map:
            colormap.append('yellow')
        self.island_map_colors = tuple(colormap)

        # Konveterer en numpy array med bokstaver (str) til en numpy array med tall 0, 1, 2 og 3.
        island_map_plot = np.copy(self._base_map)
        # Gjør det mulig at fx kan benyttes celle for celle.
        v_transform_landscape_type_from_str_to_int = np.vectorize(self.transform_landscape_type_from_str_to_int)
        # Bruker fx celle for celle på island_map_plot
        island_map_plot[:, :] = v_transform_landscape_type_from_str_to_int(island_map_plot)
        island_map_plot = np.array(island_map_plot, dtype=int) # Konverterer fra siffer (tall som str) til tall (int).

        row, col = island_map_plot.shape
        colormap = colors.ListedColormap(self.island_map_colors)

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

    def _plot_heatmap(self, heat_map_data: object, species: str, ax:object)->object:
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
            raise ValueError('Species must be Herbivore or Carnivore')

        ax = sns.heatmap(heat_map_data[:, :], cmap=cmap, ax=ax,
                         center=center, xticklabels=[x for x in range(1, heat_map_data.shape[1] + 1)],
                         yticklabels=[x for x in range(1, heat_map_data.shape[0] + 1)])
        ax.set_title(title)

        return ax

    def _plot_population_size(self, herb_data: object, carn_data: object, ax: object)->object:
        """
        Brukes til å plotte population size over tid
        Data er np array, med en sum per år i simuleringen
        """
        years =np.asarray([x for x in range(1, len(herb_data)+1)])
        ax.plot(years, herb_data, color='green', label='Herbivore')
        ax.plot(years, carn_data, color='red', label='Carnivore')
        ax.set_title('Population size', loc='left')
        ax.set_xlabel('Years')
        ax.set_ylabel('Number of animals')
        ax.legend(loc='upper left')
        if self.ymax_animals:
            ax.set(ylim=(0, self.ymax_animals))

        return ax

    def _set_histogram_specs(self, hist_specs: dict):
        """Setting the parameters for plotting histograms"""
        if hist_specs is None:
            return True

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

    def _plot_histogram(self, histogram_herbivore_data: list, histogram_carnivore_data: list,
                        ax_age:object, ax_weight:object, ax_fitness:object) -> object:
        """Plotting the histograms for age, weight and fitness"""
        # Setting colors for Herbivores, Carnivores
        hist_colors = ['green', 'red']

        herbivore_data = histogram_herbivore_data
        carnivore_data = histogram_carnivore_data

        if carnivore_data.shape == (0,):
            carnivore_data = np.zeros(shape=(1, 3))
        if herbivore_data.shape == (0,):
            herbivore_data = np.zeros(shape=(1, 3))

        # Fitness
        ax_fitness.hist([herbivore_data[:, 2], carnivore_data[:, 2]],
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
        ax_age.hist([herbivore_data[:, 0], carnivore_data[:, 0]],
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
        ax_weight.hist([herbivore_data[:, 1], carnivore_data[:, 1]],
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

    def _make_grid(self, heatmap_data_herbivore:object, heatmap_data_carnivore:object,
                   population_size_herbivore:object, population_size_carnivore:object,
                   histogram_data_herbivore:object, histogram_data_carnivore:object,
                   year:int):
        plot_year = year

        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(str(f'Year: {plot_year:.0f}'), fontsize=36, x=0.15, y=0.95)

        grid = plt.GridSpec(10, 14, wspace=0.75, hspace=1.5)

        map_ax = plt.subplot(grid[0:3, 0:4])
        self._plot_island_map(map_ax)

        herb_heatax = plt.subplot(grid[0:3, 4:9])
        self._plot_heatmap(heatmap_data_herbivore, 'Herbivore', herb_heatax)

        carn_heatax = plt.subplot(grid[0:3, 9:14])
        self._plot_heatmap(heatmap_data_carnivore, 'Carnivore', carn_heatax)

        pop_ax = plt.subplot(grid[4:10, 0:5])
        self._plot_population_size(population_size_herbivore, population_size_carnivore, pop_ax)

        age_ax = plt.subplot(grid[6:8, 6:13])
        weight_ax = plt.subplot(grid[8:10, 6:13])
        fitness_ax = plt.subplot(grid[4:6, 6:13])
        self._plot_histogram(histogram_data_herbivore, histogram_data_carnivore, age_ax, weight_ax, fitness_ax)

        return fig

    def _save_grid(self, fig: object, year: int):
        fig.savefig(f'{self.img_dir}/{self.img_base}_{year:05d}.{self.img_fmt}', format=self.img_fmt)

        msg = f'Saved: {self.img_dir}/{self.img_base}_{year:05d}.{self.img_fmt}'
        logger.info(msg)

    def show_grid(self, heatmap_data_herbivore:object, heatmap_data_carnivore:object,
                  population_size_herbivore:object, population_size_carnivore:object,
                  histogram_data_herbivore:object, histogram_data_carnivore:object,
                  pause:float, year:int, show: bool, save: bool):

        fig = self._make_grid(heatmap_data_herbivore, heatmap_data_carnivore,
                              population_size_herbivore, population_size_carnivore,
                              histogram_data_herbivore, histogram_data_carnivore, year)
        if show:
            plt.pause(pause)
            logger.info('Grid displayed')

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

        msg = f'Movie made: {filename}'
        logger.info(msg)
