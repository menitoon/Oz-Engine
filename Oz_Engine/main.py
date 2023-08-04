import io
import time


def warn(text: str):
    print(f"\033[93m!{text} \u001b[0m  ")


class Canvas:
    """
    Object that can store sprites in it to be rendered
    """

    __slots__ = "void", "sprite_names", "sprite_names_dict", "sprite_tree", "sprite_position_dict", "sprite_group_dict", "group_tree", "camera_name_dict", "camera_tree", "structure_tree", "structure_dict", \
        "position_dict"

    def __init__(self, void):
        ''' Characters that fills the canvas when nothing is rendered on a tile. '''
        self.void = void
        '''List that contains every reference of each sprite that is linked to the canvas in question '''
        self.sprite_tree = set()
        '''List that contains every groups that exists'''
        self.group_tree = set()
        '''List that contains every name of each sprite that is linked to the canvas in question '''
        self.sprite_names = set()
        '''Dictionary that has a name as a key and the corresponding Sprite reference as a value'''
        self.sprite_names_dict = {}
        '''Dictionary that has a sprite reference as a key and the corresponding position as a value'''
        self.sprite_position_dict = {}
        '''Dictionary that has a sprite reference as a key and the corresponding group as a value'''
        self.sprite_group_dict = {}
        '''List that contains every reference of every Camera that are linked to the canvas in question'''
        self.camera_tree = set()
        '''Dictionary that has a name as a key and the corresponding Camera reference as a value'''
        self.camera_name_dict = {}
        '''List that contains every reference of every Structure that are linked to the canvas in question '''
        self.structure_tree = set()
        '''Dictionary that has a name as a key and the corresponding Structure reference as a value'''
        self.structure_dict = {}
        '''Dictionary that has a position as a key and a list containing every sprite at the position'''
        self.position_dict = {}

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

    def get_structure(self, name):
        return self.structure_dict[name]


