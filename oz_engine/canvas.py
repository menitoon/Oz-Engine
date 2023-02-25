class Canvas:
    """
    Object that can store sprites in it to be rendered
    """

    __slots__ = "void", "sprite_names", "sprite_names_dict", "sprite_tree", "sprite_position_dict",\
        "sprite_group_dict", "group_tree", "camera_name_dict", "camera_tree", "structure_tree", "structure_dict",\
        "position_dict"

    def __init__(self, void):
        # Characters that fills the canvas when nothing is rendered on a tile.
        self.void = void
        # List that contains every reference of each sprite that is linked to the canvas in question
        self.sprite_tree = set()
        # List that contains every groups that exists
        self.group_tree = set()
        # List that contains every name of each sprite that is linked to the canvas in question
        self.sprite_names = set()
        # Dictionary that has a name as a key and the corresponding Sprite reference as a value
        self.sprite_names_dict = {}
        # Dictionary that has a sprite reference as a key and the corresponding position as a value
        self.sprite_position_dict = {}
        # Dictionary that has a sprite reference as a key and the corresponding group as a value
        self.sprite_group_dict = {}
        # List that contains every reference of every Camera that are linked to the canvas in question
        self.camera_tree = set()
        # Dictionary that has a name as a key and the corresponding Camera reference as a value
        self.camera_name_dict = {}
        # Dictionary that has a position as a key and a list containing every sprite at the position
        self.position_dict = {}

    def get_elements(self, position: list):
        """
        Returns sprites names at the given pos.
        """

        object_at = []

        sprite_list = list(self.sprite_position_dict.copy().keys())
        position_list = list(self.sprite_position_dict.copy().values())

        while position in position_list:
            place_index = position_list.index(position)
            # deletes the element from "sprite_list" and appends it to "object_at"
            object_at.append(sprite_list.pop(place_index).name)
            # and remove the element from "position_list"
            del position_list[place_index]

        return object_at

    def get_sprite(self, name):
        """
        returns reference to sprite that owns the given name.
        """
        return self.sprite_names_dict[name]

    def call_group(self, group_to_call: str, method_to_call, *args):
        """
        Call a method  to every sprite that belongs to the group that is
        given
        like so:
        canvas.call_group("group_name_here" , method_is_going_to_be_called_on_them() )
        """

        # gets every sprite that is in the group given

        sprite_to_call = self.sprite_group_dict.get(group_to_call)
        if sprite_to_call is None:
            # if group given doesn't exist then submit error
            raise Exception(
                f'''The group "{group_to_call}" doesn't exist please specify a valid group to call. '''
            )

        for todo_sprite in sprite_to_call:
            func = getattr(todo_sprite, method_to_call)
            func(*args)
