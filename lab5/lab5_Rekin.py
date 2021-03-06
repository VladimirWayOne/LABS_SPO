from web3 import Web3
import numpy as np
import matplotlib.pyplot as plt


def transactionsFee(block):
    feesSum = 0
    for transaction in block.transactions:
        feesSum += web3.eth.getTransactionReceipt(transaction).gasUsed * web3.eth.getTransaction(transaction).gasPrice * 1e-18
    return feesSum


def Plotting(x, y, name, Color, Ylabel):
    Fig = plt.figure(figsize=(28, 10))
    ax = Fig.add_subplot()
    ax.set(title=name, xlabel="Block's number", ylabel=Ylabel)
    ax.tick_params(axis='x', labelrotation=90, pad=10)
    ax.plot(x, y, color=Color, linewidth=0.8)
    ax.scatter(x, y, color=Color, s=6)
    Fig.savefig(name + '.png')


def ConvertGweiToETH(gwei):
    return gwei * 1e-8



fb, lb = 8961400 - 100 * (13 - 1), 8961400 - 100 * (13 - 2)  # first block, last block

CommissionPercentage = []
Commission_block = []  # commission for each block
Reward_block = []  # reward for each block
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/22ccc929d30a47be975b7fee7c05fa3e'))  # Connection via Infura
NumberOfBlock = []
for blockNumber in range(fb, lb):
    block = web3.eth.getBlock(blockNumber)  # Current block
    fee = transactionsFee(block)
    NumberOfBlock.append(blockNumber)
    Reward_block.append(2 + fee + 2*len(block.uncles)/32)
    Commission_block.append(fee)
    CommissionPercentage.append(Commission_block[len(Commission_block) - 1] / Reward_block[len(Reward_block) - 1] * 100)

MX = np.mean(Commission_block)  # мат ожидание
DX = np.var(Commission_block)  # дисперсия
Me = np.median(Commission_block)  # медиана
Range = np.ptp(Commission_block)  # размах
Sigma = np.sqrt(DX)  # среднеквадрат. отклонение

Plotting(NumberOfBlock, CommissionPercentage, 'Percentage commission for each block', 'red', 'Комиссия, %')
Plotting(NumberOfBlock, Commission_block, 'Commission for each block', 'm', 'Комиссия, ETH')
Plotting(NumberOfBlock, Reward_block, 'Reward for each block', 'orange', 'Награда, ETH')

print('MX= ', MX, '\nDX= ', DX, '\nMe= ', Me, '\nРазмах= ', Range, '\nδ= ', Sigma)
