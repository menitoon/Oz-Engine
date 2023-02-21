import math
import time


def warn(text: str):
  print(f"\033[93m!{text} \u001b[0m  ")


class Canvas:
  """
  Object that can store sprites in it to be rendered
  """

  __slots__ = "void", "sprite_names", "sprite_names_dict", "sprite_tree", "sprite_position_dict", "sprite_group_dict", "group_tree", "camera_name_dict", "camera_tree"

  def __init__(self, void):
    ''' Characters that fills the canvas when nothing is rendered on a tile. '''
    self.void = void
    '''List that contains every reference of each sprite that is linked to the canvas in question '''
    self.sprite_tree = []
    '''List that contains every groups that exists'''
    self.group_tree = []
    '''List that contains every name of each sprite that is linked to the canvas in question '''
    self.sprite_names = []
    '''Dictionary that has a name as a key and the corresponding Sprite reference as a value'''
    self.sprite_names_dict = {}
    '''Dictionary that has a sprite reference as a key and the corresponding position as a value'''
    self.sprite_position_dict = {}
    '''Dictionary that has a sprite reference as a key and the corresponding group as a value'''
    self.sprite_group_dict = {}
    '''List that contains every reference of every Camera link to the canvas in question'''
    self.camera_tree = []
    '''Dictionary that has a name as a key and the corresponding Camera reference as a value'''
    self.camera_name_dict = {}

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

    # gets every sprite that is in the group given

    sprite_to_call = self.sprite_group_dict.get(group_to_call)
    if sprite_to_call == None:
      # if group given doesn't exist then sumbit error
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

  __slots__ = "canvas_owner", "char", "position", "name", "group"

  def __init__(
    self,
    canvas_owner: object,
    char: str,
    position: dict,
    name: str,
    group=None,
  ):
    '''Character that represents the sprite when rendered.'''
    self.char = char
    '''dict that has two element "x" and "y" it tells where to render the sprite.'''
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
      # if group is new then add to "group_tree" and create new key
      # location for "sprite_group_dict".
      canvas_owner.sprite_group_dict[group] = []
      canvas_owner.group_tree.append(group)

    canvas_owner.sprite_group_dict[group].append(self)
    self.define_cameras_render_cache()
    
  def define_cameras_render_cache(self):

    for todo_camera in self.canvas_owner.camera_tree:
      #updates yourself to the render cache of camera


      render_position = {
        "x": self.position["x"] - todo_camera.position["x"],
        "y": self.position["y"] - todo_camera.position["y"]
      }



      if todo_camera.is_renderable(render_position):



        # if can be rendered
        # update key
        if todo_camera.row_render_dict.get(render_position["y"]) == None:
          todo_camera.row_render_dict[render_position["y"]] = {}

        if todo_camera.row_render_dict[render_position["y"]].get(render_position["x"]) == None:
          todo_camera.row_render_dict[render_position["y"]][render_position["x"]] = []

        row = todo_camera.row_render_dict[render_position["y"]]
        row[render_position["x"]].append(self)
        todo_camera.last_sprite_cache_dict[self] = {"y" :render_position["y"], "x" : render_position["x"]}

  
  def update_all_cameras_render_cache(self):
    
    for todo_camera in self.canvas_owner.camera_tree:
      self.update_camera_render_cache(todo_camera)

     

  def update_camera_render_cache(self , camera : object):

    if camera.is_renderable(self.position):

      # remove sprite reference
      # to update reference
      # only if was rendered before
      if camera.last_sprite_cache_dict.get(self) != None:

        # print(todo_camera.row_render_dict)
        sprite_path = camera.last_sprite_cache_dict[self]

        # print(sprite_path, self.name)

        sprite_row_list = camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]
        sprite_row_list.remove(self)



        if sprite_row_list == []:
          # if no sprite is rendered at this position in this line remove the position of the line from "row_render_dict"
          del camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]

          # if no sprite is rendered at this line remove the line entirely
          if camera.row_render_dict[sprite_path["y"]] == {}:
            del camera.row_render_dict[sprite_path["y"]]

      render_position = {"x": self.position["x"] - camera.position["x"],
                         "y": self.position["y"] - camera.position["y"]}

      if camera.row_render_dict.get(render_position["y"]) == None:
        camera.row_render_dict[render_position["y"]] = {}

      if camera.row_render_dict[render_position["y"]].get(render_position["x"]) == None:
        camera.row_render_dict[render_position["y"]][render_position["x"]] = []

      camera.row_render_dict[render_position["y"]][render_position["x"]].append(self)
      camera.last_sprite_cache_dict[self] = {"y": render_position["y"], "x": render_position["x"]}



    elif camera.last_sprite_cache_dict.get(self) != None:

      # if was rendered before and cannot be rendered remove it from row render dict
      row = camera.last_sprite_cache_dict[self]["y"]
      x = camera.last_sprite_cache_dict[self]["x"]

      camera.last_sprite_cache_dict[self] = None

      camera.row_render_dict[row][x].remove(self)
      if camera.row_render_dict[row][x] == []:
        # if nothing to render on line remove x list
        del camera.row_render_dict[row][x]



        if camera.row_render_dict[row] == {}:
          # if nothing to render on this row remove row
          del camera.row_render_dict[row]



  def destroy(self):

    del self.canvas_owner.sprite_names_dict[self.name]
    del self.canvas_owner.sprite_position_dict[self]

    # remove self from key that contain every sprite in group
    INDEX = self.canvas_owner.sprite_group_dict[self.group].index(self)
    del (self.canvas_owner.sprite_group_dict[self.group])[INDEX]

    self.canvas_owner.sprite_names.remove(self.name)
    self.canvas_owner.sprite_tree.remove(self)

    if len(self.canvas_owner.sprite_group_dict[self.group]) == 0:
      # delete group if no one is in it.
      del self.canvas_owner.sprite_group_dict[self.group]
      self.canvas_owner.group_tree.remove(self.group)


    #delete render cache in all cameras that are linked
    for todo_camera in self.canvas_owner.camera_tree:


      pass
      #del todo_camera.row_render_dict


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

  def change_x(self, value: int):
    """
    adds "value" to the y-axis of "position"
    """

    self.position["x"] += value
    update_all_cameras_render_cache()

  def change_y(self, value: int):
    """
    adds "value" to the y-axis of "position"
    """

    self.position["y"] += value
    update_all_cameras_render_cache()

  def set_x(self, value: int):
    """
    sets "value" to the x-axis of "position"
    """

    self.position["x"] = value
    self.update_all_cameras_render_cache()

  def set_y(self, value: int):
    """
    sets "value" to the y-axis of "position"
    """
    self.position["y"] = value
    self.update_all_cameras_render_cache()

  def set_position(self, value: dict):

    self.position = value
    self.update_all_cameras_render_cache()


  def change_position(self, x_val: int = 0, y_val: int = 0):

    self.position["x"] += x_val
    self.position["y"] += y_val
    self.update_all_cameras_render_cache()


