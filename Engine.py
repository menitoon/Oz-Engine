import math
import time


def warn(text: str):
  print(f"\033[93m!{text} \u001b[0m  ")


class Canvas:
  """
  Object that can store sprites in it to be rendered
  """

  __slots__ = "VOID", "SIZE", "SIZE_X", "SIZE_Y", "canvas", "camera_pos", "CORNER_TOP_LEFT", "CORNER_TOP_RIGHT", "CORNER_BOTTOM_RIGHT", "CORNER_BOTTOM_LEFT", "MAX_DISTANCE", "distance_tree", "sprite_names", "sprite_names_dict", "sprite_tree", "sprite_priority", "sprite_position_dict",

  def __init__(self, VOID):

    self.VOID = VOID

    self.distance_tree = []
    self.sprite_tree = []

    self.sprite_names = []
    self.sprite_names_dict = {}
    self.sprite_position_dict = {}

    # check size settings

  def get_elements(self, position: list, canvas: object):
    """
        Returns sprites names at the given pos
        """

    object_at = []

    sprite_list = list(self.sprite_position_dict.copy().keys())
    position_list = list(self.sprite_position_dict.copy().values())

    while position in position_list:

      INDEX = position_list.index(position)

      object_at.append(sprite_list.pop(INDEX).name)
      #deletes the element from "sprite_list" and appends it to "object_at"
      del position_list[INDEX]
      #and remove the element from "position_list"

    return object_at

  def get_sprite(self, name):
    """
    returns reference to sprite that owns the given name
    """

    return self.sprite_names_dict[name]


class Sprite:
  """
    Object that can be used to fill the canvas
    """

  __slots__ = "canvas_owner", "char", "position", "name", "group", "distance"

  def __init__(self,
               canvas_owner: object,
               char: str,
               position: list,
               name: str,
               group=None):

    self.char = char
    self.position = position
    self.name = name
    self.canvas_owner = canvas_owner

    if name in canvas_owner.sprite_names:
      # change name if already taken
      self.name = name + f"@{str(id(self))}"

    # register name in "canvas_owner" :
    canvas_owner.sprite_tree.append(self)
    canvas_owner.sprite_names.append(self.name)
    canvas_owner.sprite_names_dict[self.name] = self
    canvas_owner.sprite_position_dict[self] = position

  def destroy(self):

    del self.canvas_owner.sprite_names_dict[self.name]
    del self.canvas_owner.sprite_position_dict[self]
    self.canvas_owner.sprite_names.remove(self.name)
    self.canvas_owner.sprite_tree.remove(self)

    print(self.canvas_owner.sprite_names, "del", self.name)
    print(self.canvas_owner.sprite_tree, "del")

    del self

  def rename(self, new_name: str):
    """
        allows to change the name of a sprite, to "rename" it.
        """

    del self.canvas_owner.sprite_names_dict[self.name]

    if new_name in self.canvas_owner.sprite_names:
      # change new_name with object id()
      new_name = new_name + f"@{str(id(self))}"

    # change name

    INDEX = self.canvas_owner.sprite_names.index(self.name)
    self.canvas_owner.sprite_names[INDEX] = new_name
    self.name = new_name
    self.canvas_owner.sprite_names_dict[new_name] = self

  def get_colliding_objects(self):
    """
        Returns a list of colliding objects(by name)
        """

    object_colliding = []

    sprite_check_list = list(
      self.canvas_owner.sprite_position_dict.copy().keys())
    position_check_list = list(
      self.canvas_owner.sprite_position_dict.copy().values())

    sprite_check_list.remove(self)
    position_check_list.remove(self.position)

    for todo_sprite in sprite_check_list:

      POSITION_CHECK = self.canvas_owner.sprite_position_dict[
        todo_sprite]  # gets the position from key

      if self.position in position_check_list:

        object_colliding.append(
          todo_sprite.name) if POSITION_CHECK == self.position else None
      else:
        break

    return object_colliding


  
  

  def update_distance(self):
    """
    gets index from "render_sprite_list"
    and update "render_distance_list" like so :

    self.canvas_owner.render_distance_list[index] =                        self.distance

    """

    # update it
    self.canvas_owner.sprite_position_dict[self] = self.position

  def change_x(self, value: int):
    """
        adds "value" to the y-axis of "position"
        """

    self.position[0] += value
    self.update_distance()

  def change_y(self, value: int):
    """
        adds "value" to the y-axis of "position"
        """

    self.position[1] += value
    self.update_distance()

  def set_x(self, value: int):
    """
        sets "value" to the x-axis of "position"
        """

    self.position[0] = value
    self.update_distance()

  def set_y(self, value: int):
    """
        sets "value" to the y-axis of "position"
        """

    self.position[1] = value
    self.update_distance()

  def set_position(self, value: list):

    self.position = value
    self.update_distance()

  def change_position(self, x_val: int = 0, y_val: int = 0):

    self.position[0] += x_val
    self.position[1] += y_val
    self.update_distance()


