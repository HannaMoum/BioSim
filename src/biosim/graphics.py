import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from dataclasses import dataclass

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
        island_map_plot = np.copy(numpy_island_map) # Lager intern kopi, for å unngå å ødelegge opprinnelig array. Hadde bare blitt et view om man ikke hadde gjort det.
        vcode_landscape = np.vectorize(self.code_landscape) # Vektoriserer funksjonen. Funksjonen kan da benyttes celle for celle i arrayen (eller et utvalg av arrayen).
        island_map_plot[:, :] = vcode_landscape(island_map_plot) # Bruker den vektoriserte funksjonen element for element i slicen som er laget (her alle celler).
        island_map_plot = np.array(island_map_plot, dtype=int)  # Konverterer fra siffer (tall som str) til tall (int).

        return island_map_plot
        # Returnerer np array med verdiene 0 til 3, som kan brukes til plotting.

    def plot_island_map(self, plot_map=None, scale = 3):
        if plot_map == None:
            plot_map = self.island_plot
        row, col = plot_map.shape
        with plt.style.context('seaborn-whitegrid'): # Konfigurerbar? Skal dette være en input?
            colormap = colors.ListedColormap(['blue', 'darkgreen', 'lightgreen', 'yellow']) # Skal dette være en input
            fig, ax = plt.subplots(figsize=(col / scale, row / scale))
            ax.imshow(plot_map, cmap=colormap, extent=[1, col + 1, row + 1, 1])
            ax.set_xticks(list(range(1, col + 1)))
            ax.set_yticks(list(range(1, row + 1)))
            plt.show()

        return ax # Returnerer grafen

    def plot_population_development(self, yearly_population_size):
        with plt.style.context('seaborn-whitegrid'): # Konfigurerbar? Skal dette være en input?
            fig, ax = plt.subplots()
            ax.plot(yearly_population_size)
            plt.show()


    def plot_panel(self):
        pass
        # Skal plotte det ferdige panelet, med de ulike plottene i en figur (grid).
        # En fig med mange axes.
