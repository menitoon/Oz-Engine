import math


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


class Canvas:

  def __init__(self, size: list, void):

    self.size = size
    self.void = void

    self.canvas = []
    self.camera_pos = [0, 0]
    self.sprite_priority = []
    self.sprite = []
    self.distance_from = {}
    self.distances = []

    #sprite must start with "S" like this :   S_name_of_sprite

  def create_canvas(self, void):
    # Build The Canvas

    x_line = []  #line of canvas

    x = self.size[0]  # size setted in the constructor
    y = self.size[1]  # size setted in the constructor

    for todo in range(x):

      x_line.append(str(void))

    for subtodo in range(y):

      self.canvas.append(x_line)

  def edit_element(self, x, y, char):

    line = self.canvas[y]
    line[x] = char
    print(self.canvas)
    #self.canvas[y] = line

    return self.canvas

  def get_canvas(self, is_string: bool):  #renders the canvas

    canvas = self.canvas
    camera_pos = self.camera_pos
    size = self.size
    sprite_priority = self.sprite_priority
    distances = self.distances

    line = ""

    render_canvas = deep_copy(canvas)

    corner_one = [0, 0]
    corner_two = [size[0] - 1, 0]
    corner_three = [size[0] - 1, size[1] - 1]
    corner_four = [0, size[1] - 1]

    pos = [size[0] - 1, size[1] - 1]

    max_distance = (self.get_distance_between(corner_one, pos) +
                    self.get_distance_between(corner_two, pos) +
                    self.get_distance_between(corner_three, pos) +
                    self.get_distance_between(corner_four, pos)) / 4

    self.get_every_distance_from()

    todo = 0

    print(self.sprite_priority , "sprite prio")

    for current_sprite in self.sprite_priority:

      

      current_pos = current_sprite.position

      render_check_pos = [
        current_pos[0] - self.camera_pos[0], current_pos[1] - self.camera_pos[1]
      ]

      current_pos = deep_copy(render_check_pos)

      # check if can render

      

      if self.distances[self.sprite_priority.index(current_sprite)] > max_distance:


        #pass
        break

      else:

        print("can render")

        print([current_pos[0], current_pos[1]])
        self.edit_element(current_pos[0], current_pos[1], current_sprite.char)

      todo += 1

    if is_string:

      for current_line in render_canvas:

        for current_element in current_line:

          line += str(current_element)

        line += "\n"

      return line

    else:

      return render_canvas

  
  def get_element(self, x, y):

    line = self.canvas[y]
    return line[x]
    

  def get_distance_between(self, pos1, pos2):

    return math.sqrt((pow((pos2[0] - pos1[0]), 2) + pow(
      (pos2[1] - pos1[1]), 2)))  # √[(x₂ - x₁)² + (y₂ - y₁)²]

  def get_every_distance_from(self):

    #global distance_from
    #global distances
    #global sprite_priority

    self.sprite_priority = []
    self.distances = []                  

                                         
    corner_one = [0, 0]                                    #
    corner_two = [self.size[0] - 1, 0]                     #
    corner_three = [self.size[0] - 1, self.size[1] - 1]    # Calculates distance from all 4 corners of canvas               
    corner_four = [0, self.size[1] - 1]                    #

    self.sprite_priority = self.sprite
    print(self.sprite_priority)

    for todo_sprite in self.sprite_priority:

      gloabal_pos = [
        todo_sprite.position[0] - self.camera_pos[0],
        todo_sprite.position[1] - self.camera_pos[1]
      ]

      distance_calculated = (
        self.get_distance_between(corner_one, gloabal_pos) +
        self.get_distance_between(corner_two, gloabal_pos) +
        self.get_distance_between(corner_three, gloabal_pos) +
        self.get_distance_between(corner_four, gloabal_pos)) / 4

      self.distances.append(distance_calculated)

    sorted_list = []  # sort the distance list
    new_sprite_priority = [
    ]  # sort sprites by how close are they to render point.

    while self.distances != []:

      min_distance = min(self.distances)
      sorted_list.append(min_distance)
      new_sprite_priority.append(self.sprite_priority[self.distances.index(min_distance)])
      
      #gets the correct sprite associated to it's distance

      self.sprite_priority.remove( self.sprite_priority[self.distances.index(min_distance)])
      self.distances.remove(min(self.distances))

    self.sprite_priority = new_sprite_priority  #sets local variable new_sprite_priority to sprite_priority (global)
    self.distances = sorted_list  #same here

    print(self.sprite_priority)

    

  def send_light_update(
    self
  ):  #Microbit Function remove the hashtag to make function useable and import microbit package

    x = 0
    y = 0

    for line in self.get_canvas(False):

      for element in line:

        #display.set_pixel(x, y, element)
        x += 1

      x = 0
      y += 1

  class Sprite():

    def __init__(self, char, position, z_index):

      self.char = char
      self.position = position
      self.z_index = z_index

      Canvas.sprite.append(self)


Canvas = Canvas([5, 5], 0)
Canvas.create_canvas("0")

S_test = Canvas.Sprite("5", [2, 2], "five")

print(Canvas.get_canvas(True))
