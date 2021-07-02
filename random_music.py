import json
from os import chdir, environ, listdir, getcwd
from os.path import isdir,join
from random import shuffle
from subprocess import run
from sys import argv
from time import sleep

DST = "/storage/emulated/0/Music"
COUNT = 1000

def main():
    if len(argv) > 1:
        arg = argv[1]
        if arg == "albums":
            b = True
            f = json_load(argv[2]) if len(argv)>2 else []
        else:
            b = "albums" in argv[2:3]
            f = json_load(arg)
        do_it(f,b)
    else:
        do_it([],False)

def do_it(base,tgl):
    chdir( join(environ["HOME"], "Music") )
    choices = list_choices(tgl)
    while True:
        shuffle(choices)
        k,n = get_max_index(choices)
        cur = choices[:k]
        pprint(cur)
        print("\nSongs: {}".format(n))
        try:
            if input("Ok? ") == "y":
                adb_push(cur)
                break
        except KeyboardInterrupt:
            break
        except EOFError:
            break

# Assumes you are in ~/Music
def list_choices(albums=False):
    artists = [ s for s in listdir() if isdir(s) ]
    if albums:
        return [ join(art,alb)
                for art in artists
                for alb in listdir(art) ]
    else:
        return artists

def get_max_index(choices):
    cur,n,N = 0,0,len(choices)
    while cur < COUNT:
        if n<N:
            cur += count_songs( choices[n] )
            n += 1
        else:
            print("You have less than {} songs"
                    .format(COUNT))
            break
    return n,cur

# count how many songs in d
def count_songs(d="."):
    n = 0
    prev = getcwd()
    chdir(d)
    for f in listdir():
        if isdir(f):
            n += count_songs(f)
        elif is_audio(f):
            n += 1
    chdir(prev)
    return n

def adb_push(l):
    for i in l:
        dst = "{}/{}".format(DST,i)
        run(["adb", "push", i, dst])

# returns true if s is an audio file
EXTS = ["mp3", "wma", "flac"]
def is_audio(s):
    k = s.rfind(".")+1
    return s[k:] in EXTS

def json_load(s):
    with open(arg) as f:
        l = json.load(f)
    return l

def pprint(cur):
    cur.sort()
    for a in cur:
        print(a)

if __name__ == "__main__":
    main()
