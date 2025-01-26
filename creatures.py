"""
creatures.py - class definitions for the creatures in FOP Assignment, Sem 1 2024

Written by : Chanuka Dilusha Athalage
Student ID : 21953004

Includes:
    Puppy, Squirrel, Human and Ball classes

Versions:
    - V1.0
"""

#importing libraries
import random
import matplotlib.pyplot as plt
import matplotlib.patches as pat

#fliping coordinates
def flip_coords(pos, LIMITS):
    return((pos[1],pos[0]))


class Puppy():
    """
    Holds information and behaviour of puppy creature
    """
    def __init__(self, name, colour, pos, age):
        self.name = name
        csplit = colour.split("/")
        self.colour1 = csplit[0]
        if len(csplit) == 2:
            self.colour2 = csplit[1]
        else:
            self.colour2 = csplit[0]
        self.pos = pos
        self.age = age
        self.energy = 100

    #getting the position
    def get_pos(self):
        return self.pos

    #checking borders
    def check_borders(self, move):
        if self.pos[0] + move[0] <= 3 or self.pos[0] + move[0] >= 71:
            move = (-move[0],move[1])
        if self.pos[1] + move[1] <= 3 or self.pos[1] + move[1] >= 71:
            move = (move[0], -move[1])
        return move

    #fading energy
    def energy_fading(self):
        self.energy -= 2 

    #checking human type and reacting
    def near_human(self, humans, ax, LIMITS):
        for human in humans:
            if self.distance_to_objects(human) <= 10:
                if human.human_type == "owner":
                    self.energy = 100
                elif human.human_type == "stranger":
                    self.bark(ax, LIMITS)

    #Euclidean calculation to calculate distance between objects
    def distance_to_objects(self,obj):
        r1,c1 = self.pos
        r2,c2 = obj.pos
        return ((r2 - r1) ** 2 + (c2 - c1) ** 2) ** 0.5

    #reproducing method
    def reproduce_when_near_puppy(self, puppies):
        for puppy in puppies:
            if self.distance_to_objects(puppy) <= 5 and self.distance_to_objects(puppy) != 0 and self.age > 10:
                    return True
            else:
                    return False 

    #step change method
    def step_change(self, objs):
        validmoves = [(-3, 0), (3, 0), (0, -3), (0, 3), (3, 3), (3, -3), (-3, 3), (-3, -3)]
        print(validmoves)
    
        move_towards_object = (0, 0)  
        object_found = False  
    
    # Checking if the puppy is near an object (ball/squirrel)
        for obj in objs:
            if self.distance_to_objects(obj) <= 10:
            # If near an object, calculate a move towards it
                move_towards_object = (obj.pos[0] - self.pos[0], obj.pos[1] - self.pos[1])
                object_found = True
    
        # If near an object, move towards it
        if object_found:
            move = move_towards_object
        # Else, choose a random move from the valid moves
        else:
            move = random.choice(validmoves)
    
    # checking borders before moving
        move = self.stop_tree_collision(move)
        move = self.check_borders(move)
    
    # new position of the puppy
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])
        
        
    #plotting puppy
    def plot_me(self ,ax, LIMITS):
        fpos = flip_coords(self.pos, LIMITS)
        patch = pat.Circle(fpos, radius=1, color=self.colour1)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]-0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour2)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]+0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour2)
        ax.add_patch(patch)
        ax.annotate(self.name, (fpos[0], fpos[1]-2), color = 'white')
        ax.annotate(self.energy, (fpos[0], fpos[1]+2), color = 'red')

    #barking 
    def bark(self, ax, LIMITS):
        fpos = flip_coords(self.pos, LIMITS)
        ax.annotate("Woof, Woof, Woof", (fpos[0]+1, fpos[1]+3), color = 'black')

    #avoiding collision with trees
    def stop_tree_collision(self, move):
        if 55 < self.pos[0] + move[0] <= 70:
            move = (-move[0],move[1])
        if 5 < self.pos[1] + move[1] <= 15 or 65 < self.pos[1] + move[1] <= 75:
            move = (move[0], -move[1])
        return move

    #aging 
    def is_old(self):
        if self.age < 30:
            self.age += 1
            return False
        else:
            return True
                
    

