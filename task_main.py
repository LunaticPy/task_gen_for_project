import matplotlib.pyplot as plt
import os
import shutil
from rnd_gen import gen


class task_gen:

    def __init__(self, another=None):
        if another is None:
            self.t_name = "unknow"
            self.pattern = ""
            self.num_of_copy = 2
            self.head = ''
            self.make_head(self.head)
        else:
            self.t_name = another.t_name
            self.pattern = another.pattern
            self.num_of_copy = another.num_of_copy
            self.head = another.head

    def make_head(self, head, reg=3):
        """
        :param head: text with headlines separated '\n'
        :param reg:0 -clean 1-new 2-add
        """
        if reg==0:
            self.head = []
        elif reg==1:
            self.head = []
            self.head.extend(head.split('\n'))
        elif reg==2:
            self.head.extend(head.split('\n'))
        elif reg == 3:
            self.head = ['\documentclass[a4paper, 12pt]{article}',
                         '\\usepackage{textcomp}',
                         '\\usepackage[utf8]{inputenc}',
                         '\\usepackage[left=2cm, right=2cm, top=1.5cm, bottom=2cm]{geometry}',
                         '\\usepackage{amsmath, amsfonts, amsthm, mathtools, amssymb, icomma, units, yfonts}',
                         '\\usepackage{wrapfig}',
                         '\\usepackage{tikz}',
                         '\\usepackage{enumitem}']


    def read_pattern(self, patt, way_text=0):
        if (way_text==0):
            with open (patt, 'r') as f:
                self.pattern = f.read()
        else:
            self.pattern = patt

    def set_name_copy(self, t_name="unknow", num_of_copy=2):

        self.t_name = t_name
        self.num_of_copy = num_of_copy

    def __add__(self, other):
        """
         :type other: task_gen
        """
        npat = task_gen(self)
        npat.pattern = self.pattern + "\n\\part_split\n" + other.pattern
        return npat

    def gen(self):
        gen(self.pattern, self.num_of_copy, self.head)

    def get_latex(self, out=0):
        if out == 1:
            return gen(self.pattern, self.num_of_copy, self.head)
        else:
            var = gen(self.pattern, self.num_of_copy, self.head)
            current = os.getcwd()
            wd = current + '\\' + self.t_name
            os.makedirs(wd)
            os.chdir(wd)
            for i in range(len(var)):
                with open(self.t_name+'-'+str(i)+'.tex', 'w') as f:
                    f.write(var[i])
            os.chdir(current)

    def get_pdf(self, tex_rdy=0, sv_tex=0):
        """
        :param tex_rdy: if yes use direction /self.t_name
        :param sv_tex: if you need .tex files use 1
        """
        if tex_rdy==0:
            self.get_latex()

        current = os.getcwd()
        wd = current + '\\' + self.t_name
        #os.makedirs(wd + '_pdf')
        os.chdir(wd)# + '_pdf')

        for i in os.listdir(wd):
            os.system("pdflatex "+wd+"\\"+i)
        os.chdir(current)
        #if sv_tex==0:
        #   shutil.rmtree(wd)



#-----------------------------------------------------------------------------------------------------------------------
"""
class img_gen:
    def __init__(self):
        self.w_type = 1
        self.i_name = "unknow"
        self.pattern = ""
        self.num_of_copy = 2

    def read_pattern(self, patt, way_text=0):
        if (way_text==0):
            with open (patt, 'r') as f:
                self.pattern = f.read()
        else:
            self.pattern = patt

    def set_params(self, i_name="unknow", num_of_copy=2, w_type=1):
        self.w_type = w_type
        self.i_name = i_name
        self.num_of_copy = num_of_copy

    def get_preview(self):
        pass
    def get_imgs(self, out=0):
        pass
"""
