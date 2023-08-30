class Sprite:
    """
    Object that can be used to fill the canvas
    """

    __slots__ = "canvas_owner", "char", "position", "name", "groups", "layer"

    def __init__(
            self,
            canvas_owner,
            char: str,
            position: dict,
            name: str,
            layer=0,
            groups=[],

    ):      
      self.register_info(canvas_owner, char, position, name, groups, layer)
      

    def register_info(self, canvas_owner, char: str, position: dict, name: str, groups : list, layer: int):
        # Character that represents the sprite when rendered.
        self.char = char
        # dict that has two element "x" and "y" it tells where to render the sprite.
        self.position = position
        # Name of the sprite that can be used to get reference from it using the "get_sprite"
        # method throught a "Canvas" object.
        self.name = name
        # Canvas that the sprite is associated to.
        self.canvas_owner = canvas_owner
        # groups is a list of string that be used to call a method on each sprite that has the same method.
        # or to check collision with certain groups
        self.groups = groups
        # defines which sprites at same position gets rendered
        self.layer = layer

        if name in canvas_owner.sprite_names:
            # change name if already taken
            self.name = name + f"@{str(id(self))}"

        # register infos in "canvas_owner" :
        canvas_owner.sprite_tree.add(self)
        canvas_owner.sprite_names.add(self.name)
        canvas_owner.sprite_names_dict[self.name] = self
        canvas_owner.sprite_position_dict[self] = position
      
        for group in groups:
          if not (group in canvas_owner.sprite_group_dict):
              # if group is new then add to "group_tree" and create new key
              # location for "sprite_group_dict".
              canvas_owner.sprite_group_dict[group] = set()
              canvas_owner.group_tree.add(group)
          canvas_owner.sprite_group_dict[group].add(self)
          
        self.define_cameras_render_cache()
        position_tuple = (self.position["x"], self.position["y"])

        # creates the key "position_tuple" if doesn't exist and add self to it
        self.canvas_owner.position_dict.setdefault(position_tuple, set()).add(self)

    def update_position(self, new_position):
      
        old_position_tuple = (self.position["x"], self.position["y"])
        # remove the self from "position_dict" with "old_position_tuple" as key
        self.canvas_owner.position_dict[old_position_tuple].remove(self)
        if self.canvas_owner.position_dict[old_position_tuple] == set():
            del self.canvas_owner.position_dict[old_position_tuple]

        new_position_tuple = (new_position["x"], new_position["y"])
        self.canvas_owner.position_dict.setdefault(new_position_tuple, set()).add(self)

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

    def update_camera_render_cache(self, camera):

        render_position = camera.get_render_position(self.position)

        if camera.is_renderable(self.position):

            # remove sprite reference
            # to update reference
            # only if was rendered before
            if not camera.last_sprite_cache_dict.get(self) is None:

                sprite_path = camera.last_sprite_cache_dict[self]

                sprite_row_list = camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]
                sprite_row_list.remove(self)
                # check if list is empty
                if sprite_row_list == []:
                    # if no sprite is rendered at this position in this line remove
                    # the position of the line from "row_render_dict"
                    del camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]

                    # if no sprite is rendered at this line remove the line entirely
                    if camera.row_render_dict[sprite_path["y"]] == {}:
                        del camera.row_render_dict[sprite_path["y"]]

            if camera.row_render_dict.get(render_position["y"]) is None:
                camera.row_render_dict[render_position["y"]] = {}

            if camera.row_render_dict[render_position["y"]].get(render_position["x"]) is None:
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
            # check if empty
            if camera.row_render_dict[row][x] == []:
                # if nothing to render on line remove x list
                del camera.row_render_dict[row][x]

                if camera.row_render_dict[row] == {}:
                    # if nothing to render on this row remove row
                    del camera.row_render_dict[row]

    def kill(self):
        """
        method used to remove an object from existence.
        """
        del self.canvas_owner.sprite_names_dict[self.name]
        del self.canvas_owner.sprite_position_dict[self]

        position_tuple = (self.position["x"], self.position["y"]) 
        self.canvas_owner.position_dict[position_tuple].remove(self)
        # if no sprite at this position remove key 
        if self.canvas_owner.position_dict[position_tuple] == set():
          del self.canvas_owner.position_dict[position_tuple]
        
        # remove self from key that contain every sprite in group
        for group in self.groups:
          self.canvas_owner.sprite_group_dict[group].remove(self)
          

        self.canvas_owner.sprite_names.remove(self.name)
        self.canvas_owner.sprite_tree.remove(self)

        for group in self.groups:
          if self.canvas_owner.sprite_group_dict[group] == set():
              # delete group if no one is in it.
              del self.canvas_owner.sprite_group_dict[group]
              self.canvas_owner.group_tree.remove(group)

        # delete render cache in all cameras that are linked
        for todo_camera in self.canvas_owner.camera_tree:

            if self in todo_camera.last_sprite_cache_dict:

                if not todo_camera.last_sprite_cache_dict[self] is None:
                    sprite_path = todo_camera.last_sprite_cache_dict[self]
                    sprite_row_list = todo_camera.row_render_dict[sprite_path["y"]][sprite_path["x"]]
                    sprite_row_list.remove(self)
                    # check if list is empty
                    if sprite_row_list == []:
                        # if no sprite is rendered at this position in this line
                        # remove the position of the line from "row_render_dict"
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

        index_place = self.canvas_owner.sprite_names.index(self.name)
        self.canvas_owner.sprite_names[index_place] = new_name
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

        # remove self from set  
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
        # make it as a tuple
        at_pos = (at_pos["x"], at_pos["y"])

        # no groups
        if self.canvas_owner.position_dict.get(at_pos) is None:
          return set()
      
        for object in self.canvas_owner.position_dict[at_pos]:
            # skip self
            if object == self:
              continue
          
            for group_object in object.groups:
              groups.add(group_object)
            # if all existing groups are added break
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
