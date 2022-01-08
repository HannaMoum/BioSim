""" Class handling the geography of the island"""
import textwrap
from lowland import Landscapes #Landscape is main class
    # Do we automatically also import subclasses in this case? // Do manually?

class Island:

    def __init__(self, geography, initial_pop):
        """
        Geography: String consisting of the letters W, D, L, H representing landscapes.
                   Every row must contain the same amount of letters (same number of columns)
        """
        self._geogr = geography
        ## Må mest sannsynlig ha en attribute for initial population
        self.initial_pop = initial_pop

    @property
    def geogr(self):
        """ Source url to find all subclasses (read 08.01):
        https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name"""
        self._geogr = textwrap.dedent(self._geogr) #Remove indents
        self._geogr = self._geogr.split() # Result: ['WWW', 'WLW', 'WWW']

        length_check = len(self._geogr[0])
        for element in self._geogr:

                for letter in element: #symbol check
                    if letter not in ('W', 'L', 'H', 'D'):
                        raise TypeError(
                            f'{letter} is not a defined landscape.\n'
                            f'Defined landscapes are: \
                            {[cls.__name__ for cls in Landscapes.__subclasses__()]} \
                            respectively given by their belonging capital letter.')

            if len(element) != length_check:
                raise ValueError ('All rows must have the same number of columns')

        return self._geogr # ['WWW', 'WLW', 'WWW']

    @property
    def map(self):
        """
        convert self.geogr to dictionary of coordinates
            self.geogr = ['WWW', 'WLW', 'WWW']
        to
            {(1,1): Water(), (1,2): Lowland(), ...}

        return self.map
        """
        self._map = {}

        for row, string in enumerate(self.geogr):
            for col, letter in enumerate(string):
                self._map[(row + 1, col + 1)] = self.create_landscape(letter)
                # +1 becuase we start from (1,1) not (0,0)
        return self._map


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

    #def wordbook(self):
        #all_landscapes = {'W': Water()}... Working on idea

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


    def convert_geography_to_coordinates(self):
        """
        convert self.geogr to dictionary of coordinates
        self.geogr = ['WWW', 'WLW', 'WWW']
        to
        {(1,1): Water(), (1,2): Lowland(), ...}

        return coordinate dictionary holding landscapes // update self.geogr ?
        """
        coordinates = {}

        for row, string in enumerate(self.geogr):
            for col, letter in enumerate(string):
                coordinates[(row + 1, col + 1)] = self.create_landscape(letter)
                # +1 becuase we start from (1,1) not (0,0)

        return coordinates
        pass


    def handle_initial_population(self):
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

            coordinates[location].add_animals(herb_pop, carn_pop) #obs! kAN SENDE INN TOMME LISTER

        """
        ini_herbs = []
        ini_carns = []

        for dictionary in self.initial_pop:
            location = dictionary['loc']
            landscape_variable = coordinates[location]


            animals_in_this_pos = dictionary['pop']
            noe = add_animal(animals_in_this_pos)

            pass

        pass

    def find_color(self, landscape):
        #map_colours = {'L': 	RGB(152,251,152),
        #                'H': 	RGB(48,128,20),
        #                'D': 	RGB(255,236,139),
        #                W: RGB(0,104,139)}
        pass

    def plot_island(self):
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

