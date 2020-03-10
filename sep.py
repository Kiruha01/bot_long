from random import shuffle, seed
my = 9999999999

all_ids = [ 123, 
            my]

ids_normal = []
ids_best = [123, 
            my]

def separation(id, mem):
    seed(id)
    if id in ids_normal:
        this_mem = mem
        shuffle(this_mem)
        return this_mem[:-round((len(this_mem) * 20)/100)]
    elif id in ids_best:
        return mem
    else:
        return ["Not an Answers"]