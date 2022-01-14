import numpy as np
import random
from dataclasses import dataclass
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.landscape import Landscape
from world import World



@dataclass
class BioSim_param:
    codes_for_landscape_types: str = 'WLHD' #Brukes denne?


class BioSim(BioSim_param):
    """Island hosting landscapes with animals.

        Parameters
        ----------
        island_map:
        ini_pop: `list` of `dict`, optional


        Attributes
        ----------

        """

    def __init__(self, island_map, ini_pop=None, seed=None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        random.seed(seed) # Påvirker potensielt andre script som kjører. Vurder å lage egen Random-instans, slik at BioSIm kan eie sitt eget random seed.

        if all((self._validate_island_map(island_map),
               self._validate_ini_pop(ini_pop))):
            self.island = World(island_map, ini_pop)

        # Disse variablene lages under instansiering. De brukes for å lage data som kan sendes til grafikk-klassen.
        self._num_years = 0  # Duration of sim
        self.cube_population_herbs = np.empty(())
        self.cube_population_carns = np.empty(())
        self.cubelist_properties_herbs = []
        self.cubelist_properties_carns = []

        # self.cube_properties_herbs = np.empty(())
        # self.cube_properties_carns = np.empty(())

    def _validate_island_map(self, island_map:str)->bool:
        #map = textwrap.dedent(island_map)  # Should already be textwrapped
        island_map_list = island_map.split(sep='\n') #Endret til input

        length_check = len(island_map_list[0])
        for element in island_map_list:
            # Control all symbols
            for letter in element:
                if letter not in 'WHLD':
                    raise ValueError(
                        f'{letter} is not a defined landscape.\n'
                        f'Defined landscapes are: ["Lowland", "Highland", "Desert", "Water"]\n'
                        'respectively given by their belonging capital letter.')
            # Control size
            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')
            # Control edges
            if not (element[0] and element[-1]) == 'W':
                raise ValueError('All the islands` outer edges must be of landscape Water.')
        # Control edges
        if not (island_map_list[0] and island_map_list[-1]) == 'W' * length_check:
            raise ValueError('All the islands` outer edges must be of landscape Water.')

        return True
        # Raises value error if rules broken.
        # Returns True if all OK.

    def _validate_ini_pop(self, ini_pop:dict)-> bool:
        # TODO: Lag en valideringsrutine
        """Validates the ini_pop input, and check that it follow the rules"""
        return True

    def get_yearly_herb_count(self)-> object:
        """Dette er en datagenererings-metode for å finne ut hvor mange herbivores som finnes i verden akk nå.
        Returnerer en np array.shape(1,) 1D"""
        kube =  self.cube_population_herbs
        # kube.sum(rad_dimensjonen).sum(kolonne_dimensjonen) = array med en sum (scalar) per år.
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        assert len(serie) == self._num_years
        return serie

    def get_yearly_carn_count(self):
        """Dette er en datagenererings-metode for å finne ut hvor mange carnivores som finnes i verden akk nå."""
        kube =  self.cube_population_carns
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        assert len(serie) == self._num_years
        return serie

    def set_animal_parameters(self, species:str, params:dict): # TODO: må oppdatere for carnivore også
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivore.set_params(params)

    def set_landscape_parameters(self, landscape:str, params:dict):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
         params = {'f_max': {'Highland': 300.0,'Lowland': 800.0}}
        """
        if landscape == 'L':
            Landscape.set_params({'f_max': {'Lowland': params['f_max']}})
        elif landscape == 'H':
            Landscape.set_params({'f_max': {'Highland': params['f_max']}})
        else:
            raise ValueError('Feil input')

        # Oppdaterer alle eksisterende objekter.f_max. Denne settes normalt kun i __init__, og må oppdateres når klassevariabelen endres.
        # TODO: Sjekk om dette har tilbakevirkende kraft på instansene som allerede finnes.
        with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landskapsobjekt = element.item()
                if landskapsobjekt.landscape_type == 'H':
                    landskapsobjekt.f_max = landskapsobjekt.params['f_max']['Highland']
                elif landskapsobjekt.landscape_type == 'L':
                    landskapsobjekt.f_max = landskapsobjekt.params['f_max']['Lowland']
                else:
                    landskapsobjekt.f_max = 0

    def migration_preparation(self):
        with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landscape_obj = element.item()
                landscape_obj.migration_prep()  # Better hierarcy
                # for animal in landscape_obj.herb_pop + landscape_obj.carn_pop:
                #     animal.has_migrated = False

    def migration(self):
        """."""
        with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landscape_obj = element.item()
                #current_row, current_col = it.multi_index
                row, col = it.multi_index

                migrate_herbs, migrate_carns = landscape_obj.migrate() #-> {herb: (r,c)}

                def method_2(landscape_pop, migrate_dict, current_row, current_col, species):
                    moved = []
                    for animal, location in migrate_dict.items():
                        r, c = location
                        new_row = current_row + r
                        new_col = current_col + c

                        if self.island.object_map[new_row, new_col].is_migratable:
                            self.island.object_map[new_row, new_col].population.append(animal)
                            # if species == 'Herbivore':
                            #     self.island.object_map[new_row, new_col].herb_pop.append(animal) #Still not good...
                            # if species == 'Carnivore':
                            #     self.island.object_map[new_row, new_col].carn_pop.append(animal)

                            moved.append(animal)

                    for migrated_animal in moved:
                        landscape_pop.remove(migrated_animal)

                if landscape_obj.is_migratable:
                    method_2(landscape_obj.population, {**migrate_herbs, **migrate_carns}, row, col, 'dummy')
                    # method_2(landscape_obj.herb_pop, migrate_herbs, row, col, 'Herbivore')
                    # method_2(landscape_obj.carn_pop, migrate_carns, row, col, 'Carnivore')



                # # TODO: Look for opportunities to structure this better mtp. hierarcy
                # #Possibilities; Split over several levels;
                # #retur verdi False hvis dyr ikke beveger seg? (Mulig bug å legge til og slette objekt identitet fra samme liste?)
                # def moving(landscape_population, current_row, current_col, species): #species = self.herb_pop or self.carn_pop
                #
                #     #
                #     if landscape_population:
                #         moved = []
                #         for animal in landscape_population:
                #             if not animal.has_migrated:
                #                 row_direction, col_direction = animal.migration_direction() #Returnerer tuple av hvor dyr vil flytte seg, evt.(0,0)
                #                 new_row = current_row + row_direction
                #                 new_col = current_col + col_direction
                #
                #                 if self.island_map_objects[new_row, new_col].is_migratable:
                #
                #                     if species == 'Herbivore':
                #                         self.island_map_objects[new_row, new_col].herb_pop.append(animal)
                #                     if species == 'Carnivore':
                #                         self.island_map_objects[new_row, new_col].carn_pop.append(animal)
                #
                #                     moved.append(animal)
                #                     animal.has_migrated = True
                #
                #         for migrated_animal in moved:
                #             landscape_population.remove(migrated_animal)
                #
                #
                # if landscape_obj.is_migratable:
                #     moving(landscape_obj.herb_pop, row, col, 'Herbivore')
                #     moving(landscape_obj.carn_pop, row, col, 'Carnivore')
                    ###################
                # if landscape_obj.herb_pop:
                #     lovlige_retninger = []  # Lovlige retninger å bevege seg i for dyrene på denne lokasjoner
                #     if landscape_obj.is_migratable: # Sjekker at vi står på noe annet enn vann #TODO: Remove when assured we cannot add population to water
                #         row, col = it.multi_index # Blir en tuple, med lokasjon på hvor vi er #TODO: Handled above
                #         if self.island_map_objects[row-1, col].is_migratable:
                #             lovlige_retninger.append((-1, 0))
                #         if self.island_map_objects[row+1, col].is_migratable:
                #             lovlige_retninger.append((1,0))
                #         if self.island_map_objects[row, col-1].is_migratable:
                #             lovlige_retninger.append((0, -1))
                #         if self.island_map_objects[row, col+1].is_migratable:
                #             lovlige_retninger.append((0, 1))
                #
                #     moved = []
                #     for herbivore in landscape_obj.herb_pop: #
                #         if not herbivore.has_migrated: #
                #             row_direction, col_direction = herbivore.migration_direction() #
                #             if (row_direction, col_direction) in lovlige_retninger: #
                #                 new_row = current_row+row_direction #
                #                 new_col = current_col+col_direction #
                #
                #                 self.island_map_objects[new_row, new_col].herb_pop.append(herbivore) #
                #
                #                 moved.append(herbivore)#
                #                 herbivore.has_migrated = True #
                #
                #     for herbivore in moved:
                #         landscape_obj.herb_pop.remove(herbivore)
                #
                # if landscape_obj.carn_pop:
                #     lovlige_retninger = []  # Lovlige retninger å bevege seg i for dyrene på denne lokasjoner
                #     if landscape_obj.is_migratable:  # Sjekker at vi står på noe annet enn vann
                #         row, col = it.multi_index  # Blir en tuple, med lokasjon på hvor vi er
                #         if self.island_map_objects[row - 1, col].is_migratable:
                #             lovlige_retninger.append((-1, 0))
                #         if self.island_map_objects[row + 1, col].is_migratable:
                #             lovlige_retninger.append((1, 0))
                #         if self.island_map_objects[row, col - 1].is_migratable:
                #             lovlige_retninger.append((0, -1))
                #         if self.island_map_objects[row, col + 1].is_migratable:
                #             lovlige_retninger.append((0, 1))
                #
                #     moved = []
                #     for carnivore in landscape_obj.carn_pop:
                #         if not carnivore.has_migrated:
                #             row_direction, col_direction = carnivore.migration_direction()
                #
                #             if (row_direction, col_direction) in lovlige_retninger:
                #                 new_row = current_row + row_direction
                #                 new_col = current_col + col_direction
                #
                #                 self.island_map_objects[new_row, new_col].carn_pop.append(carnivore)
                #
                #                 moved.append(carnivore)
                #                 carnivore.has_migrated = True
                #
                #     for carnivore in moved:
                #         landscape_obj.carn_pop.remove(carnivore)


    def simulate(self, num_years:int = 10):
        self._num_years = num_years # Trenger num_years utenfor simulate metoden. Brukes i get_yearly_carn_count og get_yearly_herb_count
        yearly_pop_map_herbs = []
        yearly_pop_map_carns = []
        #yearly_property_map_herbs = []
        #yearly_property_map_carns = []

        current_year = 0
        for year in range(self._num_years):
            current_year += 1
            with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    landscape = element.item()
                    if landscape.landscape_type in 'LH':
                        landscape.regrowth()
                        landscape.grassing()
                    if landscape.landscape_type in 'LHD':
                        landscape.hunting()
            self.island.do_migration()
            #self.migration_preparation()
            #self.migration()
            with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    landscape = element.item()
                    if landscape.landscape_type in 'LHD':
                        landscape.give_birth()
                        landscape.aging()
                        landscape.do_death()

            #-------------------------------------------------------------------------------------
            # Data for every year. Her genereres data for hvert år. Dataene pakkes på slutten av simuleringen til kuber eller lister av tabeller.

            # Herbivore populasjonsstørrelse for alle lokasjoner per år
            yearly_pop_map_herbs.append(self.island.get_property_map('v_size_herb_pop'))
            # Carnivore populasjonsstørrelse for alle lokasjoner per år
            yearly_pop_map_carns.append(self.island.get_property_map('v_size_carn_pop'))

            #---------------------------------------------------------------------

            yearly_herb_objects_map = self.island.get_property_map_objects('v_herb_properties_objects')
            # Standard akkumulering i numpy fungerte ikke fordi vi hadde en array full av None verdier, der det ikke var noen dyr.
            # Måtte derfor skrive egen akkumulerings funksjon som legger sammen alle populasjonslistene på landskapene på øya, til en liste med alle dyr på øya.
            acc_list_herb = []
            with np.nditer(yearly_herb_objects_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list_herb += list_on_location
            yearly_herbivore_property_array = np.asarray(acc_list_herb)
            self.cubelist_properties_herbs.append(yearly_herbivore_property_array)
            # Brukes ikke nå, men ikke slett!
            #yearly_property_map_herbs.append(yearly_herb_objects_map)

            yearly_carn_objects_map = self.island.get_property_map_objects('v_carn_properties_objects')
            acc_list_carn = []
            with np.nditer(yearly_carn_objects_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list_carn += list_on_location
            yearly_carnivore_property_array = np.asarray(acc_list_carn)
            self.cubelist_properties_carns.append(yearly_carnivore_property_array)
            # Brukes ikke nå, men ikke slett!
            #yearly_property_map_carns.append(yearly_carn_objects_map)

            print('\r',f'Year:{current_year}  Herbivores:{yearly_pop_map_herbs[-1].sum()}   Carnivores:{yearly_pop_map_carns[-1].sum()}', end = '')


        # Data at end of simulation
        # TODO: Add evaluation. Check shape and size. Raises valueerror
        self.cube_population_herbs = np.stack(yearly_pop_map_herbs)
        self.cube_population_carns = np.stack(yearly_pop_map_carns)

        # Disse brukes ikke akkurat nå, men ikke slett!
        #self.cube_properties_herbs = np.stack(yearly_property_map_herbs)
        #self.cube_properties_carns = np.stack(yearly_property_map_carns)

    def add_population(self, population:dict):
        """Validates input dict befor sending calling add_population method in
        the world class
        Initial_population looks like:

        ini_pop = [{'loc': (3,4),
        'pop': [{'species': 'Herbivore',
                'age': 10, 'weight': 12.5},
            {'species': 'Herbivore',
                'age': 9, 'weight': 10.3}]}]
        """
        pass