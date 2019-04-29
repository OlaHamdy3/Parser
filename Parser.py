import sys
import os
dirpath = os.getcwd()
os.environ["PATH"] += os.pathsep + dirpath + os.pathsep + 'graphviz-2.38/release/bin'
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



input_file1=''

""""""""""""""""""""

from graphviz import Digraph
g = Digraph('Output_graph', format='png')
def scanner():
    #input_file = input("file address: ")
    global input_file1
    with open(str(input_file1)) as f:
        content = f.readlines()
    # content = [x.strip() for x in content]
    content[len(content) - 1] += '\n' + '\n'

    symbols = ["+", "-", "*", "/", "<", ">", ":=", "=", ";", "(", ")"]
    words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
    tokens = []
    ##print (content)
    for x in content:
        x = x.split('{', 1)[0]
        if ('}' in x):
            continue
        tokens += (x.split())

    flag = 0

    output = []

    def has_symbol(x):
        if len(x) == 1 or x == ":=":
            return False
        if ('+' in x) or ('-' in x) or ('*' in x) or ('/' in x) or ('<' in x) or ('>' in x) or (':=' in x) or (
            '=' in x) or ('(' in x) or (')' in x):
            return True
        else:
            return False

    def append(x, l1):
        if x in symbols:
            l1.append(x)
            l1.append("Special Symbol")
            output.append(l1)
        elif x in words:
            l1.append(x)
            l1.append("Reserved Word")
            output.append(l1)
        else:
            if x[0].isdigit():
                l1.append(x)
                l1.append("Number")
                output.append(l1)
            else:
                l1.append(x)
                l1.append("Identifier")
                output.append(l1)

    for x in tokens:
        l1 = []
        if ';' in x and len(x) != 1:
            x = x[:x.find(';')]
            flag = 1
        if has_symbol(x):
            index = -1
            index_start = 0
            for char in x:
                l1 = []
                index += 1
                if char == '=' and x[index - 1] == ':':
                    continue

                if char not in symbols and char != ':' and (index != len(x) - 1):
                    continue
                if index != 0 and index != len(x) - 1:
                    append(x[index_start:index], l1)

                if index == len(x) - 1:
                    if index_start == index:
                        append(char, l1)
                    else:
                        if char not in symbols:
                            append(x[index_start:index + 1], l1)
                        else:
                            append(x[index_start:index], l1)
                l1 = []

                if char in symbols or char == ':':
                    index_start = index + 1
                    if (char == ':'):
                        append(':=', l1)
                        index_start += 1

                    else:
                        append(char, l1)

                l1 = []

        else:
            append(x, l1)

        if flag:
            l2 = []
            l2.append(';')
            l2.append("Special Symbol")
            output.append(l2)
        flag = 0

    fout = open("Output.txt", "w+")
    for x in output:
       # print(x[0] + ' , ' + x[1] + '\n')
        fout.write(x[0] + ' , ' + x[1] + '\n')

    fout.close()
    return "Output.txt"



""""""""""""""""""""

