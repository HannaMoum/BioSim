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

    def update(self, new_dict):
        for key, value in new_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __setattr__(self, name, value):
        if name == 'age_max':
            if 0 <= value < 100:
                raise ValueError(f'Values must be between 0 and 100: {value} ')

class Graphics(Graphics_param):

    def __init__(self, numpy_island_map, hist_specs):
        self._island_plot = self.make_plot_map(numpy_island_map)

    @property
    def island_plot(self):
        return self._island_plot

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
        plot_map = self.island_plot
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
            #ax.set_xticklabels(range(1, data.shape[2] + 1))
            #ax.set_yticklabels(range(1, data.shape[1] + 1))

            #plt.show()
            return ax

    def plotting_population_count(self, herb_data: object, carn_data: object, ax: object, year):
        """Brukes til å plotte population size over tid"""
        """Data er np array, med en sum per år i simuleringen"""
        with plt.style.context('default'):
            # fig, ax = plt.subplots()
            ax.plot(herb_data[0:year], linestyle='dashed', color='green', label='herbs')
            ax.plot(carn_data[0:year], color='red', label='carns')
            ax.set_title('Population size', loc='left')
            ax.set_xlabel('Years')
            ax.set_ylabel('Number of animals')
            leg = ax.legend(loc='center left')
            # plt.show()
            # fig.savefig('Test_plot.pdf')
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


    def make_grid(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, year=-1):
        scale = 1.6
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(str(f'Year: {(year + 1):.0f}'), fontsize=36, x=0.08, y=0.95)

        grid = plt.GridSpec(10, 14, wspace=0.5, hspace=1)

        map_ax = plt.subplot(grid[0:3, 0:4])
        self.plot_island_map(map_ax)

        herb_heatax = plt.subplot(grid[0:3, 4:9])
        self.plot_heatmap(data_heat_herb, 'herbivore', herb_heatax, year = year)

        carn_heatax = plt.subplot(grid[0:3, 9:14])
        self.plot_heatmap(data_heat_carn, 'carnivore', carn_heatax, year = year)

        pop_ax = plt.subplot(grid[4:10, 0:5])
        self.plotting_population_count(herb_data, carn_data, pop_ax, year = year)

        age_ax = plt.subplot(grid[6:8, 5:13])
        weight_ax = plt.subplot(grid[8:10, 5:13])
        fitness_ax = plt.subplot(grid[4:6, 5:13])
        self.plot_histogram(hist_herb_data, hist_carn_data, age_ax, weight_ax, fitness_ax, year)


        return fig

    def make_movie(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, year_ = 10):
        def make_frame(year_frame):
            fig = self.make_grid(data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, int(year_frame))
            return mplfig_to_npimage(fig) # Tar fig-en og lager til numpy-image som kan brukes videre.

        animation = VideoClip(make_frame, duration=year_-1) # VideoClip får returen fra make_frame, som er en numpy-image. Duration er lengden på videoen.
        # animation.write_gif(filename + '.gif', fps=1)
        animation.write_videofile('C:/temp/direkte_video' + '.mp4', fps=1) # fps er antall bilder per sekund

    def make_from_files(self, data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, year_ = 10):
        format = 'png'

        def make_frame(year_frame):
            fig = self.make_grid(data_heat_herb, data_heat_carn, herb_data, carn_data, hist_herb_data, hist_carn_data, int(year_frame))

            fig.savefig(f'C:/temp/figs/{year_frame:05d}.{format}', format=format)

        for year in range(year_):
            make_frame(year)

        fps = 1
        image_folder = 'C:/temp/figs'
        image_files = [os.path.join(image_folder, img)
                       for img in os.listdir(image_folder)
                       if img.endswith(".png")]# Lager en liste over alle filene
        image_files.sort()

        filename = 'C:/temp/video_fra_bilder.mp4'
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps) # Går gjennom et og et bilde og bygger opp video-kuben.
        clip.write_videofile(filename) # Lager det om til en videofil.