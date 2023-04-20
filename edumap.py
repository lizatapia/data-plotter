
#TODO make a code to gather the WL and LE from each subbasin

from matplotlib import pyplot as plt
import pandas as pd
import datetime
import numpy as np
from matplotlib.lines import Line2D

# INITIATION
frequency = "1D" # "1H"
width = pd.Timedelta(days=1)
date_in = datetime.datetime(2020, 1, 10, 0, 0)
date_end = datetime.datetime(2020, 1, 27, 0, 0)
number_days = date_end - date_in + pd.Timedelta(days=1)
data_le = [0,6.5,55,2550,52500,200000,0,6.5,55,2550,52500,200000,0,6.5,55,2550,52500,200000] # the accumulation of LE values
data_wl = [255,255,255,255,255,255,1,1,1,1,1,1,3,3,3,3,3,3] # the WL values
threshold_wl = -3 # ABOVE MODERATE
threshold_le = 1 # ABOVE M1

# MANIPULATING DATA
ts = pd.date_range(date_in, date_end, freq=frequency)
timeseries = pd.Series(index=ts)
timeseries = pd.DataFrame(timeseries)
# RE-SHAPING LANDSLIDE EVENTS (VOLUMEN)
# individual value
m1_ind = 6.5
m2_ind = 55
m3_ind = 2550
m4_ind = 52500
m5_ind = 100000
# limits for each level
m1_lim = 10
m2_lim = 100
m3_lim = 5000
m4_lim = 100000
# changing values
timeline_le = [0] * len(data_le)
for j in range(len(data_le)):
    if data_le[j] == 0:
        timeline_le[j] = 0 # NO EVENT
    elif data_le[j] <= m1_lim:
        timeline_le[j] = 1 # M1
    elif data_le[j] > m1_lim and data_le[j] <= m2_lim:
        timeline_le[j] = 2 # M2
    elif data_le[j] > m2_lim and data_le[j] <= m3_lim:
        timeline_le[j] = 3 # M3
    elif data_le[j] > m3_lim and data_le[j] < m4_lim:
        timeline_le[j] = 4 # M4
    else:
        timeline_le[j] = 5 # M5
# RE-SHAPING WARNING LEVEL
timeline_wl = [0] * len(data_wl)
for i in range(len(data_wl)):
    if data_wl[i] == 255:
        timeline_wl[i] = 0 # NO WARNING
    elif data_wl[i] == 0:
        timeline_wl[i] = -1 # VERY LOW
    elif data_wl[i] == 1:
        timeline_wl[i] = -2 # LOW
    elif data_wl[i] == 2:
        timeline_wl[i] = -3 # MODERATE
    else:
        timeline_wl[i] = -4 # HIGH
# GATHERING FINAL DATA
timeseries["LE"] = timeline_le
timeseries["WL"] = timeline_wl

#PLOTTING
name_time = 'ex3' # define name to save it
fig, ax = plt.subplots(2, 1, figsize =(13, 13), tight_layout = True)
fig.suptitle("Landslide Events and Landslide Warnings over time\n" + datetime.datetime.strftime(date_in,'%Y-%m-%d') + " until " + datetime.datetime.strftime(date_end,'%Y-%m-%d'), fontsize = 25)

ax[0].axes.bar(timeseries.index, timeseries["LE"], color = '#ffffff00', ec = 'blue', align = 'edge', linewidth = 2.5, width = width)
ax[0].set_xticks(timeseries.index)
#ax[0].set_xlim(date_in, date_end)
plt.setp(ax[0].get_xticklabels(), rotation = 90, fontsize = 14)
name_date = ax[0].set_xlabel("Date", fontsize = 18) # still shows cut in the picture
ax[0].xaxis.set_label_coords(1.01, -0.13)
ax[0].set_yticks([0,1,2,3,4,5], labels =["No Event", "M1", "M2", "M3", "M4", "M5"], fontsize = 15)
ax[0].set_ylabel("Landslide Events Classification", fontsize = 18)
ax[0].axhline(y = threshold_le-0.05, linewidth = 0.9, linestyle = '-.', color = 'black')
ax[0].spines[["top", "right"]].set_visible(False)

ax[1].axes.bar(timeseries.index, timeseries["WL"], color = '#ffffff00', ec = 'red', align = 'edge', linewidth = 2.5, width = width)
ax[1].xaxis.set_visible(False)
ax[1].set_yticks([0,-1,-2,-3,-4], labels =["No Warning", "Very Low", "Low", "Moderate", "High"], fontsize = 15)
ax[1].set_ylabel("Landslide Warning Levels", fontsize = 18)
ax[1].axhline(y = threshold_wl+0.05, linewidth = 0.9, linestyle = '-.', color = 'black')
ax[1].spines[["right", "bottom"]].set_visible(False)

