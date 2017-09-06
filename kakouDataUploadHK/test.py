import os

with open('./test.ini', 'r') as file_object:
    vaules = [item.strip('\n') for item in file_object.readlines()]

print vaules