from matplotlib import colors, patches
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.colors as mcolors
import matplotlib
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.geoaxes import GeoAxes
'''
    地图
'''


# matplotlib.use('Agg')
class Display_Plot_Map(object):
    def __init__(self) -> None:
        self.default_value = "default_value"

        pass
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


if __name__ == '__main__':
    pass
