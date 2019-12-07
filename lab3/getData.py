import pandas as pd


def get_data(url):

    page = pd.read_html(url, encoding='CP1251')
    header = page[6].drop(12).T
    data = page[7].drop(12).T
    header[0] = 'УИК №'
    data.columns = header.iloc[1]
    data.reset_index()
    for i in range(1, 12):
        newint = []
        for k in data.iloc[:, i]:
            newint.append(int(i))
        data.iloc[:, i] = newint
    for i in range(12, 15):
        count = []
        pro = []
        for j in data.iloc[:, i]:
            j = j.replace("%","")
            j = j.replace("'", "")
            j = j.split()
            count.append(int(j[0]))
            pro.append(float(j[1]))
        data.iloc[:, i] = count
        data['% ' + str(data.columns.values[i])] = pro
    n = []
    ni =[]
    for i in range(data.shape[0]):
        n.append(int(data.iloc[i, 3] + data.iloc[i, 4]))
    data['Явка'] = n
    for i in range(data.shape[0]):
        ni.append(float(round(data.iloc[i, 18] / data.iloc[i, 1] * 100, 2)))
    data['% Явка'] = ni
    return data
