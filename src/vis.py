#!/usr/bin/python

import networkx as nx
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import StringVar
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import dataAccess as data
import sys

this = sys.modules['__main__']

def makeGraph():
    graph = nx.MultiGraph()

    nodes = data.getNodes()
    for id in nodes:
        graph.add_node(nodes[id])

    weeks = data.getMatchesPerWeek()
    for week in weeks:
        matches = weeks[week]
        for pair in matches:
            graph.add_edge(pair[0], pair[1])
    return graph

def setupButtons():
    b1 = tk.Button(root, text='1',command=lambda: show_week(pos,beamLabel,1),highlightbackground='#4d88ff')
    b1.pack(side=tk.LEFT)
    b2 = tk.Button(root, text='2',command=lambda: show_week(pos,beamLabel,2),highlightbackground='#4d88ff')
    b2.pack(side=tk.LEFT)
    b3 = tk.Button(root, text='3',command=lambda: show_week(pos,beamLabel,3),highlightbackground='#4d88ff')
    b3.pack(side=tk.LEFT)
    b4 = tk.Button(root, text='4',command=lambda: show_week(pos,beamLabel,4),highlightbackground='#4d88ff')
    b4.pack(side=tk.LEFT)
    button = tk.Button(root, text='5', command=lambda: show_week(pos,beamLabel,5),highlightbackground='#4d88ff')
    button.pack(side=tk.LEFT)

def show_week(pos, label, week):
    beams = str(data.getBeams()[week])
    label.configure(text = 'week '+str(week)+' has '+beams+' beam(s)')
    draw_edges(pos, week)

def draw_edges(pos, week):
    if(this.highlightedWeek != week and this.highlightedWeek != 0):
        plt.clf()
        nx.draw_networkx(this.G, with_labels=True, font_weight='bold', pos=pos)
        plt.draw()
    weekEdges = data.getMatchesPerWeek()[week] 
    this.highlightedWeek = week
    nx.draw_networkx_edges(this.G, pos,
                       edgelist=weekEdges,
                       width=3, alpha=0.5, edge_color='r')
    canvas.draw()

def updatePerfectMatch(pair):
    data.togglePerfectMatch(pair)
    index = len(data.getPerfectMatches())
    label = tk.Label(root, text=str(pair))
    label.place(x=0, y=(index*20)+30)
    label.bind("<Button-1>", lambda x:clickMatch(pair, label))
    plt.clf()
    this.G = makeGraph()
    nx.draw_networkx(this.G, with_labels=True, font_weight='bold', pos=pos)
    canvas.draw()

def clickMatch(pair, label):
    if(not data.togglePerfectMatch(pair)):
        label.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Are You The One? Match Explorer")
    # Quit when the window is done
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)

    f = plt.figure(figsize=(7,6))
    a = f.add_subplot(111)
    plt.axis('off')

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    this.highlightedWeek = 0
    data.init()
    # updatePerfectMatch(('Justin', 'Max'))
    # updatePerfectMatch(('Basit', 'Jonathan'))

    matchLabel = tk.Label(root, text='Perfect Matches: ')
    matchLabel.place(x=0,y=30)

    beamLabel = tk.Label(root,text='beams display here')
    beamLabel.place(x=0,y=10,anchor='nw')
    setupButtons()

    coupleList = list(data.getCumulativeCouples().keys())
    
    selectCouple = ttk.Combobox(root, values=coupleList)
    selectCouple.bind("<<ComboboxSelected>>",lambda x:updatePerfectMatch(tuple(selectCouple.get().split(' '))))
    selectCouple.place(x=500,y=10)

    this.G = makeGraph()
    pos=nx.shell_layout(this.G)
    nx.draw_networkx(this.G, with_labels=True, font_weight='bold', pos=pos)

    tk.mainloop()
