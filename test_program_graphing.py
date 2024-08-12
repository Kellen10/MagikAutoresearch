import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import scienceplots


degrees_of_coverage = [2, 3, 4]

# 50x50 100 sensors, rs = 10 rc = 20
one_GAMA_active_sensors = [40.7, 57, 72.9] 
one_MASS_active_sensors = [(32+33+35+34+35+33+33+34+34+35)/10,
                           (46+51+50+50+48+48+51+47+48+49)/10, 
                           (65+62+65+67+65+68+62+64+64+64)/10]

# 100x100 300 sensors, rs = 15 rc = 30
two_GAMA_active_sensors = [81, 115, 147] 
two_MASS_active_sensors = [(66+63+62+61+61+61+61+60+59+62)/10, 
                           (81+85+88+83+89+85+89+90+85+86)/10, 
                           (113+112+113+114+116+114+117+111+116+114)/10]

# 150x150 500 sensors, rs = 20, rc = 40
three_GAMA_active_sensors = [125, 160, 211] 
three_MASS_active_sensors = [(84+84+82+86+88+83+82+82+84+86)/10, 
                             (120+118+121+122+116+119+117+122+119+115)/10, 
                             (151+152+152+159+150+150+154+149+147+148)/10]
# sensing range tests
sensing_ranges = [20, 30, 40, 50, 60]
four_GAMA_active_sensors = [67, 33, 20, 13, 10]
four_MASS_active_sensors = [(50+50+49+50+49+50+49+50+54+53)/10, 
                            (24+26+26+26+25+25+26+24+25+25)/10, 
                            (17+16+16+15+16+17+16+17+15+17)/10, 
                            (11+11+12+11+12+12+11+11+12+12)/10, 
                            (8+8+8+8+7+8+9+8+8+9)/10
                            ]
bar_width = 0.35
r1 = np.arange(len(degrees_of_coverage))
r2 = [x + bar_width for x in r1]
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

axs[0, 0].bar(r1, one_MASS_active_sensors, color='red', width=bar_width, edgecolor='grey', label=r'MAGI$\it{k}$')
axs[0, 0].bar(r2, one_GAMA_active_sensors, color='midnightblue', width=bar_width, edgecolor='grey', label='GAMA')
axs[0, 0].set_xlabel('Degree of Coverage', fontweight='bold')
axs[0, 0].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[0, 0].set_xticks([r + bar_width/2 for r in range(len(degrees_of_coverage))])
axs[0, 0].set_xticklabels(degrees_of_coverage)
axs[0, 0].set_title(f'a. 50x50 RoI, $n = 100$, {r"$r_s = 10$"}, {r"$r_c = 20$"}')
axs[0, 0].legend()

axs[0, 1].bar(r1, two_MASS_active_sensors, color='red', width=bar_width, edgecolor='grey', label=r'MAGI$\it{k}$')
axs[0, 1].bar(r2, two_GAMA_active_sensors, color='midnightblue', width=bar_width, edgecolor='grey', label='GAMA')
axs[0, 1].set_xlabel('Degree of Coverage', fontweight='bold')
axs[0, 1].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[0, 1].set_xticks([r + bar_width/2 for r in range(len(degrees_of_coverage))])
axs[0, 1].set_xticklabels(degrees_of_coverage)
axs[0, 1].set_title(f'b. 100x100 RoI, $n = 300$, {r"$r_s = 15$"}, {r"$r_c = 30$"}')
axs[0, 1].legend()

axs[1, 0].bar(r1, three_MASS_active_sensors, color='red', width=bar_width, edgecolor='grey', label=r'MAGI$\it{k}$')
axs[1, 0].bar(r2, three_GAMA_active_sensors, color='midnightblue', width=bar_width, edgecolor='grey', label='GAMA')
axs[1, 0].set_xlabel('Degree of Coverage', fontweight='bold')
axs[1, 0].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[1, 0].set_xticks([r + bar_width/2 for r in range(len(degrees_of_coverage))])
axs[1, 0].set_xticklabels(degrees_of_coverage)
axs[1, 0].set_title(f'c. 150x150 RoI, $n = 500$, {r"$r_s = 20$"}, {r"$r_c = 40$"}')
axs[1, 0].legend()

