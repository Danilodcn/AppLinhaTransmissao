UNIDADES = {"Y": 1e24, "Z": 1e21, "E": 1e18, "P": 1e15, "T": 1e12, "G": 1e9, "M": 1e6, "K": 1e3, "c": .01}
x = {"m": 1e-3, "micro": 1e-6, "nano": 1e-9, "pico": 1e-12, "femto": 1e-15, "atto": 1e-18, 'μ': 1e-06, 'η': 1e-09, 'p': 1e-12, 'f': 1e-15, 'a': 1e-18}
UNIDADES.update(x)
y = {1e-6: "μ", 1e-9: "η", 1e-12: "p", 1e-15: "f", 1e-18: "a", 1: ""}

valores_unidades = dict(zip(UNIDADES.values(), UNIDADES.keys()))
valores_unidades.update(y)

__all__ = ["para_notacao_cientifica", "de_notacao_cientifica"]

def simplifica(numero, k=0):
    if numero == 0:
        return numero, k
    if abs(numero) >= .1 and abs(numero) < 1000:
        return numero, k
    if abs(numero) <= 0.1:
        return simplifica(numero * 1000, k-3)

    if abs(numero) >= 10:
        return simplifica(numero / 1000, k + 3)

def para_notacao_cientifica(numero, unidade="", qtd_unidades=None):
    modulo, potencia = simplifica(numero)
    if qtd_unidades != None:
        assert (issubclass(type(qtd_unidades), int) and qtd_unidades >= 0)
        if qtd_unidades == 0:
            qtd_unidades = None
        modulo = round(modulo, qtd_unidades)
    try: return str(modulo) + " " + valores_unidades[10**potencia] + unidade
    except: raise InterruptedError("Aconteceu um erro aqui ", modulo, potencia)

def de_notacao_cientifica(numero: str):
    modulo, *unidade = numero.split(" ")
    if type(unidade) == list:
        unidade = " ".join(unidade)

    for i in range(0, len(unidade)):
        u = unidade[:i+1]
        if u in UNIDADES.keys():
            unidade = u
            break

    return float(modulo) * UNIDADES[unidade]

def __teste(n=1000):
    for i in range(30, n, 6):
        for j in range(i, i + 6):
            print(j, " -> ", chr(j), end="\t")
        print()

if __name__ == "__main__":
    import random
    x = para_notacao_cientifica(random.random() * random.triangular(2e-12, 2e25) * 1e-13, "H/m", 3)
    y = de_notacao_cientifica("34.543 PmH sjksj skjsaks sjkska j")
    print(y)
    print("__FIM__")
