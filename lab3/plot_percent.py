import numpy as np
import matplotlib.pyplot as plt


def mnk(x, y):                          #Метод наименьших квадратов для y = Ax + B
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    xmin = min(x)
    xmax = max(x)
    ls = np.linspace(xmin, xmax)
    x2 = 0                  # sum of x^2
    xy = 0                  # sum of x*y
    for i in range(0, len(x)):
        xy += x[i] * y[i]
    for i in range(0, len(x)):
        x2 += pow(x[i], 2)

    A = (len(x) * xy - np.sum(x) * np.sum(y)) / (len(x) * x2 - pow(np.sum(x), 2))       #     n * Sum(xy) - Sum(x)*Sum(y)        Sum(y) - A*Sum(x)
    B = (np.sum(y) - A * np.sum(x)) / len(x)                                            # A = ――――――――――――――――  B = ――――――――――――
    return A, B, ls                                                                     #        n*Sum(x^2) - Sum(x)^2                     n


def plot(x, y, label):
    #    x = np.array(x).reshape(-1, 1)
    #    y = np.array(x).reshape(-1, 1)
    plt.scatter(x, y, linewidths=1)
    plt.title(label)
    plt.xlabel('Действительные бюллетени')
    plt.ylabel('Процент проголосовавших')
    plt.show()


def VoiceInTime(x, label):                  # Диаграмма зависимости процента проголосвавших(от общего числа) от времени
    axeX = [10.00, 12.00, 15.00, 18.00]
    plt.bar(axeX, x, width=0.4, color='indigo')
    plt.title(label)
   # plt.scatter(axeX, x, color='black')
    for i in axeX:
            plt.text(i-0.39, x[axeX.index(i)]+2.5, np.str(x[axeX.index(i)])+'%')
    plt.xlabel('Время')
    plt.ylabel('Процент проголосовавших, %')
    plt.xlim([9,19])
    plt.ylim([0, 100])
    plt.yticks(np.arange(0, 101, 5))
    plt.show()

def YavkaIProcent  (Beg, Am, Tix, Yavka):           # Зависимоссть процента проголосовавших за Беглова/Амосова/Тихонову от явки
    A, B, ls = mnk(Yavka,Beg)
    plt.plot(ls, A * ls + B, color='red')
    A, B, ls = mnk(Yavka, Am)
    plt.plot(ls, A * ls + B, color='green')
    A, B, ls = mnk(Yavka, Tix)
    plt.plot(ls, A * ls + B, color='blue')

    plt.scatter(Yavka, Beg, color='red', s=10, label='Беглов', marker="*")
    plt.scatter(Yavka, Am, color='green', s=10, label='Амосов')
    plt.scatter(Yavka, Tix, color='blue', s=10, label='Тихонова')



    plt.xlabel('Процент явки, %')
    plt.ylabel('Процент проголосовавших, %')
    plt.legend()
   # plt.xlim([0, 101])
   # plt.ylim([0, 101])
    plt.show()