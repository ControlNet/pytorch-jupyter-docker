import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--tag", type=str, required=True)
args = parser.parse_args()

# replace the tag in the Dockerfile
with open("Dockerfile", "r") as f:
    content = f.read()

# print(re.match(r"FROM pytorch/pytorch:(.+?)-runtime", content)[1])
content = re.sub(r"FROM pytorch/pytorch:(.+?)-runtime", f"FROM pytorch/pytorch:{args.tag}-runtime", content)

with open("Dockerfile", "w") as f:
    f.write(content)

print(content)
