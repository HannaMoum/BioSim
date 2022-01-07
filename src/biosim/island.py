""" Class handling the geography of the island"""
import textwrap

#class Island:

def __init__(self, geography):
    """
    Geography: String consisting of the letters W, D, L, H representing landscapes.
               Every row must contain the same amount of letters (same number of columns)
    """

    self.geogr = geography

def letter_conversion():
    """ Covert letter to landscape type"""
    #conversion = {'L': Lowland} NO
    pass

#INside landscape, create def create_lanscape(self, pop):

def convert_geography_string_to_landscape_list(self):
    """
    WWW
    WLW   == [ [W(), W(), W()], [W(), L(), W()], [W(), W(), W()] ] 2D array
    WWW

    or convert til dict?
    -> [[W, W, W], [W, L, W], [W, W, W]] (contains string)
    then
    {(1,1): string2D_array[0][0]}

    return coordinate_map_with_landscapes
    """
    pass

def handle_initial_population():
    """
   Initial_population looks like:

    ini_pop = [{'loc': (3,4),
    'pop': [{'species': 'Herbivore',
            'age': 10, 'weight': 12.5},
        {'species': 'Herbivore',
            'age': 9, 'weight': 10.3},
        {'species': 'Carnivore',
            'age': 5, 'weight': 8.1}]}]

    herb_pop = []
    carn_pop = []
    ^ 1 kombi eller 2 separate lister

    for element in ini_pop: (element består av loc og species)
        place_in_location =  Hent ut location
        for animal in element['pop']:
            if *somehow check species
            herb_pop.append(Herbivore(age, weight)) // same with carnivores

        #landscape_of_correct_type = Species(age, weight) #Her på lanscape selv skille mellom ulike species


        variabel = correct_landscape(ini_pop)

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



