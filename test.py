import numpy as np
import scipy
import plotly.express as px
import pandas as pd
import endaq


t=np.linspace(1,1000,1000)
print (t)

# get accelerometer data from https://info.endaq.com/hubfs/100Hz_shake_cal.ide
df_accel = endaq.ide.to_pandas(endaq.ide.get_doc(
        'https://info.endaq.com/hubfs/100Hz_shake_cal.ide').channels[8].subchannels[2],
        time_mode='seconds',
    )

# create a new dataframe filtered with a high-pass butterworth with a cutoff frequency of 1 Hz
df_accel_highpass = endaq.calc.filters.butterworth(df_accel, low_cutoff=1, high_cutoff=None)
df_accel_highpass.columns = ['1Hz high-pass filter']

# create a new dataframe filtered with a low-pass butterworth with a cutoff frequency of 100 Hz
df_accel_lowpass = endaq.calc.filters.butterworth(df_accel, low_cutoff=None, high_cutoff=100)
df_accel_lowpass.columns = ['100Hz low-pass filter']

# merge the data into a single dataframe for plotting
df_accel = df_accel.join(df_accel_highpass, how='left')
df_accel = df_accel.join(df_accel_lowpass, how='left')

# plot everything on the same axes
fig1 = px.line(
        df_accel,
        x=df_accel.index,
        y=df_accel.columns,
        labels=
            {
                "timestamp": "time [s]",
                "value": "Acceleration [g]",
            },
    )
fig1.show()

#Get Acceleration Data
bearing = pd.read_csv('https://info.endaq.com/hubfs/Plots/bearing_data.csv', index_col=0)

#Calculate PSD with 1 Hz Bin Width
psd = endaq.calc.psd.welch(df_accel, bin_width=1)

#Plot PSD
fig1 = px.line(psd[10:5161]).update_layout(
    title_text='1 Hz PSD of Bearing Vibration',
    yaxis_title_text='Acceleration (g^2/Hz)',
    xaxis_title_text='Frequency (Hz)',
    xaxis_type='log',
    yaxis_type='log',
    legend_title_text='',
)
fig1.show()