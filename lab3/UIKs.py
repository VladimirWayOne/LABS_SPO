import pandas as pd
import numpy as np
import  plot_percent as pp

url = 'http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&type=454&vibid=27820001217443'
page = pd.read_html(url, encoding='CP1251')
#print(page[6])
header=page[6].drop([0,1,2]).T
header=header.iloc[1]
PerTime=page[6].drop([0,1,2]).T
PerTime=PerTime.drop([0,1]).T
PerTime = PerTime.reset_index(drop=True)
PerTime = PerTime.T.reset_index(drop=True).T
PerTime = np.array(PerTime)         #Номер УИК и проценты проголосовавших
header = header.reset_index(drop=True)
for k in range(0,75):
    for i in range(1,5):
        PerTime[k,i]= np.float32(PerTime[k,i].replace('%',''))
        if i!=1:
            PerTime[k,i]=round(PerTime[k,i]+PerTime[k,i-1],2)
#for d in PerTime[0,1:]:
#    print(d)
for i in range(0,3):
    pp.VoiceInTime(PerTime[i,1:],header[i])

