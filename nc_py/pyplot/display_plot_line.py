import os
import xarray as xr
import time
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib
import random
from nc_py.out_input import OutInput
from matplotlib.patches import FancyBboxPatch
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import FormatStrFormatter
import math
import nc_py.pyplot.color_json as cjson

'''
    折线图
'''

color_strings = ['#3399FF', '#1767e3', '#989ba8', '#9ee0c1', '#b89889', '#2cae34', '#7c92eb', '#a17c44',
                 '#5ad487',
                 '#70dee7', '#65e846', '#aff7c3', '#05df82', '#bbabdb', '#89a52f', '#c2578d', '#f6e5e4',
                 '#3aaec3', '#a0cacd', '#776f64', '#2bacf7', '#02794b', '#549f5b', '#be8e1d', '#d803f0',
                 '#85c6b5', '#166fa4', '#95ce12', '#fdcd57', '#584748', '#bd260f', '#932f67', '#870298',
                 '#fdcb51', '#5a85bb', '#4be4a5', '#c491e3', '#d1768d', '#2f49ae', '#db4824', '#120cc9',
                 '#c8fb49', '#7f4d55', '#b51f20', '#cc8ec6', '#284d89', '#da3f6c', '#a23aa0', '#c5c1f4',
                 '#eacd9e', '#f5277d']
