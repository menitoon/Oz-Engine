import math
import time


def warn(text: str):
    print(f"\033[93m!{text} \u001b[0m  ")


class Canvas:
    """
  Object that can store sprites in it to be rendered
  """

    __slots__ = "void", "sprite_names", "sprite_names_dict", "sprite_tree",  "sprite_position_dict", "sprite_group_dict", "group_tree", "camera_name_dict", "camera_tree"

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

    __slots__ = "canvas_owner", "char", "position", "name", "group", 


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

        self.update_all_position_to_render_cache()

    def add_position_to_render_cache(self , camera):
        # update for every camera if is in render cache

        if camera.is_renderable(self.position):

            render_position = {"x": self.position["x"] - camera.position["x"],
                               "y": self.position["y"] - camera.position["y"]}
            # if can be rendered
            # update key
            camera.valid_sprite_cache[self] = render_position

            # create a list placement if row not existing
            if camera.row_render.get(render_position["y"]) == None:
                camera.row_render[render_position["y"]] = [[], []]

            camera.row_render[render_position["y"]][0].append(render_position["x"])
            camera.row_render[render_position["y"]][1].append(self)


    def update_all_position_to_render_cache(self):

        for todo_camera in self.canvas_owner.camera_tree:
            self.add_position_to_render_cache(todo_camera)


    def remove_position_to_render_cache(self , camera):

        index = camera.row_render[self.position["y"]][1].index(self) #gets the index of your sprite reference
        del camera.row_render[self.position["y"]][0][index]
        del camera.row_render[self.position["y"]][1][index]

    def remove_all_position_to_render_cache(self):
        for todo_camera in self.canvas_owner.camera_tree:
            self.remove_position_to_render_cache(todo_camera)

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

        self.remove_all_position_to_render_cache()

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

        self.remove_position_to_render_cache()
        self.position["x"] += value
        self.update_position_to_render_cache()

    def change_y(self, value: int):
        """
        adds "value" to the y-axis of "position"
        """

        self.remove_position_to_render_cache()
        self.position["y"] += value
        self.update_position_to_render_cache()

    def set_x(self, value: int):
        """
        sets "value" to the x-axis of "position"
        """
        self.remove_position_to_render_cache()
        self.position["x"] = value
        self.update_position_to_render_cache()

    def set_y(self, value: int):
        """
        sets "value" to the y-axis of "position"
        """
        self.remove_position_to_render_cache()
        self.position["y"] = value
        self.update_position_to_render_cache()

    def set_position(self, value: dict):

        self.remove_position_to_render_cache()
        self.position = value
        self.update_position_to_render_cache()

    def change_position(self, x_val: int = 0, y_val: int = 0):

        self.remove_position_to_render_cache()
        self.position["x"] += x_val
        self.position["y"] += y_val
        self.update_position_to_render_cache()

        


class Camera:
    """
    Object that can render a part of a canvas at a given position with a given size using " render() "
    """

    __slots__ = "canvas_owner", "size", "position", "name", "valid_sprite_cache" , "row_render"

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

        '''sprites that can be rendered'''
        self.valid_sprite_cache = {}
        '''Dictionary that contain "y" as a key and a list filled with Dictionaries that are like this : "x" as a key and a sprite reference as a value
        so :  {"y" : {"x" : sprite_reference_here} '''
        self.row_render = {}

        if size == [0, 0]:
            warn(
                f''' size of camera : "{name}" isn't defined so it will most likely not work.\n please define a valid size.'''
            )

        self.canvas_owner.camera_tree.append(self)
        self.canvas_owner.camera_name_dict[self.name] = self



    def is_renderable(self , position):


      return position["x"] >= 0 and position["x"] <= self.size["x"] and position["y"] >= 0 and position["y"] <= self.size["y"]


    def render(self, is_string=True):
        """
        Returns the rendered canvas as a string if "is_string" is true else as a 2D-list
        """

        line = self.canvas_owner.void * self.size["x"] + "\n"
        rows = list(self.row_render.keys())
        canvas = ""

        number_of_row_to_render = len(self.row_render)

        for todo_size_y in range(self.size["y"]):


           if todo_size_y in rows:

              #if line has something to render

              x_to_render = self.row_render[todo_size_y][0].copy()
              sprite_to_render = self.row_render[todo_size_y][1].copy()
              line_render = ""

              for todo_size_x in range(self.size["x"]):



                if todo_size_x in x_to_render:

                    index = x_to_render.index(todo_size_x)

                    line_render += sprite_to_render[index].char
                    del x_to_render[index]
                    del sprite_to_render[index]



                    if len(x_to_render) == 0:
                        #nothing else to render on this line so can fill line with "void"
                        line_render += self.canvas_owner.void * (self.size["x"] - todo_size_x)
                        break

                else:
                    line_render += self.canvas_owner.void

              canvas += line_render + "\n"
              number_of_row_to_render -= 1
              if number_of_row_to_render == 0:
                  canvas += line * (self.size["y"] - todo_size_y)
                  break
           else:

              canvas += line



        return canvas


    def update_all_sprite_render_cache(self):
        for todo_sprite in self.canvas_owner.sprite_tree:
            todo_sprite.remove_position_to_render_cache(self)
            todo_sprite.add_position_to_render_cache(self)

    def set_position(self , position : dict):
        self.position["x"] = -position["x"]
        self.position["y"] = -position["y"]
        self.update_all_sprite_render_cache()


    def set_x(self , value : int):
        self.position["x"] = -value
        self.update_all_sprite_render_cache()

    def set_y(self , value : int):
        self.position["y"] = -value
        self.update_all_sprite_render_cache()

    def change_y(self , value : int):
        self.position["y"] += -value
        self.update_all_sprite_render_cache()

    def change_x(self , value : int):
        self.position["x"] += -value
        self.update_all_sprite_render_cache()

    def change_position(self , position : dict):
        self.position["x"] += -position["x"]
        self.position["y"] += -position["y"]
        self.update_all_sprite_render_cache()

    def set_size(self, size : dict):
        self.size = size
        self.update_all_sprite_render_cache()

    def destroy(self):

        self.canvas_owner.camera_tree.remove(self)
        del self.canvas_owner.camera_name_dict[self.name]
        del self






def critic_test(size, amount, time_mid, is_print=True):

  canvas = Canvas("0")
  camera = Camera(canvas, {"x":size, "y":size}, {"x" : 0, "y" : 0}, "camera")

  for i in range(amount):
    s1 = Sprite(canvas, "0", {"x":i,"y": 0}, "s1")
    s2 = Sprite(canvas, "1", {"x":0,"y": -i}, "s2")

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

canvas = Canvas("0")
camera = Camera(canvas , {"x" : 5 , "y" : 5}, {"x":0 , "y":0}, "cam")

s1 = Sprite(canvas , "s" , {"x" : 0 , "y":1}, "s1")

print(camera.render())

camera.set_size({"x" : 2 , "y" : 2})

print(camera.render())