class Sprite:
    """
    Object that can be used to fill the canvas
    """

    __slots__ = "canvas_owner", "char", "position", "name", "group", "layer"

    def __init__(
            self,
            canvas_owner: object,
            char: str,
            position: dict,
            name: str,
            layer=0,
            group=None,

    ):
        self.register_info(canvas_owner, char, position, name, group, layer)

    def register_info(self, canvas_owner: object, char: str, position: dict, name: str, group, layer: int):

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
        '''defines which sprites at same position gets rendered'''
        self.layer = layer

        if name in canvas_owner.sprite_names:
            # change name if already taken
            self.name = name + f"@{str(id(self))}"

        # register infos in "canvas_owner" :
        canvas_owner.sprite_tree.add(self)
        canvas_owner.sprite_names.add(self.name)
        canvas_owner.sprite_names_dict[self.name] = self
        canvas_owner.sprite_position_dict[self] = position

        if not (group in canvas_owner.sprite_group_dict):
            # if group is new then add to "group_tree" and create new key
            # location for "sprite_group_dict".
            canvas_owner.sprite_group_dict[group] = []
            canvas_owner.group_tree.add(group)

        canvas_owner.sprite_group_dict[group].append(self)
        self.define_cameras_render_cache()

        position_tuple = (self.position["x"], self.position["y"])

        if self.canvas_owner.position_dict.get(position_tuple) is None:
            self.canvas_owner.position_dict[position_tuple] = set()
        self.canvas_owner.position_dict[position_tuple].add(self)

    def update_position(self, new_position):
        old_position_tuple = (self.position["x"], self.position["y"])
        self.canvas_owner.position_dict[old_position_tuple].remove(self)
        if self.canvas_owner.position_dict[old_position_tuple] == []:
            del self.canvas_owner.position_dict[old_position_tuple]

        new_position_tuple = (new_position["x"], new_position["y"])

        if self.canvas_owner.position_dict.get(new_position_tuple) is None:
            self.canvas_owner.position_dict[new_position_tuple] = set()
        self.canvas_owner.position_dict[new_position_tuple].add(self)

    def define_cameras_render_cache(self):

        for todo_camera in self.canvas_owner.camera_tree:
            # updates yourself to the render cache of camera

            render_position = todo_camera.get_render_position(self.position)

            if todo_camera.is_renderable(self.position):

                # if can be rendered
                # update key
                if todo_camera.row_render_dict.get(render_position["y"]) is None:
                    todo_camera.row_render_dict[render_position["y"]] = {}

                if todo_camera.row_render_dict[render_position["y"]].get(render_position["x"]) is None:
                    todo_camera.row_render_dict[render_position["y"]][render_position["x"]] = []

                    row = todo_camera.row_render_dict[render_position["y"]]
                    row[render_position["x"]].append(self)
                else:

                    todo_camera.append_sprite_at_order_layer(render_position, self)

                todo_camera.last_sprite_cache_dict[self] = {"y": render_position["y"], "x": render_position["x"]}

    def update_all_cameras_render_cache(self):

        for todo_camera in self.canvas_owner.camera_tree:
            self.update_camera_render_cache(todo_camera)

    def update_camera_render_cache(self, camera: object):

        render_position = camera.get_render_position(self.position)

        if camera.is_renderable(self.position):

            # remove sprite reference
            # to update reference
            # only if was rendered before
            if camera.last_sprite_cache_dict.get(self) != None:

                sprite_path = camera.last_sprite_cache_dict[self]

                sprite_row_list = camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]
                sprite_row_list.remove(self)

                if sprite_row_list == []:
                    # if no sprite is rendered at this position in this line remove the position of the line from "row_render_dict"
                    del camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]

                    # if no sprite is rendered at this line remove the line entirely
                    if camera.row_render_dict[sprite_path["y"]] == {}:
                        del camera.row_render_dict[sprite_path["y"]]

            if camera.row_render_dict.get(render_position["y"]) == None:
                camera.row_render_dict[render_position["y"]] = {}

            if camera.row_render_dict[render_position["y"]].get(render_position["x"]) == None:
                camera.row_render_dict[render_position["y"]][render_position["x"]] = []
                camera.row_render_dict[render_position["y"]][render_position["x"]].append(self)
            else:
                camera.append_sprite_at_order_layer(render_position, self)

            camera.last_sprite_cache_dict[self] = {"y": render_position["y"], "x": render_position["x"]}



        elif not camera.last_sprite_cache_dict.get(self) is None:

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

    def kill(self):

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

        # delete render cache in all cameras that are linked
        for todo_camera in self.canvas_owner.camera_tree:

            if self in todo_camera.last_sprite_cache_dict:

                if todo_camera.last_sprite_cache_dict[self] != {}:
                    sprite_path = todo_camera.last_sprite_cache_dict[self]
                    sprite_row_list = todo_camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]
                    sprite_row_list.remove(self)

                    if sprite_row_list == []:
                        # if no sprite is rendered at this position in this line remove the position of the line from "row_render_dict"
                        del todo_camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]

                        # if no sprite is rendered at this line remove the line entirely
                        if todo_camera.row_render_dict[sprite_path["y"]] == {}:
                            del todo_camera.row_render_dict[sprite_path["y"]]

                del todo_camera.last_sprite_cache_dict[self]

        del self

    def set_layer(self, new_layer: int):

        self.layer = new_layer

        for camera in self.canvas_owner.camera_tree:

            if camera.is_renderable(self.position):
                render_position = camera.get_render_position(self.position)
                camera.row_render_dict[render_position["y"]][render_position["x"]].remove(self)
                camera.append_sprite_at_order_layer(render_position, self)
                self.update_camera_render_cache(camera)

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

    def get_colliding_objects(self, at_pos=None):
        """
        Returns a list of colliding objects(by ref)
        """

        if at_pos is None:
            at_pos = self.position

        collision_set = self.canvas_owner.position_dict.get((at_pos["x"], at_pos["y"]))
        if collision_set is None:
            return set()
        else:
            collision_set = collision_set.copy()

        if at_pos is None:
            collision_set.remove(self)

        return collision_set

    def get_colliding_groups(self, at_pos=None):
        """
        Returns a list of colliding objects(by groups)
        """

        if at_pos is None:
            at_pos = self.position

        groups = set()
        colliding_objects = self.get_colliding_objects(at_pos)

        for c in colliding_objects:
            if not c.group is None:
                groups.add(c.group)

            if groups == self.canvas_owner.group_tree:
                break

        return groups

    def change_x(self, value: int):
        """
        adds "value" to the y-axis of "position"
        """
        self.update_position({"x": self.position["x"] + value, "y": self.position["y"]})
        self.position["x"] += value
        self.update_all_cameras_render_cache()

    def change_y(self, value: int):
        """
        adds "value" to the y-axis of "position"
        """
        self.update_position({"x": self.position["x"], "y": self.position["y"] + value})
        self.position["y"] += value
        self.update_all_cameras_render_cache()

    def set_x(self, value: int):
        """
        sets "value" to the x-axis of "position"
        """
        self.update_position({"x": value, "y": self.position["y"]})
        self.position["x"] = value
        self.update_all_cameras_render_cache()

    def set_y(self, value: int):
        """
        sets "value" to the y-axis of "position"
        """
        self.update_position({"x": self.position["x"], "y": value})
        self.position["y"] = value
        self.update_all_cameras_render_cache()

    def set_position(self, value: dict):


        print(value, "update set")

        self.update_position(value)
        self.position = value
        self.update_all_cameras_render_cache()

    def change_position(self, x_val: int = 0, y_val: int = 0):

        self.update_position({"x": self.position["x"] + x_val, "y": self.position["y"] + y_val})

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

        self.canvas_owner.camera_tree.add(self)
        self.canvas_owner.camera_name_dict[self.name] = self

        self.register_sprite_cache()

    def register_sprite_cache(self):

        for sprite in self.canvas_owner.sprite_tree:
            if self.is_renderable(sprite.position):

                render_postion = self.get_render_position(sprite.position)

                self.last_sprite_cache_dict[sprite] = render_postion

                if self.row_render_dict.get(render_postion["y"]) is None:
                    self.row_render_dict[render_postion["y"]] = {}
                if self.row_render_dict[render_postion["y"]].get(render_postion["x"]) is None:
                    self.row_render_dict[render_postion["y"]][render_postion["x"]] = []
                    self.row_render_dict[render_postion["y"]][render_postion["x"]].append(sprite)
                else:
                    # if there are other sprites append the sprite in correct order
                    self.append_sprite_at_order_layer(render_postion, sprite)

    def get_render_position(self, sprite_position):

        return {"x": sprite_position["x"] + self.position["x"], "y": sprite_position["y"] + self.position["y"]}

    def is_renderable(self, position):

        render_position = self.get_render_position(position)

        return render_position["x"] >= 0 and render_position["x"] < self.size["x"] and render_position[
            "y"] >= 0 and render_position["y"] < self.size["y"]

    def append_sprite_at_order_layer(self, position: dict, sprite: object):
        index = 0

        render_list = self.row_render_dict[position["y"]][position["x"]]

        for rl in render_list:

            if sprite.layer > rl.layer:
                self.row_render_dict[position["y"]][position["x"]].insert(index, sprite)
                return
            index += 1

        # if None of Sprites had smaller layer insert it at last position
        render_list.append(sprite)

    def render(self, is_string=True):
        """
        Returns the rendered canvas as a string if "is_string" is true else as a 2D-list
        """

        line = self.canvas_owner.void * self.size["x"] + "\n"
        rows = list(self.row_render_dict.keys())
        rows.sort()

        canvas = ""

        number_of_row_to_render = len(self.row_render_dict)
        last_row = 0

        if len(rows) == 0:
            # nothing to render
            canvas = line * self.size["y"]
            return canvas
        else:
            last_row = rows[0]

        canvas += line * (rows[0])  # adds line before the first one

        for todo_row in rows:

            number_to_fill_up = todo_row - 1 - last_row

            if number_to_fill_up > 0:
                canvas += line * number_to_fill_up
            del number_to_fill_up
            last_row = todo_row

            x_to_render_line = list(self.row_render_dict[todo_row].keys())
            x_to_render_line.sort()
            render_line = ""
            sprites_to_render = len(x_to_render_line)
            items_rendered = 0  # also includes void

            # todo_line is the character position that gets rendered

            for todo_line in x_to_render_line:

                # fill up with "void" until something to render
                number_to_fill_up = (todo_line - items_rendered)
                if number_to_fill_up > 0:
                    # if there is something that can be filled up
                    render_line += self.canvas_owner.void * number_to_fill_up
                    items_rendered += number_to_fill_up

                del number_to_fill_up

                row_dict = self.row_render_dict[todo_row]
                render_line += row_dict[todo_line][0].char
                items_rendered += 1
                sprites_to_render -= 1

                if sprites_to_render == 0:
                    # if nothing else to render on this line we fill up the line with "void"
                    number_to_fill_up = self.size["x"] - (todo_line + 1)
                    render_line += self.canvas_owner.void * number_to_fill_up + "\n"
                    items_rendered += number_to_fill_up
                    canvas += render_line
                    del number_to_fill_up
                    break

            number_of_row_to_render -= 1
            if number_of_row_to_render <= 0:
                # prob not here
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

    def set_size(self, new_size: dict):
        self.size = new_size
        self.update_all_sprite_render_cache()

    def set_x_size(self, value: int):
        self.size["x"] = value
        self.update_all_sprite_render_cache()

    def set_y_size(self, value: int):
        self.size["y"] = value
        self.update_all_sprite_render_cache()

    def change_x_size(self, value: int):
        self.size["x"] += value
        self.update_all_sprite_render_cache()

    def change_y_size(self, value: int):
        self.size["y"] += value
        self.update_all_sprite_render_cache()

    def change_size(self, x: int, y: int):
        self.size["x"] += x
        self.size["y"] += y
        self.update_all_sprite_render_cache()

    def kill(self):
        self.canvas_owner.camera_tree.remove(self)
        del self.canvas_owner.camera_name_dict[self.name]
        del self


