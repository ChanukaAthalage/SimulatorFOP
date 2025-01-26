"""
assessment.py - FOP Assignment, Sem 1 2024

Written by : Chanuka Dilusha Athalage
Student ID : 21953004

Usage: contains the main class, yard building, making rain

Versions:
    - V1.0
"""
#importing libraries and creature classes
import numpy as np
import matplotlib.pyplot as plt
import random
import time

from creatures import Puppy, Squirrel, Human, Ball

#building the yard and raindrops
def build_yard(dims):

    #building rain
    raindrop_area = np.zeros(dims)
    raindrop_area[90:100, :] = 1

    #building yard and sky
    plan = np.zeros(dims) 
    plan[20:60,20:60] = 10
    plan[75:78,1:79] = 7
    plan[1:20,1:79] = 5
    plan[20:60,1:20] = 5
    plan[20:60,60:79] = 5
    plan[60:75,1:79] = 5
    plan[90:,:] = 3
    plan[95:99,5:9] = 9

    #building trees
    tree_size = 5
    trunk_size = 4

    plan[60-tree_size:60+tree_size+1, 70-tree_size:70+tree_size+1] = 6
    plan[60+tree_size:60+tree_size+trunk_size+1, 70-trunk_size//2:70+trunk_size//2+1] = 8

    plan[60-tree_size:60+tree_size+1, 10-tree_size:10+tree_size+1] = 6
    plan[60+tree_size:60+tree_size+trunk_size+1, 10-trunk_size//2:10+trunk_size//2+1] = 8

    return plan, raindrop_area
   
#method for simulating rain
def make_rain(yard, raindrop_area, num_drops):
    for i in range(num_drops):
        row = random.randint(90, 99)
        col = random.randint(0, 79)
        if raindrop_area[row, col] == 1:
            yard[row, col] = 2  

    return yard

#method to plot the yard
def plot_yard(ax, p):
    ax.imshow(p, cmap=plt.cm.nipy_spectral)

#main method
def main():

    #error handling
    valid_input = False
    while not valid_input:
    
        try:
            #taking inputs from cli
            time_steps  = int(input("How many times do you want to run the life cycle: "))
            no_puppies = int(input("Enter number of puppies: "))
            no_squirrels = int(input("Enter number of squirrels: "))
            no_humans = int(input("Enter number of humans: "))
            no_balls = int(input("Enter number of balls: "))
            valid_input = True
    
        except ValueError:
            print("Please enter integer inputs...")
        

    #defining yard and raindrop area size
    size = (100,80)
    yard, raindrop_area = build_yard(size)
    
    #creating empty lists to add creatures
    creatures = []
    humans = []
    puppies = []
    squirrels = []
    balls = []

    #defining human types in a list
    human_types = ["owner", "stranger"]

    #generating balls in the yard randomly and adding them to lists
    for i in range(no_balls):
        row = random.randrange(3,79)
        col = random.randrange(3,79)
        ball = Ball("ball", "Green", (row,col))
        balls.append(ball)
        creatures.append(ball)
    
    #generating puppies in the yard randomly and adding them to lists
    for i in range(no_puppies):
        row = random.randrange(3,74)
        col = random.randrange(3,79)

        #generating random numbers for rows and columns till puppies avoid generating on the trees (since puppies can't be on trees)
        while (54 <= row < 71) and ((5 <= col < 16) or (65 <= col < 76)):
            row = random.randrange(3,74)
            column = random.randrange(3,79)

        puppy = Puppy(f"Dog {i+1}", "white/brown", (row,col), 10)
        puppies.append(puppy)
        creatures.append(puppy)


    #generating squirrels in the yard randomly and adding them to lists
    for i in range(no_squirrels):
        row = random.randrange(3,79)
        col = random.randrange(3,79)

        #generating random numbers for rows and columns till squirrels avoid generating in the house
        while 20 <= row < 60 and 20 <= col < 60 and row <= 78:
            row = random.randrange(3,74)
            column = random.randrange(3,79)
        squirrel = Squirrel(f"Squirrel {i+1}", "brown", (row,col),2)
        creatures.append(squirrel)
        squirrels.append(squirrel)

    #generating humanss in the yard randomly and adding them to lists
    for i in range(no_humans):
        row = random.randrange(3,74)
        col = random.randrange(3,79)

        #generating random numbers for rows and columns till humans avoid generating on the trees (since humans can't be generated on trees)
        while (54 <= row < 71) and ((5 <= col < 16) or (65 <= col < 76)):
            row = random.randrange(3,74)
            column = random.randrange(3,79)
        human_type = random.choice(human_types)
        human = Human(f"Human({human_type})", "pink", (row, col), human_type,25)
        creatures.append(human)
        humans.append(human)

    #plotting yard
    plt.ion()
    fig, axs = plt.subplots(figsize=(15,10))
    plot_yard(axs, yard)

    #plotting creatures
    for c in creatures:
        c.plot_me(axs, size)

    #timestep
    for i in range(0,time_steps ):
        
        #taking objects out from creatures list
        for c in creatures:   
            
            #checking if the object is a puppy
            if isinstance(c, Puppy):
                #this if statement is used to decide the night time. when 3/4 of life cycle is done, puppies go in the house
                if i >= (3/4) * time_steps :
                    c.pos = (random.randint(20, 60), random.randint(20, 60))
                #calling puppie's functions
                else:
                    #checking if the puppie's age is valid to reproduce    
                    can_reproduce = c.reproduce_when_near_puppy(puppies)
                    #if the two puppies are of valid age to reproduce, make a new puppy and adding it to creatures and puppies lists
                    if can_reproduce == True:
                        creatures.append(Puppy(f"Dog {len(puppies)+1}", "brown/white", (c.pos), 1))
                        puppies.append(Puppy(f"Dog {len(puppies)+1}", "brown/white", (c.pos), 1))
                    #calling step change function when a squirrel nearby
                    c.step_change(squirrels)
                    #calling step change function when a ball nearby
                    c.step_change(balls)
                    #fading puppie's energy everytime it moves
                    c.energy_fading()
                    #increasing energy when near human
                    c.near_human(humans, axs, size) 
                    #if the puppy is old, remove it from the lists (shows the death of puppy)   
                    if c.is_old() == True:
                        puppies.remove(c)
                        creatures.remove(c)
  
            #checking if the object is a squirrel
            elif isinstance(c, Squirrel):
                #this if statement is used to decide the night time. when 3/4 of life cycle is done, squirrels go to the trees
                if i >= (3/4) * time_steps :
                    c.pos = (random.randint(55, 65), random.randint(65, 75))
                #calling step change function of squirrel
                else:
                    c.step_change(humans, puppies)

            #checking if the object is a human
            elif isinstance(c, Human):
                #this if statement is used to decide the night time. when 3/4 of life cycle is done, humans go in the house
                if i >= (3/4) * time_steps :
                    c.pos = (random.randint(20, 60), random.randint(20, 60))
                #calling step change function of human
                else:
                    c.step_change()

        # pasing values to make_rain method and geting the yard and plotting
        yard = make_rain(yard, raindrop_area, 10)
        axs.clear()
        plot_yard(axs, yard)

        #plotting all the creatures, setting title and saving image
        for c in creatures:
            c.plot_me(axs, size)

        axs.set_title(f"Time step count - {i+1}")
        fig.savefig("assessment.png")
        fig.canvas.draw()                                   
        fig.canvas.flush_events()
        axs.clear()
        time.sleep(2)

#running main method
if __name__ == "__main__":
    main()  
