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

    # 多个子图
    def line_init_fig_more(self, name, datas, pltset):
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
                axs[k, l].plot(pltset['x'][j][:49], data[:49],
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

    def line_test(self):
        # 数据
        xAxis_data = list(range(1, 13))
        # legend_data = ['spin-up {} - {}'.format(i + 1, i) for i in range(1, 50)]
        legend_data = ['spin-up {} '.format(i) for i in range(1, 50)]

        # 原始数据
        path_log = r'F:\pro\py_conda\nc_py\log\mean_data.log'
        series_data = OutInput({
            "input_path": '',
            "out_path": ''
        }).read_log(path_log)

        # 计算差值
        series_data_new = []
        for i in range(len(series_data) - 1):
            # data = series_data[i]['data']
            # data_plus = series_data[i + 1]['data']
            data = series_data[i]
            data_plus = series_data[i + 1]
            out_data = [data_plus[j] - data[j] for j in range(len(data))]
            series_data_new.append({
                # 'name': series_data[i]['name'],
                # 'name': series_data[i + 1]['name'] + '-' + series_data[i]['name'],
                "name": 'spin-up ' + str(i + 1) + '-' + 'spin-up ' + str(i),
                "stack": i,
                'type': 'line',
                'data': out_data
            })

        # 创建图表
        plt.figure(figsize=(8, 6))
        plt.title('spin-up times difference')
        plt.xlabel('Month')
        plt.ylabel('Difference')

        # 绘制曲线

        # random_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(50)]
        # color_strings = ['#%02x%02x%02x' % rgb for rgb in random_colors]
        # 渐变色
        # start_color = mcolors.to_rgba("blue")  # 蓝色
        # end_color = mcolors.to_rgba("red")  # 红色
        # num_colors = 50
        # r = np.linspace(start_color[0], end_color[0], num_colors)
        # g = np.linspace(start_color[1], end_color[1], num_colors)
        # b = np.linspace(start_color[2], end_color[2], num_colors)
        # a = np.linspace(start_color[3], end_color[3], num_colors)
        #
        # color_strings = [mcolors.to_hex((r[i], g[i], b[i], a[i])) for i in range(num_colors)]
        # print(color_strings)
        for i, data in enumerate(series_data_new):
            plt.plot(xAxis_data, data['data'], label=legend_data[i], color=self.color_strings[i])
        # ncol指定列数
        plt.legend(loc='lower left', bbox_to_anchor=(0, -0.3), ncol=9)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        plt.grid(True)
        plt.show()

    def line_test_1(self):
        # 数据
        xAxis_data = [24, 48, 60, 96, 144, 192, 220, 440]
        legend_array = []
        # legend_data = ['core {} '.format(i) for i in range(1, 50)]

        # 计算差值

        # 创建图表
        plt.figure(figsize=(8, 6))
        plt.title('Core test of one month')
        plt.xlabel('Number of core')
        plt.ylabel('Time (s)')
        data = [150, 108, 180, 150, 190, 240, 300, 515]

        plt.plot(xAxis_data, data, label='')
        # 设置x轴显示的数
        plt.xticks(xAxis_data, xAxis_data)
        # ncol指定列数
        # plt.legend(loc='lower left', bbox_to_anchor=(0, -0.3), ncol=9)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        plt.grid(True)
        plt.show()

    def line_fun(self):
        # 创建x值的范围
        # x = np.linspace(1, 100, 100)  # 从1到10生成100个点
        #
        # # 计算对应的y值
        # y = (1 + 1 / x) ** x
        #
        # # 创建一个图形
        # plt.figure(figsize=(8, 6))
        #
        # # 绘制曲线
        # plt.plot(x, y, label='y = (1 + 1/x)^x', color='b')
        #
        # # 添加标签和标题
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.title('Plot of y = (1 + 1/x)^x')
        #
        # # 添加图例
        # plt.legend()
        #
        # # 显示图形
        # plt.grid(True)
        # plt.show()
        # 创建x值的范围，不包括0
        x = np.linspace(-100, -1, 100)
        x = np.concatenate((x, np.linspace(1, 100, 100)))

        # 计算对应的y值，处理x等于0的情况
        # y = [(1 + 1 / xi) ** xi if xi != 0 else 1 for xi in x]
        y = [(1 + xi) ** (1 / xi) if xi != 0 else 1 for xi in x]

        # 创建一个图形
        plt.figure(figsize=(8, 6))

        # 绘制曲线
        plt.plot(x, y, label='y = (1 + 1/x)^x', color='b', linewidth=2)
        plt.axhline(1.5, color='black', linewidth=1, alpha=1)
        plt.axhline(y=math.e, color='black', linewidth=1, linestyle='--')
        plt.axvline(0, color='black', linewidth=1)
        for i in np.arange(1.5, 4.25, 0.25):
            plt.text(0.04, i + 0.06, str(i), ha='right', va='center', fontsize=14, color='black')
            arrow = FancyArrowPatch((0.04, i), (0.3, i), color='black', arrowstyle='-',
                                    mutation_scale=10)
            plt.gca().add_patch(arrow)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)

        plt.xticks([])  # 隐藏x轴上的数字
        plt.yticks([])
        # 添加标签和标题
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.title('Plot of y = (1 + 1/x)^x')

        # 添加图例
        plt.legend()

        # 显示图形
        plt.grid(False)
        plt.show()

    def line_fun1(self):
        x = np.linspace(-1, -0.01, 10)
        x = np.concatenate((x, np.linspace(0.01, 100, 100)))

        # 计算对应的y值，处理x等于0的情况
        y = [(1 + xi) ** (1 / xi) if xi != 0 else 1 for xi in x]
        # x = np.linspace(0.01, 100, 100)  # 选择一个适当的 x 范围，避免 x=0 的问题
        # y = (1 + x) ** (1 / x)
        # 创建一个图形

        plt.figure(figsize=(32, 18))

        # 绘制曲线
        plt.plot(x1, y1, label='y = (1 + x)^1/x', color='b', linewidth=2)
        # plt.plot(x2, y2, label='y = (1 + x)^1/x', color='b', linewidth=2)

        plt.plot(0, math.e, 'o', markersize=8, markerfacecolor='white', markeredgecolor='black')
        plt.axhline(0, color='black', linewidth=1, alpha=1)
        plt.axhline(y=1, color='black', linewidth=1, linestyle='--')
        plt.axhline(y=math.e, color='black', linewidth=1, linestyle='--')

        plt.axvline(0, color='black', linewidth=1)
        plt.axvline(-100, color='black', linewidth=1, alpha=0)
        arr = [0, 1, math.e]
        for i in arr:
            if i == math.e:
                plt.text(0.04, i + 0.06, 'e' + ' ', ha='right', va='center', fontsize=14, color='black')
            else:
                plt.text(0.04, i + 0.06, str(i) + ' ', ha='right', va='center', fontsize=14, color='black')
            arrow = FancyArrowPatch((0.04, i), (0.3, i), color='black', arrowstyle='-',
                                    mutation_scale=10)
            plt.gca().add_patch(arrow)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)

        plt.xticks([])  # 隐藏x轴上的数字
        plt.yticks([])
        # 添加标签和标题
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.title('Plot of y = (1 + 1/x)^x')

        # 添加图例
        plt.legend()

        # 显示图形
        plt.grid(False)
        plt.show()

    def line_fun2(self):
        # x1 = np.linspace(-10, -0.1, 100)  # 从-100到100生成1000个点，包括0
        # # 计算对应的y值
        # y1 = x1 + 1 / x1
        # x2 = np.linspace(0.1, 10, 100)  # 从-100到100生成1000个点，包括0
        # # x = x[x != 0]  # 排除x=0的点
        # # 计算对应的y值
        # y2 = x2 + 1 / x2
        # x = np.linspace(-100, 100, 1000)  # 在-5到5之间生成400个均匀分布的点
        # 计算y的值
        # y = np.arctan(x)
        x1 = np.linspace(-10, -0.1, 100)  # 从-100到100生成1000个点，包括0
        # 计算对应的y值
        y1 = np.sin(1 / x1)
        x2 = np.linspace(0.1, 10, 100)  # 从-100到100生成1000个点，包括0
        # x = x[x != 0]  # 排除x=0的点
        # 计算对应的y值
        y2 = np.sin(1 / x2)
        x = np.linspace(-10, 10, 500)

        # 去除 x = 0，以避免除以零错误
        x = x[x != 0]

        # 计算对应的 y 值
        y = np.sin(1 / x)
        # x1 = np.linspace(-10, 4.99, 100)  # 从-100到100生成1000个点，包括0
        # # 计算对应的y值
        # y1 = 1 / ((x1 - 5) ** 2)
        #
        # x2 = np.linspace(5.01, 10, 100)  # 从-100到100生成1000个点，包括0
        # # x = x[x != 0]  # 排除x=0的点
        # # 计算对应的y值
        # y2 = 1 / ((x2 - 5) ** 2)
        # 创建一个图形
        plt.figure(figsize=(16, 9))

        # 绘制曲线
        # plt.plot(x1, y1, color='b', linewidth=2)
        # plt.plot(x2, y2, color='b', linewidth=2)
        # plt.plot(x, y, label='y = arctan(x)', color='b', linewidth=2)
        plt.plot(x, y, color='black', linewidth=2)
        # plt.plot(x1, y1,  color='b', linewidth=2)
        # plt.plot(x2, y2,  color='b', linewidth=2)
        plt.axhline(0, color='black', linewidth=1, alpha=1)

        # plt.axhline(-(1 / ((4.99 - 5) ** 2)), color='black', linewidth=1, alpha=0)
        plt.axvline(0, color='black', linewidth=1)

        # plt.axhline(y=math_COM.pi/2, color='black', linewidth=1, linestyle='--')
        # plt.axhline(y=-math_COM.pi/2, color='black', linewidth=1, linestyle='--')
        # plt.plot(5, 1 / ((4.99 - 5) ** 2), 'o', markersize=8, markerfacecolor='white', markeredgecolor='black')

        plt.axhline(y=1, color='black', linewidth=1, linestyle='--')
        plt.axhline(y=-1, color='black', linewidth=1, linestyle='--')
        plt.plot(0, 0, 'o', markersize=8, markerfacecolor='white', markeredgecolor='black')

        for i in np.arange(-1, 1.5, 1):
            # for i in [-math_COM.pi/2,0,math_COM.pi/2,]:
            #     if i!=0:
            #         plt.text(0.04, i + 0.06, 'π/2' + '  ', ha='right', va='center', fontsize=14, color='black')
            #     else:
            if i != 0:
                plt.text(0.04, i + 0.06, str(i) + '  ', ha='right', va='center', fontsize=14, color='black')

            arrow = FancyArrowPatch((0.01, i), (0.04, i), color='black', arrowstyle='-',
                                    mutation_scale=10)
            plt.gca().add_patch(arrow)

        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.legend().set_visible(False)
        legend = plt.legend()
        legend.get_frame().set_edgecolor('none')  # 清除图例边框
        plt.xticks([])  # 隐藏x轴上的数字
        plt.yticks([])
        # plt.text(5,0, str(5)+ '', ha='center', va='top', fontsize=14, color='black')
        #
        # arrow = FancyArrowPatch((0.01, 5), (1, 5), color='black', arrowstyle='-',
        #                         mutation_scale=10)
        # plt.gca().add_patch(arrow)
        # 添加标签和标题
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.title('Plot of y = (1 + 1/x)^x')

        # 添加图例
        plt.savefig(r'F:\test_pic\导师\5', dpi=300)
        # 显示图形
        plt.grid(False)
        plt.show()

    def test_1(self):
        import matplotlib.pyplot as plt
        import numpy as np

        # 创建示例数据
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.exp(-x)
        y4 = np.log(1 + x)

        # 创建第一个坐标轴
        fig, ax1 = plt.subplots()

        # 在第一个坐标轴上绘制第一组数据
        ax1.plot(x, y1, 'b-')
        ax1.set_xlabel('X-axis 1')
        ax1.set_ylabel('Blue curve', color='b')
        ax1.tick_params('y', colors='b')

        # 创建第二个坐标轴，共享X轴
        ax2 = ax1.twinx()

        # 在第二个坐标轴上绘制第二组数据
        ax2.plot(x, y2, 'r-')
        ax2.set_xlabel('X-axis 2')
        ax2.set_ylabel('Red curve', color='r')
        ax2.tick_params('y', colors='r')

        # 创建第三个坐标轴
        ax3 = plt.twiny()

        # 在第三个坐标轴上绘制第三组数据
        ax3.plot(y3, x, 'g-')
        ax3.set_xlabel('Green curve')
        ax3.set_ylabel('Y-axis 1', color='g')
        ax3.tick_params('x', colors='g')

        # 创建第四个坐标轴，共享Y轴
        ax4 = ax3.twinx()

        # 在第四个坐标轴上绘制第四组数据
        ax4.plot(y4, x, 'm-')
        ax4.set_xlabel('Magenta curve')
        ax4.set_ylabel('Y-axis 2', color='m')
        ax4.tick_params('x', colors='m')

        plt.show()

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

    def line_disappear(self):
        # 数据
        # 读取文件数据
        data = np.loadtxt('/Volumes/momo/pro/py_conda/uq/uqofrun/UQ/optimization/tem_Output_S.txt')

        # 分割数据为两组
        group1 = data[:, 0]
        group2 = data[:, 1]
        i = 50
        datas1 = []
        datas2= []
        while i <= len(group1):
            a = group1[:i]
            b = np.min(a)
            datas1.append(b)
            c = group2[:i]
            d = np.min(c)
            datas2.append(d)
            i += 10
        datas = [datas1, datas2]
        fig, axs = plt.subplots(2, 1, sharex=True, figsize=(16, 9))
        pltset = {
            'x': np.arange(1, 12, 1),
            'label': ['GPP', 'LH'],
            'save': '',
            'xunit': ['GPP', 'LH']
        }
        x = [np.arange(1, 12, 1), [ '50','60', '70','80','90', '100', '110','120','130', '140','150']]
        y =[np.arange(0, 2, 0.1),np.arange(8, 11, 0.5)]
        name = ['GPP(gC/m2/day)', 'LH(W/m2)']

        for j, data1 in enumerate(datas):
            axs[j].plot(pltset['x'], data1,
                        label=pltset['label'][j],
                        color=self.color_strings[j],
                        linewidth=4,
                        )
            axs[j].set_xticks(x[0])
            # 设置对应的标签

            axs[j].set_xticklabels(x[1])
            # axs[j,0].scatter(pltset['x'], data, color=self.color_strings[j], s=70, zorder=5,
            #            marker=self.marker_style[j], edgecolors='none'
            #            )

            # axs[j].set_xlabel(pltset['xunit'][j], fontsize=20, rotation=0, labelpad=0, loc='right')
            axs[j].set_ylabel(name[j], fontsize=30)
            self.set_config_ax(axs[j])
        axs[0].set_ylim(1, 2)
        axs[1].set_ylim(9, 11)
        file_save = pltset['save'] + 'line1.png'
        plt.savefig(file_save, dpi=300)
        plt.show()


if __name__ == '__main__':
    Display_Plot_Line().line_disappear()

    pass