class Camera:
  """
  Object that can render a part of a canvas at a given position with a given size using " render() "
  """

  __slots__ = "canvas_owner", "size", "position", "name", "last_sprite_cache_dict", "row_render_dict",

  def __init__(self, canvas_owner: object, size: dict, position: dict,
               name: str):
    '''canvas that is associated with. '''
    self.canvas_owner = canvas_owner
    '''size of the camera '''
    self.size = size
    ''' position of the camera '''
    self.position = position
    ''' name of the camera'''
    self.name = name
    '''last cache of every sprite'''
    self.last_sprite_cache_dict = {}
    '''Dictionary that contain "y" as a key and a list filled with Dictionaries that are like this : "x" as a key and a sprite reference as a value
        so :  {"y" : {"x" : sprite_reference_here} '''
    self.row_render_dict = {}


    if size == [0, 0]:
      warn(
        f''' size of camera : "{name}" isn't defined so it will most likely not work.\n please define a valid size.'''
      )

    self.canvas_owner.camera_tree.append(self)
    self.canvas_owner.camera_name_dict[self.name] = self

  def is_renderable(self, position):

    render_position = {"x" : position["x"] - self.position["x"],"y" : position["y"] - self.position["y"]}
    # sprite_position - camera_position

    return render_position["x"] >= 0 and render_position["x"] < self.size["x"] and render_position[
      "y"] >= 0 and render_position["y"] < self.size["y"]

  def render(self, is_string=True):
    """
    Returns the rendered canvas as a string if "is_string" is true else as a 2D-list
    """

    line = self.canvas_owner.void * self.size["x"] + "\n"
    rows = list(self.row_render_dict.keys())
    canvas = ""

    number_of_row_to_render = len(self.row_render_dict)


    if len(rows) == 0:
       #nothing to render
       canvas = line * self.size["y"]
       return canvas


    for todo_row in rows:


      number_to_fill_up = todo_row - (abs(len(self.row_render_dict) - number_of_row_to_render))

      canvas += line * number_to_fill_up
      del number_to_fill_up

      x_to_render_line = list(self.row_render_dict[todo_row].keys())
      x_to_render_line.sort()
      render_line = ""
      sprites_to_render = len(x_to_render_line)

      for todo_line in x_to_render_line:

        #fill up with "void" until something to render
        number_to_fill_up = abs((len(render_line) - todo_line))
        if number_to_fill_up > 0:
          #if there is something that can be filled up
          render_line += self.canvas_owner.void * number_to_fill_up

        del number_to_fill_up

        row_dict = self.row_render_dict[todo_row]
        render_line += row_dict[todo_line][0].char
        sprites_to_render -= 1

        if sprites_to_render == 0:
          #if nothing else to render on this line we fill up the line with "void"
          number_to_fill_up = (self.size["x"] - len(render_line))
          render_line += self.canvas_owner.void * number_to_fill_up + "\n"
          canvas += render_line
          del number_to_fill_up
          break


      number_of_row_to_render -= 1
      if number_of_row_to_render <= 0:

        number_to_fill_up = self.size["y"] - todo_row - 1
        canvas += line * number_to_fill_up
        break


    return canvas

  def update_all_sprite_render_cache(self):
    for todo_sprite in self.canvas_owner.sprite_tree:
      todo_sprite.update_camera_render_cache(self)

  def set_position(self, position: dict):
    self.position["x"] = -position["x"]
    self.position["y"] = -position["y"]
    self.update_all_sprite_render_cache()

  def set_x(self, value: int):
    self.position["x"] = -value
    self.update_all_sprite_render_cache()

  def set_y(self, value: int):
    self.position["y"] = -value
    self.update_all_sprite_render_cache()

  def change_y(self, value: int):
    self.position["y"] += -value
    self.update_all_sprite_render_cache()

  def change_x(self, value: int):
    self.position["x"] += -value
    self.update_all_sprite_render_cache()

  def change_position(self, position: dict):
    self.position["x"] += -position["x"]
    self.position["y"] += -position["y"]
    self.update_all_sprite_render_cache()

  def set_size(self, size: dict):
    self.size = size
    self.update_all_sprite_render_cache()

  def destroy(self):

    self.canvas_owner.camera_tree.remove(self)
    del self.canvas_owner.camera_name_dict[self.name]
    del self


def critic_test(size, amount, time_mid, is_print=True):

  canvas = Canvas("0")
  camera = Camera(canvas, {"x": size, "y": size}, {"x": 0, "y": 0}, "camera")

  for i in range(amount):
    s1 = Sprite(canvas, "0", {"x": i, "y": 0}, "s1")
    s2 = Sprite(canvas, "1", {"x": 0, "y": -i}, "s2")

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
    #s1.get_colliding_objects()
    mid_collision_time.append((time.monotonic_ns() - collision_start))
    camera.change_x(1)
    camera.render()
    fps += 1

  if is_print:

    mid_fps = sum(mid_fps) / len(mid_fps)
    mid_collision_time = sum(mid_collision_time) / len(mid_collision_time)
    print(f"{mid_fps} FPS")
    print(f"collision time {mid_collision_time / 100000000}")



critic_test(100 , 100 , 10)