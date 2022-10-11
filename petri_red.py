import petri_red as pr
import json
import numpy as np
import graf as gf
import petry_estructure as petry


class PetriNet:
    def __init__(self, red):
        with open(red, "r") as contenido:
            red_petri = json.load(contenido)
            self.red_petri = red_petri

    def red_inicial(self):
        red_petri = self.red_petri
        lugares = []
        m_inicial = []
        transitions = []
        m_actual = []
        shot = []
        burst = []
        #print("Red inicial")
        # print()
        # print("marcacion_inicial")
        # print()
        for mi in red_petri['m_i']:
            m_inicial.append(mi)
        # print(m_inicial)
        # print()
        for p in red_petri['Places']:
            lugares.append(petry.Place(p['name'], p['tokens']))
        for t in red_petri['Transitions']:
            transitions.append(t)
        for s in red_petri['burst']:
            burst.append(s)
        for sh in red_petri['shot']:
            shot.append(sh)
        print(burst)
        transitions_input = Arc.crear_arco(
            red_petri, "Transitions_input", lugares)
        transitions_out = Arc.crear_arco(
            red_petri, "Transitions_output", lugares)
        maxinput = Arc.matrixinput(transitions_input, lugares, transitions)
        maxout = Arc.matrixout(transitions_out, lugares, transitions)
        maxd = Arc.matrixdmax(maxinput, maxout)
        #gf.graviz.grafico_inicial(lugares, transitions,  maxinput, maxout)
        #print("Matriz Dmax")
        # print()
        # print(maxd)
        # print()
        #print("Transiciones habilitadas")
        # print()
        # enable_transition = Arc.t_enable(
        #     m_inicial, transitions, maxinput)
        # print("transiciones disponibles", enable_transition)
        # shot_check = Arc.verificar_rafaga(burst, enable_transition)
        #print("transiciones de la rafaga disponibles", shot_check)
        #rafaga(m_inicial, maxd, burst)
        # m_actual = Arc.disparo_t(
        #    lugares, m_inicial, maxd, shot, enable_transition, len(transitions), maxinput, maxout)
        print("marcacion actual", m_actual)
        #gf.graviz.grafico_disparo(lugares, transitions,  maxinput, maxout)
        # print()
        raf = Arc.rafaga(lugares, m_inicial, maxd, burst,
                         len(transitions), maxinput)
        #gf.graviz.grafico_disparo(lugares, transitions,  maxinput, maxout)
        return print()


class Arc:
    def matrixinput(transitions_input, lugares, transitions):
        m = len((transitions))
        n = len((lugares))
        max = np.zeros((m, n))
        # print()
        #print("matriz de entradas: ")
        # print()
        for tr in transitions_input:
            # print(tr)
            for i in range(m):
                for j in range(n):
                    if tr.transitio == transitions[i] and tr.place == lugares[j].nombre and tr.weight >= 1:
                        max[i][j] = tr.weight
        # print(max)
        return(max)

    def matrixout(transitions_out, lugares, transitions):
        m = len((transitions))
        n = len((lugares))
        max = np.zeros((m, n))
        # print()
        #print("matriz de salida: ")
        # print()
        for tr in transitions_out:
            # print(tr)
            for i in range(m):
                for j in range(n):
                    if tr.transitio == transitions[i] and tr.place == lugares[j].nombre and tr.weight >= 1:
                        max[i][j] = tr.weight
        return(max)

    def verificar_rafaga(burst, enable_transition):
        shot_check = []
        for i in range(len(burst)):
            if burst[i] in enable_transition:
                shot_check.append(burst[i])
        return shot_check

    def matrixdmax(maxinput, maxout):
        dmax = np.subtract(maxout, maxinput)
        return dmax

    def crear_arco(red_petri, transi, pl):
        transis = []
        for t_i in red_petri[transi]:
            for p in range(len(red_petri['Places'])):
                if(t_i['place'] == pl[p].nombre):
                    if(transi == "Transitions_input"):
                        transis.append(petry.input_transitions(
                            t_i['place'], pl[p].tokens, t_i['transition'], t_i['weight']))
                    else:
                        transis.append(petry.out_transitions(
                            t_i['transition'], t_i['place'],  pl[p].tokens, t_i['weight']))
        return transis

    def disparo_t(lugares, m_inicial, maxd, tr, enable_transition, n, maxinput, maxout):
        print("trans", tr)
        print("transissdda", enable_transition)
        for i in range(len(tr)):
            if tr[i] in enable_transition:
                t = int(tr[0].replace("t", ""))
                ej = np.zeros(n)
                ej[t] = 1
                k = [0, 1, 2, 5, 0]
                disparo = m_inicial+np.dot(ej, maxd)
                print("inicial", lugares)
                for i in range(len(lugares)):
                    up = disparo[i]
                    petry.Place.update_tokens(lugares[i], up)
                    # petry.input_transitions.update_weight(transitions_input[i],up)
                    # petry.out_transitions.update_weight(transitions_out[i],up)
                print("lugares", lugares)
                print("disparo", disparo)
                return disparo
            else:
                print("no se puede disparar la transicion")

    def rafaga(lugares, m_inicial, maxd, burst, t,maxinput):
        print("rafaga", burst)
        rafaga = np.zeros(t)
        print(rafaga)
        ej = np.zeros(t)
        print(lugares)
        initial_marking = [p.tokens for p in lugares]
        print(initial_marking)
        v = [1, 2, 2]
        for i in range(len(burst)):
            ts = int(burst[i].replace("t", ""))
            print("raf", ts)
            if(burst[i] in burst):
                rafaga[ts] += 1
            else:
                rafaga[ts] = rafaga[ts]
        print("rafaga", rafaga)
        disparos = initial_marking+np.dot(rafaga, maxd)
        print("disparos", disparos)
        #t_enables = t_enable(disparos, rafaga, maxinput)
        #print("disa",t_enables)
        print(disparos)
        for i in range(len(burst)):
            print()
            print("burst", burst[i])
            print()
            ej[int(burst[i].replace("t", ""))] = 1
            print("ej", ej)
            disparo = initial_marking+np.dot(ej, maxd)
            print("disparo com", disparo)
        for i in range(len(lugares)):
            up = disparo[i]
            a = petry.Place.update_tokens(lugares[i], up)

        return disparo

def t_enable(m_inicial, transi, maxinput):
    enable_transition = []
    ej = np.zeros(len(transi))
    u = m_inicial
    for tr in transi:
        t = int(tr[1])
        print(t)
        ej[t] = 1
        mul = np.dot(ej, maxinput)
        ej = np.zeros(len(transi))
        if((u >= mul).all()):
            enable_transition.append(tr)
    return enable_transition


# def t_enables():
#     enable_transition = []
#     ej = np.zeros(len(transi))
#     u = m_inicial
#     for tr in transi:
#         t = int(tr[1])
#         print(t)
#         ej[t] = 1
#         mul = np.dot(ej, maxinput)
#         ej = np.zeros(len(transi))
#         if((u >= mul).all()):
#             enable_transition.append(tr)
#     return enable_transition

    



if __name__ == "__main__":

    p = pr.PetriNet("red.json")
    p.red_inicial()
