import os
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns

#pip install moviepy. Må pip installeres i environmentet du jobber i
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.video.io.ImageSequenceClip

from datetime import datetime

@dataclass
class Graphics_param:
    ymax_animals: int
    cmax_animals_herbivore: int
    cmax_animals_carnivore: int

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


    def code_landscape(self, value): # Finn mer beskrivende funksjonsnavn
        # TODO: Funksjonen må oppdateres med å sjekke at input value er lovlig.
        plot_values_for_landscape_types = '0123'
        # Vurder å ha de som parametere, sånn at de kan brukes globalt
        if value in self.codes_for_landscape_types:
            replacement_values = list(zip(self.codes_for_landscape_types, plot_values_for_landscape_types))
            for letter,number in replacement_values:
                if value == letter:
                    return int(number)

    # def update_params(self, new_dict):
    #     for key, value in new_dict.items():
    #         if hasattr(self, key):
    #             setattr(self, key, value)

class Graphics(Graphics_param):

    def __init__(self, numpy_island_map, hist_specs:dict, ymax_animals:int, cmax_animals:dict, vis_years:int,
                 img_dir, img_base, img_fmt, img_years):
        """
        numpy_island_map er base_map fra World.
        """
        self._island_plot = self.make_plot_map(numpy_island_map)
        self._set_hist_specs(hist_specs)
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

    def _set_hist_specs(self, hist_specs: dict):
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

    def _set_cmax_animals(self, cmax_animals: dict):
        """{'Herbivore': 50, 'Carnivore': 20}"""
        for key, value in cmax_animals.items():
            if key == 'Herbivore':
                self.cmax_animals_herbivore = value
            if key == 'Carnivore':
                self.cmax_animals_carnivore = value

    def make_plot_map(self, numpy_island_map):
        """Lager numpy array (kartet) som brukes for å plotte verdenskartet."""
        island_map_plot = np.copy(
            numpy_island_map)  # Lager intern kopi, for å unngå å ødelegge opprinnelig array. Hadde bare blitt et view om man ikke hadde gjort det.
        vcode_landscape = np.vectorize(
            self.code_landscape)  # Vektoriserer funksjonen. Funksjonen kan da benyttes celle for celle i arrayen (eller et utvalg av arrayen).
        island_map_plot[:, :] = vcode_landscape(
            island_map_plot)  # Bruker den vektoriserte funksjonen element for element i slicen som er laget (her alle celler).
        island_map_plot = np.array(island_map_plot, dtype=int)  # Konverterer fra siffer (tall som str) til tall (int).

        return island_map_plot
        # Returnerer np array med verdiene 0 til 3, som kan brukes til plotting.

    def plot_island_map(self, ax):
        """Plotter verdenskartet"""
        #if plot_map == None:
        plot_map = self._island_plot
        row, col = plot_map.shape
        with plt.style.context('seaborn-whitegrid'):  # Konfigurerbar? Skal dette være en input?
            colormap = colors.ListedColormap(['blue', 'darkgreen', 'lightgreen', 'yellow'])  # Skal dette være en input
            #fig, ax = plt.subplots(figsize=(col / scale, row / scale))
            ax.imshow(plot_map, cmap=colormap, extent=[1, col + 1, row + 1, 1])
            ax.set_xticks(range(1, col + 1))
            ax.set_yticks(range(1, row + 1))
            ax.set_xticklabels(range(1, col + 1))
            ax.set_yticklabels(range(1, row + 1))
            #plt.show()

        return ax  # Returnerer grafen

    def plot_heatmap(self, data: object, species: str, ax, square = True, year: int = -1):
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
            raise ValueError('Feil')

        ax = sns.heatmap(data[year, :, :], annot=False, cmap=cmap, ax = ax, center = center)
        ax.set_title(title)
        #ax.set_xticklabels(range(1, data.shape[2] + 1))
        #ax.set_yticklabels(range(1, data.shape[1] + 1))

        #plt.show()
        return ax

    def plotting_population_count(self, herb_data: object, carn_data: object, ax: object, year):
        """
        Brukes til å plotte population size over tid
        Data er np array, med en sum per år i simuleringen
        """

        ax.plot(herb_data[0:year], linestyle='dashed', color='green', label='herbs')
        ax.plot(carn_data[0:year], color='red', label='carns')
        ax.set_title('Population size', loc='left')
        ax.set_xlabel('Years')
        ax.set_ylabel('Number of animals')
        ax.legend(loc='upper left')
        if self.ymax_animals:
            ax.set(ylim=(0, self.ymax_animals))

        return ax

    def plot_histogram(self, hist_herb_data:object, hist_carn_data:object, ax_age, ax_weight, ax_fitness, year: int = -1)-> object:
        """
        """
        colors = ['green', 'red']
        age, weight, fitness = (0, 1, 2)
        """
        max_age, delta_age = (60, 2) #TODO: Skal leses inn som parametere når BioSim objektet instansieres
        max_weight, delta_weight = (60, 2)
        max_fitness, delta_fitness = (1, 0.05)
        """
        #fig, ax = plt.subplots(nrows=3, ncols=1, figsize = (12, 18))
        yearly_herb_data = hist_herb_data[year]
        yearly_carn_data = hist_carn_data[year]

        # Age
        ax_age.hist([yearly_herb_data[:, 0],yearly_carn_data[:,0]],
                    bins=int(self.age_max/self.age_delta),
                    range=(0,self.age_max),
                    histtype= 'step',
                    stacked=False,
                    fill=False,
                    color=colors,
                    label=['Herbivore', 'Carnivore'])
        ax_age.set(xlim=(0, self.age_max),
                   title = 'Age')

        # Weight
        ax_weight.hist([yearly_herb_data[:, 1], yearly_carn_data[:, 1]],
                       bins=int(self.weight_max / self.weight_delta),
                       range=(0, self.weight_max),
                       histtype='step',
                       stacked=False,
                       fill=False,
                       color=colors,
                       label=['Herbivore', 'Carnivore'])
        ax_weight.set(xlim=(0, self.weight_max),
                      title = 'Weight')

        # Fitness
        ax_fitness.hist([yearly_herb_data[:, 2], yearly_carn_data[:, 2]],
                        bins=int(self.fitness_max / self.fitness_delta),
                        range=(0, self.fitness_max),
                        histtype='step',
                        stacked=False,
                        fill=False,
                        color=colors,
                        label = ['Herbivore', 'Carnivore'])
        ax_fitness.legend(bbox_to_anchor = (1.01, 1))
        ax_fitness.set(xlim=(0, self.fitness_max),
                      title='Fitness')

        return ax_age, ax_weight, ax_fitness

    def show(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, year = -1):
        """
                vis_years = 0, disables graphics
                vis_years = None, then the last year in the simulation i used to make graphics
                vis_years = any, periodic update of the graphics
                """
        if self._vis_years == 0:
            return None
        if self._vis_years == None:
            year = -1
            self._make_grid(data_heat_herb,
                           data_heat_carn,
                           herb_data,
                           carn_data,
                           hist_herb_data,
                           hist_carn_data,
                           year=year)
            return None
        if self._vis_years >= 1:
            sim_years = len(herb_data)
            for y in range(0,sim_years, self._vis_years):
                fig = self._make_grid(data_heat_herb,
                                data_heat_carn,
                                herb_data,
                                carn_data,
                                hist_herb_data,
                                hist_carn_data,
                                year=y)

                fig.pause(0.2)
                #plt.show()


    def _make_grid(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, pause, year=-1):
        if year == -1: # Convert default year to a plotable last year
            plot_year = len(herb_data)
        else:
            plot_year = year + 1

        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(str(f'Year: {(plot_year):.0f}'), fontsize=36, x=0.08, y=0.95)

        grid = plt.GridSpec(10, 14, wspace=0.5, hspace=1)

        map_ax = plt.subplot(grid[0:3, 0:4])
        self.plot_island_map(map_ax)

        herb_heatax = plt.subplot(grid[0:3, 4:9])
        self.plot_heatmap(data_heat_herb, 'Herbivore', herb_heatax, year = year)

        carn_heatax = plt.subplot(grid[0:3, 9:14])
        self.plot_heatmap(data_heat_carn, 'Carnivore', carn_heatax, year = year)

        pop_ax = plt.subplot(grid[4:10, 0:5])
        self.plotting_population_count(herb_data, carn_data, pop_ax, year = year)

        age_ax = plt.subplot(grid[6:8, 5:13])
        weight_ax = plt.subplot(grid[8:10, 5:13])
        fitness_ax = plt.subplot(grid[4:6, 5:13])
        self.plot_histogram(hist_herb_data, hist_carn_data, age_ax, weight_ax, fitness_ax, year)

        plt.pause(pause)
        return fig

    def make_movie(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, year_ = 10):
        def make_frame(year_frame):
            fig = self._make_grid(data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, int(year_frame))
            return mplfig_to_npimage(fig) # Tar fig-en og lager til numpy-image som kan brukes videre.

        animation = VideoClip(make_frame, duration=year_-1) # VideoClip får returen fra make_frame, som er en numpy-image. Duration er lengden på videoen.
        # animation.write_gif(filename + '.gif', fps=1)
        animation.write_videofile('C:/temp/direkte_video' + '.mp4', fps=1) # fps er antall bilder per sekund

    def make_from_files(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, year_ = 10):
        print(self.img_dir)
        print((f'{self.img_dir}/{self.img_base}{12:05d}.{self.img_fmt}'))

        def make_frame(year_frame):
            fig = self._make_grid(data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, int(year_frame))

            fig.savefig(f'{os.path.join(self.img_dir, self.img_base)}{year_frame:05d}.{self.img_fmt}', format=self.img_fmt)

        for year in range(year_):
            make_frame(year)

        fps = 1
        image_files = [os.path.join(self.img_dir, img)
                       for img in os.listdir(self.img_dir)
                       if img.endswith("."+self.img_fmt)]# Lager en liste over alle filene
        image_files.sort()

        filename = f'{os.path.join(self.img_dir, self.img_base)}_video.mp4'
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps) # Går gjennom et og et bilde og bygger opp video-kuben.
        clip.write_videofile(filename) # Lager det om til en videofil.