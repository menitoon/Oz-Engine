

===========================================================================
                               
![](logo.png)

===========================================================================

![PyPI](https://img.shields.io/pypi/v/Oz-Engine?label=Oz-Engine%20pypi)

# Oz-Engine, a **Text-Based Engine** made using **Python**.
It can be used to make games in:
* **Terminal**  
* **Discord** 
* [**microbit**](https://github.com/menitoon/Oz-Engine-Microbit-version)
* any matrix-led screen


![](https://thumbs.gfycat.com/AcclaimedAlienatedGiraffe-size_restricted.gif)  ![](https://thumbs.gfycat.com/ScientificTatteredCardinal-size_restricted.gif)


## Text

Play in the **console**

| 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 5 | 0 |   
| 0 | 1 | 2 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 |

```
00000
00000
00050
01200
00000
```

## Screen
Or on a **matrix led screen**

![](https://cdn.discordapp.com/attachments/958679110316617748/1075077189969645578/Microbit.png)

### STARTUP 👟

In **CommandLine** type this:

 ``` pip install Oz-Engine ```
 
 Then **import** it at the top of your project like so:
 ```python 
 import OzEngine as oz 
 ```


## How to use it 🤔

```diff 
- ⚠️ NOTE :  before reading this remind yourself that: 
- Some explanations might be unclear or wrong if so then please report them so it can changed.
- Also The pip package might not be updated yet since it's managed by @Splatcraft2404.
```

### Creating the canvas ⬜

Start by instancing a canvas like so: 
```python 
canvas = oz.Canvas("#") 
# The  argument is given what the canvas will be filled with.
```
and then instancing a camera so that we can render the scene.
```python
camera = oz.Camera(canvas , [10 , 10] , [0 , 0] , "camera")
#First argument is the canvas that it belongs to.
#Second argument is the size of the camera.
#Thid argument is the position of the camera.
#And the last one is the name.
```


Now try rendering it:
```python
print(camera.render())
```
You should see a square filled with "#"

## Adding Sprites 🍄

It's cool and all but a little boring to have just an empty canvas.
Let's add a sprite:
```python
sprite = oz.Sprite(canvas , "S" , [3 , 3] , "first_sprite" ) 
# "canvas" is the canvas that is associated with the sprite in question
# "S" is character that the sprite will be represented with.
# and "first_sprite" is the name of the sprite
```
feel free to add multiples sprites :) !

## Moving functions 🏃

If you wanted to move them then simply do that:
```python

# add 1 to x-axis:
sprite.change_x(1) 

# add -1 y-axis:
sprite.change_y(-1)

#set x-axis
sprite.set_x(1)

#set y-axis
sprite.set_y(3)

#set position (x and y)
sprite.set_position([3 , 5])

#add to x and y axis
sprite.change_postion(1 , -1)
#first argument is for "x" and the second for "y"

```

## Useful sprite methods 🎓

There are a few important function for sprites that needs to be known.
For example if you want to delete 💣 an object 
```python
albert_the_sprite.destroy()
```

or to rename it
```python
albert_the_sprite.rename("albert")
```

but also to handle collisions 💥
```python
albert_the_sprite.get_colliding_objects()
```
"get_colliding_objects" is a method that returns all sprites names that colliding with the sprite that execute
the method (albert_the_sprite here)

we can check collision like so:
```python

canvas = oz.Canvas("#")

albert_the_sprite = oz.Sprite(canvas , "a" , [0 , 0] , "albert")
robert_the_sprite = oz.Sprite(canvas , "r" , [0 , 0] , "robert")
billy_the_sprite = oz.Sprite(canvas, "b" , [2 , 0] , "billy")

if "robert" in albert_the_sprite.get_colliding_objects():
  
  print("collides with:" , albert_the_sprite.get_colliding_objects())
  print("robert collided with albert.")

else:

  print("robert didn't collide with albert.")
```

Now if we wanted to execute a method to robert with could use the "get_sprite()"
``` python
canvas.get_sprite("robert").set_position([2 , 0])
```
Please note that you will need to execute this method throught the canvas that is associated with the sprite.

## Groups

"group" is an optional argument of the object "Sprite" that can be used to call a method to each sprite that belong to this group or check collisions between groups.

### Collision with groups 💥

First things first you need to actually define the group that the sprite belongs to:
```python
snake_the_sprite = oz.Sprite(canvas , "s" , [0 , 0] , "albert" , "animal")
cat_the_sprite = oz.Sprite(canvas , "c" , [0 , 0] , "robert" , "animal")

apple_the_sprite = oz.Sprite(canvas , "a" , [0 , 0] , "robert" , "fruit")
```

now we can simply check collision:
```python
print(apple_the_sprite.get_colliding_groups())
#output : ["fruit" , "animal"]


if "animal" in apple_the_sprite.get_colliding_groups():
    print("The fruit was eaten by an animal ")

else:
    print("The fruit is still here :D !")
```

the method "get_colliding_groups()" returns a list that contains every groups that collides with the sprite
that executes the method.

## Calling groups 📢

Let's imagine that we are making a game where if a button is pressed all the doors should open
well it would simple just to use the method "call_group()".

but first we need to create our own sprite type : "Door"
we will do so by creating a New class called you guessed it : "Door"

```python

#inherits from class "Sprite"
class Door(Sprite):
  #reusing code from Sprite here:
  #if you want to know what this is for then go to the "How it works" section.
  
  __slots__ = "canvas_owner", "char", "position", "name", "group", "distance", 
  "on_function_ready"

  def __init__(self,
               canvas_owner: object,
               char: str,
               position: list,
               name: str,
               group=None,  
               ):

    
    self.char = char
    self.position = position
    self.name = name
    self.canvas_owner = canvas_owner
    self.group = group

    if name in canvas_owner.sprite_names:
      # change name if already taken
      self.name = name + f"@{str(id(self))}"

    # register infos in "canvas_owner" :
    canvas_owner.sprite_tree.append(self)
    canvas_owner.sprite_names.append(self.name)
    canvas_owner.sprite_names_dict[self.name] = self
    canvas_owner.sprite_position_dict[self] = position

    if not (group in canvas_owner.sprite_group_dict):
      #if group is new then add to "group_tree" and create new key 
      #location for "sprite_group_dict".
      canvas_owner.sprite_group_dict[group] = []
      canvas_owner.group_tree.append(group)

                 
    canvas_owner.sprite_group_dict[group].append(self)


  #our function to open the door
  def open_door(self):
    print(f'door : "{self.name}" was opened !' )

```
and then we can instance the door and call the method
```python
canvas = oz.Canvas("#")

door_one = Door(canvas , "1" , [-4 , 2] , "door_one" , "door")
door_two = Door(canvas , "2" , [2 , -3] , "door_two" , "door")
door_three = Door(canvas , "3" , [3 , 7] , "door_three" , "door")

canvas.call_group("door" , "open_door" )

#output : 
#door : "door_one" was opened !
#door : "door_two" was opened !
#door : door_three was opened !

```

but now let's say we want to give and argument well it's super easy :) 
```python
#add method to the door class
def multiply_x_axis(self , times):
    self.set_x(self.position[0] * times) #position[0] is the x-axis
```

then just call the method:
```python
canvas = oz.Canvas("#")

door_one = Door(canvas , "1" , [-4 , 2] , "door_one" , "door")
door_two = Door(canvas , "2" , [2 , -3] , "door_two" , "door")
door_three = Door(canvas , "3" , [3 , 7] , "door_three" , "door")

print(canvas.sprite_position_dict.values()) #prints all positions
#output before call : dict_values([[-4, 2], [2, -3], [3, 7]])

canvas.call_group("door" , "multiply_x_axis", 2 )
print(canvas.sprite_position_dict.values()) #prints all positions multiplied by 2
#output after call : dict_values([[-4, 2], [2, -3], [3, 7]])
```

giving multiple arguments is possible.

# Making a Game : __**Connect-4**__

Power-4 is a classic game that can be easily made with __**Oz-Engine**__


![](https://thumbs.gfycat.com/ScientificTatteredCardinal-size_restricted.gif)

_(Snake 🐍 is also possible if you possess a microbit card, go [here](https://github.com/menitoon/Oz-Engine-Microbit-version) if you are interested._) 


## Explaining How the **Gameloop** is structured

Here I will be explain ``game`` function and then I'l explain how functions it uses are working.
````python
def game():

  #make these accessibles through any functions
  global canvas
  global coin_red_position
  global coin_yellow_position
  global coin_level

  #Instance "canvas"
  canvas = oz.Canvas("██")
  #Instance "camera"
  camera = oz.Camera(canvas, [7, 6], [0, 0], "cam")

  coin_level = [5 for i in range(camera.size[0])]*
  #Contains every positions of red coins
  coin_red_position = []
  #Contains every positions of yellow coins
  coin_yellow_position = []

  #Tell who's playing
  is_turn_p_one = True
  #render
  print(camera.render())
  #Print the list of valid inputs
  print( " " + (" ".join(get_possible_input())))

  while True:

    action = input(": ") #ask input

    if action in get_possible_input(): #if action token is possible
    
      place_coin(int(action), "🔴" if is_turn_p_one else "🟡") #place "🔴" if red's                                                                 #turn else place"🟡"
      is_turn_p_one = not is_turn_p_one
      is_aligned = check_aligned()    #Tells if 4 coins of the same color are aligned


      if is_aligned[0]: #if is_aligned[0] == True

        break
    
    os.system('cls')        #clears the screen
    print(camera.render())  #render
    print( " " + (" ".join(get_possible_input()))) #print possible inputs

  #End game script :
  os.system('cls') #clear screen
  print(camera.render()) #render
  print(f"Aligned ! {is_aligned[1]} won !") #print win message
  #ask if you want to do a knew a game
  if input("Would you like to play an other round ?(y/n): ") == "y": #if input given is "y" 
    game()                                                           #then restart game by calling "game()"
    
  else:
    exit() #quit
````
```coin_level``` is a list with every high of every **column** the lower that high is the higher the coins are.

## Creating the **Coin** class 🟡

To be able to have more control over our sprites we will create the **Coin** class

````python
class Coin(oz.Sprite):

  __slots__ = "canvas_owner", "char", "position", "name", "group", "distance",
  "on_function_ready"

  def __init__(
    self,
    canvas_owner: object,
    char: str,
    position: list,
    name: str,
    group=None,
  ):
    '''Character that represents the sprite when rendered.'''
    self.char = char
    '''List that has two element "x" and "y" it tells where to render the sprite.'''
    self.position = position
    '''Name of the sprite that can be used to get reference from it using the "get_sprite" method throught a "Canvas" object.'''
    self.name = name
    '''Canvas that the sprite is associated to.'''
    self.canvas_owner = canvas_owner
    '''group is a string that be used to call a method on each sprite that has the same method with 
    the method "call_group" through the canvas and it can also be used to check collision by seing which sprite of which
    group is colliding with our sprite with the method "get_colliding_groups" that can be executed by a "Sprite" object. '''
    self.group = group

    if name in canvas_owner.sprite_names:
      # change name if already taken
      self.name = name + f"@{str(id(self))}"

    # register infos in "canvas_owner" :
    canvas_owner.sprite_tree.append(self)
    canvas_owner.sprite_names.append(self.name)
    canvas_owner.sprite_names_dict[self.name] = self
    canvas_owner.sprite_position_dict[self] = position

    if not (group in canvas_owner.sprite_group_dict):
      #if group is new then add to "group_tree" and create new key
      #location for "sprite_group_dict".
      canvas_owner.sprite_group_dict[group] = []
      canvas_owner.group_tree.append(group)

    canvas_owner.sprite_group_dict[group].append(self)

    if self.char == "🟡":
      coin_yellow_position.append(self.position)
    else:
      coin_red_position.append(self.position)
````
Here we created a custom **Sprite** class like we did [here](#calling-groups)

## Placing down a coin
Let's create a function to place down some coins.
````python
def place_coin(x, val):

  coin = Coin(canvas, val, [x, coin_level[x]], "coin")
  coin_level[x] -= 1 #so that the next coin at this column will go up

````
**x** represents the column where we place our coin and **val** whethever it's a **red** one 🔴 or a **yellow** one 🟡

## Giving valid inputs
The two players needs to know in which column they can place a coin, so let's make a function to do this:
```python
def get_possible_input():

  return [str(c) for c in range(len(coin_level)) if not (coin_level[c] == -1)] 
````
we return a list of all column that aren't full, we also use **str()** to later on have more control over
what we print to the player.

## detecting if coins are aligned

```python
def check_aligned():


  has_alignement = (False , "None") # if someone won or not
  
  # check if red are aligned
  for red_coin_pos in coin_red_position:

    horizontal_match = 0
    vertical_match = 0
    diagonal_left_match = 0
    diagonal_right_match = 0

    POS_X = red_coin_pos[0]
    POS_Y = red_coin_pos[1]

    # horizontal_match check
    
    for i in range(1, 4):
      if [i + POS_X ,POS_Y] in coin_red_position: # if are aligned add 1 to horizontal_match 
        horizontal_match += 1
        

      else:
        break

    # to get a win you need at least 3 matches
    # we break if someone won 
    if horizontal_match == 3:
      has_alignement = (True , "red")
      break

    #we do same for others directions

    # vertical_match check
    for i in range(1, 4):
      if [POS_X, i + POS_Y] in coin_red_position:
        vertical_match += 1

      else:
        break

    if vertical_match == 3:
      has_alignement = (True , "red")
      break

    
    # diagonal_left_match check
    for i in range(1, 4):
      if [-i + POS_X, -i + POS_Y] in coin_red_position:
        diagonal_left_match += 1

      else:
        break

    if diagonal_left_match == 3:
      has_alignement = (True , "red")
      break

    # diagonal_right_match check
    for i in range(1, 4):
      if [i + POS_X, -i + POS_Y] in coin_red_position:
        diagonal_right_match += 1

      else:
        break

    if diagonal_right_match == 3:
      has_alignement = (True , "red")
      break
  
  if has_alignement[1] != "None":
    return has_alignement

  #we do the same for yellow coins
  
  for yellow_coin_pos in coin_yellow_position:

    POS_X = yellow_coin_pos[0]
    POS_Y = yellow_coin_pos[1]

    horizontal_match = 0
    vertical_match = 0
    diagonal_left_match = 0
    diagonal_right_match = 0

    # horizontal_match check
    for i in range(1, 4):
      if [i + POS_X ,POS_Y] in coin_yellow_position:
        horizontal_match += 1

      else:
        break

    if horizontal_match == 3:
      has_alignement = True
      break


    # vertical_match check
    for i in range(1, 4):
      if [POS_X, i + POS_Y] in coin_yellow_position:
        vertical_match += 1

      else:
        break

    if vertical_match == 3:
      has_alignement = (True , "yellow")
      break

    
    # diagonal_left_match check
    for i in range(1, 4):
      if [-i + POS_X, -i + POS_Y] in coin_yellow_position:
        diagonal_left_match += 1

      else:
        break

    if diagonal_left_match == 3:
      has_alignement = (True , "yellow")
      break

    # diagonal_right_match check
    for i in range(1, 4):
      if [i + POS_X, -i + POS_Y] in coin_p_two_position:
        diagonal_right_match += 1

      else:
        break

    if diagonal_right_match == 3:
      has_alignement = (True , "yellow")
      break

  return has_alignement
```


## Executing the **game** 🕹️

Just execute the ```game()``` function at the end of your script, save it and close it.
Now just double click on the ``main.py`` file to run it.

And we have a working Connect-4 game 😊.

_if you have any issue you can find the full code [here](https://github.com/menitoon/Connect-4-with-Oz-Engine)


# Contributing 💻

Contributions to this project are greetly apreciated 😁 for more info ℹ️
check the [Contribution Guidelines](https://github.com/menitoon/Oz-Engine/blob/main/CONTRIBUTING.md).
