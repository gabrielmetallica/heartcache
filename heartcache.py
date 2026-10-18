import turtle as t
import math as m
import random as r
import time

# ===== CONFIGURAÇÕES (mexa aqui) =====
LINHA_1 = "Te amo"
LINHA_2 = "Jheyy"
FONTE_1 = ("Segoe UI Light", 40, "normal")
FONTE_2 = ("Segoe UI", 40, "bold")
Y_LINHA_1 = 5       # posição vertical da 1ª linha (suba/desça se precisar)
Y_LINHA_2 = -70     # posição vertical da 2ª linha

FUNDO = (11, 11, 20)
ROSA = (255, 70, 150)
ROXO = (150, 80, 255)
QTD_MIOLO = 2600
QTD_POEIRA = 500
# =====================================


# ---------- utilidades de cor ----------
def mix(c1, c2, k):
    """Mistura duas cores RGB (k=0 -> c1, k=1 -> c2)."""
    return tuple(c1[i] + (c2[i] - c1[i]) * k for i in range(3))


def hexa(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in c)


def apagar(c, brilho):
    """Escurece a cor em direção ao fundo (simula transparência)."""
    return mix(FUNDO, c, brilho)


# ---------- tela ----------
s = t.Screen()
s.setup(700, 700)
s.bgcolor(hexa(FUNDO))
s.title("Para Jheyy")
s.tracer(0)

p = t.Turtle()      # desenha o coração
p.hideturtle()
p.speed(0)
p.penup()

tx = t.Turtle()     # desenha o texto
tx.hideturtle()
tx.penup()

fx = t.Turtle()     # desenha os brilhos que piscam
fx.hideturtle()
fx.penup()


def heart(a, scale):
    x = 16 * (m.sin(a) ** 3) * scale
    y = (13 * m.cos(a) - 5 * m.cos(2 * a) - 2 * m.cos(3 * a) - m.cos(4 * a)) * scale
    return x, y


# contorno do coração
N = 420
contorno = [heart(2 * m.pi * i / N, 16) for i in range(N + 1)]
Y_MIN = min(y for _, y in contorno)
Y_MAX = max(y for _, y in contorno)


def cor_em(y):
    """Degradê vertical: rosa no topo, roxo embaixo."""
    k = (Y_MAX - y) / (Y_MAX - Y_MIN)
    return mix(ROSA, ROXO, max(0, min(1, k)))


def na_zona_do_texto(x, y):
    """Abre um espaço suave no centro para a mensagem respirar."""
    dx = x / 185
    dy = (y + 10) / 100
    d = dx * dx + dy * dy
    if d < 1:
        return True
    if d < 1.8:
        return r.random() < (1.8 - d) / 0.8
    return False


# 1) Contorno neon (camadas largas e escuras primeiro, núcleo brilhante por último)
camadas = [(18, 0.08), (12, 0.16), (8, 0.30), (4, 0.65), (2, 1.0)]
for largura, brilho in camadas:
    p.width(largura)
    for i in range(N):
        x1, y1 = contorno[i]
        x2, y2 = contorno[i + 1]
        p.pencolor(hexa(apagar(cor_em(y1), brilho)))
        p.goto(x1, y1)
        p.pendown()
        p.goto(x2, y2)
        p.penup()
    s.update()
    time.sleep(0.12)

# 2) Poeira de luz ao redor do contorno
for i in range(QTD_POEIRA):
    a = r.uniform(0, 2 * m.pi)
    x, y = heart(a, 16 * (1 + abs(r.gauss(0, 0.07))))
    p.goto(x, y)
    p.dot(r.uniform(1, 2.6), hexa(apagar(cor_em(y), r.uniform(0.2, 0.7))))
    if i % 25 == 0:
        s.update()
        time.sleep(0.004)

# 3) Miolo feito de pontinhos de luz (mais densos perto da borda)
for i in range(QTD_MIOLO):
    a = r.uniform(0, 2 * m.pi)
    k = r.random() ** 0.4
    x, y = heart(a, 16 * k * 0.97)
    if na_zona_do_texto(x, y):
        continue
    brilho = 0.25 + 0.75 * k * r.uniform(0.6, 1.0)
    tamanho = r.uniform(1.2, 3.4) * (0.6 + 0.6 * k)
    p.goto(x, y)
    p.dot(tamanho, hexa(apagar(cor_em(y), brilho)))
    if i % 60 == 0:
        s.update()
        time.sleep(0.005)


# 4) Mensagem surgindo em fade
def escrever(brilho):
    tx.clear()
    tx.goto(0, Y_LINHA_1)
    tx.pencolor(hexa(apagar((255, 255, 255), brilho)))
    tx.write(LINHA_1, align="center", font=FONTE_1)
    tx.goto(0, Y_LINHA_2)
    tx.pencolor(hexa(apagar((255, 120, 185), brilho)))
    tx.write(LINHA_2, align="center", font=FONTE_2)
    s.update()


for brilho in (0.15, 0.35, 0.6, 0.85, 1.0):
    escrever(brilho)
    time.sleep(0.12)


# 5) Brilhinhos piscando (roda até você fechar a janela)
def novo_brilho():
    while True:
        x, y = heart(r.uniform(0, 2 * m.pi), 16 * r.uniform(0.2, 1.1))
        if not na_zona_do_texto(x, y):
            return [x, y, r.uniform(0, m.pi)]


brilhos = [novo_brilho() for _ in range(9)]

try:
    while True:
        fx.clear()
        for b in brilhos:
            b[2] += 0.18
            if b[2] > m.pi:
                b[:] = novo_brilho()
                b[2] = 0
            tam = m.sin(b[2]) * 9
            if tam > 0.5:
                fx.pencolor("white")
                fx.width(1.5)
                for ang in (0, m.pi / 2):
                    dx, dy = tam * m.cos(ang), tam * m.sin(ang)
                    fx.goto(b[0] - dx, b[1] - dy)
                    fx.pendown()
                    fx.goto(b[0] + dx, b[1] + dy)
                    fx.penup()
        s.update()
        time.sleep(0.04)
except Exception:
    pass  # janela fechada