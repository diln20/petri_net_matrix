from graphviz import Digraph
import numpy as np


class graviz:
    def grafico_inicial(places, transitions, mOutput, mInput):
    
        f = Digraph('PetriNet')
        for i in transitions:
            f.attr('node', shape='box')
            f.node(i, label=i.upper())

        for i in range(np.size(places)):
            f.attr('node', shape='circle')
            f.node(places[i].nombre, label=str(
                places[i].nombre+": "+str(places[i].tokens)),)

        for i in range(len(mOutput[0])):
            for j in range(len(mOutput)):
                if mOutput[j][i] != 0:
                    f.edge(places[i].nombre, transitions[j],
                            label=str(mOutput[j][i]))
                if mInput[j][i] != 0:
                    f.edge(transitions[j], places[i].nombre,
                            label=str(mInput[j][i]))

        f.attr(rankdir='LR')
        return f.view()
    
    def grafico_disparo(places, transitions, mOutput, mInput):
        
        g = Digraph('PetriDisparo')

        for i in transitions:
            g.attr('node', shape='box')
            g.node(i, label=i.upper())

        for i in range(np.size(places)):
            g.attr('node', shape='circle')
            g.node(places[i].nombre, label=str(
                places[i].nombre+": "+str(places[i].tokens)),)

        for i in range(len(mOutput[0])):
            for j in range(len(mOutput)):
                if mOutput[j][i] != 0:
                    g.edge(places[i].nombre, transitions[j],
                            label=str(mOutput[j][i]))
                if mInput[j][i] != 0:
                    g.edge(transitions[j], places[i].nombre,
                            label=str(mInput[j][i]))

        g.attr(rankdir='LR')
        return g.view()
