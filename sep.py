from random import shuffle, seed
my = 276820555

all_ids = [ 181599740, # Алина Ахметшина
            181599456, # Виктория Кузнецова
            151838872, # Арина Кожарина
            148552711, # Лена Булыкина
            171227472, # Валерия Тимакова
            255873986, # Даня Михеев
            my]

ids_normal = []
ids_best = [181599740, # Алина Ахметшина
            181599456, # Виктория Кузнецова
            151838872, # Арина Кожарина
            148552711, # Лена Булыкина
            171227472, # Валерия Тимакова
            255873986, # Даня Михеев
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