import random; random.seed(777); del random


import random

print(random.random())  # 0.22933408950153078
print(random.random())  # 0.44559617334521107

print((a := random.random()), a < 0.5)
print((b := random.random()), b < 0.5)
print((c := random.random()), c < 0.5)
print((d := random.random()), d > 0.5)
print((e := random.random()), 0.9 < e < 0.95)
