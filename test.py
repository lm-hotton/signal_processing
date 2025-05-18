import numpy as np
import scipy
import plotly.express as px
import pandas as pd
import endaq
import matplotlib.pyplot as plt


t=np.linspace(0,1,1*400000)
random=np.random.uniform(1,-1,1*400000)

fig0 = px.line(
        t,
        x=t,
        y=random,
    )
#fig0.show()


#Calculate PSD
f, psd = scipy.signal.welch(t,fs=400000.,window='hann', nperseg=32768,noverlap=0.5)

#Plot PSD
fig1 = px.line(f,
               x=f,
               y=psd,
               log_y=True
    )
#fig1.show()

expo=1*np.exp(-10*t)
choc=random*expo

fig2 = px.line(
        t,
        x=t,
        y=choc,
    )
#fig2.show()

b, a = scipy.signal.butter(8, 10000/400000)
choc2 = scipy.signal.filtfilt(b, a, choc, padlen=150)

fig3 = px.line(
        t,
        x=t,
        y=choc2,
    )
fig3.show()

pdchoc2=pd.DataFrame(choc2,t)
print(pdchoc2)

#Calculate SRS
freqs = endaq.calc.utils.logfreqs(pdchoc2, init_freq=1, bins_per_octave=12)
srs = endaq.calc.shock.shock_spectrum(pdchoc2, freqs=freqs, damp=10., mode='srs')

#Plot SRS
fig4 = px.line(srs).update_layout(
    title_text='Shock Response Spectrum (SRS) of Motorcycle Crash',
    xaxis_title_text="Natural Frequency (Hz)",
    yaxis_title_text="Peak Acceleration (g)",
    legend_title_text='',
    xaxis_type="log",
    yaxis_type="log",
  )
fig4.show()