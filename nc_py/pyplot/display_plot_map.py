# import os
# from nc_py.compute_nc.xlatlong_m import XLatLong_Out

import os
from matplotlib import colors, patches
from nc_py.out_input import OutInput
import matplotlib as mpl
import xarray as xr
# import time
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from time import sleep
from netCDF4 import Dataset
import pandas as pd
from nc_py.math_COM import metrics
import matplotlib.colors as mcolors
import matplotlib
import math
from cartopy.io import shapereader
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.ticker import FixedLocator

from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDrawingArea, AnchoredSizeBar, AnchoredAuxTransformBox, \
    AnchoredDirectionArrows, AnchoredEllipse
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse

# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# from scipy.interpolate import interpn
# # 引入自建module，同级文件
# from compute_nc.soil_out import Soil_Out
'''
    地图
'''


# matplotlib.use('Agg')
class Display_Plot_Map(object):
    def __init__(self) -> None:
        self.default_value = "default_value"

        pass

    def map_ini_two(datas, lons, lats, name, pltset):
        # 展示条的大小值，与间隔
        for data in datas:
            pass
        fig = plt.figure()
        cbar_kwargs = {
            'orientation': 'horizontal',
            'label': name[0],
            'shrink': 0.8,
        }
        # 画图
        ax1 = fig.add_subplot(1, 2, 1,
                              projection=ccrs.PlateCarree())

        # ax1 = plt.axes(projection=ccrs.PlateCarree())
        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax1.set_global()
        ax1.coastlines()
        ax1.add_feature(cfeat.BORDERS, zorder=2)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        # ax1.add_feature(cfeat.STATES, zorder=4)
        # 标题
        ax1.set_title(pltset["title"][0])
        ax1.contourf(lons, lats, data[0],
                     transform=ccrs.PlateCarree(),
                     cmap='RdBu_r')
        ax1.set_extent([-125, -67, 25, 53], crs=ccrs.PlateCarree())
        # ax1.stock_img()
        ax2 = fig.add_subplot(1, 2, 2,
                              projection=ccrs.PlateCarree())
        # ax2.stock_img()

        # ax2 = plt.axes(projection=ccrs.PlateCarree())
        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax2.set_global()
        ax2.coastlines()
        ax2.add_feature(cfeat.BORDERS, zorder=2)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        # ax2.add_feature(cfeat.STATES, zorder=4)
        # 标题
        ax2.set_title(pltset["title"][1])
        # ax2.contourf(lons, lats, data[1],
        #              transform=ccrs.PlateCarree(),
        #              cmap='nipy_spectral')
        ax2.contourf(lons, lats, data[1],
                     transform=ccrs.PlateCarree(),
                     cmap='RdBu_b')
        ax2.set_extent([-125, -67.9, 25, 53], crs=ccrs.PlateCarree())
        # plt.savefig('UA Pre 2022'+'.png')
        plt.savefig(pltset["title"][0])
        plt.show()

    def map_ini_two_simple(self, datas, lonlat, name, pltset):
        datas = datas[0]
        var_data_1 = datas[0]
        var_data_2 = datas[1]
        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        fig = plt.figure(figsize=(16, 9))
        plt.title(name)
        plt.axis('off')
        proj = ccrs.PlateCarree()
        # 画图
        ax1 = fig.add_subplot(1, 2, 1,
                              projection=proj)

        # ax1 = plt.axes(projection=ccrs.PlateCarree())
        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax1.set_global()
        ax1.coastlines()
        ax1.add_feature(cfeat.BORDERS, zorder=2)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        # ax1.add_feature(cfeat.STATES, zorder=4)
        # 标题
        ax1.set_title(pltset["title"][0])
        norm = pltset['norm']
        im1 = ax1.imshow(var_data_1, extent=[lon_min, lon_max, lat_min, lat_max],
                         origin='lower', cmap=pltset['cmap'][0],
                         norm=colors.Normalize(vmin=norm[0][0], vmax=norm[0][1]), transform=proj)
        ax1.set_extent([-125, -67, 25, 53], crs=ccrs.PlateCarree())
        ax2 = fig.add_subplot(1, 2, 2,
                              projection=proj)

        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax2.set_global()
        ax2.coastlines()
        ax2.add_feature(cfeat.BORDERS, zorder=2)
        # 标题
        ax2.set_title(pltset["title"][1])
        # cmap = 'tab24'
        im2 = ax2.imshow(var_data_2, extent=[lon_min, lon_max, lat_min, lat_max],
                         origin='lower', cmap=pltset['cmap'][1],
                         norm=colors.Normalize(vmin=norm[1][0], vmax=norm[1][1]), transform=proj)

        ax2.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        # plt.savefig('UA Pre 2022'+'.png')
        # plt.savefig(pltset["title"][0])
        cbar1 = fig.colorbar(im1, ax=ax1, shrink=0.7)
        cbar2 = fig.colorbar(im2, ax=ax2, shrink=0.7)

        # 添加单位
        cbar1.ax.set_title(pltset['unit'][0], fontsize=10)
        cbar2.ax.set_title(pltset['unit'][1], fontsize=10)
        # 设置每个标签的名称
        # if pltset['ticks']:
        #     #     levels1 = np.linspace(0, len(pltset['ticks'][0]), num=len(pltset['ticks'][0]))
        #     #     labels1 = pltset['ticks'][0]
        #     levels2 = np.linspace(0, len(pltset['ticks'][0]), num=len(pltset['ticks'][1]))
        #     labels2 = pltset['ticks'][1]
        # #     print('levels2', levels1, levels2)
        # #     # 分级标签列表
        # #     cbar1.set_ticks(levels1)
        # #     cbar1.set_ticklabels(labels1)
        # #
        #     cbar2.set_ticks(levels2)
        #
        #     cbar2.set_ticklabels(labels2)

        # 添加bar标题
        # cbar.set_label('K', fontsize=12)
        file_save = pltset['save'] + "map.png"
        # manager = plt.get_current_fig_manager()
        # manager.resize(*manager.window.maxsize())
        plt.savefig(file_save, dpi=600)

        # plt.show()

    def map_ini_one_simple(self, datas, lonlat, name, pltset):
        # 显示
        # matplotlib.use('TkAgg')
        # 不显示
        matplotlib.use('Agg')

        # 展示条的大小值，与间隔
        var_data = datas[0]
        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        cbar_kwargs = {
            'orientation': 'horizontal',
            'label': name[0],
            'shrink': 0.8,
        }
        # plt.title(name)
        plt.axis('off')
        plt.figure(figsize=(16, 9))
        proj = ccrs.PlateCarree()
        # 画图
        ax1 = plt.axes(projection=proj)

        # ax1 = plt.axes(projection=ccrs.PlateCarree())
        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax1.set_global()
        ax1.coastlines()
        ax1.add_feature(cfeat.BORDERS, zorder=2, linewidth=2)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        ax1.add_feature(cfeat.STATES, zorder=4, alpha=0.5, edgecolor='gray', linewidth=1)
        # 标题
        ax1.set_title(pltset["title"][0], fontsize=30)
        # cmap = 'viridis',tab24
        norm = pltset['norm']
        print('norm:', norm[0])
        im1 = ax1.imshow(var_data, extent=[lon_min, lon_max, lat_min, lat_max],
                         origin='lower', cmap=pltset['cmap'][0],
                         norm=colors.Normalize(vmin=int(norm[1][0]), vmax=int(norm[1][1])),
                         transform=proj)
        ax1.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        # gls = ax1.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
        #                     color='k', linestyle='dashed', linewidth=0.3, alpha=1,
        #                     y_inline=False, x_inline=False,
        #                     rotate_labels=0, xpadding=5,
        #                     xlocs=range(-180, 180, 10), ylocs=range(-90, 90, 10),
        #                     xlabel_style={"size": 8},
        #                     ylabel_style={"size": 8}
        #                     )
        # gls.top_labels = False
        # gls.right_labels = False
        ax1.tick_params(axis='x', labelsize=24)  # 设置 x 轴刻度标签的大小
        ax1.tick_params(axis='y', labelsize=24)
        gls = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                            linewidth=0)
        gls.xlabel_style = {'size': 24}  # 设置 x 轴标签的字体大小
        gls.ylabel_style = {'size': 24}
        # ax1.tick_params(axis='x', labelsize=30)  # 设置 x 轴刻度标签的大小
        # ax1.tick_params(axis='y', labelsize=30)
        # gls = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
        #                     linewidth=0)
        # gls.xlabel_style = {'size': 30}  # 设置 x 轴标签的字体大小
        # gls.ylabel_style = {'size': 30}
        # 添加文字到右上角

        rmse_bool = pltset["title"][0].find('RMSE')
        if rmse_bool != -1:
            rmse = round(np.nanmean(var_data).item(), 2)
            text_content = "RMSE = " + str(rmse)
            print(text_content, 'text_content')
            ax1.text(0.96, 0.91, text_content, transform=ax1.transAxes,
                     fontsize=16, ha='right', va='top')
        else:
            rmse = round(np.nanmean(var_data).item(), 1)
            text_content = "spin-up time(year): " + str(rmse + 1)
            print(text_content, 'text_content')
            # ax1.text(0.96, 0.91, text_content, transform=ax1.transAxes,
            #          fontsize=12, ha='right', va='top')
        gls.top_labels = False
        gls.right_labels = False

        cbar = plt.colorbar(im1, ax=ax1, orientation='horizontal', shrink=0.5, pad=0.15, )
        # # 添加单位
        cbar.ax.set_title(pltset['unit'][0], fontsize=16)
        if norm[0][1] > 10 and norm[0][1] < 50:
            cbar.locator = MultipleLocator(5)
        if norm[0][1] > 50:
            cbar.locator = MultipleLocator(5)

        cbar.update_ticks()
        cbar.ax.tick_params(labelsize=16)

        # 添加bar标题
        # cbar.set_label('K', fontsize=12)
        # 添加比例尺和指南针
        # self.add_scalebar(ax1, lon0=-75, lat0=26, length=500)
        # self.add_north(ax1)
        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=300)
        # plt.show()

    def map_ini_one_simple_wrf(self, datas, lonlat, name, pltset):
        # 显示
        # matplotlib.use('TkAgg')
        # 不显示
        matplotlib.use('Agg')

        # 展示条的大小值，与间隔
        var_data = datas[0]
        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        cbar_kwargs = {
            'orientation': 'horizontal',
            'label': name[0],
            'shrink': 0.8,
        }
        # plt.title(name)
        plt.axis('off')
        plt.figure(figsize=(16, 10))
        proj = ccrs.PlateCarree()
        # 画图
        ax1 = plt.axes(projection=proj)

        # ax1 = plt.axes(projection=ccrs.PlateCarree())
        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax1.set_global()
        ax1.coastlines()
        ax1.add_feature(cfeat.BORDERS, zorder=2, linewidth=2)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        ax1.add_feature(cfeat.STATES, zorder=4, alpha=0.5, edgecolor='gray', linewidth=1)
        # 标题
        ax1.set_title(pltset["title"][0], fontsize=30)
        # cmap = 'viridis',tab24
        norm = pltset['norm']
        print('norm:', norm[0])
        filtered_data = var_data.where(~np.isnan(var_data), drop=False)
        # 将 xarray.DataArray 转换为 numpy 数组
        numpy_data = filtered_data.to_numpy()
        # 使用布尔索引移除 NaN 值
        non_nan_data = numpy_data[~np.isnan(numpy_data)]
        unique_values = np.unique(non_nan_data)  # 获取唯一值
        colors_all = plt.cm.viridis(np.linspace(0, 1, len(unique_values)))
        data_min = np.nanmin(var_data)
        data_max = np.nanmax(var_data)
        norm_all = colors.Normalize(vmin=data_min, vmax=data_max)
        color_list = pltset['cmap']
        cmap = colors.ListedColormap(color_list)

        im1 = ax1.imshow(var_data, extent=[lon_min, lon_max, lat_min, lat_max],
                         origin='lower',
                         cmap=plt.cm.viridis,
                         norm=norm_all,
                         # cmap=cmap,
                         # norm=colors.Normalize(vmin=int(norm[0][0]), vmax=int(norm[0][1])),

                         transform=proj)
        ax1.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        # gls = ax1.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
        #                     color='k', linestyle='dashed', linewidth=0.3, alpha=1,
        #                     y_inline=False, x_inline=False,
        #                     rotate_labels=0, xpadding=5,
        #                     xlocs=range(-180, 180, 10), ylocs=range(-90, 90, 10),
        #                     xlabel_style={"size": 8},
        #                     ylabel_style={"size": 8}
        #                     )
        # gls.top_labels = False
        # gls.right_labels = False
        ax1.tick_params(axis='x', labelsize=24)  # 设置 x 轴刻度标签的大小
        ax1.tick_params(axis='y', labelsize=24)
        gls = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                            linewidth=0)
        gls.xlabel_style = {'size': 24}  # 设置 x 轴标签的字体大小
        gls.ylabel_style = {'size': 24}
        # ax1.tick_params(axis='x', labelsize=30)  # 设置 x 轴刻度标签的大小
        # ax1.tick_params(axis='y', labelsize=30)
        # gls = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
        #                     linewidth=0)
        # gls.xlabel_style = {'size': 30}  # 设置 x 轴标签的字体大小
        # gls.ylabel_style = {'size': 30}
        # 添加文字到右上角

        rmse_bool = pltset["title"][0].find('RMSE')
        if rmse_bool != -1:
            rmse = round(np.nanmean(var_data).item(), 2)
            text_content = "RMSE = " + str(rmse)
            print(text_content, 'text_content')
            ax1.text(0.96, 0.91, text_content, transform=ax1.transAxes,
                     fontsize=16, ha='right', va='top')
        else:
            rmse = round(np.nanmean(var_data).item(), 1)
            text_content = "spin-up time(year): " + str(rmse + 1)
            print(text_content, 'text_content')
            # ax1.text(0.96, 0.91, text_content, transform=ax1.transAxes,
            #          fontsize=12, ha='right', va='top')
        gls.top_labels = False
        gls.right_labels = False
        # 创建自定义图例
        legend = pltset['legend']
        # legend = unique_values
        legend_patches = []
        for lg_i, lg in enumerate(legend):
            legend_patches.append(patches.Patch(
                color=colors_all[lg_i],
                label=pltset['legend'][lg_i]), )

            # 添加图例
        # ax1.legend(handles=legend_patches, loc='upper right', fontsize=20, frameon=False)
        # ax1.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=20,
        #            frameon=False)
        ax1.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, -0.28), ncol=7, fontsize=20,
                   frameon=False)
        # cbar = plt.colorbar(im1, ax=ax1, orientation='horizontal', shrink=0.5, pad=0.15, )


        # 添加比例尺和指南针
        # self.add_scalebar(ax1, lon0=-75, lat0=26, length=500)
        # self.add_north(ax1)
        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=300)
        # plt.show()

    def map_ini_one_simple_legend(self, datas, lonlat, name, pltset):
        # matplotlib.use('Agg')

        # 展示条的大小值，与间隔
        var_data = datas[0]
        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        plt.axis('off')
        proj = ccrs.PlateCarree()
        # 画图
        ax1 = plt.axes(projection=proj)

        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax1.set_global()
        # ax1.stock_img()
        ax1.coastlines()
        ax1.add_feature(cfeat.BORDERS, zorder=2)
        ranges = pltset['legend']
        ax1.set_title(pltset["title"][0])
        norm = pltset['norm']
        # array_as_string = '\n'.join(['~'.join(map(str, row)) for row in ranges])
        # array_as_s = array_as_string.split('\n')
        # 创建单色的colormap
        i = 0
        legend_data = []
        while i < len(ranges):
            range_data = ranges[i]
            cmap1 = mcolors.ListedColormap([pltset['cmap'][i]])
            array_as_s = '~'.join(map(str, range_data))
            a1 = ax1.imshow(np.where((var_data >= ranges[i][0]) & (var_data <= ranges[i][1]), var_data, np.nan),
                            extent=[lon_min, lon_max, lat_min, lat_max],
                            origin='lower', cmap=cmap1,
                            norm=colors.Normalize(vmin=ranges[i][0], vmax=ranges[i][1]), transform=proj,
                            label=array_as_s)

            # 创建代理艺术家用于图例
            proxy_artist1 = mpatches.Patch(color=pltset['cmap'][i], label=array_as_s)
            legend_data.append(proxy_artist1)
            i += 1
        # cmap1 = mcolors.ListedColormap([pltset['cmap'][0]])
        # cmap2 = mcolors.ListedColormap([pltset['cmap'][1]])
        # cmap3 = mcolors.ListedColormap([pltset['cmap'][2]])
        # a1 = ax1.imshow(np.where((var_data >= ranges[0][0]) & (var_data <= ranges[0][1]), var_data, np.nan),
        #                 extent=[lon_min, lon_max, lat_min, lat_max],
        #                 origin='lower', cmap=cmap1,
        #                 norm=colors.Normalize(vmin=ranges[0][0], vmax=ranges[0][1]), transform=proj,
        #                 label=array_as_s[0])
        # a2 = ax1.imshow(np.where((var_data >= ranges[1][0]) & (var_data <= ranges[1][1]), var_data, np.nan),
        #                 extent=[lon_min, lon_max, lat_min, lat_max],
        #                 origin='lower', cmap=cmap2,
        #                 norm=colors.Normalize(vmin=ranges[1][0], vmax=ranges[1][1]), transform=proj,
        #                 label=array_as_s[2])
        # a3 = ax1.imshow(np.where((var_data >= ranges[2][0]) & (var_data <= ranges[2][1]), var_data, np.nan),
        #                 extent=[lon_min, lon_max, lat_min, lat_max],
        #                 origin='lower', cmap=cmap3,
        #                 norm=colors.Normalize(vmin=ranges[2][0], vmax=ranges[2][1]), transform=proj,
        #                 label=array_as_s[2])
        # # 标题
        # legend = ax1.legend(
        #     [a1, a2, a3],
        #     ['Range 1', 'Range 2', 'Range 3'],
        #     loc='upper right',
        # )

        # 创建代理艺术家用于图例
        # proxy_artist1 = mpatches.Patch(color='blue', label=array_as_s[0])
        # proxy_artist2 = mpatches.Patch(color='green', label=array_as_s[1])
        # proxy_artist3 = mpatches.Patch(color='orange', label=array_as_s[2])

        # 创建分段图例
        # legend = ax1.legend(
        #     handles=[proxy_artist1, proxy_artist2, proxy_artist3],
        #     loc='lower right',
        #     # title='Legend Title',
        # )
        ax1.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        gls = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                            linewidth=0)
        gls.top_labels = False
        gls.right_labels = False
        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=600)
        plt.show()

    def map_ini_sixteen_simple_legend(self, datas, lonlat, name, pltset):
        # matplotlib.use('Agg')
        proj = ccrs.PlateCarree()

        fig = plt.figure(figsize=(32, 18))
        axes_class = (GeoAxes,
                      dict(projection=proj))
        axgr = AxesGrid(fig, 111, axes_class=axes_class,
                        nrows_ncols=(4, 4),
                        axes_pad=0.6,
                        label_mode='keep')
        # 展示条的大小值，与间隔

        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        # 画图
        legend_data = []
        norm = pltset['norm']
        # 创建单色的colormap
        data_index = 0
        data_index_i = 0
        datas = datas[0]
        for i, ax in enumerate(axgr):
            var_data = datas[data_index][data_index_i]
            if i != 0 and i % 4 == 0:
                data_index += 1
                data_index_i = 0

            else:
                data_index_i = i % 4
            if i % 4 == 0:
                ax.text(-0.2, 0.5, name[data_index], rotation=90, va='center', ha='center', transform=ax.transAxes,
                        fontsize=20)
            if data_index == 0:
                ax.text(0.5, 1.2, pltset['title'][i], va='center', ha='center', transform=ax.transAxes, fontsize=20)

            # ax.set_title(name[data_index_i])

            ax.coastlines()
            # 在左侧添加文字

            # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
            ax.set_global()
            # ax.stock_img()
            ax.coastlines()
            ax.add_feature(cfeat.BORDERS, zorder=2)
            ranges = pltset['legend']
            legend_data = []
            j = 0

            while j < len(ranges):
                range_data = ranges[j]
                cmap1 = mcolors.ListedColormap([pltset['cmap'][j]])
                array_as_s = '~'.join(map(str, range_data))
                a1 = ax.imshow(np.where((var_data >= ranges[j][0]) & (var_data <= ranges[j][1]), var_data, np.nan),
                               extent=[lon_min, lon_max, lat_min, lat_max],
                               origin='lower', cmap=cmap1,
                               norm=colors.Normalize(vmin=ranges[j][0], vmax=ranges[j][1]), transform=proj,
                               label=array_as_s)

                # 创建代理艺术家用于图例
                proxy_artist1 = mpatches.Patch(color=pltset['cmap'][j], label=array_as_s)
                legend_data.append(proxy_artist1)
                ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
                gls = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                                   linewidth=0)
                gls.top_labels = False
                gls.right_labels = False
                j += 1
        legend_ax = fig.add_subplot(222)
        # 隐藏图例子图的坐标轴
        legend_ax.axis('off')
        array_as_string = '\n'.join(['~'.join(map(str, row)) for row in ranges])
        array_as_s = array_as_string.split('\n')
        proxy_artist1 = mpatches.Patch(color='blue', label=array_as_s[0])
        proxy_artist2 = mpatches.Patch(color='green', label=array_as_s[1])
        proxy_artist3 = mpatches.Patch(color='orange', label=array_as_s[2])
        legend_ax.legend(handles=[proxy_artist1, proxy_artist2, proxy_artist3], loc='lower right',
                         bbox_to_anchor=(0, -1.3),
                         prop={'size': 16}, ncol=3)
        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=600)
        # plt.savefig(file_save[:-3]+'pdf', dpi=1200)
        # plt.show()

    def map_ini_more_fig(self, datas, lonlat, name, pltset):
        # matplotlib.use('Agg')
        proj = ccrs.PlateCarree()
        datas = datas[0]

        fig = plt.figure(figsize=(32, 18))
        axes_class = (GeoAxes,
                      dict(projection=proj))
        sub_y = pltset['suby']
        sub_x = len(datas) / sub_y
        axgr = AxesGrid(fig, 111, axes_class=axes_class,
                        nrows_ncols=(4, 4),
                        axes_pad=0.6,
                        label_mode='keep')
        # 展示条的大小值，与间隔

        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        # 画图
        legend_data = []
        norm = pltset['norm']
        # 创建单色的colormap
        data_index = 0
        data_index_i = 0
        for i, ax in enumerate(axgr):
            var_data = datas[data_index][data_index_i]
            if i != 0 and i % 4 == 0:
                data_index += 1
                data_index_i = 0

            else:
                data_index_i = i % 4
            if i % 4 == 0:
                ax.text(-0.2, 0.5, name[data_index], rotation=90, va='center', ha='center', transform=ax.transAxes,
                        fontsize=20)
            if data_index == 0:
                ax.text(0.5, 1.2, pltset['title'][i], va='center', ha='center', transform=ax.transAxes, fontsize=20)

            # ax.set_title(name[data_index_i])

            ax.coastlines()
            # 在左侧添加文字

            # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
            ax.set_global()
            # ax.stock_img()
            ax.coastlines()
            ax.add_feature(cfeat.BORDERS, zorder=2)
            ranges = pltset['legend']
            legend_data = []
            j = 0

            while j < len(ranges):
                range_data = ranges[j]
                cmap1 = mcolors.ListedColormap([pltset['cmap'][j]])
                array_as_s = '~'.join(map(str, range_data))
                a1 = ax.imshow(np.where((var_data >= ranges[j][0]) & (var_data <= ranges[j][1]), var_data, np.nan),
                               extent=[lon_min, lon_max, lat_min, lat_max],
                               origin='lower', cmap=cmap1,
                               norm=colors.Normalize(vmin=ranges[j][0], vmax=ranges[j][1]), transform=proj,
                               label=array_as_s)

                # 创建代理艺术家用于图例
                proxy_artist1 = mpatches.Patch(color=pltset['cmap'][j], label=array_as_s)
                legend_data.append(proxy_artist1)
                ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
                gls = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                                   linewidth=0)
                gls.top_labels = False
                gls.right_labels = False
                j += 1
        legend_ax = fig.add_subplot(222)
        # 隐藏图例子图的坐标轴
        legend_ax.axis('off')
        array_as_string = '\n'.join(['~'.join(map(str, row)) for row in ranges])
        array_as_s = array_as_string.split('\n')
        proxy_artist1 = mpatches.Patch(color='blue', label=array_as_s[0])
        proxy_artist2 = mpatches.Patch(color='green', label=array_as_s[1])
        proxy_artist3 = mpatches.Patch(color='orange', label=array_as_s[2])
        legend_ax.legend(handles=[proxy_artist1, proxy_artist2, proxy_artist3], loc='lower right',
                         bbox_to_anchor=(0, -1.3),
                         prop={'size': 16}, ncol=3)
        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=300)
        # plt.savefig(file_save[:-3]+'pdf', dpi=1200)
        # plt.show()

    def map_ini_more_fig_2(self, datas, lonlat, name, pltset):
        # matplotlib.use('Agg')
        proj = ccrs.PlateCarree()
        datas = datas[0]

        fig = plt.figure(figsize=(32, 18))
        axes_class = (GeoAxes,
                      dict(projection=proj))
        sub_y = pltset['suby']
        sub_x = len(datas) / sub_y
        fig, axs = plt.subplots(int(sub_x), int(sub_y), figsize=(16, 9), layout='constrained')
        # 展示条的大小值，与间隔

        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        # 画图
        legend_data = []
        norm = pltset['norm']
        # 创建单色的colormap
        k = 0
        l = 0
        proj = ccrs.PlateCarree()
        # 画图

        for i, data in enumerate(datas):
            var_data = data
            axs[k, l] = plt.axes(projection=proj)
            # ax[k, l].text(0.5, 1.2, pltset['title'][i], va='center', ha='center', transform=ax.transAxes, fontsize=20)
            # ax.set_title(name[data_index_i])
            axs[k, l].coastlines()
            # 在左侧添加文字

            # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
            axs[k, l].set_global()
            axs[k, l].add_feature(cfeat.BORDERS, zorder=2)
            ranges = pltset['legend']
            legend_data = []
            j = 0

            img = axs[k, l].imshow(var_data,
                                   extent=[lon_min, lon_max, lat_min, lat_max],
                                   origin='lower', cmap=pltset['cmap'][0],
                                   norm=colors.Normalize(vmin=ranges[0][0], vmax=ranges[0][1]), transform=proj,
                                   label=pltset['lable'][i])
            axs[k, l].text(0.96, 0.91, pltset['lable'][i], transform=axs[k, l].transAxes,
                           fontsize=12, ha='right', va='top')
            cbar = plt.colorbar(img, ax=axs[k, l], shrink=0.7)
            # 添加单位
            cbar.ax.set_title(pltset['unit'][0], fontsize=10)
            cbar.locator = MultipleLocator(5)
            cbar.update_ticks()

            if l != 0 and l % sub_y == 0:
                k += 1
                l = 0
            j += 1

        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=300)
        # plt.savefig(file_save[:-3]+'pdf', dpi=1200)
        # plt.show()

    def map_ini_more_fig_1(self, datas, lonlat, name, pltset):
        # matplotlib.use('Agg')
        proj = ccrs.PlateCarree()
        datas = datas[0]

        sub_y = pltset['suby']
        sub_x = int(len(datas) / sub_y) + (len(datas) % sub_y > 0)  # 确保有足够的行

        fig, axs = plt.subplots(sub_x, sub_y, figsize=(16, 3), subplot_kw={'projection': proj},
                                constrained_layout=True)

        lon_min, lon_max, lat_min, lat_max = lonlat.values()

        for i, data in enumerate(datas):
            k, l = divmod(i, sub_y)
            ax = axs[k, l] if sub_x > 1 else axs[l]

            ax.coastlines()
            ax.set_global()
            ax.add_feature(cfeat.BORDERS, zorder=2, linewidth=2)
            ax.add_feature(cfeat.STATES, zorder=4, alpha=0.5, edgecolor='gray', linewidth=1)
            ax.set_title(pltset['title'][i], fontsize=16)
            ranges = pltset['norm']
            img = ax.imshow(data, extent=[lon_min, lon_max, lat_min, lat_max], origin='lower',
                            cmap=pltset['cmap'][0], norm=colors.Normalize(vmin=ranges[0][0], vmax=ranges[0][1]),
                            transform=proj)
            ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=proj)
            ax.text(0.05, 0.97, pltset['label'][i], transform=ax.transAxes, fontsize=16, ha='left', va='top')
            # if (i + 1) % sub_y == 0:
            #     cbar = plt.colorbar(img, ax=ax, shrink=0.7)
            #     cbar.ax.set_title(pltset['unit'][0], fontsize=10)
            #     cbar.locator = MultipleLocator(5)
            #     cbar.set_ticks(FixedLocator(ranges[0]))
            #     cbar.update_ticks()
            ax.tick_params(axis='x', labelsize=24)  # 设置 x 轴刻度标签的大小
            ax.tick_params(axis='y', labelsize=24)

            gls = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                               linewidth=0)
            gls.top_labels = False
            gls.right_labels = False
            gls.xlabel_style = {'size': 16}  # 设置 x 轴标签的字体大小
            gls.ylabel_style = {'size': 16}

            # cbar = plt.colorbar(img, ax=axs[0, :].ravel().tolist(), orientation='horizontal', shrink=0.3, pad=0.1)
        # 只有一行子图时
        # cbar = plt.colorbar(img, ax=axs, orientation='horizontal', shrink=0.3, pad=0.1)
        # cbar.ax.set_title(pltset['unit'][0], fontsize=16)
        # if ranges[0][1] > 10:
        #     cbar.locator = MultipleLocator(5)
        # else:
        #     cbar.set_ticks(FixedLocator(ranges[0]))
        # cbar.update_ticks()
        # cbar.ax.tick_params(labelsize=16)
        file_save = pltset['save']
        plt.savefig(file_save, dpi=600)

    def map_ini_twelve_simple_legend(self, datas, lonlat, name, pltset):
        # matplotlib.use('Agg')
        proj = ccrs.PlateCarree()

        fig = plt.figure(figsize=(32, 18))
        # fig.suptitle(pltset['title'], fontsize=18,x=0.5,y=0.95)
        axes_class = (GeoAxes,
                      dict(projection=proj))
        axgr = AxesGrid(fig, 111, axes_class=axes_class,
                        nrows_ncols=(3, 4),
                        axes_pad=0.6,
                        label_mode='keep')
        # 展示条的大小值，与间隔

        lon_min = lonlat["lon_min"]
        lon_max = lonlat["lon_max"]
        lat_min = lonlat["lat_min"]
        lat_max = lonlat["lat_max"]

        # 画图
        legend_data = []
        norm = pltset['norm']
        # 创建单色的colormap
        data_index = 0
        data_index_i = 0
        data_index_j = 0
        datas = datas[0]
        for i, ax in enumerate(axgr):
            var_data = datas[data_index_j]
            if i != 0 and i % 4 == 0:
                data_index += 1
                data_index_i = 0

            else:
                data_index_i = i % 4
            if i % 4 == 0:
                ax.text(-0.2, 0.5, name[data_index], rotation=90, va='center', ha='center', transform=ax.transAxes,
                        fontsize=20)
            if data_index == 0:
                pass
            if data_index_j == 1:
                ax.text(1, 1.2, pltset['title'], va='center', ha='center', transform=ax.transAxes, fontsize=20)

            data_index_j += 1
            # ax.set_title(name[data_index_i])

            ax.coastlines()
            # 在左侧添加文字

            # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
            ax.set_global()
            # ax.stock_img()
            ax.coastlines()
            ax.add_feature(cfeat.BORDERS, zorder=2)
            ranges = pltset['legend']
            legend_data = []
            cmap1 = mcolors.ListedColormap([pltset['cmap']])
            cmap2 = mcolors.ListedColormap(['g', 'b', 'r', ])
            a1 = ax.imshow(var_data,
                           extent=[lon_min, lon_max, lat_min, lat_max],
                           origin='lower', cmap='coolwarm',
                           norm=colors.Normalize(vmin=norm[0][0], vmax=norm[0][1]), transform=proj,
                           label='')
            cbar = plt.colorbar(a1, ax=ax, shrink=0.7, anchor=(1.5, 0.5))
            # 添加单位
            cbar.ax.set_title(pltset['unit'][0], fontsize=10)

            # 创建代理艺术家用于图例
            # proxy_artist1 = mpatches.Patch(color=cmap1)
            # legend_data.append(proxy_artist1)
            ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
            gls = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                               linewidth=0)
            gls.top_labels = False
            gls.right_labels = False
        # legend_ax = fig.add_subplot(222)
        # 隐藏图例子图的坐标轴
        # legend_ax.axis('off')
        # array_as_string = '\n'.join(['~'.join(map(str, row)) for row in ranges])
        # array_as_s = array_as_string.split('\n')
        # proxy_artist1 = mpatches.Patch(color='blue', label=array_as_s[0])
        # proxy_artist2 = mpatches.Patch(color='green', label=array_as_s[1])
        # proxy_artist3 = mpatches.Patch(color='orange', label=array_as_s[2])
        # legend_ax.legend(handles=[proxy_artist1, proxy_artist2, proxy_artist3], loc='lower right',
        #                  bbox_to_anchor=(0, -1.3),
        #                  prop={'size': 16}, ncol=3)
        # plt.legend(handles=legend_data, loc='lower left', bbox_to_anchor=(0, -0.3),
        #            ncol=3)
        file_save = pltset['save']
        # dpi=600提高分辨率
        plt.savefig(file_save, dpi=600)
        # plt.savefig(file_save[:-3]+'pdf', dpi=1200)
        # plt.show()

    def map_ini_one(datas, lons, lats, name, pltset, dataset):
        # figsize = (n, n) 设置图片像素
        fig = plt.figure(figsize=(10, 10))
        cbar_kwargs = {
            'orientation': 'horizontal',
            'label': name[0],
            'shrink': 0.8,
        }
        # 画图

        ax1 = plt.axes(projection=ccrs.PlateCarree())
        # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        ax1.set_global()
        ax1.coastlines()
        ax1.add_feature(cfeat.BORDERS, zorder=2)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        # ax1.add_feature(cfeat.STATES, zorder=4)
        # 标题
        ax1.set_title(pltset["title"][0])
        # 添加面
        polygon_1 = ax1.contourf(lons, lats, datas[0],
                                 transform=ccrs.PlateCarree(),
                                 cmap='OrRd')
        # line_c = ax1.contour(lons, lats, datas[1], levels=pic_1.levels,
        #                     colors=['black'],
        #                     transform=ccrs.PlateCarree())
        # 展示条
        fig.colorbar(polygon_1, orientation='horizontal')
        # 范围
        ax1.set_extent([-125, -67.9, 29, 50.4], crs=ccrs.PlateCarree())

        ax1.stock_img()
        # 全屏保存
        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
        plt.savefig(pltset["title"][0])
        plt.show()

    def nc_map_display(self, file, varname):
        # 打开netCDF文件
        ds = xr.open_dataset(file)
        # 读取变量和属性
        var_name = varname
        # var = ds[var_name].sel(south_north=slice(1, 50), west_east=slice(1, 50)).isel(Time=1)
        var = ds[var_name]
        print(var.values)
        # for i in var.values[0]:
        #     print(i)
        var_units = var.units
        # lon = ds['lon']
        # lat = ds['lat']

        # 关闭netCDF文件
        ds.close()

        # 绘制图形
        # var.plot()
        proj = ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        # ax1 = plt.axes(projection=ccrs.PlateCarree())
        # # 加载国界、海岸线、河流、湖泊,zorder 确定图层顺序
        # ax1.set_global()
        # ax1.coastlines()

        ax.set_global()
        ax.coastlines()
        ax.stock_img()
        extent = [-124.9375, -67.0625, 25.0625, 52.9375]
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeat.BORDERS, zorder=2)
        # im1 = ax.imshow(var[0], extent=extent,
        #                 origin='lower', transform=proj)

        # gls = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
        #                    color='k', linestyle='dashed', linewidth=0.3, alpha=1,
        #                    y_inline=False, x_inline=False,
        #                    rotate_labels=0, xpadding=5,
        #                    xlocs=range(-180, 180, 10), ylocs=range(-90, 90, 10),
        #                    xlabel_style={"size": 8},
        #                    ylabel_style={"size": 8}
        #                    )

        gls = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                           linewidth=0)
        gls.top_labels = False
        gls.right_labels = False
        ax.set_title('the North American Region ')
        # 添加比例尺
        # scalebar  = AnchoredSizeBar(ax.transData, 3, '3 units', 4, pad=0.5,
        #                                  sep=5, borderpad=0.5, frameon=False,
        #                                  size_vertical=0.5, color='k',
        #                                  )
        # scalebar = ScaleBar(1, location='lower right', units='km', scale_loc='bottom', length_fraction=0.1)
        # ax.add_artist(scalebar)
        # north_arrow_x =-120  # 指北针的X坐标
        # north_arrow_y = 30  # 指北针的Y坐标
        # north_arrow_length = 10  # 指北针的长度
        # north_arrow_label = 'N'  # 指北针的标签
        #
        # # 绘制指北针箭头
        # ax.annotate(north_arrow_label, xy=(north_arrow_x, north_arrow_y),
        #             xytext=(north_arrow_x, north_arrow_y + north_arrow_length),
        #             arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=2', alpha=0.7))

        self.add_scalebar(ax, lon0=-75, lat0=26, length=500)

        self.add_north(ax)

        # 添加指北针
        # compass = AnchoredDrawingArea(width=0.4, height=0.2, xdescent=45, ydescent=45, loc='upper left')
        # ax.add_artist(compass)
        # 自带的方向箭头
        # arrows = AnchoredDirectionArrows(ax.transAxes, 'N', 'E',
        #                                  loc='upper right', color='k',
        #                                  aspect_ratio=1, sep_x=0.01,
        #                                  sep_y=-0.01,
        #                                  text_props={'ec': 'w', 'fc': 'k'},
        #                                  )
        # ax.add_artist(arrows)

        # 设置坐标轴范围

        # ell = AnchoredEllipse(ax.transAxes, width=2, height=1, angle=45, loc='upper right', )
        # ax.add_artist(ell)
        # 鹰眼
        # box = AnchoredAuxTransformBox(ax.transData, loc='upper left')
        # el = Ellipse((0, 0), width=0.1, height=0.4, angle=30)
        # box.drawing_area.add_artist(el)
        # ax.add_artist(box)

        # cbar = plt.colorbar(im1, ax=ax, shrink=0.7)
        # 添加单位
        # cbar.ax.set_title('test1', fontsize=10)
        # ax.add_feature(cfeat.RIVERS, zorder=3)
        # ax.add_feature(cfeat.STATES, zorder=4)
        # 标题
        # ax1.set_title(pltset["title"][0])
        # plt.xlabel('west_east')
        # plt.ylabel('south_north')
        # plt.title(var_name)

        plt.show()

    def nc_grass_display(self, file, varname):
        # 打开netCDF文件
        ds = xr.open_dataset(file).sortby("south_north", ascending=True)

        # 筛选草地类型数据
        grassland_data = ds[varname].where(ds['IVGTYP'] == 16, drop=True)
        # 绘制图形
        grassland_data.plot()
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Grassland Data')
        plt.show()

    def add_north(self, ax, labelsize=10, loc_x=0.97, loc_y=1.05, width=0.02, height=0.06, pad=0.14):
        """
        画一个比例尺带'N'文字注释
        主要参数如下
        :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
        :param labelsize: 显示'N'文字的大小
        :param loc_x: 以文字下部为中心的占整个ax横向比例
        :param loc_y: 以文字下部为中心的占整个ax纵向比例
        :param width: 指南针占ax比例宽度
        :param height: 指南针占ax比例高度
        :param pad: 文字符号占ax比例间隙
        :return: None
        """
        minx, maxx = ax.get_xlim()
        miny, maxy = ax.get_ylim()
        ylen = maxy - miny
        xlen = maxx - minx
        left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
        right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
        top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
        center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
        triangle = mpatches.Polygon([left, top, right, center], color='k')
        ax.text(s='N',
                x=minx + xlen * loc_x,
                y=miny + ylen * (loc_y - pad + height),
                fontsize=labelsize,
                horizontalalignment='center',
                verticalalignment='bottom')
        ax.add_patch(triangle)

    def add_scalebar(self, ax, lon0, lat0, length, size=0.5):
        '''
        ax: 坐标轴
        lon0: 经度
        lat0: 纬度
        length: 长度
        size: 控制粗细和距离的
        '''
        # style 3
        ax.hlines(y=lat0, xmin=lon0, xmax=lon0 + length / 111, colors="black", ls="-", lw=2, label='%d km' % (length))
        ax.vlines(x=lon0, ymin=lat0 - size, ymax=lat0 + size, colors="black", ls="-", lw=2)
        ax.vlines(x=lon0 + length / 2 / 111, ymin=lat0 - size, ymax=lat0 + size, colors="black", ls="-", lw=2)
        ax.vlines(x=lon0 + length / 111, ymin=lat0 - size, ymax=lat0 + size, colors="black", ls="-", lw=2)
        ax.text(lon0 + length / 111, lat0 + size + 0.05, '%d' % (length), horizontalalignment='center', fontsize=16)
        ax.text(lon0 + length / 2 / 111, lat0 + size + 0.05, '%d' % (length / 2), horizontalalignment='center',
                fontsize=16)
        ax.text(lon0, lat0 + size + 0.05, '0', horizontalalignment='center', fontsize=16)
        ax.text(lon0 + length / 111 / 2 * 2 + 1.8, lat0 + size + 0.05, 'km', horizontalalignment='center', fontsize=16)


if __name__ == '__main__':
    dis_map = Display_Plot_Map()
    file = r'F:\Noah\data\1982_huo_out\20230524\loop1\loop0\output.19821001.nc.loop0001'
    dis_map.nc_map_display(file, 'GPP')
    pass
