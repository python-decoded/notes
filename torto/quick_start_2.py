import turtle

turtle.pensize(5)
turtle.color("red")

turtle.speed(1)
turtle.shape("turtle")
turtle.shapesize(3)

turtle.begin_fill()

turtle.write(turtle.position())
turtle.forward(200)
turtle.write(turtle.position())
turtle.left(90)
turtle.forward(250)
turtle.write(turtle.position())

angle = turtle.towards(0, 0)
distance = turtle.distance(0, 0)

turtle.setheading(angle)
turtle.forward(distance)

turtle.end_fill()

turtle.done()
