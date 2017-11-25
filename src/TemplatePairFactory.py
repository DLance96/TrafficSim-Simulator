import random

class TemplatePairFactory:
    def __init__(self, spawning_frequency,
                 prebuilt_vehicle_probs,
                 mix_and_match = False,
                 driver_template_probs = None,
                 vehicle_template_probs = None):
        """
        A TemplatePairFactory behaves in one of two ways.
        If the parameter mix_and_match is False, a VehicleTemplate-DriverTemplate pair are returned according to
        the prebuilt probabilities. If mix_and_match is true, the VehicleTemplate-DriverTemplate pair are selected
        independantly from the driver_template and vehicle_template probability lists.

        :param spawning_frequency: An integer representing the number of milliseconds to wait between spawning vehicles
        :param prebuilt_vehicle_probs: Format - [((a, b), DriverTemplate, VehicleTemplate),...]
            (a, b) represents a probability range open on the left and closed on the right.
        :param mix_and_match: Boolean to choose if the factory spawns from the prebuilt template, or by
            randomly combining vehicles and drivers from the probability lists.
        :param driver_template_probs: Format - [((a, b), DriverTemplate),...]
        :param vehicle_template_probs: Format - [((a, b), VehicleTemplate),...]
        """

        # time since the last template pair was created in milliseconds
        self.counter = 0

        # a template pair is spawned when the counter exceeds this value
        self.frequency = spawning_frequency

        # determines the spawning mode, either fixed or mix and match
        self.mix_and_match = mix_and_match

        # list of prebuilt template pair configurations and their probabilities
        self.prebuilts = prebuilt_vehicle_probs

        # list of driver templates and their probabilities
        self.drivers = driver_template_probs

        # list of vehicle templates and their probabilities
        self.vehicles = vehicle_template_probs

    def prompt_spawn(self, time_since_last_prompt):
        """
        Prompt the factory to possibly produce a template pair by providing the amount of (simulation) time since
        the last prompt. If the factory has not served up a template pair for more than frequency ms, it will
        generate a template pair and return it. Otherwise it returns none.
        It is up to the controlling intersection how frequently it wishes to call this function, but it should probably
        be as frequently as possible.
        :param time_since_last_prompt: The time since the last time this factory was prompted for a template pair
        :return:
        """
        self.counter += time_since_last_prompt
        if self.counter >= self.frequency:
            self.counter = 0
            rand = random.random() # float in the range [0, 1)
            if self.mix_and_match:
                for range, template in self.drivers:
                    if rand >= range[0] and rand < range[1]:
                        driver = template
                        break
                for range, template in self.vehicles:
                    if rand >= range[0] and rand < range[1]:
                        vehicle = template
                        break
                return vehicle, driver
            else:
                for range, driver, vehicle in self.prebuilts:
                    if rand >= range[0] and rand < range[1]:
                        return vehicle, driver
        else:
            return None
