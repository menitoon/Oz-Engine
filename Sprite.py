sprite = []
distance_from = {}
distances = []

class Sprite:

  def __init__(self, char, position, z_index):

    self.char = char
    self.position = position
    self.z_index = z_index

    sprite.append(self)

  def get_pos(self):
    print(self.position)

  #sprite must start with "S" like this :   S_name_of_sprite
