import math


def deep_copy(L): #Credit to Lacobus for this function
    
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
    __slots__ = "VOID", "SIZE", "SIZE_X", "SIZE_Y", "canvas", "camera_pos", "CORNER_TOP_LEFT", "CORNER_TOP_RIGHT", "CORNER_BOTTOM_RIGHT", "CORNER_BOTTOM_LEFT", "MAX_DISTANCE", "distances", "sprite_names", "sprite_names_dict", "sprite_tree", "sprite_priority"

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
                "!Canvas size is not defined and will most likely not work.")  # warn
            print("\u001b[0m")

        x_line = []

        for todo in range(SIZE_Y):
            x_line.append(str(VOID))

        for subtodo in range(SIZE_X):
            self.canvas.append(x_line.copy())

    def edit_element(self, canvas, x, y, char):
  
        (canvas[y])[x] = char
        
        
      


    def get_square_distance_to(self, position: list):

        # sum of the distance between the 4 corners of the square divided by 4 ( corner_sum / 4 )

        return (self.get_distance_between(self.CORNER_TOP_LEFT, position) +
                self.get_distance_between(self.CORNER_TOP_RIGHT, position) +
                self.get_distance_between(self.CORNER_BOTTOM_RIGHT, position) +
                self.get_distance_between(self.CORNER_BOTTOM_LEFT, position)) / 4

    def is_renderable(self, distance):
        return not (distance > self.MAX_DISTANCE)

    def get_canvas(self,is_string: bool = True, is_optimized: bool = True):  # renders the canvas



        render_canvas = deep_copy(self.canvas)  # deep_copy of empty canvas to stack sprite instance on it.
      
        self.get_every_distance_from(is_optimized)  # define sprite_priority, which sprite should be rendered first



        for current_sprite in self.sprite_priority:
            current_pos = current_sprite.position  # set position of the sprite we are looking at throught the for loop

            camera_x = self.camera_pos[0]  # define x_axis of camera
            camera_y = self.camera_pos[1]  # define y_axis of camera

            current_pos_x = current_pos[
                0]  # define x_axis of the current sprite position we are looking at
            current_pos_y = current_pos[
                1]  # define y_axis of the current sprite position we are looking at

            RENDER_POS = [current_pos_x - camera_x, current_pos_y - camera_y
                          ]  # sprite postion - camera_position

            RENDER_POS_X = RENDER_POS[0]  # define x_axis of render position
            RENDER_POS_Y = RENDER_POS[1]  # define y_axis of render position


            self.edit_element(render_canvas, RENDER_POS_X, RENDER_POS_Y,
                                              current_sprite.char)  # Update render

          
        if is_string:

            line = ""

            for current_line in render_canvas:

                for current_element in current_line:
                    line += str(current_element)

                line += "\n"


            return line

        else:
            return render_canvas

    def get_element(self, x, y , canvas):

        line = canvas[y]
        return line[x]

    def get_distance_between(self, pos1, pos2):

        return math.sqrt((pow((pos2[0] - pos1[0]), 2) + pow(
            (pos2[1] - pos1[1]), 2)))  # √[(x₂ - x₁)² + (y₂ - y₁)²]

    def get_every_distance_from(self, is_optimized: bool = True):

        self.distances = []

        camera_pos = self.camera_pos
        camera_pos_x = camera_pos[0]
        camera_pos_y = camera_pos[1]



        if is_optimized != True:

            # for every sprite appends it's distance from square to list "distances"
            for todo_sprite in self.sprite_tree:
                sprite_pos = [
                    todo_sprite.position[0] - camera_pos_x,
                    todo_sprite.position[1] - camera_pos_y
                ]  # sprite_postion - camera_position

                distance_calculated = self.get_square_distance_to(sprite_pos)
                self.distances.append(distance_calculated)

            
          
            self.sprite_priority = self.sprite_tree
            sorted_distances = []
            new_sprite_priority = []

            for todo in range(len(self.distances)):

                min_distance = min(
                    self.distances)  # gets the smallest distance in list "distances"
                sorted_distances.append(
                    min_distance)  # and appends it to list "sorted_distances"

                new_sprite_priority.append(self.sprite_priority[self.distances.index(min_distance)])  
                # gets the correct sprite associated to it 's distance and appends list to "new_sprite_priority"
                                           
                                           
                self.sprite_priority.remove(self.sprite_priority[self.distances.index(min_distance)])  # then remove this sprite from list "sprite_priority"
                self.distances.remove(min(self.distances))  # do same for list "distances"

            self.sprite_priority = new_sprite_priority  # set list "sprite_priority" to list "new_sprite_priority"
            self.distances = sorted_distances  # set list "distances" to list "sorted_distances"

        else:

            # Optimized Run:
            # for every sprite appends it's distance from square to list "distances"


            for todo_sprite in self.sprite_tree:

                sprite_pos = [
                    todo_sprite.position[0] - camera_pos_x,
                    todo_sprite.position[1] - camera_pos_y
                ]  # sprite_postion - camera_position

                distance_calculated = self.get_square_distance_to(sprite_pos)

                if self.is_renderable(distance_calculated) == False:

                    # sprite is Invalid and won't be rendered
                    break

                self.distances.append(distance_calculated)

            self.sprite_priority = self.sprite_tree.copy()
            sorted_distances = []
            new_sprite_priority = []

            for todo in range(len(self.distances)):



                min_distance = min(self.distances)  # gets the smallest distance in list "distances"
                sorted_distances.append(min_distance)  # and appends it to list "sorted_distances"

                new_sprite_priority.append(self.sprite_priority[self.distances.index(min_distance)]
                                           # gets the correct sprite associated to it 's
                                           # distance and appends list to"new_sprite_priority"
                                           )
                self.sprite_priority.remove(self.sprite_priority[self.distances.index(
                    min_distance)])  # then remove this sprite from list "sprite_priority"
                self.distances.remove(min(
                    self.distances))  # do same for list "distances"

            self.sprite_priority = new_sprite_priority  # set list "sprite_priority" to list "new_sprite_priority"
            #self.sprite_tree = self.sprite_priority
            self.distances = sorted_distances  # set list "distances" to list "sorted_distances"



    def send_light_update(self):

        x = 0
        y = 0

        for line in self.get_canvas(False):

            for element in line:
                # display.set_pixel(x, y, element)
                x += 1

            x = 0
            y += 1


class Sprite:
    # sprite must start with "s" like this when initiated :   S_name_of_sprite

    __slots__ = "canvas_object", "char", "position", "name", "group"

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
            # crash and send the follow error back:
            raise (ValueError(
                "Sprite name already exists , please choose another name , only unique names are allowed or consider deleting the older one."
            ))

    def destroy(self):

        self.canvas_object.sprite_tree.remove(self)
        del self






