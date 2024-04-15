import re

with open("Dockerfile", "r") as f:
    content = f.read()

print(re.match(r"FROM pytorch/pytorch:(.+?)-runtime", content)[1])