import os
import xarray as xr
import time
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

'''
    Line_Bar Chart
'''

class Display_Plot_BarLine(object):
    def __init__(self) -> None:
        pass
    def BarlineInit1(file):
        var_input = 'rmse of line 0529'
        colors = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#FC8452', '#73C0DE', '#3BA272', '#9A60B4']
        #Data from the Computation in nc_py.compute_nc.compute_data
        gpp_data = {
            'SP_82': (1.9, 1.86, 1.82, 1.81, 1.8, 1.79,),
            'SP_87': (1.57, 1.27, 1.23, 1.21, 1.21, 1.2,
                      ),
            'SP_02': (1.72,
                      1.56,
                      1.51,
                      1.49,
                      1.47,
                      1.47,
                      ),
            'SP_82-87': (1.41,
                         1.29,
                         1.28,
                         1.28,
                         1.28,
                         ),
            'SP_82-02': (1.56,
                         1.51,
                         1.5,
                         1.5,
                         1.5,
                         )
        }
        lh_data = {
            'SP_82': (17.03,
                      16.46,
                      16.06,
                      15.93,
                      15.87,
                      15.83,
                      ),
            'SP_87': (15.73,
                      13.71,
                      13.59,
                      13.54,
                      13.54,
                      13.54,

                      ),
            'SP_02': (16.52,
                      15.35,
                      14.89,
                      14.72,
                      14.64,
                      14.6,

                      ),
            'SP_82-87': (14.09,
                         13.51,
                         13.51,
                         13.5,
                         13.51

                         ),
            'SP_82-02': (15.31,
                         14.96,
                         14.91,
                         14.9,
                         14.89,

                         )
        }
        x = [1, '10', "20", "30", "40", "50"]
        x1 = [1,  '5', "10", "15", "20", ]

        a1 = np.arange(len(x))
        a2 = np.arange(len(x1))
        width = 0.2  # the width of the bars
        multiplier = 0

        fig, ax = plt.subplots(2, 2, figsize=(16, 9))
        k, l = 0, 0
        for attribute, measurement in gpp_data.items():
            if attribute in ['SP_82', 'SP_87', 'SP_02']:
                ax[k, l].plot(a1, measurement, marker='o', color=colors[multiplier], label=attribute,
                              linestyle='-', )
                ax[k, l].set_ylabel('The RMSE of GPP (gC/m2/day)', fontsize=16)
                ax[k, l].set_xlabel('Cycles', fontsize=16, rotation=0, labelpad=0, loc='center')
                ax[k, l].set_xticks(a1, x)
                y_ticks = [0, 1, 2, 3]
                ax[k, l].legend(loc='lower right', ncols=3, fontsize=12)
                ax[k, l].set_yticks(y_ticks)
                ax[k, l].tick_params(axis='x', labelsize=16)
                ax[k, l].tick_params(axis='y', labelsize=16)
                ax[k, l].axhline(0, color='white', linewidth=1)
                # Bar
                # offset = width * multiplier
                # offset_list = [offset] * len(a1)
                # new_x = [x_val + offset_val for x_val, offset_val in zip(a1, offset_list)]
                # rects = ax[k, l].bar(new_x, measurement, width, label=attribute, color=colors[multiplier])
                # ax[k, l].bar_label(rects, padding=3)

            if attribute not in ['SP_82', 'SP_87', 'SP_02']:
                l = 1
                ax[k, l].plot(a2, measurement, marker='o', color=colors[multiplier], label=attribute,
                              linestyle='-', )
                ax[k, l].set_ylabel('The RMSE of GPP (gC/m2/day)', fontsize=16)
                ax[k, l].set_xlabel('Cycles', fontsize=16, rotation=0, labelpad=0, loc='center')
                ax[k, l].set_xticks(a2, x1)
                y_ticks = [0, 1, 2, 3]
                ax[k, l].legend(loc='lower right', ncols=3, fontsize=12)
                ax[k, l].set_yticks(y_ticks)
                ax[k, l].tick_params(axis='x', labelsize=16)
                ax[k, l].tick_params(axis='y', labelsize=16)
                ax[k, l].axhline(0, color='white', linewidth=1)
                # Bar
                # offset = width * multiplier
                # offset_list = [offset] * len(a2)
                # new_x = [x_val + offset_val for x_val, offset_val in zip(a2, offset_list)]
                # rects = ax[k, l].bar(new_x, measurement, width, label=attribute, color=colors[multiplier])
                # ax[k, l].bar_label(rects, padding=3)

            multiplier += 1
        multiplier = 0
        k, l = 1, 0
        for attribute, measurement in lh_data.items():
            if attribute in ['SP_82', 'SP_87', 'SP_02']:
                ax[k, l].plot(a1, measurement, marker='o', color=colors[multiplier], label=attribute,
                              linestyle='-', )
                ax[k, l].set_ylabel('The RMSE of LH (W/m2)', fontsize=16)
                ax[k, l].set_xlabel('Cycles', fontsize=16, rotation=0, labelpad=0, loc='center')

                ax[k, l].set_xticks(a1, x)
                y_ticks = [0, 8, 16, 24]
                ax[k, l].legend(loc='lower right', ncols=3, fontsize=12)
                ax[k, l].set_yticks(y_ticks)
                ax[k, l].tick_params(axis='x', labelsize=16)
                ax[k, l].tick_params(axis='y', labelsize=16)
                ax[k, l].axhline(0, color='white', linewidth=1)
                # Bar
                # offset = width * multiplier
                # offset_list = [offset] * len(a1)
                # new_x = [x_val + offset_val for x_val, offset_val in zip(a1, offset_list)]
                # rects = ax[k, l].bar(new_x, measurement, width, label=attribute, color=colors[multiplier])
                # ax[k, l].bar_label(rects, padding=3)

            if attribute not in ['SP_82', 'SP_87', 'SP_02']:
                l = 1
                ax[k, l].plot(a2, measurement, marker='o', color=colors[multiplier], label=attribute,
                              linestyle='-', )
                ax[k, l].set_ylabel('The RMSE of LH (W/m2)', fontsize=16)
                ax[k, l].set_xlabel('Cycles', fontsize=16, rotation=0, labelpad=0, loc='center')

                ax[k, l].set_xticks(a2, x1)
                y_ticks = [0, 8, 16, 24]
                ax[k, l].legend(loc='lower right', ncols=3, fontsize=12)
                ax[k, l].set_yticks(y_ticks)
                ax[k, l].tick_params(axis='x', labelsize=16)
                ax[k, l].tick_params(axis='y', labelsize=16)
                ax[k, l].axhline(0, color='white', linewidth=1)
                # Bar
                # offset = width * multiplier
                # offset_list = [offset] * len(a2)
                # new_x = [x_val + offset_val for x_val, offset_val in zip(a2, offset_list)]
                # rects = ax[k, l].bar(new_x, measurement, width, label=attribute, color=colors[multiplier])
                # ax[k, l].bar_label(rects, padding=3)
            multiplier += 1

        title_text = plt.gca().get_title()
        plt.title(title_text, fontsize=16)

        plt.savefig(var_input, dpi=600)
        plt.show()


if __name__ == '__main__':
    Display_Plot_BarLine().BarlineInit1()

