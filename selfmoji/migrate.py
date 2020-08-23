import sys, os, crayons
from utils import extract_emoji

def main():

    filename = sys.argv[1] if len(sys.argv) > 1 else 'emojis.dict'

    if os.path.isfile(filename):
        emojis = {}
        with open(filename, 'r') as file:
            for line in file:
                k, v = line.strip().split(" : ")
                emojis[k] = v
        for k, v in emojis.items():
            if extracted := extract_emoji(v):
                emojis[k] = extracted
            else:
                print(crayons.red(f"Couldn't extract emoji [{k}: {v}]"))
        with open(filename, "w") as file:
            for k, v in emojis.items():
                file.write(f"{k} : {v}\n")
        print(crayons.green("Migration successful"))
    else:
        print(crayons.red(f"[{filename}] doesn't exist"))


if __name__ == "__main__":
    main()