axs[1, 1].plot(sensing_ranges, four_MASS_active_sensors, color='red', label=r'MAGI$\it{k}$')
axs[1, 1].plot(sensing_ranges, four_GAMA_active_sensors, color='midnightblue', label='GAMA')
axs[1, 1].set_xlabel('Sensing Range', fontweight='bold')
axs[1, 1].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[1, 1].set_xticks(sensing_ranges)
axs[1, 1].set_xticklabels(sensing_ranges)
axs[1, 1].set_title(r'd. 100x100 RoI, $n = 300$, $\it{k} = 3$, $r_c = 2r_s$')
axs[1, 1].legend()

plt.tight_layout()
plt.show()


# communication range tests
communication_ranges = [10, 15, 20, 25, 30]
bar_width = 0.5
r1 = np.arange(len(communication_ranges))
r2 = [x + bar_width for x in r1]

k1_active_sensors = [(74+77+79+76+77+81+84+76+75+83)/10,
                     (47+45+49+47+49+47+47+49+48+47)/10,
                     (35+35+38+38+33+37+35+35+35+36)/10,
                     (32+32+36+35+31+34+32+30+33+32)/10,
                     (34+32+34+33+31+31+35+34+32+34)/10]

five_MASk_active_sensors = [(92+88+91+89+88+93+88+93+94+93)/ 10,
                            (67+61+59+62+67+64+62+63+68+63)/ 10,
                            (62+63+60+61+60+60+62+59+62+60)/ 10,
                            (63+61+61+62+60+65+58+61+62+61)/ 10,
                            (62+66+64+58+59+63+62+60+61+61)/ 10]

six_MASk_active_sensors = [(108+107+103+107+107+103+101+101+104+104)/ 10,
                            (85+86+87+88+89+87+86+86+87+94)/ 10,
                            (90+87+87+91+89+87+85+85+84+91)/ 10,
                            (90+86+88+83+87+87+89+88+87+86)/ 10,
                            (89+89+88+85+88+88+89+86+85+92)/ 10]

seven_MASk_active_sensors = [(122+126+124+123+122+123+120+124+121+121)/ 10,
                            (114+114+116+115+119+113+116+113+114+112)/ 10,
                            (116+114+110+115+117+112+114+114+115+117)/ 10,
                            (111+114+112+110+111+116+112+115+113+116)/ 10,
                            (118+114+112+114+115+114+119+111+114+115)/ 10]

k5_active_sensors = [(138+142+144+137+141+145+144+147+144+142)/10,
                     (138+137+144+137+136+138+139+140+140+142)/10,
                     (139+140+137+138+143+141+136+139+138+140)/10,
                     (141+139+145+137+135+138+141+139+140+142)/10,
                     (140+141+141+137+137+145+137+141+141+139)/10]

eight_MASk_active_sensors = [(92+88+91+89+88+93+88+93+94+93)/ 10,
                            (67+61+59+62+67+64+62+63+68+63)/ 10,
                            (62+63+60+61+60+60+62+59+62+60)/ 10,
                            (63+61+61+62+60+65+58+61+62+61)/ 10,
                            (62+66+64+58+59+63+62+60+61+61)/ 10]

nine_MASk_active_sensors = [(108+107+103+107+107+103+101+101+104+104)/ 10,
                            (85+86+87+88+89+87+86+86+87+94)/ 10,
                            (90+87+87+91+89+87+85+85+84+91)/ 10,
                            (90+86+88+83+87+87+89+88+87+86)/ 10,
                            (89+89+88+85+88+88+89+86+85+92)/ 10]

ten_MASk_active_sensors = [(122+126+124+123+122+123+120+124+121+121)/ 10,
                            (114+114+116+115+119+113+116+113+114+112)/ 10,
                            (116+114+110+115+117+112+114+114+115+117)/ 10,
                            (111+114+112+110+111+116+112+115+113+116)/ 10,
                            (118+114+112+114+115+114+119+111+114+115)/ 10]


fig, axs = plt.subplots(3, 2, figsize=(12, 16))

axs[0, 0].bar(r1, k1_active_sensors, color='red', width=bar_width, edgecolor='grey')
axs[0, 0].set_xlabel('Communication Range', fontweight='bold')
axs[0, 0].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[0, 0].set_xticks(r1)
axs[0, 0].set_xticklabels([r'$\frac{2}{3}r_s$', r'$r_s$', r'$\frac{4}{3}r_s$', r'$\frac{5}{3}r_s$', r'$2r_s$']) 
axs[0, 0].set_title(r'a. $\it{k} = 1$,  RoI = 100x100, $n = 300$, $r_s = 15$')

