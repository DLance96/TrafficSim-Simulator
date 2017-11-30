from itertools import cycle

class TrafficCycle:
    def __init__(self, green_lights, timings, yellow_light_length):

        if not len(green_lights) == len(timings):
            raise ValueError("The list of green light combinations and associated timings must be the same length.")

        # A list of tuples of lists of roads which have green lights at the same time and their durations.
        # Format, [ ([1, 2, 3], 50), ([0, 4], 20), etc]
        self.greens = cycle(list(zip(green_lights, timings)))

        self.yellow_length = yellow_light_length

    def get_next(self):
        return self.greens.__next__()

    def get_yellow_duration(self):
        return self.yellow_length


