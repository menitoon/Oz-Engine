import math

sprite = []
distances = []
distance_from = {}


def deep_copy(L):
  if isinstance(L, list):
    ret = []
    for i in L:
      ret.append(deep_copy(i))
  elif isinstance(L, (int, float, type(None), str, bool)):
    ret = L
  else:
    raise ValueError("Unexpected type for mydeepcopy function")

  return ret


class Sprite:

  def __init__(self, char, position, name="null"):

    self.char = char
    self.position = position
    self.name = name

    sprite.append(self)

  def get_pos(self):
    print(self.position)

  #sprite must start with "S" like this :   S_name_of_sprite


canvas = []
camera_pos = [0, 0]
size = [0, 0]

sprite_priority = []


def _create_canvas(x, y, void):
  # allow to define size of canvas

  x_line = []

  for todo in range(x):

    x_line.append(str(void))

  for subtodo in range(y):

    canvas.append(x_line)


def _edit_element(x, y, char, name_canvas):

  line = deep_copy(name_canvas[y])
  line[x] = char
  name_canvas[y] = line

  return name_canvas


def _get_canvas(is_string: bool):  #renders the canvas

  line = ""

  render_canvas = deep_copy(canvas)

  corner_one = [0, 0]
  corner_two = [size[0] - 1, 0]
  corner_three = [size[0] - 1, size[1] - 1]
  corner_four = [0, size[1] - 1]

  pos = [size[0] - 1, size[1] - 1]

  max_distance = (_get_distance_between(corner_one, pos) +
                  _get_distance_between(corner_two, pos) +
                  _get_distance_between(corner_three, pos) +
                  _get_distance_between(corner_four, pos)) / 4

  _get_every_distance_from()

  todo = 0

  for current_sprite in sprite:

    

    current_pos = current_sprite.position

    render_check_pos = [
      current_pos[0] - camera_pos[0], current_pos[1] - camera_pos[1]
    ]
    
    current_pos = deep_copy(render_check_pos)

    

    # check if can reder

    if distances[sprite.index(current_sprite)] > max_distance:

      print("can't render")
      #pass
      break

    else:

      _edit_element(current_pos[0], current_pos[1], current_sprite.char,
                    render_canvas)

    todo += 1

  if is_string:

    for current_line in render_canvas:

      for current_element in current_line:

        line += str(current_element)

      line += "\n"

    return line

  else:

    return render_canvas


def _get_element(x, y):

  line = canvas[y]
  return line[x]


def _get_distance_between(pos1, pos2):

  return math.sqrt((pow((pos2[0] - pos1[0]), 2) + pow(
    (pos2[1] - pos1[1]), 2)))  # √[(x₂ - x₁)² + (y₂ - y₁)²]


def _get_every_distance_from():

  global distance_from
  global distances

  distances = []
  

  corner_one = [0, 0]
  corner_two = [size[0] - 1, 0]
  corner_three = [size[0] - 1, size[1] - 1]
  corner_four = [0, size[1] - 1]

  

  for todo_sprite in sprite:

    gloabal_pos = [
      todo_sprite.position[0] - camera_pos[0],
      todo_sprite.position[1] - camera_pos[1]
    ]

    distance_calculated = (_get_distance_between(corner_one, gloabal_pos) +
                           _get_distance_between(corner_two, gloabal_pos) +
                           _get_distance_between(corner_three, gloabal_pos) +
                           _get_distance_between(corner_four, gloabal_pos)) / 4


    distances.append(distance_calculated)

  print(distances, "distances")

  
  sorted_list = []
  sprite_priority = []

  while distances != [] :

    min_distance = min(distances)
    
    sorted_list.append(min_distance)
    sprite_priority.append( sprite[distances.index(min_distance)] ) #gets the correct sprite associated to it 's distance
    distances.remove(min(distances))
    
  
  distances = sorted_list
  print(sprite_priority)


def _send_light_update():

  x = 0
  y = 0

  for line in _get_canvas(False):

    for element in line:

      #display.set_pixel(x, y, element)
      x += 1

    x = 0
    y += 1


### Init Canvas ###

size = [5, 5]
_create_canvas(size[0], size[1], 0)

### Init Snake ###

S_ok = Sprite(7, [0, 0], "ok")
S_Head = Sprite(6, [1, 2], "Head")
S_Body = Sprite(6, [3, 2], "Body")

#while True:

#if input("b r u h : ") == "d":

#S_Head.position[0] += 1

#print(_get_canvas(True))

print(_get_canvas(True))