class Structure(Sprite):
    __slots__ = "canvas_owner", "structure", "position", "name", "group", "is_space_empty", "structure_sprite_tree"

    def __init__(self, canvas_owner: object, structure: io.TextIOWrapper, position, name, group=None,
                 is_space_empty=True):

        self.canvas_owner = canvas_owner
        self.position = position
        self.group = group
        self.is_space_empty = is_space_empty
        self.name = name

        self.structure = structure
        self.structure_sprite_tree = []
        self.is_space_empty = is_space_empty

        if name in canvas_owner.structure_tree:
            self.name = f"@{name}{str(id(self))}"

        canvas_owner.structure_tree.add(self.name)
        canvas_owner.structure_dict[self.name] = self

        todo = 0
        lines = structure.readlines()

        for y in range(len(lines)):

            line_length = len(lines[todo])
            todo += 1
            for x in range(line_length):
                char = lines[y][x]

                if char != "\n":

                    if not (is_space_empty == True and char == " "):
                        structure_sprite = StructureSprite(canvas_owner, char, {"x": x, "y": y}, "struc", self)

    def update_all_sprite_child(self):
        for todo_child_sprite in self.structure_sprite_tree:
            todo_child_sprite.update_all_cameras_render_cache()

    def set_x(self, value: int):
        self.position["x"] = value
        self.update_all_sprite_child()

    def change_x(self, value: int):
        self.position["x"] += value
        self.update_all_sprite_child()

    def set_y(self, value: int):
        self.position["y"] = value
        self.update_all_sprite_child()

    def change_y(self, value: int):
        self.position["y"] += value
        self.update_all_sprite_child()

    def set_position(self, value: dict):
        self.position = value
        self.update_all_cameras_render_cache()

    def change_position(self, x_val: int = 0, y_val: int = 0):
        self.position["x"] += x_val
        self.position["y"] += y_val
        self.update_all_cameras_render_cache()

    def kill(self):

        for todo_child_sprite in self.structure_sprite_tree:
            todo_child_sprite.kill()

        del self