axs[0, 1].bar(r1, five_MASk_active_sensors, color='red', width=bar_width, edgecolor='grey')
axs[0, 1].set_xlabel('Communication Range', fontweight='bold')
axs[0, 1].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[0, 1].set_xticks(r1)
axs[0, 1].set_xticklabels([r'$\frac{2}{3}r_s$', r'$r_s$', r'$\frac{4}{3}r_s$', r'$\frac{5}{3}r_s$', r'$2r_s$']) 
axs[0, 1].set_title(r'b. $\it{k} = 2$, RoI = 100x100, $n = 300$, $r_s = 15$')

axs[1, 0].bar(r1, six_MASk_active_sensors, color='red', width=bar_width, edgecolor='grey')
axs[1, 0].set_xlabel('Communication Range', fontweight='bold')
axs[1, 0].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[1, 0].set_xticks(r1)
axs[1, 0].set_xticklabels([r'$\frac{2}{3}r_s$', r'$r_s$', r'$\frac{4}{3}r_s$', r'$\frac{5}{3}r_s$', r'$2r_s$']) 
axs[1, 0].set_title(r'c. $\it{k} = 3$,  RoI = 100x100, $n = 300$, $r_s = 15$')

axs[1, 1].bar(r1, seven_MASk_active_sensors, color='red', width=bar_width, edgecolor='grey')
axs[1, 1].set_xlabel('Communication Range', fontweight='bold')
axs[1, 1].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[1, 1].set_xticks(r1)
axs[1, 1].set_xticklabels([r'$\frac{2}{3}r_s$', r'$r_s$', r'$\frac{4}{3}r_s$', r'$\frac{5}{3}r_s$', r'$2r_s$']) 
axs[1, 1].set_title(r'd. $\it{k} = 4$,  RoI = 100x100, $n = 300$, $r_s = 15$')

axs[2, 0].bar(r1, k5_active_sensors, color='red', width=bar_width, edgecolor='grey')
axs[2, 0].set_xlabel('Communication Range', fontweight='bold')
axs[2, 0].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[2, 0].set_xticks(r1)
axs[2, 0].set_xticklabels([r'$\frac{2}{3}r_s$', r'$r_s$', r'$\frac{4}{3}r_s$', r'$\frac{5}{3}r_s$', r'$2r_s$']) 
axs[2, 0].set_title(r'e. $\it{k} = 5$,  RoI = 100x100, $n = 300$, $r_s = 15$')

axs[2, 1].plot(communication_ranges, k1_active_sensors, color='red', linewidth=2, label=r'$\it{k}=1$')
axs[2, 1].plot(communication_ranges, eight_MASk_active_sensors, color='red', linestyle='-.', label=r'$\it{k}=2$')
axs[2, 1].plot(communication_ranges, nine_MASk_active_sensors, color='red', linestyle='--', linewidth=2, label=r'$\it{k}=3$')
axs[2, 1].plot(communication_ranges, ten_MASk_active_sensors, color='red', linestyle=':', linewidth=2, label=r'$\it{k}=4$')
axs[2, 1].plot(communication_ranges, k5_active_sensors, color='red', linestyle=(0, (5, 10)), linewidth=2, label=r'$\it{k}=5$')
axs[2, 1].set_xlabel('Communication Range', fontweight='bold')
axs[2, 1].set_ylabel('Number of Active Sensors', fontweight='bold')
axs[2, 1].set_xticks([10, 15, 20, 25, 30]) 
axs[2, 1].set_xticklabels([r'$\frac{2}{3}r_s$', r'$r_s$', r'$\frac{4}{3}r_s$', r'$\frac{5}{3}r_s$', r'$2r_s$']) 
axs[2, 1].set_title(r'f. RoI = 100x100, $n = 300$, $r_s$ = 15')
axs[2, 1].legend()

plt.tight_layout()
plt.show()