class Squirrel():
    """
    Holds information and behaviour of squirrel creature
    """
    def __init__(self, name, colour, pos,age):
        self.name = name
        self.colour = colour
        self.pos = pos
        self.age = age

    #getting the position
    def get_pos(self):
        return self.pos

    #checking borders
    def check_borders(self, move):
        if self.pos[0] + move[0] <= 3 or self.pos[0] + move[0] >= 76 or 20 < self.pos[0] + move[0] <= 60:
            move = (-move[0],move[1])
        if self.pos[1] + move[1] <= 3 or self.pos[1] + move[1] >= 78 or 20 < self.pos[1] + move[1] <= 60:
            move = (move[0], -move[1])
        return move

    #step change method
    def step_change(self, humans, puppies):
        move_away_from_humans = (0, 0)
        move_away_from_puppies = (0, 0)
    
        # Check if the squirrel is near a human
        for human in humans:
            if self.distance_to_objects(human) <= 10:
            # If near a human, calculate a move away from it
                move_away_from_humans = (self.pos[0] - human.pos[0], self.pos[1] - human.pos[1])
    
        # Check if the squirrel is near a puppy
        for puppy in puppies:
            if self.distance_to_objects(puppy) <= 10:
            # If near a puppy, calculate a move away from it
                move_away_from_puppies = (self.pos[0] - puppy.pos[0], self.pos[1] - puppy.pos[1])
    
        #moving away from both puppies and humans
        move_away = (move_away_from_humans[0] + move_away_from_puppies[0], move_away_from_humans[1] + move_away_from_puppies[1])
    
        #using below valid moves to run away from humans and puppies
        if move_away != (0, 0):
            validmoves = [(-3, 0), (3, 0), (0, -3), (0, 3), (3, 3), (3, -3), (-3, 3), (-3, -3)]
            move = random.choice(validmoves)

        # else, use the normal set of moves
        else:
            validmoves = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            move = random.choice(validmoves)
    
    # Adjust the move based on borders
        move = self.check_borders(move)
    
    # Update the position of the squirrel
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1]) 

    #plotting squirrel
    def plot_me(self ,ax, LIMITS):
        fpos = flip_coords(self.pos, LIMITS)
        patch = pat.Circle(fpos, radius=1, color=self.colour)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]-0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]+0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour)
        ax.add_patch(patch)
        ax.annotate(self.name, (fpos[0], fpos[1]-2), color = 'white')

    #Euclidean calculation to calculate distance between objects
    def distance_to_objects(self,obj):
        r1,c1 = self.pos
        r2,c2 = obj.pos
        return ((r2 - r1) ** 2 + (c2 - c1) ** 2) ** 0.5

   

class Human():
    """
    Holds information and behaviour of cat creature
    """
    def __init__(self, name, colour, pos, human_type, age):
        self.name = name
        self.colour = colour
        self.pos = pos
        self.human_type = human_type
        self.age = age

    #getting the position
    def get_pos(self):
        return self.pos

    #checking borders
    def check_borders(self, move):
        if self.pos[0] + move[0] <= 3 or self.pos[0] + move[0] >= 74:
            move = (-move[0],move[1])
        if self.pos[1] + move[1] <= 3 or self.pos[1] + move[1] >= 76:
            move = (move[0], -move[1])
        return move

    #step change method
    def step_change(self):
        validmoves = [(-1,0),(1,0),(0,-1),(0,1), (1,1), (1,-1), (-1,1), (-1,-1)]
        print(validmoves)
        move = random.choice(validmoves)
        move = self.check_borders(move)
        move = self.stop_tree_collision(move)
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])

    #plotting human
    def plot_me(self ,ax, LIMITS):
        fpos = flip_coords(self.pos, LIMITS)
        patch = pat.Circle(fpos, radius = 1.5, color=self.colour)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]-0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]+0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour)
        ax.add_patch(patch)
        ax.annotate(self.name, (fpos[0], fpos[1]-2), color = 'white')

    #avoiding collision with trees
    def stop_tree_collision(self, move):
        if 55 < self.pos[0] + move[0] <= 70:
            move = (-move[0],move[1])
        if 5 < self.pos[1] + move[1] <= 15 or 65 < self.pos[1] + move[1] <= 75:
            move = (move[0], -move[1])
        return move



class Ball():
    """
    Holds information and behaviour of ball
    """
    def __init__(self, name, colour, pos):
        self.name = name
        self.colour = colour
        self.pos = pos

    #getting the position
    def get_pos(self):
        return self.pos

    #plotting ball
    def plot_me(self ,ax, LIMITS):
        fpos = flip_coords(self.pos, LIMITS)
        patch = pat.Circle(fpos, radius = 1.5, color=self.colour)
        ax.add_patch(patch)


