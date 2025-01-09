import os
from nc_py.out_input import OutInput
import numpy as np
import nc_py.compute_nc.unit as unit
from nc_py.compute_nc.simulation.simulation import Compute_Data_Simulation as cdm
import re


class Compute_Data_Simulation_Objection_Function(object):
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
        self.year_all = [1983, 1988, 2003, 19821988, 19822003]
        self.var_inputs = ['GPP', 'LH']
        self.best_s = 'bestx_MOASMO_OUT_y_plusorg.txt'

        pass

    def get_simulation_scdf(self, compute_tpye, dataset=None, year=1983, year_name=1983):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        datas_all = []
        for index, var_input in enumerate(self.var_inputs):
            datas_rmse = []
            datas = []
            x_aix = []

            data_change = OutInput({
                "input_path": self.input_path,
                "out_path": self.out_path
            })

            read_file_son = self.cdm.read_file_rmse(data_change, var_input)
            files_arr = read_file_son['files_arr']
            nc_datas = read_file_son['nc_datas']
            self.file_all = files_arr
            for data_one_index, data_one in enumerate(nc_datas):
                data_one = data_one['data'][var_input]
                path_name = re.findall(r'\d+', files_arr[0])[0]

                return_data = self.cdm.compute_scdf(files_arr, data_one, var_input)

                x_aix.append(return_data['datas'][0][0])
                datas.append(return_data['datas'][0][1])
            print(datas, 'datas')
            sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + 'compare.png'
            units = [self.unit_data[var_input]['unit']]
            lonlat = {
                "lon_min": -124.9375,
                "lon_max": -67.0625,
                "lat_min": 25.0625,
                "lat_max": 52.9375
            }
            pltset = {
                'title': '',
                'save': sava_name,
                'unit': units,
                'cmap': ['coolwarm', 'coolwarm', 'coolwarm'],
                'legend': var_input

            }

            pltset_out = cn.type_gpp_lh(pltset)
            data_in = {
                "datas": [datas],
                "lonlat": lonlat,
                "name": '',
            }
            pltset_out['x'] = x_aix
            pltset_out['legend'] = var_input
            pltset_out['xunit'] = ['RMSE']
            pltset_out['name'] = 'CDF of ' + var_input + '(' + str(units[0]) + ')'
            data_in["name"] = 'CDF of ' + var_input + '(' + str(units[0]) + ')'

            pltset_out['legend'] = var_input
            # label_2 = ['Default','Best_1', "Best_2", "Best_3"]
            # label_2 = ['Default-1','Default-10','Best-1_1', 'Best-10_1',"Best-10_2", "Best-10_3"]
            label_2 = ["Best-10_3", 'Best-1_1', ]
            pltset_out['label'] = label_2
            pltset_out['xunit'] = ['RMSE']

            cn.data_map(data_in, 'moreline_x', pltset_out)
            datas_all.append(datas)
        return datas_all

    def get_simulation_monthly(self, compute_tpye, dataset=None, year=1983, year_name=1983):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        # 加载 NetCDF 数据
        data = OutInput(self.data)
        var_input_arr = ['GPP', 'LH']
        # var_input_arr = ['GPP']

        path_name = self.input_path[self.input_path.rfind('/') + 1:]
        datas_all = []

        for var_input in var_input_arr:
            data_change = OutInput({
                "input_path": self.input_path,
                "out_path": self.out_path
            })
            read_file_son = self.cdm.read_file_rmse(data_change, var_input)
            files_arr = read_file_son['files_arr']
            titles = []
            datas = []
            nc_datas = read_file_son['nc_datas']
            for data_one_index, data_one in enumerate(nc_datas):
                mean_data = np.nanmean(data_one)
                titles.append('Best_' + str(data_one_index))
                self.units = [self.cdm.unit_data[var_input]['unit']]
                datas.append(mean_data)

            print("datas:", datas)

            sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + '1016.png'
            lonlat = {
                "lon_min": -124.9375,
                "lon_max": -67.0625,
                "lat_min": 25.0625,
                "lat_max": 52.9375
            }
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
                "lonlat": lonlat,
                "name": name,
            }
            pltset_out['legend'] = legend

            pltset_out['x'] = np.arange(1, 13, 1)
            pltset_out['legend'] = var_input
            data_in["name"] = 'Monthly average ' + var_input + '(' + self.units[0] + ')'
            pltset_out['legend'] = var_input
            label_2 = ['Best_1', "Best_2", "Best_3", 'Default', 'Observation']
            pltset_out['label'] = label_2

            cn.data_map(data_in, 'moreline', pltset_out)
            datas_all.append(datas)
        return datas_all


if __name__ == '__main__':
    pass