plt.autoscale()
#plt.savefig('path..._' + name_time + '.png', bbox_inches='tight', bbox_extra_artists = (name_date,), dpi=600)
plt.show()

# DURATION-MATRIX
wl_num = 5
le_num = 6
limit_wl = (threshold_wl + 1) * (-1)
limit_le = threshold_le - 1
dur_matrix = np.zeros((wl_num, le_num)) # matrix
for k in range(len(data_wl)):
    dur_matrix[timeline_wl[k]*(-1), timeline_le[k]] = dur_matrix[timeline_wl[k]*(-1), timeline_le[k]] + 1
FP = 0
TP = 0
FN = 0
TN = 0
# CALCULATE TN-FP-TP-FN
for l in range(0, limit_wl + 1): # add one at the end of every range
    TN = TN + dur_matrix[l, limit_le]

for m in range(limit_wl + 1, wl_num):
    FP = FP + dur_matrix [m, limit_le]

for n in range(limit_le + 1, le_num):
    for p in range(limit_wl + 1, wl_num):
        TP = TP + dur_matrix[p, n]

for o in range(limit_le + 1, le_num):
    for q in range(0, limit_wl+1):
        FN = FN + dur_matrix[q, o]
print("Warning Classification Criterion\nTP = " + str(TP) + "\nTN = " + str(TN) + "\nFP = " + str(FP) + "\nFN = " + str(FN))

# CALCULATE GRADE OF CORRECTNESS
limit_y = 1
limit_o = 2
limit_r = 3
g_value = TN + TP # green
y_value = 0 # yellow
o_value = 0 # orange
r_value = 0 # red
# CALCULATE YELLOW-ORANGE-RED
for r in range(1, limit_y +1 ):
    for s in range(0, limit_wl + 1):
        y_value = y_value + dur_matrix[s, r]

for t in range(limit_y + 1, limit_o +1 ):
    for u in range(0, limit_wl + 1):
        o_value = o_value + dur_matrix[u, t]
o_value = o_value + dur_matrix[3,0] # additional value

for v in range(limit_o + 1, wl_num +1):
    for w in range(0, limit_wl + 1):
        r_value = r_value + dur_matrix[w, v]
r_value = r_value + dur_matrix[4,0] # additional value
print("Grade of Correctness Criterion\nG = " + str(g_value) + "\nY = " + str(y_value) + "\nO = " + str(o_value) + "\nR = " + str(r_value))

# CALCULATE PERFORMANCE INDICATORS
I_eff = (TN + TP) / (float(number_days.days) - dur_matrix[0,0]) # exclude when no-no situation
HR_L = TP / (TP + FN)
PP_W = TP / (TP + FP)
TS = TP / (TP + FN + FP)
OR = (TP + TN) / (FN + FP)
MR = 1 - I_eff
RMA = 1 - HR_L
RFA = 1 - PP_W
ER = (o_value + r_value) / (float(number_days.days) - dur_matrix[0,0]) # exclude when no-no situation
print("Performance Indicators\nIeff = " + str(I_eff) + "\nHR_L = " + str(HR_L) + "\nPP_W = " + str(PP_W) + "\nTS = " + str(TS)
      + "\nOR = " + str(OR) + "\nMR = " + str(MR) +"\nRMW = " + str(RMA) + "\nRFW = " + str(RFA) + "\nER = " + str(ER))

# STACKED BAR GRAPHS
name_bar = 'ex2' # define name to save it
cp_g = (TN+TP) / float(number_days.days) * 100 # correct predictions
#tp_g = TP / float(number_days.days) * 100
fn_g = FN / float(number_days.days) * 100
fp_g = FP / float(number_days.days) * 100
r_g = r_value / float(number_days.days) * 100
y_g = y_value / float(number_days.days) * 100
o_g = o_value / float(number_days.days) * 100
g_g = g_value / float(number_days.days) * 100

fig, ax = plt.subplots(1, 2, figsize =(5, 6))
fig.suptitle("Performance Assessment Results", fontsize = 18)

