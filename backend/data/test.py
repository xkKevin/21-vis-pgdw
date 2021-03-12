import os
from shutil import copyfile

r_path = "./benchmarks"
for root,dirs,files in os.walk(r_path):
    for fi in files:
        if fi.endswith("csv"):
            copyfile(os.path.join(root, fi), os.path.join(r_path, fi))