color_strings = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#FC8452', '#73C0DE', '#3BA272', '#9A60B4']
class Display_Plot_Line(object):
    def __init__(self) -> None:
        # matplotlib.use("Agg")
        # self.color_strings = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#FC8452', '#73C0DE', '#3BA272', '#9A60B4']
        self.marker_style = ['o', '*', 's', '^', 'd', '>', "<", "v", 'p', "P", "H"]
        self.title_fontsize = 30
        # self.color_strings = cjson.get_color()["10"]["color"]
        self.color_strings = ['#5470C6', '#91CC75', '#FAC858', '#EE6666',"#9999ff","#CC00CC"]
        pass

    def set_config(self, pl):
        # pl.xticks(fontsize=20)  # 设置 x 轴刻度字体大小
        # pl.yticks(fontsize=20)  # 设置 y 轴刻度字体大小
        pl.xticks(fontsize=30)  # 设置 x 轴刻度字体大小
        pl.yticks(fontsize=30)
        title_text = plt.gca().get_title()
        pl.title(title_text, fontsize=30)
        return pl

    def set_config_ax(self, pl):
        pl.tick_params(axis='both', labelsize=self.title_fontsize)
        return pl

    def line_init_two(self, name, data, pltset):
        legend = pltset['legend']
        # 折线图上下错误条
        # 折线图
        plt.plot(pltset['x'], data[1],
                 label=legend[1])

        plt.legend(loc='lower right')
        plt.title(name)
        self.set_config(plt)
        file_save = pltset['save'] + 'line.png'
        plt.savefig(file_save, dpi=300)
        plt.show()
        plt.errorbar(pltset['x'], data[0], uplims=True, lolims=True,
                     label=legend[0])

    def line_init_one(self, name, data, pltset):
        # matplotlib.use('Agg')
        plt.figure(figsize=(16, 9))
        legend = pltset['legend']
        # 折线图上下错误条
        step = 5
        # plt.errorbar(pltset['x'][1:][::step], data[0][1:][::step], uplims=True, lolims=True,
        #              label=pltset['label'])
        plt.plot(pltset['x'], data[0],
                 label=pltset['label'], linewidth=3,
                 # color='#EE6666'
                 )
        # plt.bar(pltset['x'],
        # data[0], alpha=0.3,)

        # 设置x轴的长度，和字体斜放
        plt.xticks(ha="right")

        # y_min = np.min(data[0])
        # y_max = np.max(data[0])
        # y_range = y_max - y_min

        # 设置y轴刻度为数据的最大最小值的差除以4
        # plt.yticks(np.arange(y_min, y_max + y_range, y_range))

        # label=legend[0])

        # plt.legend(loc='lower right', prop={'size': 16})
        if 'axhline' in pltset:
            ticks_labels = [year for i, year in enumerate(pltset['x']) if (i % 5 == 0 or year == 2011)]  # 每隔5年取一个年份
            # 设置x轴的刻度位置和标签
            plt.xticks(ticks_labels)
            plt.axhline(pltset['axhline'], color='black', linewidth=2, linestyle='--', alpha=1)
            plt.ylabel(pltset['unit'][0], fontsize=16, rotation=0, labelpad=-30, loc='top')
            plt.xlabel(pltset['xunit'][0], fontsize=16, rotation=0, labelpad=-20, loc='right')

        else:
            # plt.xticks(pltset['x'], pltset['x'])
            plt.xlabel(pltset['xunit'][0], fontsize=16, rotation=0, labelpad=-30, loc='right')
        plt.title(name)
        self.set_config(plt)
        # 高亮
        if "highlight" in pltset:
            highlights = pltset['highlight']
            x = np.array(pltset['x'])
            y = np.array(data[0])
            highlight_arr = []
            for hl_i, hl in enumerate(highlights):
                index_hl = np.where(x == hl)
                index_hl = index_hl[0][0] if index_hl[0].size > 0 else None
                highlight_arr.append(index_hl)
                # 创建一个长方形的高亮区域
                if hl_i % 2 == 0:
                    # 获取高亮区域的左右边界
                    x_left = x[index_hl] - 1  # 矩形的左边界
                    x_right = x[index_hl + 1] + 1  # 矩形的右边界

                    # 获取 y 轴的最小和最大值
                    y_min, y_max = plt.ylim()
                    highlight_rect = Rectangle((x_left, y_min), x_right - x_left, y_max - y_min, color='#E4FCFC', )
                    plt.gca().add_patch(highlight_rect)
            plt.scatter(x[highlight_arr], y[highlight_arr], color='#00B8B4', s=70, zorder=5, edgecolors='#047674',
                        linewidths=2)
        file_save = pltset['save'] + 'line.png'
        plt.savefig(file_save, dpi=300)
        # plt.show()

    def line_init_more(self, name, datas, pltset):
        # matplotlib.use('Agg')
        legend = pltset['legend']
        fig, ax = plt.subplots(figsize=(16, 9))
        # plt.figure(figsize=(16, 9))
        # 折线图
        datas = datas[0]
        j = 0
        # self.color_strings = cjson.get_color()[str(len(datas))]["color"]
        marker_style = ['o', '*', 's', '^', 'd', '>', "<", "v", 'p', "P", "H"]
        for data in datas:
            # plt.plot(pltset['x'][:50], data[:50],
            # plt.plot(pltset['x'][:12], data[:12],
            # rmse =
            # label =  pltset['label'][j][:pltset['label'][j].rfind(' ')]+
            ax.plot(pltset['x'], data,
                    label=pltset['label'][j],
                    color=self.color_strings[j],
                    # linestyle=':',
                    # marker=marker_style[j],
                    linewidth=4,
                    # markersize=10
                    )
            ax.scatter(pltset['x'], data, color=self.color_strings[j], s=70, zorder=5,
                       marker=marker_style[j], edgecolors='none'
                       )
            j += 1
        # plt.legend(loc='lower left', bbox_to_anchor=(0, -0.3), ncol=9)
        ax.legend(loc='upper right', prop={'size': 16})
        if 'xunit' in pltset:
            ax.set_xlabel(pltset['xunit'][0], fontsize=20, rotation=0, labelpad=0, loc='right')

        # plt.title(name, loc='center')
        # plt.ylabel(pltset['unit'][0], fontsize=16)
        ax.set_ylabel(name, fontsize=30)
        self.set_config(plt)
        file_save = pltset['save'] + 'line.png'
        plt.savefig(file_save, dpi=300)
        # plt.show()
        # plt.errorbar(pltset['x'][:10], data[0][:10], uplims=True, lolims=True,
        #              label=legend[0])

    def line_init_more_x(self, name, datas, pltset):
        # matplotlib.use('Agg')
        legend = pltset['legend']
        fig, ax = plt.subplots(figsize=(16, 9))
        # plt.figure(figsize=(16, 9))
        # 折线图
        datas = datas[0]
        j = 0
        marker_style = ['o', '*', 's', '^', 'd', '>', "<", "v", 'p', "P", "H"]
        for index, data in enumerate(datas):
            ax.plot(pltset['x'][index], data,
                    label=pltset['label'][j],
                    color=self.color_strings[j],
                    # linestyle=':',
                    # marker=marker_style[j],
                    linewidth=2,
                    # markersize=10
                    )
            # ax.scatter(pltset['x'][index], data, color=self.color_strings[j], s=70, zorder=5,
            #            marker=marker_style[j], edgecolors='none'
            #            )
            j += 1
        # ax.legend(loc='upper right', prop={'size': 16})
        ax.legend(loc='lower right', prop={'size': 16})

        ax.set_xlabel(pltset['xunit'][0], fontsize=20, rotation=0, labelpad=0, loc='right')

        ax.set_ylabel(name, fontsize=30)
        self.set_config(plt)
        file_save = pltset['save'] + 'line.png'
        plt.savefig(file_save, dpi=300)
        # plt.show()

    def line_init_more_fig(self, name, datas, pltset):
        # matplotlib.use('Agg')
        datas = datas[0]
        len_data = len(datas)
        sub_y = 2
        sub_x = len_data / 2
        # fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
        fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(16, 9))

        legend = pltset['legend']
        # 折线图
        j = 0
        yAxis_data = [-20, -15, -10, -5, 0]
        xAxis_data = [2, 4, 6, 8, 10, 20, 30, 40, 50]
        # xAxis_data = [2, 4, 6, 8, 10]
        a = [0, 2, 4, 6, 8, 18, 28, 38, 48]
        # a = [0, 2, 4, 6, 8]
        marker_style = ['o', '*', 's', '^', 'd', '>', "<", "v", 'p', "P", "H"]
        k = 0
        l = 0

        for data in datas:
            n = 0
            if isinstance(data[0], (int, float)):
                # axs[k, l].plot(pltset['x'][j][:49], data[:49],
                axs[k, l].plot(pltset['x'][j], data,
                               label=pltset['label'][j], )
                # color=self.color_strings[j],
                # linestyle=':', marker=marker_style[j])
                axs[k, l].set_yticks(yAxis_data, yAxis_data)
                axs[k, l].set_xticks(xAxis_data, xAxis_data)
                axs[k, l].legend(loc='lower right', prop={'size': 16})
                axs[k, l].set_ylabel(name[j], fontsize=16)
            else:
                # axs[k, l].set_yticks(yAxis_data, yAxis_data)
                axs[l].set_xticks(a)
                axs[l].set_ylabel(name[j], fontsize=11)
                for data_on in data:
                    print(pltset['label'][j][n])
                    # axs[l].plot(pltset['x'][:49], data_on[:49],
                    axs[l].plot(pltset['x'][:50], data_on[:50],
                                # axs[l].plot(pltset['x'][:9], data_on[:9],
                                label=pltset['label'][j][n],
                                # color=self.color_strings[n],
                                linestyle=':', marker=marker_style[n])
                    axs[l].legend(loc='lower right', prop={'size': 16})
                    n += 1
            l += 1
            if j == 1:
                k += 1
                l = 0
            j += 1
        # plt.legend(loc='lower left', bbox_to_anchor=(0, -0.3), ncol=9)
        # plt.title(name, loc='center')
        self.set_config(plt)
        file_save = pltset['save'] + 'line.png'
        plt.savefig(file_save, dpi=600)
        plt.show()
        # plt.errorbar(pltset['x'][:10], data[0][:10], uplims=True, lolims=True,
        #              label=legend[0])


    def line_init_fig_more_1(self, name, datas, pltset):
        # matplotlib.use('Agg')
        datas = datas[0]
        len_data = len(datas)
        sub_y = 4
        sub_x = len_data / sub_y
        # fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
        # 共享x，y轴
        # sharex = True, sharey = True
        fig, axs = plt.subplots(int(sub_x), int(sub_y), figsize=(16, 9), layout='constrained')
        # a = [0, 5, 10, 20, 30, 40, 50]
        if len(datas[0][0]) > 30:
            a = [0, 4, 9, 19, 29, 39, 49]
        else:
            a = [0, 4, 9, 19]

        legend = pltset['legend']
        # 折线图
        j = 0
        # a = [0, 2, 4, 6, 8]

        marker_style = ['o', '*', 's', '^', 'd', '>', "<", "v", 'p', "P", "H"]
        k = 0
        l = 0

        for data in datas:
            n = 0
            axs[k, l].tick_params(axis='x', labelsize=16)
            axs[k, l].tick_params(axis='y', labelsize=16)
            axs[k, l].set_xlabel(pltset['xunit'][0], fontsize=16, rotation=0, labelpad=2, loc='center')
            if len(data) == 1:
                axs[k, l].set_xticks(a)
                axs[k, l].plot(pltset['x'][:50], data[0][:50],
                               # axs[k, l].plot(pltset['x'][:40], data[0][:40],
                               label=pltset['label'][j][0], linewidth=3)
                # axs[k, l].legend(loc='lower right', prop={'size': 16})
                axs[k, l].set_ylabel(name[j], fontsize=16)
                years = int(pltset['years'][j][n])
                # 右上角预热文字
                if years == 0:
                    text_content = 'spin-up time(year) > 50'
                else:
                    text_content = 'spin-up time(year) = ' + str(int(pltset['years'][j][n]))
                # axs[k, l].text(0.96, 0.97, text_content, transform=axs[k, l].transAxes,
                #                fontsize=14, ha='right', va='top')
                # 设置子图的 y 轴范围
                # print(a)
                print(np.min(data), np.max(data))
                same_count = 0

                for c, d in zip(str(np.min(data)), str(np.max(data))):
                    if c == d:
                        same_count += 1
                    else:
                        minu_data = 10 ** (-(same_count - 1))
                        break
                if np.min(data) > 1:
                    if pltset['label'][j][0] == 'ZWT':
                        minu_data = np.max(data) - np.min(data)
                        axs[k, l].set_ylim(0, 15)
                        axs[k, l].margins(y=3)
                        axs[k, l].set_yticks(np.arange(0, 16, 3))
                    else:
                        axs[k, l].set_ylim(np.min(data) - 0.2, np.max(data) + 0.2)
                        axs[k, l].set_yticks(
                            np.round(np.linspace(np.min(data) - 0.2, np.max(data) + 0.2, 5),
                                     2))
                else:
                    if pltset['label'][j][0] == 'ZWT':
                        minu_data = np.max(data) - np.min(data)
                        axs[k, l].set_ylim(0, 15)
                        axs[k, l].margins(y=3)
                        axs[k, l].set_yticks(np.arange(0, 16, 3))
                    else:
                        minu_data = np.max(data) - np.min(data)
                        axs[k, l].set_ylim(np.min(data) - minu_data * 10, np.max(data) + minu_data * 10)
                        y_ticks = np.round(np.linspace(np.min(data) - minu_data * 10, np.max(data) + minu_data * 10, 5),
                                           3)
                        if y_ticks[0] == y_ticks[1] or y_ticks[3] == y_ticks[4]:
                            y_ticks = np.round(
                                np.linspace(y_ticks[0] - y_ticks[0] / 2, y_ticks[0] + y_ticks[0] / 2 + y_ticks[0] / 5,
                                            5),
                                3)

                        axs[k, l].set_yticks(
                            y_ticks)

            else:
                # axs[k, l].set_yticks(yAxis_data, yAxis_data)
                axs[k, l].set_ylabel(name[j], fontsize=16)

                axs[k, l].set_xticks(a)

                # 设置子图的 y 轴范围
                # print(np.min(data), np.max(data))
                axs[k, l].set_ylim(np.min(data), np.max(data))
                axs[k, l].set_yticks(
                    np.round(np.linspace(np.min(data) - (np.max(data) - np.min(data)) / 10,
                                         np.max(data) + (np.max(data) - np.min(data)) / 3, 5), 3))
                y_text = 0
                for data_on_i, data_on in enumerate(data):
                    # axs[l].plot(pltset['x'][:49], data_on[:49],
                    axs[k, l].plot(pltset['x'][:50], data_on[:50],
                                   # axs[k, l].plot(pltset['x'][:40], data_on[:40],
                                   # axs[l].plot(pltset['x'][:9], data_on[:9],
                                   label=pltset['label'][j][n],
                                   color=self.color_strings[n],
                                   # linestyle=':',
                                   marker=marker_style[n], markersize=1,
                                   linewidth=3)
                    axs[k, l].legend(loc='upper right', prop={'size': 9}, bbox_to_anchor=(1, 1.01))
                    text_content = 'layer ' + str(data_on_i + 1) + ' spin-up time(year) = ' + str(
                        int(pltset['years'][j][n]))
                    # axs[k, l].text(0.96, 0.97 - y_text, text_content, transform=axs[k, l].transAxes,
                    #                fontsize=12, ha='right', va='top')

                    y_text += 0.05

                    n += 1
            l += 1
            if l != 0 and l % 4 == 0:
                k += 1
                l = 0
            j += 1

        # self.set_config(plt)
        file_save = pltset['save'] + 'line7.png'
        plt.savefig(file_save, dpi=600)

    def more_y(self, name, datas, pltset):
        import matplotlib.pyplot as plt
        import numpy as np

        # 创建示例数据
        x = np.arange(1, 51, 1)
        arr = [[0.05868797, 0.05864973, 0.05868063, 0.05870716, 0.05871608, 0.05871193
                   , 0.0587194, 0.05872088, 0.0587338, 0.05872715, 0.05872296, 0.05872801
                   , 0.05873403, 0.05872421, 0.05873456, 0.05872589, 0.05873885, 0.05873408
                   , 0.05873, 0.05872221, 0.058739, 0.05873208, 0.05874395, 0.0587325
                   , 0.05874234, 0.05872842, 0.05874247, 0.05871711, 0.05873569, 0.05872299
                   , 0.05874477, 0.05871674, 0.05874504, 0.05871764, 0.05873756, 0.05872091
                   , 0.05874836, 0.05871696, 0.0587447, 0.05871469, 0.05874595, 0.05871849
                   , 0.05874952, 0.05871548, 0.05874804, 0.05872042, 0.05873985, 0.05871777
                   , 0.05874785, 0.05871247],
               [15.34105015, 15.3258152, 15.3289423, 15.3329401, 15.33404732, 15.33687496
                   , 15.33588791, 15.3390379, 15.33914948, 15.33978558, 15.33692741, 15.34031582
                   , 15.33828831, 15.33889484, 15.33901119, 15.34035778, 15.33919525, 15.34148884
                   , 15.33927727, 15.33933353, 15.34020424, 15.34152222, 15.34173298, 15.34209347
                   , 15.34225464, 15.34108734, 15.34269714, 15.33892536, 15.34082031, 15.34017563
                   , 15.34314919, 15.33893013, 15.34323883, 15.3397913, 15.34206581, 15.33996582
                   , 15.34385204, 15.33920956, 15.34344578, 15.33919334, 15.34384155, 15.33884048
                   , 15.34508705, 15.33946896, 15.3439827, 15.34065151, 15.34298992, 15.33983231
                   , 15.34449005, 15.33928299],
               [0.35340658, 0.36819506, 0.37358218, 0.37769043, 0.37338132, 0.3750779
                   , 0.3752856, 0.37350833, 0.37395039, 0.37447652, 0.37197369, 0.37246773
                   , 0.37374356, 0.37140724, 0.37155759, 0.3724272, 0.37135422, 0.37148944
                   , 0.372078, 0.37032071, 0.37138426, 0.37139708, 0.36969495, 0.37084782
                   , 0.37107405, 0.36978722, 0.37024614, 0.37013519, 0.36979932, 0.37003702
                   , 0.37001556, 0.36919373, 0.36927289, 0.37007055, 0.36879829, 0.36926851
                   , 0.36997458, 0.36860815, 0.36852893, 0.36929864, 0.36878067, 0.36888841
                   , 0.36885455, 0.36827418, 0.368752, 0.36886707, 0.36777964, 0.36839196
                   , 0.36900973, 0.36773077]
               ]
        y1 = arr[0]
        y2 = arr[1]
        y3 = arr[2]
        pltset = {
            'label': ['SNOWH', 'SNEQV', 'LAI']
        }
        # 创建第一个坐标轴
        fig, ax1 = plt.subplots(figsize=(16, 9))

        ax1.plot(x, y1, 'b-')
        # ax1.set_xlabel('X-axis 1')
        ax1.set_ylabel(pltset['label'][0], color=self.color_strings[0])
        ax1.tick_params('y', color=self.color_strings[2])

        # 创建第二个坐标轴，共享X轴
        ax2 = ax1.twinx()

        # 在第二个坐标轴上绘制第二组数据
        ax2.plot(x, y2, 'r-')
        # ax2.set_xlabel('X-axis 2')
        ax2.set_ylabel(pltset['label'][1], color=self.color_strings[2])
        ax2.tick_params('y', color=self.color_strings[2])

        # 创建第三个坐标轴，共享Y轴
        ax3 = plt.twiny()

        # 在第三个坐标轴上绘制第三组数据
        ax3.plot(y3, x, 'g-')
        ax3.set_xlabel(pltset['label'][2])
        ax3.set_ylabel('Y-axis')
        ax3.tick_params('x', colors=self.color_strings[2])

        plt.show()
        plt.savefig('file_save.png', dpi=600)


if __name__ == '__main__':

    pass
