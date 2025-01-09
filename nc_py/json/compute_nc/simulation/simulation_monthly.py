import os
from nc_py.out_input import OutInput
import numpy as np
import xarray as xr
import datetime
import nc_py.compute_nc.unit as unit
from nc_py.compute_nc.simulation.simulation import Compute_Data_Simulation as cdm


class Compute_Data_Simulation_Monthly(object):
    def __init__(self, data) -> None:
        self.data = data
        self.input_path = data["input_path"]
        self.out_path = data["out_path"]
        self.cdm = cdm(self.data)
        self.x_aix = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.unit_data = unit.get_unit()
        self.vali_year = [1983, 1988, 2003]
        self.year_cycles = {
            'GPP': {'1983': [1, 3, 10, 50],
                    '1988': [1, 3, 10, 50],
                    '2003': [1, 6, 10, 50],
                    '19821988': [1, 2, 5, 20],
                    '19822003': [1, 3, 5, 20], },
            'LH': {'1983': [1, 3, 10, 50],
                   '1988': [1, 3, 10, 50],
                   '2003': [1, 6, 10, 50],
                   '19821988': [1, 2, 5, 20],
                   '19822003': [1, 3, 5, 20], }

        }
        self. lonlat = {
                "lon_min": -124.9375,
                "lon_max": -67.0625,
                "lat_min": 25.0625,
                "lat_max": 52.9375
            }

        pass

    '''save OP Monthly to .nc'''
    def get_simulation_monthly_save(self, compute_tpye, dataset=None, year=1983, year_name=1983):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        var_input_arr = ['GPP', 'LH']
        path_name = self.input_path[self.input_path.rfind('/') + 1:]
        datas_all = []

        for var_input in var_input_arr:
            file_all_1 = sorted(os.listdir(self.input_path), key=lambda x: int(x[-2:]))
            file_all = file_all_1
            self.file_all = file_all
            x_aix = []
            datas_rmse = []
            datas = []
            [vali_data, land_cover, shp_geom] = self.cdm.vali_all(var_input, self.vali_year)
            for files_nc in file_all:
                nc_file = self.input_path + os.sep + files_nc
                data_change = OutInput({
                    "input_path": nc_file,
                    "out_path": self.out_path
                })

                read_file_son = self.cdm.read_file_son(data_change, var_input)
                files_arr = read_file_son['files_arr']
                nc_datas = read_file_son['nc_datas']
                print('files_arr:', files_arr)
                return_data = self.cdm.compare_mean(files_arr, nc_datas, vali_data, land_cover, shp_geom,
                                                    var_input,
                                                    compute_tpye)

                datas.append(return_data['datas'][0])
                self.units = return_data['units']
                self.x_aix = return_data['x_aix']
                xr_out = xr.DataArray(return_data['datas'][1]).rename({'dim_0': 'time'})
                datas_rmse.append(xr_out)
                print(len(return_data['datas'][1]),'保存长度')
            xr_vail_out = xr.DataArray(vali_data).rename({'dim_0': 'time'})
            datas_rmse.append(xr_vail_out)
            data_combined = xr.concat(datas_rmse, dim='time')
            sava_name_nc = '/Volumes/momo/op2024/op_20240710_out' + os.sep + var_input + compute_tpye + 'threeyear' + '.nc'
            ex = os.path.exists(sava_name_nc)
            if ex == False:
                data_combined.to_netcdf(sava_name_nc)  # 输出合并后的nc文件
            vali_mean = self.cdm.out_month_mean_vail(vali_data)['valdata_mean']
            datas.append(vali_mean)
            print("datas:", datas)

            datas = self.datas_compute(datas)
            print(datas)
            print(datas_rmse)
            sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + '0710.png'


            soil_T_title = ['TOP', 'MID', '1m', 'BOT']
            time_arr = [1, 2, 10, 20, 30, 40]
            soil_T_name = ['spin-up {} '.format(i) for i in time_arr]
            name = soil_T_name
            legend = [[0, 1], [0, 2], [0.0001, 2]]

            pltset = {
                'title': soil_T_title,
                'save': sava_name,
                'unit': self.units,
                'cmap': ['coolwarm', 'coolwarm', 'coolwarm'],
                'legend': var_input

            }
            pltset_out = cn.type_gpp_lh(pltset)
            data_in = {
                "datas": [datas],
                "lonlat": self.lonlat,
                "name": name,
            }
            pltset_out['legend'] = legend

            pltset_out['x'] = np.arange(1, 13, 1)
            pltset_out['legend'] = var_input
            data_in["name"] = 'Monthly average ' + var_input
            pltset_out['legend'] = var_input
            label_2 = ['Best_1', "Best_2", "Best_3", 'Default', 'Observation']
            pltset_out['label'] = label_2

            cn.data_map(data_in, 'moreline', pltset_out)
            datas_all.append(datas)
        return datas_all

    '''OP Monthly'''
    def get_simulation_monthly(self, compute_tpye, dataset=None, year=1983, year_name=1983):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        var_input_arr = ['GPP', 'LH']
        path_name = self.input_path[self.input_path.rfind('/') + 1:]
        datas_all = []

        for var_input in var_input_arr:
            data_change = OutInput({
                "input_path": self.input_path,
                "out_path": self.out_path
            })
            read_file_son = self.cdm.read_file_rmse(data_change, var_input)
            titles = []
            datas = []
            nc_datas = read_file_son['nc_datas']
            for data_one_index, data_one in enumerate(nc_datas):
                data_one= data_one['data'][var_input]
                titles.append('Best_' + str(data_one_index))
                self.units = [self.cdm.unit_data[var_input]['unit']]
                '月均值，12time'
                a = np.nanmean(data_one, axis=(1, 2))
                datas.append(a)


            print("datas:", datas)

            sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + '1016.png'
            soil_T_title = ['TOP', 'MID', '1m', 'BOT']
            time_arr = [1, 2, 10, 20, 30, 40]
            soil_T_name = ['spin-up {} '.format(i) for i in time_arr]
            name = soil_T_name
            legend = [[0, 1], [0, 2], [0.0001, 2]]

            pltset = {
                'title': soil_T_title,
                'save': sava_name,
                'unit': self.units,
                'cmap': ['coolwarm', 'coolwarm', 'coolwarm'],
                'legend': var_input

            }
            pltset_out = cn.type_gpp_lh(pltset)
            data_in = {
                "datas": [datas],
                "lonlat": self.lonlat,
                "name": name,
            }
            pltset_out['legend'] = legend

            pltset_out['x'] = np.arange(1, 13, 1)
            pltset_out['legend'] = var_input
            data_in["name"] = 'Average ' + var_input + '(' + self.units[0] + ')'
            pltset_out['legend'] = var_input
            label_2 = ['Observation', "1-Year Spin-Up", "10-Year Spin-Up"]
            pltset_out['xunit'] = ['month']
            pltset_out['label'] = label_2

            cn.data_map(data_in, 'moreline', pltset_out)
            datas_all.append(datas)
        return datas_all

    '''SPIN-UP Monthly'''
    def get_simulation_monthly_loop_change(self, compute_tpye, dataset=None, year=1983, year_name=1983):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        # 加载 NetCDF 数据
        data = OutInput(self.data)
        var_input_arr = ['GPP', 'LH']
        # var_input_arr = ['GPP']

        path_name = self.input_path[self.input_path.rfind('/') + 1:]
        datas_all = []

        for var_input in var_input_arr:

            file_all_1 = sorted(os.listdir(self.input_path), key=lambda x: int(x[-2:]))

            x_aix = []
            datas = []
            data_years_grid = []
            [vali_data, land_cover, shp_geom] = self.cdm.vali_all(var_input, [year])
            # 先加验证数据
            vali_mean = self.cdm.out_month_mean_vail(vali_data)['valdata_mean']
            datas.append(vali_mean)

            file_all = []

            [vali_data, land_cover, shp_geom] = self.cdm.vali_all(var_input, [year])
            for time_index, time_i in enumerate(self.year_cycles[var_input][str(year_name)]):
                if time_i < 10:
                    name_time_i = 'test_0' + str(time_i)
                else:
                    name_time_i = 'test_' + str(time_i)
                if name_time_i in file_all_1:
                    file_all.append(name_time_i)
            self.file_all = file_all
            print(self.file_all, 'self.file_all')
            for files_nc in file_all:
                nc_file = self.input_path + os.sep + files_nc
                data_change = OutInput({
                    "input_path": nc_file,
                    "out_path": self.out_path
                })

                read_file_son = self.cdm.read_file_son(data_change, var_input)
                files_arr = read_file_son['files_arr']
                nc_datas = read_file_son['nc_datas']
                print('files_arr:', files_arr)
                return_data = self.cdm.compare_mean(files_arr, nc_datas, vali_data, land_cover, shp_geom,
                                                    var_input,
                                                    compute_tpye)

                data_years = return_data['datas'][0]
                data_years_grid.extend(return_data['datas'][1])
                self.units = return_data['units']
                x_aix = return_data['x_aix']
                datas.append(data_years)
            print("datas:", datas, data_years_grid)
            # if need save #
            data_combined = xr.concat(data_years_grid, dim='time')
            sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + str(
                year_name) + files_nc + '.nc'
            ex = os.path.exists(sava_name)
            if ex == False:
                data_combined.to_netcdf(sava_name)
            sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + '.png'
            legend = [[0, 1], [0, 2], [0.0001, 2]]
            pltset = {
                'title': '',
                'save': sava_name,
                'unit': self.units,
                'cmap': ['coolwarm', 'coolwarm', 'coolwarm'],
                'legend': var_input

            }
            pltset_out = cn.type_gpp_lh(pltset)
            data_in = {
                "datas": [datas],
                "lonlat": self.lonlat,
                "name": '',
            }
            pltset_out['legend'] = legend

            pltset_out['x'] = self.x_aix
            pltset_out['legend'] = var_input
            time_arr_n = [str(int(file_i[-2:])) for file_i in self.file_all]
            label_2 = [
                var_input + ' for ' + str(num) + ' cycles' if num != "1" else var_input + ' for ' + str(num) + ' cycle'
                for num_i, num in enumerate(time_arr_n)]
            pltset_out['label'] = ['Observation']
            pltset_out['label'].extend(label_2)
            pltset_out['xunit'] = ['']
            data_in["name"] = var_input + ' in ' + str(year) + ' (' + str(
                self.units[0]) + ')'
            cn.data_map(data_in, 'moreline', pltset_out)
            datas_all.append(datas)
        return datas_all

    def datas_compute(self, datas):
        chunk_size = 12
        chunks_arr = []
        for l in datas:
            chunks = [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]

            chunks_arr.append(chunks)
        chunks_size = len(chunks)
        out_arr = []
        for o in chunks_arr:
            j = 0
            arr = []

            while j < chunk_size:
                a = 0
                for index, k in enumerate(o):
                    a = a + k[j]
                b = a / chunks_size
                arr.append(b)
                j += 1
            out_arr.append(arr)
        print("out_arr:", out_arr)
        return out_arr


if __name__ == '__main__':
    pass
