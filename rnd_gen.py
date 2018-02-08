import re
import random
import numpy as np



def get_str(pat, d_pat, pos=0):
    for j in d_pat.keys():
        temp = re.compile("<~" + j + "~>")
        pat = temp.sub(d_pat[j][pos], pat)
    return pat


def py_scr(pat, n_copy, pos=2):
    """
    format: alg__py__%name% : '%alg%' or {'%alg%' : '%variables%'}
    expl: {'(~x~)+(~y~)' : ['x':['np.pi', '3', %py_script%, .....], ['y':[....]]]} }
    """

    if isinstance(pat, str):
        rez = eval(pat)
        if len(rez) < n_copy:
            print("too few args")
            return list(rez)+["empty"]*(n_copy-len(rez))
        else:
            return rez[:n_copy]
    elif isinstance(pat, dict):
        d_pat = get_var(next (iter (pat.values())), n_copy)
        
        rez = []
        for j in range(n_copy):
            rez.append(str(eval(get_str(next (iter (pat.keys())), d_pat, j))))
        return rez

    else:
        print("error in py script")
        return ["error"]*n_copy #check it


def rnd(pat, n_copy, pos=0):
    np.random.seed(pos)
    return np.random.choice(pat, n_copy)


def shuffle(pat, n_copy, pos=0):
    np.random.seed(pos)

    if n_copy>len(pat):
        pat = pat*(n_copy//len(pat)) + pat[:(n_copy%len(pat))]
    np.random.shuffle(pat)
    if n_copy<len(pat):
        pat = pat[:n_copy]

    return pat


alg = {"rnd": lambda pat, n_copy : rnd(pat, n_copy),
      'py': lambda pat, n_copy: py_scr(pat,  n_copy),
      'smp': lambda pat, n_copy:shuffle(pat, n_copy),
      'scn': lambda pat, n_copy:make_scn(pat, n_copy)}


def make_scn(pat, n_copy, pos=0):
    """
    format: 'alg__scn__%name%' : {
    'alg': '%rnd/smp%',
    'vars':['%name1%|%name2%|...', '%name3%|%name2|...', '%name1%|%name3|...'], #should be equal and more than 1
    'args':{dicts in get_var() format},
    'rez_names': '%name1%|%name2%|...' #should be equal with vars elements
    }
    :return dict!!
    """
    rez = dict.fromkeys(pat['rez_names'].split('|'), [])

    n_val = np.random.randint(1, n_copy,size=(len(pat['vars']),))
    if n_val.sum()<n_copy:
        while n_val.sum()<n_copy:
            n_val[np.argmin(n_val)] +=1
    elif n_val.sum()>n_copy:
        while n_val.sum()>n_copy:
            n_val[np.argmax(n_val)] -=1

    for num, vars in zip(n_val, pat['vars']):
        loc_rez = dict()

        for i in vars.split('|'):
            loc_rez[i] = pat['args'][i]

        for i in vars.split('|'):
            loc_rez[i] = pat['args'][i]
        loc_rez = get_var(loc_rez, num)
        id = vars.split('|')
        for i in range(len(id)):
            id[i] = id[i].split('__')[-1]

        for i, j in zip(id, pat['rez_names'].split('|')):  # attantion rez[key] != one of 'rez_names'

            rez[j] = rez[j] + list(loc_rez[i])


    return rez


def get_var(pat, n_copy):
    """
    format: alg__%alg_name%__%name% ... or just %name%
    my_dict = {'key': 'value'}
    """
    var = dict()
    for i, j in zip(pat.keys(), range(len(pat))):
        if 'alg' in i[:3]:
            alg_w = alg[i.split('__')[1]](pat[i], n_copy)

            if isinstance(alg_w, dict):
                var.update(alg_w)
            else:
                var[i.split('__')[-1]] = alg_w
        else:
            var[i] = shuffle(pat[i], n_copy, j)
    return var


def gen(pattern, n_copy, head):
    head = '\n'.join(head)
    rez = [""]*n_copy

    for part in re.split(r"\\part_split", pattern):
        r_val = re.split(r"\\text_start", part)
        d_pat = get_var(eval(r_val[0]), n_copy)
        print(d_pat)
        for i in range(n_copy):
            rez[i] = rez[i] + '\n' + get_str(r_val[1], d_pat, i)

    for i in range(n_copy):
        rez[i] = head + '\n' + "\\begin{document}\n" + rez[i] + '\n' + "\\end{document}"

    return rez