ax[0].axes.bar(1, cp_g, color = '#C1C1C1', ec = 'black', width = 0.1)
cp_l = Line2D([0], [0], color='#C1C1C1', marker='s', mec = 'black', markersize=6, lw=0)
#ax[0].axes.bar(1, tn_g, bottom = tp_g, color = 'yellow', ec = 'black', width = 0.2)
#tn_l = Line2D([0], [0], color='yellow', marker='s', mec = 'black', markersize=5, lw=0)
ax[0].axes.bar(1, fp_g, bottom = cp_g, color = '#8E8E8E', ec = 'black', width = 0.1)
fp_l = Line2D([0], [0], color='#8E8E8E', marker='s', mec = 'black', markersize=6, lw=0)
ax[0].axes.bar(1, fn_g, bottom = cp_g+fp_g, color = '#5B5B5B', ec = 'black', width = 0.1)
fn_l = Line2D([0], [0], color='#5B5B5B', marker='s', mec = 'black', markersize=6, lw=0)
ax[0].xaxis.set_visible(False)
ax[0].set_yticks([0,10,20,30,40,50,60,70,80,90,100], labels =["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], fontsize = 11)
ax[0].set_ylabel("Warning Classification Criterion", fontsize = 14)
handles_1 = [fn_l, fp_l, cp_l] #[cp_l, fp_l, fn_l]
labels_1 = ["False Negative","False Positive","Correct Predictions"] #["Correct Predictions", "False Positive", "False Negative"]
ax[0].legend(handles=handles_1, labels = labels_1, fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox = True, shadow = True)
ax[0].spines[["top", "right"]].set_visible(False)

ax[1].axes.bar(1, r_g, color = '#FFFACD', ec = 'black', width = 0.1)
g_l = Line2D([0], [0], color='#FFFACD', marker='s', mec = 'black', markersize=6, lw=0)
ax[1].axes.bar(1, y_g, bottom = r_g, color = '#EEE685', ec = 'black', width = 0.1) #EEE9BF
y_l = Line2D([0], [0], color='#EEE685', marker='s', mec = 'black', markersize=6, lw=0) #CDC9A5
ax[1].axes.bar(1, o_g, bottom = r_g+y_g, color = '#CDC673', ec = 'black', width = 0.1)
o_l = Line2D([0], [0], color='#CDC673', marker='s', mec = 'black', markersize=6, lw=0)
ax[1].axes.bar(1, r_g, bottom = r_g+y_g+o_g, color = '#8B864E', ec = 'black', width = 0.1)
r_l = Line2D([0], [0], color='#8B864E', marker='s', mec = 'black', markersize=6, lw=0)
ax[1].xaxis.set_visible(False)
ax[1].set_yticks([0,10,20,30,40,50,60,70,80,90,100], labels =["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], fontsize = 11)
ax[1].set_ylabel("Grade of Correctness Criterion", fontsize = 14)
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position("right")
handles_2 = [r_l, o_l, y_l, g_l] #[g_l, y_l, o_l, r_l]
labels_2 = ["Worst errors", "Significant errors", "Minor errors","Best response"] #["Best response", "Minor errors", "Significant errors", "Worst errors"]
ax[1].legend(handles=handles_2, labels = labels_2, fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox = True, shadow = True)
ax[1].spines[["left", "top"]].set_visible(False)

plt.tight_layout()
#plt.savefig('path..._' + name_bar + '.png', dpi=500)
plt.show()

# BOTH GRAPHS (SUCCESS AND ERROR)
name_star = 'ex2' # define the name to save it
fig, ax = plt.subplots(1, 2, figsize =(7, 6))
fig.suptitle("Success and Error Analysis", fontsize = 19)

i_l = Line2D([0], [0], color='#104E8B', marker='o', markersize=6, lw=0, mec = 'black')
hr_l = Line2D([0], [0], color='#1C86EE', marker='o', markersize=6, lw=0, mec = 'black')
ts_l = Line2D([0], [0], color='#009ACD', marker='o', markersize=6, lw=0, mec = 'black')
pp_l = Line2D([0], [0], color='#00BFFF', marker='o', markersize=6, lw=0, mec = 'black')
ax[0].set(xlim = (-1.05, 1.05), ylim = (-1.05, 1.05))
ax[0].plot([1,0], [0,1], '-', linewidth=0.5, color='black')
ax[0].plot([1,0], [0,-1], '-', linewidth=0.5, color='black')
ax[0].plot([0,-1], [-1,0], '-', linewidth=0.5, color='black')
ax[0].plot([-1,0], [0,1], '-', linewidth=0.5, color='black')
ax[0].plot(0, I_eff, 'o', color = '#104E8B', mec = 'black', markersize = 8)
ax[0].plot(HR_L, 0, 'o', color = '#1C86EE', mec = 'black', markersize = 8)
ax[0].plot(-TS, 0, 'o', color = '#009ACD', mec = 'black', markersize = 8)
ax[0].plot(0, -PP_W, 'o', color = '#00BFFF', mec = 'black', markersize = 8)
ax[0].xaxis.set_visible(False)
ax[0].yaxis.set_visible(False)
ax[0].text(0,-1.20, r'$PP_W$', fontsize = 11, ha = 'center')
ax[0].text(0,1.13, r'$I_{eff}$', fontsize = 11, ha = 'center')
ax[0].text(-1.23, 0, "TS", fontsize = 11, va = 'center')
ax[0].text(1.13, 0, r'$HR_L$', fontsize = 11, va = 'center')
ax[0].plot([HR_L,0], [0,I_eff], '--', linewidth=1, color='black')
ax[0].plot([HR_L,0], [0,-PP_W], '--', linewidth=1, color='black')
ax[0].plot([-TS,0], [0,-PP_W],'--', linewidth=1, color='black')
ax[0].plot([-TS,0], [0,I_eff], '--', linewidth=1, color='black')
handles_3 = [i_l, hr_l, ts_l, pp_l]
labels_3 = [r'$I_{eff}$ = Efficiency index',r'$HR_L$ = Hit rate',"TS = Threat score", r'$PP_W$ = Predictive power']
ax[0].legend(handles=handles_3, labels = labels_3, fontsize=10, loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox = True, shadow = True)
ax[0].axhline(y = 0, xmin=-1, xmax=1, linewidth = 0.5, linestyle = '-', color = 'black')
ax[0].axvline(x = 0, ymin=-1, ymax=1, linewidth = 0.5, linestyle = '-', color = 'black')
ax[0].spines[["top", "right", "bottom", "left"]].set_visible(False)

mr_l = Line2D([0], [0], color='#008000', marker='o', markersize=6, lw=0, mec = 'black')
rma_l = Line2D([0], [0], color='#00CD00', marker='o', markersize=6, lw=0, mec = 'black')
er_l = Line2D([0], [0], color='#00FF00', marker='o', markersize=6, lw=0, mec = 'black')
rfa_l = Line2D([0], [0], color='#ADFF2F', marker='o', markersize=6, lw=0, mec = 'black')
ax[1].set(xlim = (-1.05, 1.05), ylim = (-1.05, 1.05))
ax[1].plot([1,0], [0,1], '-', linewidth=0.5, color='black')
ax[1].plot([1,0], [0,-1], '-', linewidth=0.5, color='black')
ax[1].plot([0,-1], [-1,0], '-', linewidth=0.5, color='black')
ax[1].plot([-1,0], [0,1], '-', linewidth=0.5, color='black')
ax[1].plot(0, MR, 'o', color = '#008000', mec = 'black', markersize = 8)
ax[1].plot(RMA, 0, 'o', color = '#00CD00', mec = 'black', markersize = 8)
ax[1].plot(-ER, 0, 'o', color = '#00FF00', mec = 'black', markersize = 8)
ax[1].plot(0, -RFA, 'o', color = '#ADFF2F', mec = 'black', markersize = 8)
ax[1].xaxis.set_visible(False)
ax[1].yaxis.set_visible(False)
ax[1].text(0,-1.20, r'$R_{FW}$', fontsize = 11, ha = 'center')
ax[1].text(0,1.13, "MR", fontsize = 11, ha = 'center')
ax[1].text(-1.23, 0, "ER", fontsize = 11, va = 'center')
ax[1].text(1.13, 0, r'$R_{MW}$', fontsize = 11, va = 'center')
ax[1].plot([RMA,0], [0,MR], '--', linewidth=1, color='black')
ax[1].plot([RMA,0], [0,-RFA], '--', linewidth=1, color='black')
ax[1].plot([-ER,0],[0,-RFA], '--', linewidth=1, color='black')
ax[1].plot([-ER,0], [0,MR], '--', linewidth=1, color='black')
handles_4 = [mr_l, rma_l, er_l, rfa_l]
labels_4 = ["MR = Misclassification rate",r'$R_{MW}$ = Missed warning rate',"ER = Error rate", r'$R_{FW}$ = False warning rate']
ax[1].legend(handles=handles_4, labels = labels_4, fontsize=10, loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox = True, shadow = True)
ax[1].axhline(y = 0, xmin = -1, xmax=1, linewidth = 0.5, linestyle = '-', color = 'black')
ax[1].axvline(x = 0, ymin=-1, ymax=1, linewidth = 0.5, linestyle = '-', color = 'black')
ax[1].spines[["left", "top", "right", "bottom"]].set_visible(False)

plt.tight_layout(pad = 2)
#plt.savefig('path..._' + name_star + '.png', dpi=500)
plt.show()
