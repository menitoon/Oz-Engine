import main as oz

cs = oz.Canvas("#")
cam = oz.Camera(cs, {"x" : 5, "y" : 5}, {"x" : 0, "y" : 0}, "cam")
cam2 = oz.Camera(cs, {"x" : 5, "y" : 5}, {"x" : 1, "y" : 0}, "cam")

s = oz.Sprite(cs,"o" , {"x" : 1, "y" : 3}, "s")
s2 = oz.Sprite(cs,"o" , {"x" : 3, "y" : 3}, "s")

print(cam.render())
print()
print(cam2.render())

