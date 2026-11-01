import os
import shutil

from generate_page import generate_page

def clean_destination(dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)


def copy_helper(curr_src: str, dest: str):
    print(f"Curr src: {curr_src}, dest: {dest}")
    for f in os.listdir(curr_src):
        curr_f = os.path.join(curr_src, f)
        if os.path.isfile(curr_f):
            print(f"copying file {curr_f} to {dest}")
            shutil.copy(curr_f, dest)
        else:
            # Directory so create corresponding dir in dest and then recurse into it
            dest_f = os.path.join(dest, f)
            print(f"Creating copy of dir {curr_f} at dest {dest_f}")
            os.mkdir(dest_f)
            copy_helper(curr_f, dest_f)



def copy(src: str, dest: str):
    clean_destination(dest)
    copy_helper(src, dest)


def main():
    copy("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()