class StructureSprite(Sprite):
    __slots__ = "canvas_owner", "char", "position", "name", "group", "structure_owner"

    def __init__(
            self,
            canvas_owner: object,
            char: str,
            position: dict,
            name: str,
            structure_owner: object,
            group=None

    ):
        self.structure_owner = structure_owner
        self.register_info(canvas_owner, char, position, name, group)
        self.structure_owner.structure_sprite_tree.add(self)

    def get_render_position(self, camera):
        return {
          "x": self.position["x"] + camera.position["x"] + self.structure_owner.position["x"],
          "y": self.position["y"] + camera.position["y"] + self.structure_owner.position["y"]
        }


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

    while ((time.monotonic_ns() - start_perf_counter) / 1000000000) < time_mid:

        if ((time.monotonic_ns() - start) / 100000000) > 1.0:
            start = time.monotonic_ns()
            mid_fps.append(fps)
            fps = 0

        collision_start = time.monotonic_ns()
        s1.get_colliding_objects()
        mid_collision_time.append((time.monotonic_ns() - collision_start))
        camera.change_x(1)
        camera.render()
        fps += 1

    if is_print:
        mid_fps = sum(mid_fps) / len(mid_fps)
        mid_collision_time = sum(mid_collision_time) / len(mid_collision_time)
        print(f"{mid_fps} FPS")
        print(f"collision time {mid_collision_time / 100000000}")


