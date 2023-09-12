def clean_alternative():
    cv = []
    alternative = []
    for i in instances_1:
        cv.extend(i.split(','))
    new_alternative = [x.strip(' \n').capitalize()+'\n' for x in cv]
    with open(f'../Project_Files/emergencies_alternative.txt','w+') as k:        
        new_alternative = list(set(new_alternative))
        new_alternative.sort()
        k.write(''.join(new_alternative))
        instanc = k.readlines()
        
def combine():
    with open(f'../Project_Files/emergencies.txt','r+') as f:
        instances = f.readlines()
    with open(f'../Project_Files/emergencies_alternative_new.txt','r+') as x:
        instances_1 = x.readlines()

    with open(f'../Project_Files/xtx.txt','w+') as k:
        w = list(set(instances+instances_1))
        w.sort()
        k.write(''.join(w))
        instanc = k.readlines()