active_sensors_pre = [(13, 23), (45, 16), (26, 31), (10, 11), (7, 35), (0, 31), (11, 21), (46, 36), (34, 35), (44, 36), 
                      (0, 41), (50, 12), (6, 48), (34, 38), (9, 4), (12, 24), (40, 9), (30, 45), (2, 34), (17, 23), 
                      (45, 41), (33, 18), (34, 32), (1, 8), (15, 16), (34, 27), (13, 34), (48, 1), (35, 5), (24, 18), 
                      (13, 45), (38, 37), (17, 34), (18, 22), (48, 25), (10, 18), (22, 8), (42, 19), (37, 36), (17, 31), 
                      (8, 21), (50, 13), (5, 4), (48, 8), (36, 8), (4, 18), (20, 9), (8, 8), (7, 38), (43, 50), (32, 35), 
                      (41, 3), (28, 37), (39, 16), (41, 25), (6, 4), (28, 10), (21, 30), (14, 42), (27, 29), (23, 17), 
                      (40, 3), (34, 46), (12, 47), (15, 41), (23, 34), (13, 46), (31, 28), (12, 18), (2, 43), (10, 24), 
                      (28, 1), (6, 6), (10, 20), (44, 41), (22, 14), (38, 38), (19, 43), (45, 34), (39, 10), (3, 4),
                        (45, 6), (47, 32), (25, 0), (41, 42), (27, 12), (10, 35), (14, 26), (0, 33), (12, 22), (1, 40), 
                        (4, 6), (35, 4), (25, 8), (17, 38), (20, 0), (3, 12), (43, 46), (23, 49), (15, 46)]

active_sensors_post = [(21, 30), (48, 8), (2, 43), (36, 8), (3, 12), (41, 25), (10, 18), (2, 34), (45, 34), (42, 19), (17, 38), 
                       (0, 31), (5, 4), (35, 5), (34, 35), (19, 43), (17, 34), (4, 18), (9, 4), (12, 22), (48, 1), (30, 45), 
                       (25, 0), (1, 40), (13, 46), (27, 29), (34, 46), (27, 12), (45, 41), (20, 0), (34, 27), (22, 14), (43, 50),
                         (50, 12), (50, 12), (45, 41), (5, 4), (48, 1), (13, 46), (19, 43), (4, 18), (22, 14), (27, 29), (17, 38),
                           (9, 4), (34, 27), (17, 34), (42, 19), (27, 12), (48, 8), (2, 43), (0, 31), 
                       (35, 5), (41, 25), (30, 45), (25, 0), (34, 46), (34, 35), (45, 34), (3, 12), (2, 34), (12, 22), 
                       (20, 0), (21, 30), (1, 40), (43, 50), (36, 8), (10, 18)]

inactive_sensors_post = []
active_sensor_count = 100
for pos in active_sensors_pre:
    if pos not in active_sensors_post:
        active_sensor_count -= 1
        inactive_sensors_post.append(pos)

print(active_sensor_count)

inactive_sensors_pre = []  

x_active_pre, y_active_pre = zip(*active_sensors_pre) if active_sensors_pre else ([], [])
x_active_post, y_active_post = zip(*active_sensors_post) if active_sensors_post else ([], [])
x_inactive_pre, y_inactive_pre = zip(*inactive_sensors_pre) if inactive_sensors_pre else ([], [])
x_inactive_post, y_inactive_post = zip(*inactive_sensors_post) if inactive_sensors_post else ([], [])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 16))

base_station_x, base_station_y = 25, 25
base_station_size = 1  
def add_base_station(ax, x, y, size, color):
    square = plt.Rectangle((x - size / 2, y - size / 2), size, size, color=color, label='Base station')
    ax.add_patch(square)


ax1.scatter(x_active_pre, y_active_pre, color='red', label='ON sensor')
ax1.scatter(x_inactive_pre, y_inactive_pre, edgecolor='black', facecolor='none', label='OFF sensor')
add_base_station(ax1, base_station_x, base_station_y, base_station_size, 'green')
ax1.set_xlim(0, 50)
ax1.set_ylim(0, 50)
ax1.set_title(r'$\it{ON}$/$\it{OFF}$ Sensors Before MAGI$\it{k}$')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, handlelength=0.7)

ax2.scatter(x_active_post, y_active_post, color='red', label='ON sensor')
ax2.scatter(x_inactive_post, y_inactive_post, edgecolor='black', facecolor='none', label='OFF sensor')
add_base_station(ax2, base_station_x, base_station_y, base_station_size, 'green')
ax2.set_xlim(0, 50)
ax2.set_ylim(0, 50)
ax2.set_title(r'$\it{ON}$/$\it{OFF}$ Sensors Post MAGI$\it{k}$')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, handlelength=0.7)

plt.tight_layout()
plt.show()


