import os
from rnd_gen import gen

"""
Created on March 2 02:16:34 2018
@author: Chertkov Maxim
"""

class task_gen:
    """

    This class get text similar to Latex buffed template syntax
    produce pdf and/or latex document

    """
    def __init__(self, another=None):
        """
        construct base format of class
        :param another: copy parameters of another task_gen object
        """
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
        helps with changes of head files in tex syntax

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
        """
        read and save text data in class object

        :param patt: way to txt file or text
        :param way_text: indicator for read mode
        :return:
        """
        if (way_text==0):
            with open (patt, 'r') as f:
                self.pattern = f.read()
        else:
            self.pattern = patt

    def set_name_copy(self, t_name="unknow", num_of_copy=2):
        """
        set ordinal parameters
        :param t_name: name of files series
        :param num_of_copy: number of variations 2-default
        :return:
        """
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
        """
        make latex data in tex files of return list of texts
        :param out: mod 0-not 1-yes
        :return:
        """
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
        make pdf files and save latex, if you need

        :param tex_rdy: if yes use direction /self.t_name
        :param sv_tex: if you need .tex files use 1
        """
        if tex_rdy==0:
            self.get_latex()

        current = os.getcwd()
        wd = current + '\\' + self.t_name
        os.chdir(wd)

        for i in os.listdir(wd):
            os.system("pdflatex "+wd+"\\"+i)

        if sv_tex==0:
            for i in os.listdir():
                if i[-3:] != 'pdf':
                    os.remove(i)
        os.chdir(current)


#-----------------------------------------------------------------------------------------------------------------------

