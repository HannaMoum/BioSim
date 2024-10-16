import os
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
import moviepy.video.io.ImageSequenceClip
from biosim.base_logger import logger


@dataclass
class GraphicsParams:
    """Provide default parameters for class :py:class:`.Graphics`."""
    cmax_animals_herbivore: int = 50  #: maximum color-code value for herbivore densities
    cmax_animals_carnivore: int = 50  #: maximum color-code value for carnivore densities

    age_max: float = 60  #: Maximum value for age histogram
    age_delta: float = 2  #: Bin width for age histogram
    weight_max: float = 60  #: Maximum value for weight histogram
    weight_delta: float = 2  #: Bin width for weight histogram
    fitness_max: float = 1  #: Maximum value for fitness histogram
    fitness_delta: float = 0.05  #: Bin width for fitness histogram

    codes_for_landscape_types: str = 'WLHD'  #: Landscape-codes as letters
    plot_values_for_landscape_types: str = '0123'  #: Landscape-codes as numbers
    island_map_colors: tuple = ('blue', 'darkgreen', 'lightgreen', 'yellow')  #: Island map colors

    def transform_landscape_type_from_str_to_int(self, value):
        """Replace landscape type letter with a number.

        Parameters
        ----------
        value: `{'L', 'H', 'D', W'}`
            Landscape letter

        Returns
        -------
        {'0', '1', '2', '3'}
            Integer representing a landscape.
        """
        if value in self.codes_for_landscape_types:
            replacement_values = list(zip(self.codes_for_landscape_types,
                                          self.plot_values_for_landscape_types))
            for letter, number in replacement_values:
                if value == letter:
                    return int(number)


