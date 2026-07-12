import tkinter as tk
import turtle


# 1. Створюємо головне вікно Tkinter (root)
root = tk.Tk()
root.title("Програма з двома незалежними кенвасами")

# 2. Створюємо перший кенвас (лівий)
canvas1 = tk.Canvas(root, width=400, height=400, bg="lightyellow")
canvas1.pack(side=tk.LEFT, padx=10, pady=10)

# 3. Створюємо другий кенвас (правий)
canvas2 = tk.Canvas(root, width=400, height=400, bg="lightcyan")
canvas2.pack(side=tk.RIGHT, padx=10, pady=10)

# 4. Прив'язуємо Turtle до першого кенвасу
screen1 = turtle.TurtleScreen(canvas1)
t1 = turtle.RawTurtle(screen1)
t1.color("red")
t1.circle(50)

# 5. Прив'язуємо Turtle до другого кенвасу
screen2 = turtle.TurtleScreen(canvas2)
t2 = turtle.RawTurtle(screen2)
t2.color("blue")
for _ in range(4):
    t2.forward(100)
    t2.left(90)

# Запускаємо головний цикл Tkinter замість turtle.done()
root.mainloop()
