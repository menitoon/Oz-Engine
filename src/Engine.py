import math
import time


def warn(text: str):
  print(f"\033[93m!{text} \u001b[0m  ")


class Canvas:
  """
  Object that can store sprites in it to be rendered
  """

  __slots__ = "VOID", "distance_tree", "sprite_names", "sprite_names_dict", "sprite_tree", "sprite_priority", "sprite_position_dict", "sprite_group_dict", "group_tree"

  def __init__(self, VOID):
    ''' Characters that fills the canvas when nothing is rendered on a tile. '''
    self.VOID = VOID
    '''List that contains every distance of each sprite '''
    self.distance_tree = []
    '''List that contains every reference of each sprite '''
    self.sprite_tree = []
    '''List that contains every groups that exists'''
    self.group_tree = []
    '''List that contains every name of each sprite '''
    self.sprite_names = []
    '''Dictionary that has a sprite reference as a key and the corresponding name as a value'''
    self.sprite_names_dict = {}
    '''Dictionary that has a sprite reference as a key and the corresponding position as a value'''
    self.sprite_position_dict = {}
    '''Dictionary that has a sprite reference as a key and the corresponding group as a value'''
    self.sprite_group_dict = {}

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
      # deletes the element from "sprite_list" and appends it to "object_at"
      del position_list[INDEX]
      # and remove the element from "position_list"

    return object_at

  def get_sprite(self, name):
    """
    returns reference to sprite that owns the given name
    """

    return self.sprite_names_dict[name]

  def call_group(self, group_to_call: str, method_to_call, *args):
    """
    Call a method  to every sprites that belongs to the group that is
    given 

    like so:

    canvas.call_group("group_name_here" , method_is_going_to_be_called_on_them() )
    
    """

    #gets every sprite that is in the group given

    sprite_to_call = self.sprite_group_dict.get(group_to_call)
    if sprite_to_call == None:
      #if group given doesn't exist then sumbit error
      raise Exception(
        f'''The group "{group_to_call}" doesn't exist please specify a valid group to call. '''
      )

    for todo_sprite in sprite_to_call:

      func = getattr(todo_sprite, method_to_call)
      func(*args)


class Sprite:
  """
  Object that can be used to fill the canvas
  """

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

  def destroy(self):

    del self.canvas_owner.sprite_names_dict[self.name]
    del self.canvas_owner.sprite_position_dict[self]

    #remove self from key that contain every sprite in group
    INDEX = self.canvas_owner.sprite_group_dict[self.group].index(self)
    del (self.canvas_owner.sprite_group_dict[self.group])[INDEX]

    self.canvas_owner.sprite_names.remove(self.name)
    self.canvas_owner.sprite_tree.remove(self)

    if len(self.canvas_owner.sprite_group_dict[self.group]) == 0:
      #delete group if no one is in it.
      del self.canvas_owner.sprite_group_dict[self.group]
      self.canvas_owner.group_tree.remove(self.group)

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

  def get_colliding_groups(self):
    """
    Returns a list of colliding objects(by groups)
    """

    groups_colliding = []

    sprite_check_list = list(
      self.canvas_owner.sprite_position_dict.copy().keys())
    position_check_list = list(
      self.canvas_owner.sprite_position_dict.copy().values())

    sprite_check_list.remove(self)
    position_check_list.remove(self.position)

    for todo_sprite in sprite_check_list:

      POSITION_CHECK = self.canvas_owner.sprite_position_dict[
        todo_sprite]  # gets the position from key

      if self.position in position_check_list and not (set(
          self.canvas_owner.group_tree) == set(groups_colliding)):

        groups_colliding.append(
          todo_sprite.group) if POSITION_CHECK == self.position else None
      else:
        break

    return groups_colliding

  def update_distance(self):
    """

        update the dictionary : "sprite_position_dict" of "canvas_owner"
        like so :

        sprite_reference :  sprite_position

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
  """

    Object that can render a part of a canvas at a given position with a given size using " render() "

    """

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

    if size == [0, 0]:

      warn(
        f''' size of camera : "{name}" isn't defined so it will most likely not work.\n please define a valid size.'''
      )

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

    line = [self.canvas_owner.VOID for _ in range(SIZE_X)]

    clear_canvas = [line.copy() for _ in range(SIZE_Y)]
    return clear_canvas

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

  def render(self, is_string=True):
    """
    Returns the rendered canvas as a string if "is_string" is true else as a          2D-list
    """

    self.update_sprite_distance_dict()
    canvas = self.clear_canvas()

    MAX_DISTANCE = (self.get_square_distance_to([0, 0]))

    distances = list(self.sprite_distance_dict.copy().values())
    sprite_list = list(self.sprite_distance_dict.copy().keys())

    for todo in range(len(self.canvas_owner.sprite_tree)):

      min_distance = min(distances)
      # gets the smallest distance in list "distances"
      is_off_screen = (min_distance + self.get_square_distance_to(
        self.position)) > (MAX_DISTANCE +
                           self.get_square_distance_to(self.position))

      if is_off_screen:
        # if the smallest distance of the sprite(+ camera offset)
        # is bigger than "MAX_DISTANCE"
        break

      #get corresponding sprite reference
      index = distances.index(min_distance)
      sprite = sprite_list[index]
      position_to_render_sprite = [
        sprite.position[0] - self.position[0],
        sprite.position[1] - self.position[1]
      ]

      #edit canvas
      self.edit_element(canvas, position_to_render_sprite[0],
                        position_to_render_sprite[1], sprite.char)

      # remove thoses
      del sprite_list[index]
      del distances[index]

    if is_string == True:

      canvas = ["".join(canvas[line]) for line in range(len(canvas))]

      for element in range(len(canvas) - 1):

        canvas[0] += "\n" + canvas[element + 1]
      canvas = canvas[0]

    return canvas

  def is_renderable(self, distance):
    """
        returns whether a sprite a renderable from the distance given.
        """

    MAX_DISTANCE = (self.get_square_distance_to([0, 0]))

    return not (distance + self.get_square_distance_to(self.position)) > (
      MAX_DISTANCE + self.get_square_distance_to(self.position))


def critic_test(size, amount, time_mid, is_print=True):

  canvas = Canvas("0")
  camera = Camera(canvas, [size, size], [0, 0], "camera")

  for i in range(amount):
    s1 = Sprite(canvas, "0", [i, 0], "s1")
    s2 = Sprite(canvas, "1", [0, -i], "s2")

  fps = 0
  start = time.monotonic_ns()

  mid_fps = []
  mid_collision_time = []

  start_perf_counter = time.monotonic_ns()

  while ((time.monotonic_ns() - start_perf_counter) / 100000000) < time_mid:

    if ((time.monotonic_ns() - start) / 100000000) > 1.0:
      start = time.monotonic_ns()
      mid_fps.append(fps)
      fps = 0

    collision_start = time.monotonic_ns()
    s1.get_colliding_objects()
    mid_collision_time.append((time.monotonic_ns() - collision_start))
    camera.render(False)
    fps += 1

  if is_print:

    mid_fps = sum(mid_fps) / len(mid_fps)
    mid_collision_time = sum(mid_collision_time) / len(mid_collision_time)
    print(f"{mid_fps} FPS")
    print(f"collision time {mid_collision_time / 100000000}")


