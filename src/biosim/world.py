import numpy as np
from landscape import Landscape
from random import choice


class World:

    #valid_letters = 'LHWD' noe som dette kanskje?

    def __init__(self, island_map, ini_pop): #TODO: Edit other files so that ini_pop is not an input
        """
        World er en klasse som skaper verden ut i fra ett gitt kart og parametere.
        Klassen holder orden på landskaps-objekter som ligger i kartet, og hvert landskapsobjekt
        kan inneholde dyr.
        Inneholder nårværende status (state). Tid ligger i BioSim.

        Tar i mot:
            island_map: Island_map er en tekst-streng som er ferdig validert i BioSim.
            ini_pop: dict for alle dyra som skal plasseres ut i verden. Den er ferdig valide
        """
        self._base_map = self._make_base_map(island_map)
        self._migrate_map = self._make_migrate_map()
        self._object_map = self._make_object_map()

        self._ini_pop = ini_pop #Not an input, not an attribute
        self.add_population(ini_pop) #Restructure this. Method has to be called in Biosim
        # TODO: Save ini_pop directly from input
        # Add_population returns nothing, it is an action of its' own

    @property
    def base_map(self):
        """Map of island consisting of landscape letters (`ndarray` of `str`)."""
        return self._base_map

    @property
    def migrate_map(self):
        """Map of the island's migratable and non-migratable cells (`ndarray` of `bool`).
        #Gives True/False if movement on to location is allowed"""
        return self._migrate_map

    @property
    def object_map(self):
        """Map of island consisting of landscape-object references (`ndarray` of `obj`)."""
        return self._object_map

    def _validate_island_map(self, island_map_list: list) -> bool:
        # Should already be textwrapped

        length_check = len(island_map_list[0])
        for element in island_map_list:

            for letter in element:
                if letter not in 'WHLD':
                    raise ValueError(
                        f'{letter} is not a defined landscape.\n'
                        f'Defined landscapes are: ["Lowland", "Highland", "Desert", "Water"]\n'
                        'respectively given by their belonging capital letter.')

            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')

            if not (element[0] and element[-1]) == 'W':
                raise ValueError('All the islands` outer edges must be of landscape Water.')

        if not (island_map_list[0] and island_map_list[-1]) == 'W' * length_check:
            raise ValueError('All the islands` outer edges must be of landscape Water.')

        return True

    def _make_base_map(self, input_map: str)-> object:
        """
        Mapping island with respect to each landscape letter.

        Parameters
        ----------
        input_map: `str`
            Geography of island.

            Made up by the letters 'W', 'D', 'L' and 'H' each representing a landscape.
            Forutsetter at den er ferdig validert.

        Returns
        -------
        _build_map: `ndarray` of `str`
            Array containing landscape letters in their respective positions.
        """

        map_list = input_map.split()
        self._validate_island_map(map_list)  # Validerer her, inne i øya selv
        row, col = len(map_list), len(map_list[0])

        build_map = np.empty(shape=(row, col), dtype='str')
        for row_index, row_string in enumerate(map_list):
            for col_index, landscape_letter in enumerate(row_string):
                build_map[row_index, col_index] = landscape_letter

        return build_map


    def _make_migrate_map(self) -> object:
        """Create a map mapping all migratable cells (`ndarray` of `bool`)."""
        return self._base_map != 'W'

    def _make_object_map(self)->object:
        """
        Create map of the island's landscape objects references.

        Returns
        -------
        _island_map_objects: `ndarray` of `obj`
            Array containing landscape objects in their respective positions.
        """
        object_map = np.empty(self._base_map.shape, dtype='object')
        vLandscape = np.vectorize(Landscape)
        object_map[:, :] = vLandscape(self._base_map)

        return object_map

    def add_population(self, population:dict):
        """
        Tar populasjons-dicten for hvert landskap og ber landskapet oppdatere populasjonen
        """
        for dictionary in population:

            r, c = dictionary['loc']
            r -= 1
            c -= 1
            landscape_object = self.object_map[r, c]

            population = dictionary['pop']
            landscape_object.add_animals(population)


    ###################################################################################################################
    # Data-objekter. Data som kan brukes til analyse, plotting.
    # Data per tidsenhet. Dataene inneholder nåværende status til world.
    # ----------------------------------------------------------------------------------------------------------------
    # Her kommer det ut en np.array med scalar-verdier
    def get_property_map(self, fx_map_type:str)->object:
        """
        Brukergrensesnittet som gjør at man kan skrive inn hvilken type informasjon som fabrikke nskal benytte seg av.
        Forteller fabrikken hvilken funksjon man vil bruke.
        getattr slår opp i klassen og ser om vi har en tilsvarende funksjon i klassen som samsvarer med navnet på den funksjonen vi putter inn.
        dir(BioSim)
        Om funksjonen ligger i klassen så sender den tilbake en referanse til funksjonsobjektet.
        """
        return self._make_property_map(getattr(self, fx_map_type), self.base_map, self.object_map)

    # Factory for property_maps
    def _make_property_map(self, fx: callable(object), base_map: object, object_map: object):
        property_map = np.empty(base_map.shape, dtype=float)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(object_map)
        return property_map

    # Parameter-funksjoner som kan brukes i fabrikken
    def v_size_herb_pop(self, location: object)->int:
        """Population sizer for herbivores at given location. """
        return location.herbivores_number

    def v_size_carn_pop(self, location: object)->int:
        """Population sizer for carnivores at given location."""
        return location.carnivores_number

    # ----------------------------------------------------------------------------------------------------------------
    # Her kommer det ut en np.array med objekter, som f.eks. inneholder hele landskapsobjektet

    def get_property_map_objects(self, fx_map_type:str) -> object:
        return self._make_property_map_objects(getattr(self, fx_map_type), self.base_map, self.object_map)

    def _make_property_map_objects(self, fx: callable(object), base_map: object, object_map: object):
        property_map = np.empty(base_map.shape, dtype=object)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(object_map)
        return property_map

    # TODO: Om vi får en populasjon per landskap kan disse bli til 1 funksjon
    def v_herb_properties_objects(self, location: object)->list:
        population_list = location.herbivores
        if len(population_list) > 0: # bare sjekke om den eksisterer
            liste = []
            for animal in population_list:
                liste.append((animal.age, animal.weight, animal.fitness))
            return liste

    def v_carn_properties_objects(self, location: object)->list:
        population_list = location.carnivores
        if len(population_list) > 0: # bare sjekke om den eksisterer
            liste = []
            for animal in population_list:
                liste.append((animal.age, animal.weight, animal.fitness))
            return liste
    ###################################################################################################################

    def do_migration(self):
        global_migrated_animals = []
        with np.nditer(self.object_map, flags=['multi_index', 'refs_ok']) as it:
            for grid_cell in it:
                current_loaction = grid_cell.item()

                if len(current_loaction.population) > 0: #if current_loaction.population:
                    local_migrated_animals = []
                    for animal in current_loaction.population:
                        if animal not in global_migrated_animals:

                            migrate_to_location = self._get_migrate_to_location(animal, it.multi_index)

                            if migrate_to_location:
                                migrate_to_location.population.append(animal)
                                local_migrated_animals.append(animal)

                    for animal in local_migrated_animals:
                        current_loaction.population.remove(animal)

                    global_migrated_animals += local_migrated_animals

    def _get_migrate_to_location(self, animal:object, location_coordinates: tuple)-> object:
        r, c = location_coordinates
        view = self.migrate_map[r - 1:r + 2, c - 1:c + 2]

        if animal.probability_to_migrate():
            direction = choice('NSEW')
            mask = np.array([[False, direction == 'N', False],
                             [direction == 'W', False, direction == 'E'],
                             [False, direction == 'S', False]])

            destination_location = self.object_map[r - 1:r + 2, c - 1:c + 2][view & mask]
            if destination_location.size > 0:
                return destination_location.item() # Returnerer landskapsobjektet dyret skal migrere til (om dyret skal migrere)
        #else:
            # return False















