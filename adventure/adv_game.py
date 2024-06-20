clues = [
    "There is a faint scent of gunpowder in the air, as if a conflict recently took place.",
    "There is a subtle draft coming from a direction where no visible openings exist.",
    "There is a single, worn-out shoe lying in the corner, its pair nowhere to be seen.",
    "There is a series of hurried footprints leading to a hastily closed door.",
    "There is an unusual pattern of scorch marks along the walls, suggesting a sudden blaze.",
    "There is a cryptic message hastily scribbled on a piece of paper, partially torn.",
    "There is a noticeable silence, broken only by the distant sound of dripping water.",
    "There is a heavy book left open, its pages fluttering in the breeze from an unseen window.",
    "There is a collection of ancient artifacts, each casting an eerie shadow under the dim light.",
    "There is a lingering smell of herbs and flowers, oddly out of place in this setting."
]

sense_exp = [
    "You see a flickering light casting long shadows on the stone walls.",
    "You hear the distant clanking of chains echoing through the empty halls.",
    "You smell the musty air, mixed with the faint scent of old books and parchment.",
    "You feel a cold draft brushing against your skin, sending shivers down your spine.",
    "You sense an unexplained presence, as if someone or something is watching you.",
    "You see intricate tapestries that seem to whisper ancient secrets in the dim light.",
    "You hear a soft murmur, like voices from the past trapped within these walls.",
    "You smell a sudden aroma of lit candles and incense, though no flame is in sight.",
    "You feel the rough texture of the stone beneath your fingertips, worn by time.",
    "You sense a sudden shift in the air, as if the castle itself is breathing.",
    "You see shadows moving in the corner of your eye, but when you look, nothing is there.",
    "You hear the soft patter of rain against the windows, a melancholy rhythm in the silence."
]

import random

class RandomItemSelector:
    def __init__(self, items):
        self.items = items  # Store the original list of items
        self.used_items = []  # Keep track of items that have been selected

    def add_item(self, item):
        self.items.append(item)  # Add a new item to the items list

    def pull_random_item(self):
        if not self.items:  # If the items list is empty, return None
            return None
        if len(self.used_items) == len(self.items):  # If all items have been used, reset the used_items list
            self.used_items = []
        available_items = [item for item in self.items if item not in self.used_items]  # List of items not yet selected
        selected_item = random.choice(available_items)  # Select a random item from the available items
        self.used_items.append(selected_item)  # Add the selected item to the used_items list
        return selected_item

    def reset(self):
        self.used_items = []  # Clear the used_items list


from random import choice

class RandomItemSelector:
    def __init__(self, items):
        self.items = items
        self.used_items = []

    def add_item(self, item):
        self.items.append(item)

    def pull_random_item(self):
        if not self.items:
            return None
        if len(self.used_items) == len(self.items):
            self.used_items = []
        available_items = [item for item in self.items if item not in self.used_items]
        selected_item = choice(available_items)
        self.used_items.append(selected_item)
        return selected_item

    def reset(self):
        self.used_items = []

class SenseClueGenerator:
    _instance = None

    def __new__(cls, clues, sense_exp):
        if cls._instance is None:
            cls._instance = super(SenseClueGenerator, cls).__new__(cls)
            cls.clue_selector = RandomItemSelector(clues)
            cls.sense_selector = RandomItemSelector(sense_exp)
        return cls._instance

    def get_senseclue(self):
        clue = self.clue_selector.pull_random_item()
        sense = self.sense_selector.pull_random_item()
        return f"{sense} {clue}"

from enum import Enum

class EncounterOutcome(Enum):
    CONTINUE = 1
    END = 2

from abc import ABC, abstractmethod
from enum import Enum

class EncounterOutcome(Enum):
    CONTINUE = 1
    END = 2

class Encounter(ABC):
    @abstractmethod
    def run_encounter(self) -> EncounterOutcome:
        pass

class DefaultEncounter(Encounter):
    def __init__(self, clues, sense_exp):
        self.sense_clue_generator = SenseClueGenerator(clues, sense_exp)

    def run_encounter(self) -> EncounterOutcome:
        sense_clue = self.sense_clue_generator.get_senseclue()
        print(sense_clue)
        return EncounterOutcome.CONTINUE
    
class Room:
    def __init__(self, name, encounter):
        self.name = name
        self.encounter = encounter

    def visit_room(self):
        print(f"Entering {self.name}...")
        return self.encounter.run_encounter()
    
    
# Assuming DefaultEncounter is defined elsewhere and properly imports EncounterOutcome
# Assuming clues and sense_exp lists are defined elsewhere

# Placeholder lists for demonstration
clues = ["A mysterious shadow lurks in the corner.", "An ancient book lies open, its pages fluttering."]
sense_exp = ["You hear a distant echo.", "The scent of old parchment fills the air."]

# Initialize a single DefaultEncounter instance for simplicity
default_encounter = DefaultEncounter(clues, sense_exp)

# List of room names
room_names = [
    "The Grand Hall",
    "The Forgotten Library",
    "The Royal Chambers",
    "The Secret Garden",
    "The Dungeon Depths",
    "The Tower Lookout"
]

# Create room objects
rooms = [Room(name, default_encounter) for name in room_names]

# This assumes that each room can use the same encounter instance.
# If each room needs a unique encounter, you would create separate instances for each.

import random

class Castle:
    def __init__(self, rooms):
        self.room_selector = RandomItemSelector(rooms)

    def select_door(self):
        door_count = random.randint(2, 4)  # Randomly choose between 2 and 4 doors
        print(f"There are {door_count} doors in front of you. Choose one (1-{door_count}):")
        while True:
            try:
                selected_door = int(input("Your choice: "))
                if 1 <= selected_door <= door_count:
                    return selected_door
                else:
                    print(f"Please select a valid door number between 1 and {door_count}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def next_room(self):
        self.select_door()  # Let the user select a door
        chosen_room = self.room_selector.pull_random_item()  # Get a random room
        print(f"You enter {chosen_room.name}.")
        return chosen_room.visit_room()

    def reset(self):
        self.room_selector.reset()  # Reset the room selector for a new game or round

class Game:
    def __init__(self, rooms):
        self.castle = Castle(rooms)

    def play_game(self):
        print("Welcome to the Castle Adventure!")
        print("Objective: Navigate through the castle and find the treasure.")
        
        while True:
            outcome = self.castle.next_room()
            if outcome == EncounterOutcome.END:
                print("Game Over. You've met an unfortunate end.")
                self.castle.reset()
                if input("Would you like to explore a different castle? (yes/no): ").lower() != 'yes':
                    print("Thank you for playing. Goodbye!")
                    break
            # If EncounterOutcome.CONTINUE, the loop will automatically continue

# run the game

game = Game(rooms)
game.play_game()

