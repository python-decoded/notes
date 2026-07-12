
import turtle


coords = [
    (0, 60), (-16, 40), (-23, 15), (-23, -25), (-40, -40), (-28, -42),
    (-17, -35), (-15, -40),  (-5, -40), (0, -65),(5, -40), (15, -40),
    (17, -35), (28, -42), (40, -40), (23, -25), (23, 15), (16, 40)
]
turtle.register_shape("rocket", turtle.Shape("polygon", coords))


turtle.shape("rocket")
turtle.left(30)

turtle.done()
