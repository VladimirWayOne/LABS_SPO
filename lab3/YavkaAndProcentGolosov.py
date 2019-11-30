import table as tb
import UIKs as uik
import  plot_percent as pp

Yavka = []    # процент явки (проголосовавших, чьи голоса учтены)
for i in range(0,75):
    Yavka.append(uik.PerTime[i, 4])
#print(Yavka)
pp.YavkaIProcent(tb.Beglov, tb.Amosov, tb.Tihonova, Yavka)
