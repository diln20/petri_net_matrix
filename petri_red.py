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
        for mi in red_petri['m_i']:
            m_inicial.append(mi)
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
        print("Red inicial")
        print()
        print("m_inicial: ", m_inicial)
        print()
        print("Lugares: ", lugares)
        print()
        print("Transiciones: ", transitions)
        print()
        print("Arcos de entrada: ", transitions_input)
        print()
        print("Arcos de salida: ", transitions_out)
        print()
        print("Matriz de entrada: ")
        print(maxinput)
        print()
        print("Matriz de salida: ")
        print(maxout)
        print()
        print("Matriz de disparo: ")
        print(maxd)
        print()
        print("Shot: ", shot)
        print()
        print("Burst: ", burst)
        print()
        print("--------------------------------------------------")
        return m_inicial, lugares, transitions, transitions_input, transitions_out, maxinput, maxout, maxd, shot, burst


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
    def verificar_t(lugares, maxinput, t, tr, input):
        marks = []
        for i in range(len(lugares)):
            marks.append(lugares[i].tokens)
        ej = np.zeros(t)
        print("verificar transicion: ", tr)
        if (input != True):
            ej[int(tr[0].replace("t", ""))] = 1
        else:
            ej[int(tr[1])] = 1
        # print("e[j]",ej)
        ver = np.dot(ej, maxinput)
        if (np.all(ver <= marks)):
            return True
        else:
            return False

        # μ + e[j] ⋅ D
    def disparar(lugares, maxd, t, maxinput, ts, input):
        m_actual = []
        ej = np.zeros(ts)
        for i in range(len(lugares)):
            m_actual.append(lugares[i].tokens)
        print("marcacion actual", m_actual)
        print("disparo transicion: ", t)
        ver = Arc.verificar_t(lugares, maxinput, ts, t, input)
        if (ver == True):
            print("transicion habilitada")
            print(t)
            if (input != True):
                ej[int(t[0].replace("t", ""))] = 1
            else:
                ej[int(t[1])] = 1
            d = m_actual+np.dot(ej, maxd)
            print("disparando.....")
            for i in range(len(lugares)):
                lugares[i].tokens = d[i]
            return print("marcacion actual", d)

        else:
            return print("no permite disparar")

    # disparar en orden rafagas
    def disparar_rafaga(lugares, transicions, maxd, rafaga, maxinput):
        m_actual = []
        ej = np.zeros(len(transicions))
        ez = np.zeros(len(transicions))
        for i in range(len(lugares)):
            m_actual.append(lugares[i].tokens)
        print("marcacion actual", m_actual)
        for i in range(len(rafaga)):
            if (Arc.verificar_t(lugares, maxinput, len(transicions), rafaga[i], True) == True):
                ej[int(rafaga[i][1])] = 1
                print(ej)
                print("disparando transicion: ", rafaga[i])
                m_actual = m_actual+np.dot(ej, maxd)
                ej = np.zeros(len(transicions))
                for i in range(len(lugares)):
                    lugares[i].tokens = m_actual[i]
                print("disparando.....")
                print("marcacion actualizada", m_actual)
                print()
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
    menuprincipal = int(
        input("Menu Principal\n1. Cargar json\n2. Cargar Red Petri\n3. Disparar transición\n4. Disparar transicion por teclado\n5. disparar rafaga\n6. disparar rafaga sin secuencia\n Salir\n"))
    print()
    while menuprincipal != 0:
        if (menuprincipal == 1):
            print("Cargar json: ")
            red = str(input('ingrese_nombre del json: '))
            p = pr.PetriNet(red+".json")
        elif menuprincipal == 2:
            print("Cargar Red Petri y mostrar")
            (m_inicial, lugares, transitions, transitions_input, transitions_out,
             maxinput, maxout, maxd, shot, burst) = p.red_inicial()
            gf.graviz.grafico_inicial(lugares, transitions,  maxinput, maxout)
        elif menuprincipal == 3:
            print("disparar una transicion: ")
            print()
            Arc.disparar(lugares, maxd, shot, maxinput,
                         len(transitions), False)
            gf.graviz.grafico_disparo(lugares, transitions, maxout, maxinput)
        elif menuprincipal == 4:
            print("disparar una transicion por teclado: ")
            print()
            a = str(input("digite transicion: "))
            Arc.disparar(lugares, maxd, a, maxinput, len(transitions), True)
            gf.graviz.grafico_disparo(lugares, transitions, maxout, maxinput)
        elif menuprincipal == 5:
            print("disparar una rafaga: ")
            Arc.disparar_rafaga(
                lugares, transitions, maxd, burst, maxinput)
            gf.graviz.grafico_disparo(lugares, transitions,  maxinput, maxout)
        elif menuprincipal == 6:
            print("disparar una rafaga sin secuencia: ")
            Arc.disparar_rafaga_final(
                lugares, transitions, maxd, burst, maxinput)
            gf.graviz.grafico_disparo(lugares, transitions,  maxinput, maxout)
        else:
            print("Opcion no valida")
        menuprincipal = int(
            input("Menu Principal\n1. Cargar Red Petri\n2. Mostrar Red Petri\n3. Disparar transición\n4. Disparar transicion por teclado\n5. disparar rafaga\n6. disparar rafaga sin secuencia\n Salir\n"))
