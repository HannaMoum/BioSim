""" Class handling the geography of the island"""
import textwrap
from landscapes import Landscapes #Landscape is main class
    # Do we automatically also import subclasses in this case? // Do manually?

#class Island:

def __init__(self, geography):
    """
    Geography: String consisting of the letters W, D, L, H representing landscapes.
               Every row must contain the same amount of letters (same number of columns)
    """

    self._geogr = geography


@property
def geography(self):
    self._geogr = textwrap.dedent(self._geogr) #Remove indents
    self._geogr = self._geogr.split() # Result: ['WWW', 'WLW', 'WWW']

    length_check = len(self._geogr[0])
    for element in self._geogr:
            for letter in element: #symbol check
                if letter not in('W', 'L', 'H', 'D'):
                    raise TypeError(f'{letter} is not a defined landscape. Use W, L, H or D.')
        if len(element) != length_check:
            raise ValueError ('All rows must have the same number of columns')
    return self._geogr



""" 
#Inside landscape:
    # Adjust input arguments to not exist.
    # Create add_animals method instead.
    # todo: This code should be transferred to animals after branchmerges, possibly as a general method
    # !!Does not apply to water. Raise error either in add_animals or the setters...
    def __init__(self):
        self._herb_pop = [] #or None...
        self._carn_pop = [] # ------

    @property
    def herb_pop(self):
        return self._herb_pop
    @herb_pop.setter
    def herb_pop(self, pop):
        self._herb_pop = pop

    #Same goes for carnivores...

    def add_animals(self, herb_population, carn_population): #Decide if this should be one or two args
        if len(herb_population) > 0:
             # Noe i denne duren for å ikke appende tomme lister til listene
        self.herb_pop += herb_population
        self.carn_pop += carn_population

"""

def create_landscape(self, string_letter):
    """
    returns a certain coordinate landscape type based on the geography-string
    ! Landscape requires no input values --> Getters and setters must be created as shown above."""
    if string_letter == 'W':
         return Water()
    if string_letter == 'L':
         return Lowland()
    if string_letter == 'H':
         return Highland()
    if string_letter == 'D':
         return Desert()
    pass


def convert_geography_string_to_landscape_list(self):
    """
    WWW
    WLW
    WWW

    convert til dict
    -> list = [[W, W, W], [W, L, W], [W, W, W]] (contains string) ?. split string
    then
    {(1,1): self.create_landscape(list[0][0])}
    {(1,1): Water(), (1,2): Lowland(), ...}

    return coordinate_map_with_landscapes // update self.geogr
    """
    coordniates = {}
    self._geogr = textwrap.dedent(self._geogr) #Remove indents #MVE TO PROPERTY
    geography_list = self._geogr.split()  # Result: ['WWW', 'WLW', 'WWW'] #MOVE TO PROPERTY
        #Every element represents a row, and the position of the letter represents the column
    rows = len(geography_list) #Attribue ?
    columns = len(geography_list[0])
    for element in geography_list:
        coordinates[]
    pass

def handle_initial_population():
    """
   Initial_population looks like:

    ini_pop = [{'loc': (3,4),
    'pop': [{'species': 'Herbivore',
            'age': 10, 'weight': 12.5},
        {'species': 'Herbivore',
            'age': 9, 'weight': 10.3}]}]

    herb_pop = []
    carn_pop = []                   <-- 1 kombi eller 2 separate lister

    CODE:
    for element in ini_pop: (element består av loc og species)
        location =  Hent ut location

        for animal in element['pop']:
            if *somehow check species
            herb_pop.append(Herbivore(age, weight)) // same with carnivores #Appending to temporary lists

        self.geogr[location].add_animals(herb_pop, carn_pop) #obs! kAN SENDE INN TOMME LISTER

    """
    pass

def find_color(landscape):
    #map_colours = {'L': 	RGB(152,251,152),
    #                'H': 	RGB(48,128,20),
    #                'D': 	RGB(255,236,139),
    #                W: RGB(0,104,139)}
    pass

def plot_island():
    pass

############# temporarily test area ###########
geo = """\
            WWW
            WLW
            WWW
        """

geo = textwrap.dedent(geo)
print(geo)

two_dim = [['W', 'L', 'H'], ['W', 'W', 'W'], ['L', 'L', 'L']]

print(two_dim[0][2])

ini_pop = [{'loc': (3,4),
'pop': [{'species': 'Herbivore',
'age': 10, 'weight': 12.5},
{'species': 'Herbivore',
'age': 9, 'weight': 10.3},
{'species': 'Carnivore',
'age': 5, 'weight': 8.1}]}]

