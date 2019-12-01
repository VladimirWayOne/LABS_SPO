from web3 import Web3
import numpy as np
import matplotlib.pyplot as plt


def Plotting(x,y, name, Color,Ylabel):
    Fig = plt.figure(figsize=(35, 15))
    ax = Fig.add_subplot()
    ax.set(title=name, xlabel="Block's number", ylabel=Ylabel)
    ax.tick_params(axis='x', labelrotation=90, pad=10)
    ax.plot(x, y, color=Color, linewidth=0.8)
    ax.scatter(x, y, color=Color, s=6)
    Fig.savefig(name + '.png')


def ConvertGweiToETH(gwei):
    return gwei * 1e-8


def BlockReward(block):
    return 2 + ConvertGweiToETH(block.gasUsed) + 2*len(block.uncles)/32


fb, lb = 8961400 - 100 * (13 - 1), 8961400 - 100 * (13 - 2)    #first block, last block

ComissionPercentage = []
Comission_block = []        # commission for each block
Reward_block = []           # reward for each block
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/22ccc929d30a47be975b7fee7c05fa3e'))     # Connection via Infura
NumberOfBlock = []
for blockNumber in range(fb, lb):
    NumberOfBlock.append(blockNumber)
    block = web3.eth.getBlock(blockNumber)      # Current block
    Reward_block.append(BlockReward(block))
    Comission_block.append(ConvertGweiToETH(block.gasLimit))
    ComissionPercentage.append(Comission_block[len(Comission_block)-1]/Reward_block[len(Reward_block)-1]*100)


MX = np.mean(Comission_block)   # мат ожидание
DX = np.var(Comission_block)    # дисперсия
Me = np.median(Comission_block) # медиана
Range = np.ptp(Comission_block) # размах
Sigma = np.sqrt(DX)             # среднеквадрат. отклонение

Plotting(NumberOfBlock, ComissionPercentage, 'Percentage commission for each block', 'red', 'Комиссия, %')
Plotting(NumberOfBlock, Comission_block, 'Commission for each block', 'm', 'Комиссия, ETH')
Plotting(NumberOfBlock, Reward_block, 'Reward for each block', 'orange', 'Награда, ETH')

print('MX= ', MX, '\nDX= ', DX, '\nMe= ', Me, '\nРазмах= ', Range, '\nδ= ', Sigma)
