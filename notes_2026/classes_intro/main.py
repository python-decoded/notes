import random
import time


class Character:
    name = "John Doe"
    health = 100

    def __init__(self, name, strength=5, agility=6, intelligence=9):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

        if strength > 10:
            self.health = 150
        elif strength > 5:
            self.health = 120

        self.attack = 15 * (1 + strength / 100)
        self.crit_chance = 5 + intelligence

        print("Персонажа успішно Створено")

    def attack_target(self, target):

        attack = self.attack
        if random.random() * 100 < self.crit_chance:
            attack = attack * 2
            print(f"КРИТИЧНА АТАКА {self.name}: {attack}")
        else:
            print(f"Атака {self.name}: {attack}")

        target.health = max(target.health - attack, 0)



char_1 = Character("Olaf")
char_2 = Character("Michael", strength=12, agility=6, intelligence=2)

print(vars(char_1))
print(vars(char_2))

while char_1.health > 0 and char_2.health > 0:
    char_1.attack_target(char_2)
    time.sleep(1)
    if char_2.health > 0:
        char_2.attack_target(char_1)
    time.sleep(1)


print("Переміг: ", char_1.name if char_1.health > 0 else char_2.name)
