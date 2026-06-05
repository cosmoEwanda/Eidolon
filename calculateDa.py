import re

"""
0	Senza Effetto (Vanilla)	1
1	Scartare 1 Carta (Self)	0.7
2	Pescare 1 Carta	1.5
3	Fare Scartare (Avversario)	2.2
4	Dissotterrare (Self)	0.5
5	Rimuovere un'Abilità	2.5
6	Reborn	3
7	Far Dissotterrare	3.5
8	Fa Rimbalzare in mano	3.3
9	Dissolvi	5
10	Distruggere	6
11	Prendere carta dal mazzo	4.5
12	Autodistruggere	0.4
13	+1 Forza	2.3
14	Diminuzione costi (1 Runa)	3.1
15	Protezione	3.5
16	Infliggere 1 Danno	2
17	Effetto Svantaggioso	0.3
18	Modificatore Risorse	5
19	Bandire una carta	7
20	Bandire (con ritorno)	5.3
21	Rivelare la mano	2.6
22	Generare un Incarnato	2.8
23	Trasformare un Incarnato	5.7
24	+1 Tenacia	1.8
25	+1 Astuzia	2.7
26	-1 Forza	0.6
27	-1 Tenacia	0.7
28	-1 Astuzia	0.5
29  1 danno al Portale"""


def get_coefficients():
    # Scala Intera (Base 100)
    # Mapping: ID -> Valore numerico intero (ex_valore * 100)

    # ai: Valori Base degli Effetti
    ai = {
        0: 100,  # Senza Effetto (Vanilla)
        1: 70,  # Scartare 1 Carta (Self)
        2: 150,  # Pescare 1 Carta
        3: 220,  # Fare Scartare (Avversario)
        4: 50,  # Dissotterrare (Self)
        5: 250,  # Rimuovere un'Abilità
        6: 300,  # Reborn
        7: 350,  # Far Dissotterrare
        8: 330,  # Fa Rimbalzare in mano
        9: 500,  # Dissolvi
        10: 600,  # Distruggere
        11: 450,  # Prendere carta dal mazzo
        12: 40,  # Autodistruggere
        13: 230,  # +1 Forza
        14: 310,  # Diminuzione costi (1 Runa)
        15: 350,  # Protezione
        16: 200,  # Infliggere 1 Danno
        17: 30,  # Effetto Svantaggioso
        18: 500,  # Modificatore Risorse
        19: 700,  # Bandire una carta
        20: 530,  # Bandire (con ritorno)
        21: 260,  # Rivelare la mano
        22: 280,  # Generare un Incarnato
        23: 570,  # Trasformare un Incarnato
        24: 180,  # +1 Tenacia
        25: 270,  # +1 Astuzia
        26: 60,  # -1 Forza
        27: 70,  # -1 Tenacia
        28: 50,  # -1 Astuzia
        29: 330 # 1 Danno al Varco
    }

    # bi: Condizioni
    bi = {
        1: 100,  # Neutro
        2: 120,  # Vantaggiosa
        3: 80,  # Svantaggiosa
        4: 70,  # Trigger Passivo
        5: 130,  # Trigger Attivo
        6: 70,  # Trigger Morte
        7: 140,  # Trigger evento
        8: 90,  # Pagamento di 1 Runa
        9: 70  # Pagamento di una gemma
    }

    # ci: Protezioni
    ci = {
        1: 100,  # Nessuna
        2: 130  # Personalità
    }

    # di: Natura/Area
    di = {
        1: 100,  # Istantaneo Singolo
        2: 150,  # Istantaneo Area
        3: 160,  # Permanente Singolo
        4: 220  # Permanente Area (Aura)
    }

    # ei: Velocità
    ei = {
        1: 80,  # Rituale (Lenta)
        2: 100,  # Normale
        3: 150  # Rapida
    }

    return ai, bi, ci, di, ei

def calculate_da(text):
    ai, bi, ci, di, ei = get_coefficients()
    
    # La regex deve catturare l'ID effetto (una o più cifre) 
    # seguito dalle 3 cifre fisse per b, c, d.
    # Esempio: "2312" -> a=2, b=3, c=1, d=2
    # Esempio: "10123" -> a=10, b=1, c=2, d=3
    # Regex: cattura da 1 a 2 cifre iniziali, seguite da esattamente 3 cifre
    pattern = r'\((\d+)\)\((\d+)\)\((\d+)\)\((\d+)\)\((\d+)\)(?:N(\d+))?'
    
    # Dividiamo la stringa se ci sono più effetti separati da ';'
    segments = text.split(';')
    
    total_da = 0
    for segment in segments:
        segment = segment.strip()
        if not segment: continue
        
        match = re.match(pattern, segment)
        if match:
            # Estraiamo i gruppi
            a_id = int(match.group(1))
            b_id = int(match.group(2))
            c_id = int(match.group(3))
            d_id = int(match.group(4))
            e_id = int(match.group(5))
            # Calcolo recuperando i valori dai dizionari
            # .get(id, 0) evita errori se l'ID non esiste nel dizionario

            n_repeat = int(match.group(6)) if match.group(6) else 1


            val_a = ai.get(a_id, 0)
            val_b = bi.get(b_id, 1)
            val_c = ci.get(c_id, 1)
            val_d = di.get(d_id, 1)
            val_e = ei.get(e_id, 1)

            effect_value = (val_a * val_b * val_c * val_d * val_e) * n_repeat

            total_da += effect_value
            
    return round(total_da, 4)

if __name__ == "__main__":
    # Test con il tuo esempio: Sorvegliante di cimiteri
    # 2312 (Pesca 1 Svantaggioso) + 1312 (Scarta 1 Svantaggioso)
    string = input("Inserisci la codifica degli effetti (es. '2312;1312'): ")
    result = calculate_da(string)
    
    print(f"Valore D(a) calcolato: {result}") # Dovrebbe restituire 1.76