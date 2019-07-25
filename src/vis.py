#!/usr/bin/python

import networkx as nx
import tkinter as Tk
from tkinter import messagebox
from tkinter import StringVar
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import dataManager as data
import sys

this = sys.modules['__main__']

def setupButtons():
    beamLabel = Tk.Label(root,text='beams display here')
    beamLabel.place(x=0,y=10,anchor='nw')

    b1 = Tk.Button(root, text='1',command=lambda: show_week(G,pos,beamLabel,1),highlightbackground='#4d88ff')
    b1.pack(side=Tk.LEFT)
    b2 = Tk.Button(root, text='2',command=lambda: show_week(G,pos,beamLabel,2),highlightbackground='#4d88ff')
    b2.pack(side=Tk.LEFT)
    b3 = Tk.Button(root, text='3',command=lambda: show_week(G,pos,beamLabel,3),highlightbackground='#4d88ff')
    b3.pack(side=Tk.LEFT)
    b4 = Tk.Button(root, text='4',command=lambda: show_week(G,pos,beamLabel,4),highlightbackground='#4d88ff')
    b4.pack(side=Tk.LEFT)
    button = Tk.Button(root, text='5', command=lambda: show_week(G,pos,beamLabel,5),highlightbackground='#4d88ff')
    button.pack(side=Tk.LEFT)

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

def show_week(G, pos, label, week):
    beams = str(data.getBeams()[week])
    label.configure(text = 'week '+str(week)+' has '+beams+' beam(s)')
    draw_edges(G, pos, week)

def draw_edges(G, pos, week):
    if(this.highlightedWeek != week and this.highlightedWeek != 0):
        plt.clf()
        nx.draw_networkx(G, with_labels=True, font_weight='bold', pos=pos)
        plt.draw()
    weekEdges = data.getMatchesPerWeek()[week] 
    this.highlightedWeek = week
    nx.draw_networkx_edges(G, pos,
                       edgelist=weekEdges,
                       width=3, alpha=0.5, edge_color='r')
    canvas.draw()

def updatePerfectMatch(pair, matchLabel):
    data.addPerfectMatch(pair)
    matchText = 'Perfect Matches: '
    for match in data.getPerfectMatches():
        matchText = matchText + str(match) + ", "
    matchLabel.configure(text=matchText)

if __name__ == "__main__":
    root = Tk.Tk()
    root.wm_title("Are You The One? Match Explorer")
    # Quit when the window is done
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)

    f = plt.figure(figsize=(7,6))
    a = f.add_subplot(111)
    plt.axis('off')

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    matchLabel = Tk.Label(root, text='Perfect Matches: ')
    matchLabel.place(x=0,y=30)

    this.highlightedWeek = 0
    data.loadData()
    updatePerfectMatch(('Justin', 'Max'), matchLabel)

    G = makeGraph()
    pos=nx.shell_layout(G)
    nx.draw_networkx(G, with_labels=True, font_weight='bold', pos=pos)

    # G.set_picker(10)
    # root.canvas.mpl_connect('pick_event', lambda: show_week(label,3))


    setupButtons()

    Tk.mainloop()
