import random
f = str(open('preset.txt','r').read())

f = f.replace('\n',',').replace(' ','').split('--')
ALL = [preset.split(',') for preset in f]
final = []
for preset in ALL:
    p = []
    for part in preset:
        if part != '':
            p.append(part)
    final.append(p)

def getInfo(name):
    index = [i for i,preset in enumerate(map(lambda x: x[0],final)) if preset == name][0]
    data = ALL[index]
    data = [d.split('->') for d in data if d != name and d != '']
    p = {p[0]:p[1] for p in data}
    if p['seed'] == 'random':
        p['seed'] = random.randint(0,100)
    return p

#format

# name
# screen ->
# cells ->
# seed ->
# mag ->
# extraMag ->
# weight ->
# passes ->
# --
