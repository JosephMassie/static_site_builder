import os
import shutil

def copy_dir():
    target = "./public"

    # clear contents of public
    if os.path.exists(target):
        shutil.rmtree(target)
        print("target already exists clearing it out")

    #os.mkdir(target)
    shutil.copytree("./static", target)
    # copy contents of src into public
    pass
