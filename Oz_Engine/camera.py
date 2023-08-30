class Camera:
    """
    Object that can render a part of a canvas at a given position with a given size using " render() "
    """

    __slots__ = "canvas_owner", "size", "position", "name", "last_sprite_cache_dict", "row_render_dict",

    def __init__(self, canvas_owner, size: dict, position: dict,
                 name: str):
        # canvas that is associated with.
        self.canvas_owner = canvas_owner
        # size of the camera
        self.size = size
        # position of the camera
        self.position = position
        # name of the camera
        self.name = name
        # last cache of every sprite
        self.last_sprite_cache_dict = {}
        # Dictionary that contain "y" as a key and a list filled with Dictionaries
        # that are like this : "x" as a key and a sprite reference as a value
        # so :  {"y" : {"x" : sprite_reference_here}
        self.row_render_dict = {}
        self.canvas_owner.camera_tree.add(self)
        self.canvas_owner.camera_name_dict[self.name] = self

        self.register_sprite_cache()

    def register_sprite_cache(self):
        """
        used to get the render cache of all sprites
        related to the canvas.
        It is used in __init__
        """

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
        """
        Returns the render position of a position.
        """
        return {"x": sprite_position["x"] + self.position["x"], "y": sprite_position["y"] + self.position["y"]}

    def is_renderable(self, position):

        render_position = self.get_render_position(position)

        return render_position["x"] >= 0 and render_position["x"] < self.size["x"] and render_position[
            "y"] >= 0 and render_position["y"] < self.size["y"]

    def append_sprite_at_order_layer(self, position: dict, sprite):
        index = 0

        render_list = self.row_render_dict[position["y"]][position["x"]]

        for rl in render_list:

            if sprite.layer > rl.layer:
                self.row_render_dict[position["y"]][position["x"]].insert(index, sprite)
                return
            index += 1

        # if None of Sprites had smaller layer insert it at last position
        render_list.append(sprite)

    def render(self):
        """
        Returns the rendered canvas as a string if "is_string" is true else as a 2D-list
        """

        line = self.canvas_owner.void * self.size["x"] + "\n"
        rows = list(self.row_render_dict.keys())

        rows.sort()
        canvas = ""
        number_of_row_to_render = len(self.row_render_dict)

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
                    render_line += (self.canvas_owner.void * number_to_fill_up) + "\n"
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
