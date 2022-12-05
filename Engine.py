import copy
import Sprite as sp
import math

canvas = []

camera_pos = [0, 0]

size = [40, 40]


def _create_canvas(x, y, void):
  # allow to define size of canvas

  x_line = []

  for todo in range(x):

    x_line.append(str(void))

  for subtodo in range(y):

    canvas.append(x_line)


def _edit_element(x, y, char, name_canvas):

  line = copy.copy(name_canvas[y])
  line[x] = char
  name_canvas[y] = line

  return name_canvas


def _get_canvas():  #renders the canvas

  line = ""

  render_canvas = copy.copy(canvas)

  #here add sprites ( stuff that can be moved or modified (without including bg) )

  _get_every_distance_from()



  for todo_distances in sp.distances:

    current_sp = list(sp.distance_from.keys())[list(sp.distance_from.values()).index(todo_distances)]
    
    current_pos = current_sp.position

    print(current_pos)

    
    if current_pos[1]  < 0  or current_pos[1] > size[1] - 1 or current_pos[0] - camera_pos[1] < 0  or current_pos[0]> size[0] - 1: #check if has to render by saying if in canvas size then render else do not render it.

      print("invalid")

      break

    else:

      

      print(current_pos[1] - camera_pos[1])

      _edit_element(current_pos[0] ,
                    current_pos[1] , current_sp.char,
                    render_canvas)

  for current_line in render_canvas:

    for current_element in current_line:

      line += current_element

    line += "\n"

  return line


def _get_element(x, y):

  line = canvas[y]
  return line[x]


def _get_distance_between(pos1, pos2):

  return math.sqrt((pow((pos2[0] - pos1[0]), 2) + pow(
    (pos2[1] - pos1[1]), 2)))  # √[(x₂ - x₁)² + (y₂ - y₁)²]


def _get_every_distance_from():

  sp.distance_from = {}
  sp.distances = []

  for todo_sprite in sp.sprite:

    distance_calculated = _get_distance_between([size[0] / 2, size[1] / 2],
                                                todo_sprite.position)

    sp.distance_from[
      todo_sprite] = distance_calculated  #adds corresponding distance from center to object to dict
    sp.distances.append(distance_calculated)

  sp.distances.sort()



###TEST HERE TO DELETE###



S_X = sp.Sprite("X", [0, 10], 1)


_create_canvas(size[0], size[1], "#")

_get_every_distance_from()
print(_get_canvas())

end = False

while end == False:

  action = input("give action ")

  if action == "s":

    camera_pos[1] += 1

  elif action == "z":

    camera_pos[1] -= 1


  elif action == "q":

    S_Player.position[0] -= 1

  elif action == "d":

    S_Player.position[0] += 1


  print(_get_canvas())
  
  print( S_Player.position )
  print(camera_pos)
