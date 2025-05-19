import numpy as np
import scipy
import plotly.express as px
import pandas as pd
import endaq
import matplotlib.pyplot as plt
 
#Paramètres du choc
duree=1
fe=400000
fc=20000
nbr_chocs=3
lambdaa=10
 

#Création des chocs
t=np.linspace(0,duree,duree*fe)
expo=1*np.exp(-lambdaa*t)
b, a = scipy.signal.butter(8, fc/fe)
random=np.random.normal(loc=0, scale=1, size=duree*fe)
y=random*expo
y[0]=0
y = scipy.signal.filtfilt(b, a, y, padlen=150)
choc=y


#Decimation
choc_decim=[]
t_decim = []
for q in range(11):
    choc_decim.append(scipy.signal.decimate(choc, (q+1)))
    t_decim.append(np.linspace(0, duree, len(choc_decim), endpoint=False))
    plt.plot(t_decim[q],choc_decim[q])
plt.show()

src=[]
freqs = np.logspace(start=np.log10(1),stop=np.log10(50000), num=1000, endpoint=True, base=10)
for q in range(11):
    src.append(endaq.calc.shock.shock_spectrum(pd.DataFrame(choc,t), freqs=freqs, damp=0.05, mode='srs'))
    plt.loglog(freqs,src[q-1])
plt.show()