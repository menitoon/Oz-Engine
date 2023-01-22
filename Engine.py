import math
import time

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

  def __init__(self, SIZE: list, VOID):

    self.VOID = VOID
    self.SIZE = SIZE
    self.SIZE_X = SIZE[0]
    self.SIZE_Y = SIZE[1]

    self.canvas = []
    self.camera_pos = [0, 0]

    self.CORNER_TOP_LEFT = (0, 0)
    self.CORNER_TOP_RIGHT = (self.SIZE_X - 1, 0)
    self.CORNER_BOTTOM_RIGHT = (self.SIZE_X - 1, self.SIZE_Y - 1)
    self.CORNER_BOTTOM_LEFT = (0, self.SIZE_Y - 1)
    self.MAX_DISTANCE = (
      self.get_distance_between(self.CORNER_TOP_LEFT, self.CORNER_BOTTOM_LEFT)
      + self.get_distance_between(self.CORNER_TOP_RIGHT,
                                  self.CORNER_BOTTOM_LEFT) +
      self.get_distance_between(self.CORNER_BOTTOM_RIGHT,
                                self.CORNER_BOTTOM_LEFT) +
      self.get_distance_between(self.CORNER_BOTTOM_LEFT,
                                self.CORNER_BOTTOM_LEFT)) / 4

    self.distances = []
    self.sprite_tree = []
    self.sprite_priority = []
    self.sprite_names = []
    self.sprite_names_dict = {}

    self.create_canvas()



  
  def create_canvas(self):
    # allow to define size of canvas

    

    SIZE = self.SIZE
    SIZE_X = self.SIZE_X
    SIZE_Y = self.SIZE_Y
    VOID = self.VOID

    if SIZE == [0, 0]:

      print(
        '\033[93m' +
        "!Canvas size is not defined and will most likely not work.")  #warn
      print("\u001b[0m")

    x_line = []

    for todo in range(SIZE_Y):

      x_line.append(str(VOID))

    for subtodo in range(SIZE_X):

      self.canvas.append(x_line)


  

  def edit_element(self, x, y, char):

    line = deep_copy(self.canvas[y])
    line[x] = char
    self.canvas[y] = line

    return self.canvas

  def get_canvas(self, is_string: bool = True):  #renders the canvas

    
    render_canvas = deep_copy(self.canvas) #deep_copy of empty canvas to stack sprite instance on it.
    self.get_every_distance_from()         #define sprite_priority, which sprite should be rendered first
    
    

    for current_sprite in self.sprite_priority:


      current_pos = current_sprite.position #set position of the sprite we are looking at throught the for loop

      camera_x = self.camera_pos[0]         #define x_axis of camera
      camera_y = self.camera_pos[1]         #define y_axis of camera

      current_pos_x = current_pos[0]        #define x_axis of the current sprite position we are looking at
      current_pos_y = current_pos[1]        #define y_axis of the current sprite position we are looking at

      RENDER_POS = [current_pos_x - camera_x, current_pos_y - camera_y]  #sprite postion - camera_position

      RENDER_POS_X = RENDER_POS[0]          #define x_axis of render position
      RENDER_POS_Y = RENDER_POS[1]          #define y_axis of render position

      
      current_distance = self.distances[self.sprite_priority.index(current_sprite)]  #gets the distance of sprite from square with sprite_priority index
                                                                                     # sprite = [ sprite1 , sprite2 ]
                                                                                     # distances = [4.0 , 5.0]
                                                                                     # sprite_priority.index(current_sprite) returns 1 so = distances[1]

      if current_distance > self.MAX_DISTANCE:
        break

      else:
        render_canvas = self.edit_element(RENDER_POS_X, RENDER_POS_Y, current_sprite.char)

      
    if is_string:

      line = ""

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

    self.distances = []

    camera_pos = self.camera_pos
    CORNER_TOP_LEFT = self.CORNER_TOP_LEFT
    CORNER_TOP_RIGHT = self.CORNER_TOP_RIGHT
    CORNER_BOTTOM_RIGHT = self.CORNER_BOTTOM_RIGHT
    CORNER_BOTTOM_LEFT = self.CORNER_BOTTOM_LEFT

    camera_pos_x = camera_pos[0]
    camera_pos_y = camera_pos[1]

    for todo_sprite in self.sprite_tree:

      sprite_pos = [
        todo_sprite.position[0] - camera_pos_x,
        todo_sprite.position[1] - camera_pos_y
      ]

      distance_calculated = (
        self.get_distance_between(CORNER_TOP_LEFT, sprite_pos) +
        self.get_distance_between(CORNER_TOP_RIGHT, sprite_pos) +
        self.get_distance_between(CORNER_BOTTOM_RIGHT, sprite_pos) +
        self.get_distance_between(CORNER_BOTTOM_LEFT, sprite_pos)) / 4

      self.distances.append(distance_calculated)

    self.sprite_priority = self.sprite_tree
    sorted_list = []
    new_sprite_priority = []

    for todo in range(len(self.distances)):

      min_distance = min(self.distances)

      sorted_list.append(min_distance)

      new_sprite_priority.append(self.sprite_priority[self.distances.index(
        min_distance)])  #gets the correct sprite associated to it 's distance

      self.sprite_priority.remove(
        self.sprite_priority[self.distances.index(min_distance)])
      self.distances.remove(min(self.distances))

    self.sprite_priority = new_sprite_priority
    self.sprite_tree = self.sprite_priority
    self.distances = sorted_list

  def send_light_update(self):

    x = 0
    y = 0

    for line in self.get_canvas(False):

      for element in line:

        #display.set_pixel(x, y, element)
        x += 1

      x = 0
      y += 1


class Sprite:

  #sprite must start with "s" like this when initiated :   S_name_of_sprite

  def __init__(self,
               canvas_object: object,
               char: str,
               position: list,
               name: str,
               group=None):

    self.char = char
    self.position = position
    self.name = name
    self.canvas_object = canvas_object

    canvas_object.sprite_tree.append(self)

    if name not in canvas_object.sprite_names:

      canvas_object.sprite_names.append(self.name)
      canvas_object.sprite_names_dict[self.name] = self

    else:
      #crash and send the follow error back:
      raise (ValueError(
        "Sprite name already exists , please choose another name , only unique names are allowed or consider deleting the older one."
      ))

  def destroy(self):

    self.canvas_object.sprite_tree.remove(self)
    del self