token = ''
index = 0
tokens = [[] for row in range(2)]
def parser():
    input_file = scanner()
    with open(input_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    global tokens


    for i in range(len(content)):
        index = content[i].find(',')
        tokens[0].append(content[i][:index - 1])
        tokens[1].append(content[i][index + 2:])
    get_token()
    stmt_seq()
    g.view()


def get_token():
    if index == len(tokens[0]):
        g.view()
        exit()
        return
    if (tokens[1][index] == 'Identifier') or (tokens[1][index] == 'Number'):
        global token

        token = tokens[1][index]
        global index
        #print(index)
        index += 1
    else:
        global token
        token = tokens[0][index]
        global index

        index += 1
    print (token)
    return

node='1'
nodes_list=[]
nodeID={}
flag=0
def MakeNode(given_token,ass):

    if (given_token == 'Identifier') or (given_token == 'Number'):
        given = tokens[0][index-1]
    else:
        given = given_token
        if given_token == ':=':
            given = 'assign'


    global node
    node = chr(ord(node) + 1)
    global flag
    given+= '\n (' + str(flag) + ')'
    current_flag=flag
    flag +=1
    nodeID[current_flag] = given
    if given_token != ':=' and ass !=1:
        g.node(given)
    return current_flag

def child(parent,childd,flag):
    x=1
    if nodeID[parent][:6]=='assign' and flag==1:
        f1=nodeID[parent][:nodeID[parent].find('(')]
        f2=nodeID[parent][nodeID[parent].find('('):]
        nodeID[parent]=f1+nodeID[childd][:nodeID[childd].find('(')]+'\n'+f2
        g.node(nodeID[parent])
        return

    token_parent=nodeID[parent]
    token_child=nodeID[childd]
    g.edge(token_parent,token_child)


def match(expected_token):
    if expected_token==token:
        get_token()
    return
sub=0
def same_rank(element1,element2):
    x=1
    if element2==0:
        print("OKAAAAYY........")
        return
    token_element1=nodeID[element1]
    token_element2 = nodeID[element2]
    global sub
    s = Digraph('subgraph'+str(sub))
    sub+=1
    s.graph_attr.update(rank='same')
    s.node(token_element1,color='red')
    s.node(token_element2,color='red')
    g.edge(token_element1,token_element2)
    g.subgraph(s)
    print (element1,' ', element2)


def stmt_seq():
    temp=statement()

    first=temp
    print (first)
    while token == ';':
        match(token)
        if (token != ';'):
            newtemp=statement()
            same_rank(temp,newtemp)
            temp=newtemp
    return first

def statement():
    temp=0
    if (token=='if'):
        temp=if_stmt()
    elif token == 'repeat':
        temp =repeat_stmt()
    elif token == 'read':
        temp = read_stmt()
    elif token == 'write':
        temp = write_stmt()
    elif (index != len(tokens[0])) and (tokens[0][index] == ':='):
        temp = assign_stmt()
    return temp

def assign_stmt():
    newtemp=0
    temp=MakeNode(token,1)
    match(token)

    newtemp=MakeNode(token,0) # :=
    match(token)
    child(newtemp, temp,1)
    child(newtemp, exp(),0 )
    temp = newtemp
    return temp

def read_stmt():
    temp=MakeNode(token,0)
    match(token)
    child(temp,MakeNode(token,0),0 )
    match(token)
    return temp


def write_stmt():
    temp=MakeNode(token,0)
    match(token)
    child(temp, exp(),0 )
    return temp

def term():
    temp = factor()
    while (token == '*') or token =='/':
        newTemp = MakeNode(token,0)
        match(token)
        child(newTemp, temp,0 )
        child(newTemp, factor(),0 )
        temp = newTemp
    return temp



def simple_exp():
    temp = term()
    while (token == '+') or (token == '-'):
        newTemp = MakeNode(token,0)
        match(token)
        child(newTemp, temp,0 )
        child(newTemp, term(),0 )
        temp = newTemp
    return temp


def if_stmt():
    newTemp = MakeNode(token,0)
    match(token)
    child(newTemp, exp(),0 )
    match(token)
    child(newTemp, stmt_seq(),0 )
    if token == 'else':
        match(token)
        child(newTemp, stmt_seq(),0 )
        match(token)
        temp = newTemp
    elif token == 'end':
        match(token)
        temp = newTemp
    return temp


def repeat_stmt():
    newTemp = MakeNode(token,0)
    match(token)
    child(newTemp, stmt_seq(),0 )
    match(token)
    child(newTemp, exp(),0 )
    temp = newTemp
    return temp


def exp():
    temp = simple_exp()
    if (token == '<') or (token == '='):
        newTemp = MakeNode(token,0)
        match(token)
        child(newTemp, temp,0)
        child(newTemp, simple_exp(),0)
        temp = newTemp
    return temp


def factor():
    temp=0
    if token == '(':
        match(token)
        temp = exp()
        match(token) #')'
    elif token == 'Identifier':
        newTemp = MakeNode(token,0)
        match(token)
        temp = newTemp
    elif token == 'Number':
        newTemp = MakeNode(token,0)
        match(token)
        temp = newTemp

    return temp






class App(QWidget):


    def __init__(self):
        super().__init__()


        self.title = 'Parser'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)


        self.setGeometry(150, 150, self.width, self.height)

        #label
        label = QLabel("Input file", self)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        label.move(20,25)


        #browseButton
        browseButton = QPushButton('browse',self)
        browseButton.setToolTip('This is an example button')
        browseButton.move(70, 20)
        browseButton.clicked.connect(self.browse)

        #button
        button = QPushButton('Run', self)
        button.setToolTip('This is an example button')
        button.move(70, 50)
        button.clicked.connect(self.on_click)

        #image = QPushButton('',self)
        #image.setIcon(QIcon('test.gv.png'))
        #image.move(100,10)
        #image.resize(500,100)


        self.show()


    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        parser()


    def browse(self):
        global input_file1
        input_file1 = QFileDialog.getOpenFileName(self,'Open File')
        input_file1 = str(input_file1)[2:str(input_file1).find(',')-1]

        print ("____",input_file1,"____")

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = App()
     sys.exit(app.exec_())