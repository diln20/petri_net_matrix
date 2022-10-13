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
        transitions_input = Arc.crear_arco(
            red_petri, "Transitions_input", lugares)
        transitions_out = Arc.crear_arco(
            red_petri, "Transitions_output", lugares)
        maxinput = Arc.matrixinput(transitions_input, lugares, transitions)
        maxout = Arc.matrixout(transitions_out, lugares, transitions)
        maxd = Arc.matrixdmax(maxinput, maxout)
        rafaga = ["t2", "t1", "t2", "t1", "t0"]
        Arc.disparar_rafaga_final(lugares, transitions, maxd, rafaga, maxinput)
        gf.graviz.grafico_inicial(lugares, transitions,  maxinput, maxout)
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
        #print("marcacion actual", m_actual)
        #gf.graviz.grafico_disparo(lugares, transitions,  maxinput, maxout)
        # print()
        # raf = Arc.rafaga(lugares, m_inicial, maxd, burst,
        #                  len(transitions), maxinput)
        #gf.graviz.grafico_disparo(lugares, transitions,  maxinput, maxout)
        #t = Arc.verificar_t(lugares, maxinput, len(transitions),"t2")
        # print("validacion",t)
        #Arc.disparar(lugares, maxd, "t2",maxinput, len(transitions))
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
        return (max)

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
        return (max)

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
                if (t_i['place'] == pl[p].nombre):
                    if (transi == "Transitions_input"):
                        transis.append(petry.input_transitions(
                            t_i['place'], pl[p].tokens, t_i['transition'], t_i['weight']))
                    else:
                        transis.append(petry.out_transitions(
                            t_i['transition'], t_i['place'],  pl[p].tokens, t_i['weight']))
        return transis

        #   μ ≥ e[j] ⋅ D−
    def verificar_t(lugares, maxinput, t, tr):
        marks = []
        for i in range(len(lugares)):
            marks.append(lugares[i].tokens)
        ej = np.zeros(t)
        print("verificar transicion: ", tr)
        ej[int(tr[1])] = 1
        # print("e[j]",ej)
        ver = np.dot(ej, maxinput)
        if (np.all(ver <= marks)):
            return True
        else:
            return False

        # μ + e[j] ⋅ D
    def disparar(lugares, maxd, t, maxinput, ts):
        m_actual = []
        ej = np.zeros(ts)
        for i in range(len(lugares)):
            m_actual.append(lugares[i].tokens)
        print("marcacion actual", m_actual)
        print("disparo transicion: ", t)
        ver = Arc.verificar_t(lugares, maxinput, ts, t)
        if (ver == True):
            print("transicion habilitada")
            ej[int(t[1])] = 1
            d = m_actual+np.dot(ej, maxd)
            print("disparando.....")
            for i in range(len(lugares)):
                lugares[i].tokens = d[i]
            print(lugares.tokens)
            return print("marcacion actual", d)
        else:
            return ("no permite disparar")

    #disparar en orden rafagas
    def disparar_rafaga(lugares, transicions, maxd, rafaga, maxinput):
        m_actual = []
        ej = np.zeros(len(transicions))
        ez = np.zeros(len(transicions))
        for i in range(len(lugares)):
            m_actual.append(lugares[i].tokens)
        print("marcacion actual", m_actual)
        for i in range(len(rafaga)):
            if (Arc.verificar_t(lugares, maxinput, len(transicions), rafaga[i]) == True):
                print("disparo en secuencia: ", rafaga[i])
                ej[int(rafaga[i][1])] = 1
                print(ej)
                print("disparando transicion: ", rafaga[i])
                m_actual = m_actual+np.dot(ej, maxd)
                ej = np.zeros(len(transicions))
                for i in range(len(lugares)):
                    lugares[i].tokens = m_actual[i]
                print("disparando.....")
                print("marcacion actual", m_actual)
            else:
                print("no permite disparar")
        return print()
    
    # δ(μ, σ) = μ + f(σ) ⋅ D
    def disparar_rafaga_final(lugares, transicions, maxd, rafaga, maxinput):
        initial_marking = [p.tokens for p in lugares]
        print(initial_marking)
        rafagas = np.zeros(len(transicions))
        for i in range(len(rafaga)):
            ts = int(rafaga[i].replace("t", ""))
            if (rafaga[i] in rafaga):
                rafagas[ts] += 1
            else:
                rafagas[ts] = rafagas[ts]
        print("rafaga", rafagas)
        final_marking = initial_marking+np.dot(rafagas, maxd)
        for i in range(len(lugares)):
            lugares[i].tokens = final_marking[i]
        return print(final_marking)


if __name__ == "__main__":

    p = pr.PetriNet("red2.json")
    p.red_inicial()
