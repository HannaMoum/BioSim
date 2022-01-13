import numpy as np
from landscape import Landscape
from animals import Herbivore, Carnivore

class World:

    def __init__(self, island_map, ini_pop):
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
        self._ini_pop = self.add_population(ini_pop)
        # TODO: Save ini_pop directly from input
        # Add_population returns nothing, it is an action of its' own


    def _make_base_map(self, input_map: str)-> object:
        """
        Mapping island with respect to each landscape letter.

        Parameters
        ----------
        island_map: `str`
            Geography of island.

            Made up by the letters 'W', 'D', 'L' and 'H' each representing a landscape.
            Forutsetter at den er ferdig validert.

        Returns
        -------
        _build_map: `ndarray` of `str`
            Array containing landscape letters in their respective positions.
        """

        map_list = input_map.split(sep='\n')
        row, col = len(map_list), len(map_list[0])

        build_map = np.empty(shape=(row, col), dtype='str')
        for row_index, row_string in enumerate(map_list):
            for col_index, landscape_letter in enumerate(row_string):
                build_map[row_index, col_index] = landscape_letter
        return build_map

    def _make_migrate_map(self)-> object:
        """Make migration map (np bool)."""
        self._migrate_map = self._base_map != 'W'

    def _make_object_map(self)->object:
        """
        Mapping island with landscape objects.

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

            r, c = dictionary['loc'] #Tuple
            r -= 1  # Adjustments
            c -= 1  # Adjustments. Checked.

            landscape_object = self.object_map[r, c]

            population = dictionary['pop']  # [{},{}]
            landscape_object.add_animals(population)

    @property
    def base_map(self):
        """Base map. Det initsielle verdenskartet."""
        return self._base_map

    @property
    def migrate_map(self):
        """Migration map. Gives True/False if movement on to location is allowed"""
        return self._migrate_map

    @property
    def object_map(self):
        """Dette kartet inneholder referanser til landskapsobjekter.
        Det er en transformering av island_map. Kart med landskapsobjekter."""
        return self._object_map
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
        return len(location.herb_pop)

    def v_size_carn_pop(self, location: object)->int:
        """Population sizer for carnivores at given location."""
        return len(location.carn_pop)

    # ----------------------------------------------------------------------------------------------------------------
    # Her kommer det ut en np.array med objekter, som f.eks. inneholder hele landskapsobjektet

    def get_property_map_objects(self, fx_map_type:str)->object:
        return self._make_property_map_objects(getattr(self, fx_map_type), self.base_map, self.object_map)

    def _make_property_map_objects(self, fx: callable(object), base_map: object, object_map: object):
        property_map = np.empty(base_map.shape, dtype=object)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(object_map)
        return property_map

    # TODO: Om vi får en populasjon per landskap kan disse bli til 1 funksjon
    def v_herb_properties_objects(self, location: object)->list:
        population_list = location.herb_pop
        if len(population_list) > 0:
            liste = []
            for animal in population_list:
                liste.append((animal.age, animal.weight, animal.fitness))
            return liste

    def v_carn_properties_objects(self, location: object)->list:
        population_list = location.carn_pop
        if len(population_list) > 0:
            liste = []
            for animal in population_list:
                liste.append((animal.age, animal.weight, animal.fitness))
            return liste
    ###################################################################################################################

















