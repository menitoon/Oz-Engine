
==============================================================================
# OZ ENGINE 

Oz-Engine is a text based engine made by @menitoon using python.
It can be used to make games in terminal and with additional modules in discord or any matrix led based screen

#### STARTUP

 ``` pip install Oz-Engine ```
 
 ```python 
 import OzEngine as oz 
 ```


# How to use it

## Creating the canvas

Start by instancing a canvas like so: 
```python 
canvas = Canvas("#") 
# The  argument is given what the canvas will be filled with.
```
and then instancing a camera so that we can render the scene.
```python
camera = Camera(canvas , [10 , 10] , [0 , 0] , "camera")
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

## Adding Sprites

It's cool and all but a little boring to have just an empty canvas.
Let's add a sprite:
```python
sprite = Sprite(canvas , "S" , [3 , 3] , "first_sprite" ) 
# "canvas" is the canvas that is associated with the sprite in question
# "S" is character that the sprite will be represented with.
# and "first_sprite" is the name of the sprite
```
feel free to add multiples sprites :) !

# moving functions

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

## Useful sprite methods

There are a few important function for sprites that needs to be known.
For example if you want to delete an object
```python
albert_the_sprite.destroy()
```

or to rename it
```python
albert_the_sprite.rename("albert")
```

but also to handle collisions
```python
albert_the_sprite.get_colliding_objects()
```
"get_colliding_objects" is a method that returns all sprites names that colliding with the sprite that execute
the method (albert_the_sprite here)

we can check collision like so:
```python

canvas = Canvas([4 , 5] , 0)

albert_the_sprite = Sprite(canvas , "a" , [0 , 0] , "albert")
robert_the_sprite = Sprite(canvas , "r" , [0 , 0] , "robert")
billy_the_sprite = Sprite(canvas, "b" , [2 , 0] , "billy")

if "robert" in albert_the_sprite.get_colliding_objects():
  
  print("collides with:" , albert_the_sprite.get_colliding_objects())
  print("robert collided with albert.")

else:

  print("robert didn't collide with albert.")
```

Now if we wanted to execute a method to robert with could use the "get_sprite()"
``` python
canvas.get_sprite("robert").position = [2 , 0]
```
Please note that you will need to execute this method throught the canvas that is associated with the sprite.

# How it works

⚠️ NOTE :  before reading this remind yourself that is still work in progress and unfinished this section might be changed in the future.


To start simple imagine we have a board that is filled with "0"

![](grid_zero.png)

this board can be represented with an 2D-array:
```python
[  
   [0, 0 , 0 , 0, 0],
   [0, 0 , 0 , 0, 0],
   [0, 0 , 0 , 0, 0],
   [0, 0 , 0 , 0, 0],
                       ]
```

and that what the method "clear_canvas" from the "Camera" class makes for you:
``` python
   def clear_canvas(self):
    """

    returns a clean canvas, setted
    in to it's empty state

    """

    SIZE_X = self.size[0]
    SIZE_Y = self.size[1]

    return [[self.canvas_owner.VOID for _ in range(SIZE_X)]
            for _ in range(SIZE_Y)]

```

and we should get what we had at first using this function.