class Camera:

  __slots__ = "canvas_owner", "size", "position", "name", "sprite_render_priority", "sprite_distance_dict"

  def __init__(self, canvas_owner: object, size: list, position: list,
               name: str):
    '''canvas that is associated with. '''
    self.canvas_owner = canvas_owner
    '''size of the camera '''
    self.size = size
    ''' position of the camera '''
    self.position = position
    ''' name of the camera'''
    self.name = name
    ''' define the order of rending sprties '''
    self.sprite_render_priority = []
    ''' dictionnary that contain keys "sprite" for value "distance" '''
    self.sprite_distance_dict = {}

  def render(
    self,
    is_string: bool = True,
  ):
    """
        Returns the rendered canvas as a string if "is_string" is true else as a 2D-list
        """

    self.update_sprite_distance_dict()

    # clear canvas
    render_canvas = self.clear_canvas()

    self.get_every_distance_from()

    for current_sprite in self.sprite_render_priority:

      current_pos = current_sprite.position  # set position of the sprite we are looking at throught the for loop

      camera_x = self.position[0]  # define x_axis of camera
      camera_y = self.position[1]  # define y_axis of camera

      current_pos_x = current_pos[0]
      # define x_axis of the current sprite position we are looking at
      current_pos_y = current_pos[1]
      # define y_axis of the current sprite position we are looking at

      RENDER_POS = [current_pos_x - camera_x, current_pos_y - camera_y
                    ]  # sprite postion - camera_position

      RENDER_POS_X = RENDER_POS[0]  # define x_axis of render position
      RENDER_POS_Y = RENDER_POS[1]  # define y_axis of render position

      self.edit_element(render_canvas, RENDER_POS_X, RENDER_POS_Y,
                        current_sprite.char)
      # Update render

    if is_string:

      line = ""

      for current_line in render_canvas:

        for current_element in current_line:
          line += str(current_element)

        line += "\n"

      return line

    else:
      return render_canvas

  def update_sprite_distance_dict(self):
    """
        update the distance of every sprite
        """

    self.sprite_distance_dict = {}

    for todo_sprite in self.canvas_owner.sprite_tree:

      sprite_position = [
        todo_sprite.position[0] - self.position[0],
        todo_sprite.position[1] - self.position[1]
      ]
      self.sprite_distance_dict[todo_sprite] = self.get_square_distance_to(
        sprite_position)

  def clear_canvas(self):
    """

        returns a clean canvas, setted
        in to it's empty state

        """

    SIZE_X = self.size[0]
    SIZE_Y = self.size[1]

    return [[self.canvas_owner.VOID for _ in range(SIZE_X)]
            for _ in range(SIZE_Y)]

  def edit_element(self, canvas, x, y, char):
    """
        allows to edit an element of a canvas
        """

    (canvas[y])[x] = char

  def get_square_distance_to(self, position: list):
    """
    returns the sum of the distance between the 4 corners of         the square
    """

    SIZE_X = self.size[0] - 1
    SIZE_Y = self.size[1] - 1

    corner_top_left = [0, 0]
    corner_top_right = [SIZE_X, 0]
    corner_bottom_right = [SIZE_X, SIZE_Y]
    corner_bottom_left = [0, SIZE_Y]

    return (math.dist(corner_top_left, position) +
            math.dist(corner_top_right, position) +
            math.dist(corner_bottom_right, position) +
            math.dist(corner_bottom_left, position))

  def get_every_distance_from(self):
    """
        define sprite_priority, which sprite should be rendered first.
        """

    self.sprite_render_priority = []

    distances = list(self.sprite_distance_dict.copy().values())
    sprite_list = list(self.sprite_distance_dict.copy().keys())

    for todo in range(len(self.canvas_owner.sprite_tree)):

      min_distance = min(distances)
      # gets the smallest distance in list "distances"

      if not self.is_renderable(min_distance):
        # if the smallest distance of the sprite(+ camera offset)
        # is bigger than "MAX_DISTANCE"

        break

      index = distances.index(min_distance)
      self.sprite_render_priority.append(sprite_list[index])

      # gets the correct sprite associated to it 's
      # distance and appends list to"sprite_priority"

      del sprite_list[index]
      del distances[index]
      # remove thoses

  def is_renderable(self, distance):
    """
        returns whether a sprite a renderable from the distance given.
        """

    MAX_DISTANCE = (self.get_square_distance_to([0, 0]))

    return not (distance + self.get_square_distance_to(self.position)) > (
      MAX_DISTANCE + self.get_square_distance_to(self.position))





def critic_test(size , amount):

  canvas = Canvas(0)
  camera = Camera(canvas, [size, size], [0, 0], "camera")
  
  for i in range(amount):

    s1 = Sprite(canvas, 1, [i, 0], "s1")
    s2 = Sprite(canvas, 2, [0, -i], "s2")

  fps = 0
  start = time.monotonic_ns()

  mid_fps = []

  for i in range(1000):

    if ((time.monotonic_ns() - start) / 100000000) > 1.0:

      start = time.monotonic_ns()
      mid_fps.append(fps)

      fps = 0

    s1.get_colliding_objects()
    camera.render()
    fps += 1

  mid_fps = sum(mid_fps) / len(mid_fps)
  print(f"{mid_fps} FPS")

