import numpy as np
import scipy
import plotly.express as px
import pandas as pd
import endaq
import matplotlib.pyplot as plt
 
#Paramètres du choc
duree=1
fe=400000
fc=30000
nbr_chocs=3
lambdaa=10
 
choc=[]

#Création des chocs
t=np.linspace(0,duree,duree*fe)
expo=1*np.exp(-lambdaa*t)
b, a = scipy.signal.butter(8, fc/fe)
for i in range(nbr_chocs):
    random=np.random.normal(loc=0, scale=1, size=duree*fe)
    y=random*expo
    y[0]=0
    y = scipy.signal.filtfilt(b, a, y, padlen=150)
    choc.append(y)
 
#Affichage des chocs
for i in range(nbr_chocs):
    plt.plot(t,choc[i])
plt.show()

#f,dsp=scipy.signal.welch(choc[1], fs=fe, window='hann', nperseg=None, noverlap=0.5, nfft=None, detrend='constant', return_onesided=True, scaling='density', axis=-1, average='mean')
#plt.loglog(f,dsp)
#plt.show()
 
#Calcul de SRS
srs=[]
freqs = np.logspace(start=np.log10(1),stop=np.log10(50000), num=1000, endpoint=True, base=10)
for i in range(nbr_chocs):
    srs.append(endaq.calc.shock.shock_spectrum(pd.DataFrame(choc[i],t), freqs=freqs, damp=0.05, mode='srs'))
 
#Plot SRS
for i in range(nbr_chocs):
    plt.loglog(freqs,srs[i])
plt.show()