class Graphics(GraphicsParams):
    """Create visualization from simulation ran by :py:class:`.BioSim`

    Parameters
    ----------
    base_map: `ndarray` of `str`
        Island map consisting of singular landscape letters.
    hist_specs: hist_specs: `dict`
            Specifications for histograms
    ymax_animals: `int` or `float`
        Number specifying y-axis limit for graph showing animal numbers
    cmax_animals: `dict`
        Dictionary specifying color-code limits for animal densities
    vis_years: `int`
        Years between visualization updates
    img_dir: `str`
        String with path to directory for figures
    img_base: `str`
        String with beginning of file name for figures
    img_fmt: `str`
        String with file type for figures, e.g. 'png'
    img_years: `int`
        Years between visualizations saved to files
    """

    def __init__(self, base_map, hist_specs, ymax_animals, cmax_animals, vis_years,
                 img_dir, img_base, img_fmt, img_years):

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

    def _plot_island_map(self, ax) -> object:
        """ Plot the map of the island.

        Notes
        ------
        Color-codes for the map are:
        Lowland: lightgreen, Highland: darkgreen, Desert: yellow, Water: blue.

        Parameters
        ----------
        ax: `object`
            Axes to hold the plot

        Returns
        -------
        ax: `object`
            Axes with the plot
        """
        colormap = ['blue']
        if 'L' in self._base_map:
            colormap.append('darkgreen')
        if 'H' in self._base_map:
            colormap.append('lightgreen')
        if 'D' in self._base_map:
            colormap.append('yellow')
        self.island_map_colors = tuple(colormap)

        island_map_plot = np.copy(self._base_map)
        v_transform_landscape_type_from_str_to_int = \
            np.vectorize(self.transform_landscape_type_from_str_to_int)
        island_map_plot[:, :] = v_transform_landscape_type_from_str_to_int(island_map_plot)
        island_map_plot = np.array(island_map_plot, dtype=int)

        row, col = island_map_plot.shape
        colormap = colors.ListedColormap(self.island_map_colors)

        ax.imshow(island_map_plot, cmap=colormap, extent=[1, col + 1, row + 1, 1])
        ax.set_xticks(range(1, col + 1))
        ax.set_yticks(range(1, row + 1))
        ax.set_xticklabels(range(1, col + 1), rotation=90)
        ax.set_yticklabels(range(1, row + 1))
        ax.set(title='Island map')

        return ax

    def _set_cmax_animals(self, cmax_animals):
        """Set cmax values for each species, if given.

        Parameters
        ----------
        cmax_animals: `dict`
            Dictionary specifying color-code limits for animal densities

        Returns
        -------
        `bool`
            True if :math:`\mathtt{cmax\_animals}` are unprovided.
        """
        if cmax_animals is None:
            return True

        for key, value in cmax_animals.items():
            if key == 'Herbivore':
                self.cmax_animals_herbivore = value
            if key == 'Carnivore':
                self.cmax_animals_carnivore = value

    def _plot_heatmap(self, heat_map_data, species, ax) -> object:
        """Plot heatmaps based on provided data from simulation.

        Parameters
        ----------
        heat_map_data: `ndarray`
            Array containing population for every location.
        species: `str`
            The species to make heat-map for.
        ax: `object`
            The axes to hold the plot

        Returns
        -------
        ax: `object`
            Axes containing the heatmap plot
        """
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

        ax = sns.heatmap(heat_map_data[:, :],
                         cmap=cmap,
                         ax=ax,
                         center=center,
                         xticklabels=[x for x in range(1, heat_map_data.shape[1] + 1)],
                         yticklabels=[x for x in range(1, heat_map_data.shape[0] + 1)])
        ax.set_title(title)

        return ax

    def _plot_population_size(self, herb_data, carn_data, ax):
        """
        Plot population size of herbivores and carnivores.

        Parameters
        ----------
        herb_data: `ndarray`
            One dimensional array containing the herbivores' population size for all
            simulated years.
        carn_data: `ndarray`
            One dimensional array containing the carnivores' population size for all
            simulated years.
        ax: `object`
            Axes to hold the plot

        Returns
        -------
        ax: `object`
            Axes with population size plot for both herbivores and carnivores.
        """
        years = np.asarray([x for x in range(1, len(herb_data) + 1)])
        ax.plot(years, herb_data, color='green', label='Herbivore')
        ax.plot(years, carn_data, color='red', label='Carnivore')
        ax.set_title('Population size', loc='left')
        ax.set_xlabel('Years')
        ax.set_ylabel('Number of animals')
        ax.legend(loc='upper left')
        if self.ymax_animals:
            ax.set(ylim=(0, self.ymax_animals))

        return ax

    def _set_histogram_specs(self, hist_specs):
        """Set histogram specifications.

        Parameters
        ----------
        hist_specs: `dict`, optional
            Specifications for histograms

            If not specified, :math:`\mathtt{hist\_specs}` are set to default values.

        Returns
        -------
        `bool`
            True if :math:`\mathtt{hist\_specs}` are unprovided.
        """
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

    def _plot_histogram(self,
                        histogram_herbivore_data,
                        histogram_carnivore_data,
                        ax_age,
                        ax_weight,
                        ax_fitness):
        """Plot histograms for age, weight and fitness.

        Parameters
        ----------
        histogram_herbivore_data: `ndarray`
            Array with one column per property, and one row per animal
        histogram_carnivore_data: `ndarray`
            Array with one column per property, and one row per animal
        ax_age: `object`
            Axes to hold plot for age histogram.
        ax_weight: `object`
            Axes to hold plot for weight histogram.
        ax_fitness: `object`
            Axes to hold plot for fitness histogram.

        Returns
        -------
        ax_age: `object`
            Axes with age distribution plot
        ax_weight: `object`
            Axes with weight distribution plot
        ax_fitness: `object`
            Axes with fitness distribution plot
        """
        # Set colors for Herbivores and Carnivores respectively
        hist_colors = ['green', 'red']

        herbivore_data = histogram_herbivore_data
        carnivore_data = histogram_carnivore_data

        if carnivore_data.shape == (0,):
            carnivore_data = np.zeros(shape=(1, 3))
        if herbivore_data.shape == (0,):
            herbivore_data = np.zeros(shape=(1, 3))

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

    def _make_grid(self, heatmap_data_herbivore,
                   heatmap_data_carnivore,
                   population_size_herbivore,
                   population_size_carnivore,
                   histogram_data_herbivore,
                   histogram_data_carnivore,
                   year):
        """Make grid with several plots.

        Parameters
        ----------
        heatmap_data_herbivore: `object`
            Array containing population data of herbivores in every location.
        heatmap_data_carnivore: `object`
            Array containing population data of carnivores in every location.
        population_size_herbivore: `object`
            One dimensional array containing the herbivores' population size for
            all simulated years.
        population_size_carnivore: `object`
            One dimensional array containing the carnivores' population size for
            all simulated years.
        histogram_data_herbivore: `object`
            Array with one column per property, and one row per herbivore.
        histogram_data_carnivore: `object`
            Array with one column per property, and one row per carnivore.
        year: `int`
            Specifying the year being displayed in the grid

        Returns
        -------
        fig: `object`
            Figure containing several axes with plots.
        """
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
        self._plot_histogram(histogram_data_herbivore,
                             histogram_data_carnivore,
                             age_ax, weight_ax, fitness_ax)

        return fig

    def _save_grid(self, fig, year):
        """Save grid with several plots.

        Parameters
        ----------
        fig: `object`
            Figure which is being saved
        year: `int`
            Specification of the year
        """
        fig.savefig(f'{self.img_dir}/{self.img_base}_{year:05d}.{self.img_fmt}',
                    format=self.img_fmt)

        msg = f'Saved: {self.img_dir}/{self.img_base}_{year:05d}.{self.img_fmt}'
        logger.info(msg)

    def show_grid(self, heatmap_data_herbivore, heatmap_data_carnivore,
                  population_size_herbivore, population_size_carnivore,
                  histogram_data_herbivore, histogram_data_carnivore,
                  pause, year, show, save):
        """Show grid created by :py:meth:`._make_grid`.

        Parameters
        ----------
        heatmap_data_herbivore: `object`
            Array containing population data of herbivores in every location.
        heatmap_data_carnivore: `object`
            Array containing population data of carnivores in every location.
        population_size_herbivore: `object`
            One dimensional array containing the herbivores' population size for
            all simulated years.
        population_size_carnivore: `object`
            One dimensional array containing the carnivores' population size for
            all simulated years.
        histogram_data_herbivore: `object`
            Array with one column per property, and one row per herbivore.
        histogram_data_carnivore: `object`
            Array with one column per property, and one row per carnivore.
        pause: `float`
            Specification of time the figure is displayed.
        year: `int`
            Specification of the year being displayed in the grid.
        show: `bool`
            Specification of whether the figure should be shown.
        save: `bool`
            Specification of whether the figure should be saved.
        """
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
        """Make movie in mp4 format from saved files of figures."""
        fps = 1
        image_files = [os.path.join(self.img_dir, img)
                       for img in os.listdir(self.img_dir)
                       if img.endswith("." + self.img_fmt)]
        image_files.sort()

        filename = f'{self.img_dir}/{self.img_base}_video.mp4'
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile(filename)

        msg = f'Movie made: {filename}'
        logger.info(msg)
