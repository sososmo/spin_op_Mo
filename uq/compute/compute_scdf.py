import os
import numpy as np
import xarray as xr
from scipy.stats import norm
import geopandas as gpd
from time import sleep
import re
import pandas as pd
import time
from rasterio.transform import from_origin
import rasterio.features as features
from netCDF4 import Dataset


class Compute_Data_Scdf(object):
    def __init__(self) -> None:
        self.input_path = '/public1/home/scfa3271/soso/Noah-MP/results/test_01'
        self.out_path = ''
        self.var_read = ''
        self.input_name = '/public1/home/scfa3271/soso/python/data'
        self.file = ''
        self.vali_year = [1983, 1988, 2003]
        self.default_value = "default_value"

    '''
    Calculation of Simulation Data
    '''

    def data_simulation_scdf(self, compute_tpye):
        var_input_arr = ['GPP', 'LH']
        # var_input_arr = ['LH']
        datas_all = []
        for var_input in var_input_arr:
            datas = []
            self.var_read = var_input
            files_years = []
            for year_r in self.vali_year:
                year_str = 'output.' + str(year_r)
                nc_files = self.file_all(self.input_path, '.nc', year_str, True)
                files_years.extend(nc_files['files'])
            # 倒序

            files = sorted(files_years, key=lambda x: x.split('.')[1])
            nc_datas = self.files_one(self.input_path, '.nc', False, [var_input], files)
            return_data = self.compute_compare_all_scdf(files, nc_datas,
                                                        var_input,
                                                        compute_tpye)
            datas = return_data['datas']
            print(datas)
            print(np.nanmean(datas), 'mean')
            datas_all.append(datas)
        print(datas_all, 'datas_all')
        np.savetxt('scdf_python_data.txt', datas_all, delimiter=' ')
        return datas_all

    '''
    Validation Data from 1982 to 2011
    '''

    def map_vali_data(self, compute_tpye, year, var_arr=['GPP']):
        # var_arr = ['GPP']
        varify_attrs = self.plot_gpp_lh()
        land = self.get_wrf_data('land')
        land_cover = land['land_cover']
        shp_geom = self.read_shp_geom()
        attrs = []
        attrs_map = []
        units = []
        norm = []
        year_i = year - 1982
        year_i_min = year_i * 12
        year_i_max = year_i * 12 + 12
        for i in var_arr:
            varify_attr = varify_attrs[i]
            j = year_i_min
            # while j < len(varify_attrs[i]):
            arr_mean = []
            x_aix = []
            while j >= year_i_min and j < year_i_max:
                varify_attr_j = varify_attr[j]
                # varify_attr_j = np.ma.filled(varify_attr_j, fill_value=0)
                var_data_1 = np.ma.filled(varify_attr_j, fill_value=0)
                var_data_1 = np.where(shp_geom == True, var_data_1, np.nan)
                var_data_1 = np.where((land_cover == 7), var_data_1, np.nan)
                if i == 'GPP':
                    var_data_1 = var_data_1 * 1000 * 86400
                else:
                    var_data_1 = var_data_1 * 1000000.0 / 86400

                arr_mean = var_data_1
                j += 1
                aix_name = str(j) + '月'
                x_aix.append(aix_name)
                attrs.append(arr_mean)
                attrs_map.append(varify_attr_j)
        return {
            'validation': attrs,
            'land_cover': land_cover,
            'shp_geom': shp_geom
        }

    def plot_gpp_lh(self):
        arr_data = ['GPP', 'LE']
        varify_attrs = {}
        for i in arr_data:
            in_dir_verify = self.input_name + '/data_jung/test_jung_huo/' + i
            varify_data = self.files_one(in_dir_verify, 'nc', False, [i])
            varify_attr = varify_data[0]['data'][i]
            lat_name, lon_name = 'LATITUDE', 'LONGITUDE'
            lat_data, lon_data = varify_data[0]['data'][lat_name], varify_data[0]['data'][lon_name]
            if i == 'LE':
                i = 'LH'
            varify_attrs[i] = varify_attr
            varify_attrs[lat_name] = lat_data
            varify_attrs[lon_name] = lon_data

        return varify_attrs

    '''
    wrfinput Data
    '''

    def get_wrf_data(self, land_type_data):
        # in_dir = input('输入文件路径：')
        # in_dir = self.input_path
        # out_dir = self.out_path
        shp_geom = self.read_shp_geom()

        in_dir = self.input_name + r'/Noah/data/wrf_out'
        # in_dir = r'F:\Noah\data\1987_out\wrf'

        out_dir = self.input_name + r'/Noah/data'
        nc_files = self.file_all(in_dir, '.nc')
        nc_file_veg = nc_files['roads'][0]
        nc_data_veg = xr.open_dataset(nc_file_veg)
        files = nc_files['roads']

        if land_type_data == 'soil':
            var_input = 'ISLTYP'
        else:
            var_input = 'IVGTYP'

        var_arr_one = var_input.split(";")
        var_arr = []
        for var_i in var_arr_one:
            var_i = var_i.split(",")
            var_arr.append(var_i)

        print(var_arr)
        nc_i = 0
        for nc in files:
            print(nc)
            sleep(2)
            if len(files) > 0 and ';' in var_input:
                var_j = nc_i
            else:
                var_j = 0
            nc_file = nc
            nc_file_name = nc_files['files'][nc_i]
            # print(nc)
            nc_data = xr.open_dataset(nc_file)
            name_time = nc_data.get('Times', default=self.default_value)
  
            print(name_time, type(name_time))
            k = 0
            for time_i in name_time.values:
                print(k)
                print(time_i)
                if isinstance(time_i, bytes):
                    time_i = str(time_i, encoding='utf-8')
                time_i = str(time_i)
                index_h = time_i.find(':')
                index_d = time_i.find('_')
                index_m = time_i.find('-')
                str_d = time_i[index_d - 2:index_d]
                str_d = int(str_d)
                str_h = time_i[index_h - 2:index_h]
                str_h = int(str_h)
                str_m = time_i[index_m + 1:index_m + 3]
                str_m = int(str_m)
                print(str_m, str_d, str_h, )
                # if 20 < str_h < 23 and (str_d == 5 or
                if (str_h == 0) and (str_d == 1):
                    # 设置属性的index
                    var_index = k
                    name = time_i
                    lat_name, lon_name = 'XLAT', 'XLONG'
                    lat_data, lon_data = nc_data[lat_name][var_index].values, nc_data[lon_name][
                        var_index].values

                    lon_data = np.where(np.abs(lon_data) > 1e10, np.nan, lon_data)
                    lat_data = np.where(np.abs(lat_data) > 1e10, np.nan, lat_data)
                    lon_min = np.nanmin(lon_data)
                    lon_max = np.nanmax(lon_data)
                    lat_min = np.nanmin(lat_data)
                    lat_max = np.nanmax(lat_data)
                    land_cover = nc_data.get('IVGTYP', default=self.default_value)
                    land_cover = land_cover[var_index]
                    lonlat = {
                        "lon_min": lon_min,
                        "lon_max": lon_max,
                        "lat_min": lat_min,
                        "lat_max": lat_max
                    }
                    print(lonlat)
                    if land_type_data == 'land' or land_type_data == 'soil':
                        return {
                            "land_cover": land_cover,
                            'lonlat': lonlat
                        }
                k += 1

            nc_i += 1

    '''
    shp extent
    '''

    def read_shp_geom(self, data=None):
        in_dir = self.input_name + r'/arcgis/data_america/polygon.shp'
        sf = gpd.read_file(in_dir)
        lat1 = np.arange(25.0625, 52.9375 + 0.125, 0.125)
        lon1 = np.arange(-124.9375, -67.0625 + 0.125, 0.125)
        transform = from_origin(-124.9375, 25.0625, 0.125, -0.125)
        first_geometry = sf['geometry'].iloc[0]
        shape_mask = features.geometry_mask([first_geometry],
                                            out_shape=(len(lat1), len(lon1)),
                                            invert=True,
                                            transform=transform)
        if data != None:
            shape_mask = xr.DataArray(shape_mask, dims=(data['x'], data['y']))
        else:
            shape_mask = xr.DataArray(shape_mask, dims=("south_north", "west_east"))

        return shape_mask

    '''
    NCPathName:org name
    '''

    def file_all(self, input_path, data_format, condition=None, match=False):
        file_name_list = os.listdir(input_path)
        arr_content = []
        arr_name = []
        for name in file_name_list:
            if condition != None:
                if match == True:
                    pattern = re.compile(fr'{condition}')
                    match_result = pattern.match(name)
                    if match_result:
                        file = input_path + os.sep + str(name)
                        arr_name.append(name)
                        arr_content.append(file)
                else:
                    if name.find(condition) != -1:
                        file = input_path + os.sep + str(name)
                        arr_name.append(name)
                        arr_content.append(file)

            else:
                file = input_path + os.sep + str(name)
                arr_name = file_name_list
                name_index = str(name).find(data_format)
                if (name_index == -1):
                    #    OutInput.WriteToNc(file)
                    pass
                else:
                    # print(file)
                    pass
                arr_content.append(file)

        return {
            "roads": arr_content,
            'files': arr_name
        }

    '''
    read data
    '''

    def files_one(self, input_path, data_format, isout, attr_name, roads=None):
        out_path = ''
        if roads != None:
            file_name_list = roads
        else:
            file_name_list = os.listdir(input_path)
        arr_content = []
        for name in file_name_list:
            self.file = input_path + os.sep + str(name)
            name_idx = str(name).find('.idx')
            if name_idx != -1:
                os.remove(self.file)
            else:
                name_index_end = str(name).find(data_format)
                if name_index_end != -1:
                    content = {}
                    if data_format == '.nc':
                        content = self.read_nc_data(name, attr_name)
                    elif data_format == 'nc':
                        content = self.read_nc_data_netcdf(name, attr_name)
                    elif data_format == '.shp':
                        content = self.read_shp_data(name, attr_name)
                    arr_content.append(content)
        if data_format == '.nc.loop':
            self.file = input_path + os.sep + '*' + data_format + '*'
            content = self.read_nc_files(name, attr_name)
            arr_content.append(content)
        if isout:
            # 输出log日志
            self.WriteLog(out_path, arr_content)
        else:
            # 返回数据
            return arr_content

    '''
    # Output .log
    '''

    def WriteLog(self, out_path, content):
        times = time.time()
        local_time = time.localtime(times)
        local_time = time.strftime("%Y-%m-%d%H%M%S", local_time)
        # Y 年 - m 月 - d 日 H 时 - M 分 - S 秒
        path = out_path + os.sep + local_time + '.log'
        print('输出路径', path)
        # file = open(path, 'w')
        # list to str
        string_cont = [str(x) for x in content]
        # dict to str to bytes
        cont = bytes(str(string_cont), encoding='utf-8')
        with open(path, 'wb') as contents:
            contents.write(cont)
            print('log is outputed')

    '''
    Reading .nc
    '''

    def read_nc_data(self, name, attr_name):
        name_index = str(name).find('.nc')
        if name_index == -1:
            self.WriteToNc(self.file)
        else:
            data = xr.open_dataset(self.file)
            print('data为:', data)
            variable = data.variables
            print("文件为：", self.file)
            content = {
                "file": self.file,
                "filename": str(name),
                "variable": variable,
                "data": data,
                "attr_name": ''
            }
            # 获取属性值，属性值为一个字符串数组
            if len(attr_name) > 0:
                attrs = self.ReadDataAttr(data, attr_name)
                content['attr_name'] = attrs
            return content

    '''
    read shpfile
    '''

    def read_shp_data(self, name, attr_name):
        a = gpd.read_file(self.file)

    '''
    read loop file
    '''

    def read_nc_files(self, name, attr_name):
        name_index = str(name).find('.nc')
        if name_index == -1:
            self.WriteToNc(self.file)
        else:
            data = xr.open_mfdataset(self.file, concat_dim="time", combine='nested', engine='netcdf4')
            print('data为:', data)
            # variable = data.variables
            print("文件为：", self.file)
            content = {
                "file": self.file,
                "filename": str(name),
                "data": data,
                "attr_name": ''
            }
            # 获取属性值，属性值为一个字符串数组
            if len(attr_name) > 0:
                attrs = self.ReadDataAttr(data, attr_name)
                content['attr_name'] = attrs
            return content
        pass

    '''Reading .nc by netcdf4'''

    def read_nc_data_netcdf(self, name, attr_name):

        name_index = str(name).find('.nc')
        if name_index == -1:
            self.WriteToNc(self.file)
        else:
            print("文件为：", self.file)
            data = Dataset(self.file, "r")
            variable = data.ncattrs()
            # print(data.variables['GPP'])
            variablearr = []
            if len(attr_name) > 0:
                for attr in attr_name:
                    variable_one = data.variables[attr][:]
                    variablearr.append(variable_one)
            content = {
                "file": self.file,
                "filename": str(name),
                "variable": variable,
                "data": data,
                "attr_name": variablearr,
                # "variable_value": variablearr,
                # 'dimention': dimobjarr
            }
            return content

    '''
    Retrieve Attribute Values as a String Array
    '''

    def ReadDataAttr(self, data, attr_name):
        attrs = []
        for attr_one in attr_name:
            attr = data[attr_one]
            attr_data = data[attr_one].variable.attrs
            attrs.append({
                attr_one: attr,
                'Attributes': attr_data
            })
        return attrs

    def out_month_mean(self, out_datas, valdata, land_cover, shp_geom, vail=False):
        datas = 0
        outdata = None
        var_data_1 = None
        out_data_sq = None
        # 模拟数据
        # data_sim = out_datas.sum(dim='Time')
        # data_sim = out_datas.mean(dim='Time')
        data_sim = out_datas.where(shp_geom == True)
        data_sim = data_sim.where(land_cover == 7)
        data_sim = data_sim.mean(dim='Time')

        # data_sim = data_sim.where((land_cover == 7) | (land_cover == 11))
        if self.var_read == 'LH':
            # data_sim = (data_sim / len(out_datas))
            data_sim = data_sim

        else:
            data_sim = data_sim * 86400
        datas = data_sim
        # 验证数据
        if vail == True:
            var_data_1 = valdata
            outdata = np.sqrt((datas - var_data_1) ** 2)
            out_data_sq = (datas - var_data_1) ** 2
            print(np.nanmean(out_data_sq), ':out_data_sq', np.nanmean(var_data_1), ':var_data_1')
            # print('maxrmse', np.sum(outdata > 2), np.sum(outdata > 1), np.nanmax(outdata),
            #       'np.sum((~np.isnan(data_sim)) & (data_sim == 0))')
        # self.write_to_excel(self.title_name, datas)
        return {
            'simdata': datas,
            'valdata': var_data_1,
            'outdata': outdata,
            'out_data_sq': out_data_sq
        }

    def out_month_mean_vail(self, vali_data, land_cover, shp_geom, compute_tpye=None, ):
        var_data_arr = []
        var_data_arr_mean = []
        i = 0
        for valdata in vali_data:
            # var_data_1 = np.ma.filled(valdata, fill_value=0)
            # var_data_1 = np.where(shp_geom == True, var_data_1, np.nan)
            # var_data_1 = np.where(land_cover == 7, var_data_1, np.nan)
            # var_data_1 = var_data_1 * 1000 * 86400
            var_data_1 = valdata
            var_data_arr.append(var_data_1)
            valdata_mean = np.nanmean(var_data_1)
            var_data_arr_mean.append(valdata_mean)
            i += 2
        return {
            'valdata': var_data_arr,
            'valdata_mean': var_data_arr_mean,
        }

    '''
    Calculation of Simulation and Validation Comparison
    '''

    def compute_compare_all_scdf(self, files, nc_datas, var_input, compute_tpye):
        i = 0
        data_funcs = 0
        datas = []
        units = []
        x_aix = []
        vali_datas_out = []
        for vali_y in self.vali_year:
            vali_data_return = self.map_vali_data('compare', vali_y, [var_input])
            land_cover = vali_data_return['land_cover']
            shp_geom = vali_data_return['shp_geom']
            vali_data = vali_data_return['validation']
            vali_datas_out.append(vali_data)
        # 按第一轴拼接所有数组
        vali_datas_out = np.concatenate(vali_datas_out, axis=0)
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_datas_out[i]
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            # 筛选条件
            x_aix.append(i)
            if compute_tpye == 'SCDF' or compute_tpye == 'SCDFS' or compute_tpye == 'SCDF_RMSE':
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                data_func = return_data['out_data_sq']
                data_funcs = data_funcs + data_func
            i += 1
        if compute_tpye == 'SCDF' or compute_tpye == 'SCDFS':
            a = np.sqrt(data_funcs / len(nc_datas))
            sorted_data = np.sort(a.values.flatten())
            sorted_data = sorted_data[~np.isnan(sorted_data)]
            y_equals_1 = np.ones_like(sorted_data)
            theoretical_cdf = norm.cdf(sorted_data, loc=np.nanmean(a), scale=np.nanstd(a))
            area_under_curve = np.trapz(y_equals_1 - theoretical_cdf, sorted_data)
            datas.append(area_under_curve)
        elif compute_tpye == 'SCDF_RMSE':
            a = np.sqrt(data_funcs / len(nc_datas))

        return {
            "datas": datas,
            "x_aix": x_aix
        }


if __name__ == '__main__':
    Compute_Data_Scdf().data_simulation_scdf('SCDFS')
    pass
