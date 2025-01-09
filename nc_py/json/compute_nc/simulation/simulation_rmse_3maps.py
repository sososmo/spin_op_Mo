import os
from nc_py.out_input import OutInput
import numpy as np
import xarray as xr
from nc_py.compute_nc.simulation.simulation import Compute_Data_Simulation as cdm


class Compute_Data_Simulation_ThreeMap(object):
    def __init__(self, data) -> None:
        self.data = data
        self.input_path = data["input_path"]
        self.out_path = data["out_path"]
        self.cdm = cdm(self.data)
        self.data_org = None
        self.units = None
        self.x_aix = None
        self.file_all = [1983, 1988, 2003, 19821988, 19822003]
        self.input_name = '/Volumes/momo'
        self.year_op_al = [1983, 1988, 2003]
        self.lonlat = {
                    "lon_min": -124.9375,
                    "lon_max": -67.0625,
                    "lat_min": 25.0625,
                    "lat_max": 52.9375
                }
        pass

    '''
    the RMSE of Multiple OP Schemes
    '''

    def get_simulation_rmse_1maps(self, compute_tpye, dataset=None, year=1983, year_name=1983):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        var_input_arr = ['GPP', 'LH']
        datas_all = []

        for var_input in var_input_arr:
            datas = []
            data_change = OutInput({
                "input_path": self.input_path,
                "out_path": self.out_path
            })

            read_file_son = self.cdm.read_file_rmse(data_change, var_input)
            files_arr = read_file_son['files_arr']
            nc_datas = read_file_son['nc_datas']
            self.file_all = files_arr

            for data_one_index, data_one in enumerate(nc_datas):
                path_name = files_arr[data_one_index][-6:-3]
                year = path_name[-4:]
                data = data_one['data'][var_input].values[1]
                units = [self.cdm.unit_data[var_input]['unit']]
                datas = data
                sava_name = self.out_path + os.sep + var_input + compute_tpye + str(data_one_index) + '_' + str(
                    path_name) + '_1.png'


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
                    "lonlat": self.lonlat,
                    "name": '',
                }

                data_in["name"] = 'Comparison of ' + str(year) + var_input + ' Simulation and Validation(' + str(
                    units[0]) + ')'
                all_title = ['RMSE of ' + var_input + ': 1-Year Spin-Up',
                             'RMSE of ' + var_input + ': 10-Year Spin-Up']

                pltset_out['title'] = [all_title[data_one_index]]
                if data_one_index>2:
                    if var_input == 'GPP':
                        pltset_out['norm'] = [[0, 4], [0, 3]]
                    elif var_input == 'LH':
                        pltset_out['norm'] = [[0, 35], [0, 35]]
                    else:
                        pltset_out['norm'] = [[0, 25], [0, 4]]
                else:
                    if var_input == 'GPP':
                        pltset_out['norm'] = [[0, 4], [0, 3]]
                    elif var_input == 'LH':
                        pltset_out['norm'] = [[0, 35], [0, 35]]
                    else:
                        pltset_out['norm'] = [[0, 25], [0, 4]]

                cn.data_map(data_in, '1map', pltset_out)

            datas_all.append(datas)
        return datas_all


    '''
    Save the Simulation Results as an RMSE File to Eliminate the Need for Recalculating RMSE Each Time
    '''

    def rmse_all_percent_save_op(self, compute_tpye, year, var_input):

        [vali_data, land_cover, shp_geom] = self.cdm.vali_all(var_input, self.year_op_al)

        data_reshaped_val = vali_data.reshape(3, 12, 224, 464)
        # 按列（对应月份）计算均值
        monthly_mean_val = np.nanmean(data_reshaped_val,axis=0)
        vali_data_mean_arr =np.nanmean(monthly_mean_val, axis=(1, 2))
        print('vali_data_mean_arr:', vali_data_mean_arr, )
        '''验证月均'''
        data_combined_val_m = xr.DataArray(monthly_mean_val, dims=['time','south_north','west_east'],name=var_input)
        print(2)
        sava_name_val_m = var_input + compute_tpye + '_month_' + self.input_path[-1:] + '.nc'
        sava_name_val_m = self.out_path + os.sep + sava_name_val_m

        ex = os.path.exists(sava_name_val_m)
        if ex == False:
            data_combined_val_m.to_netcdf(sava_name_val_m)  # 输出合并后的nc文件
        # nc_file = self.input_path
        # data_change = OutInput({
        #     "input_path": nc_file,
        #     "out_path": self.out_path
        # })
        #
        # read_file_son = self.cdm.read_file_son(data_change, var_input)
        # files_arr = read_file_son['files_arr']
        # nc_datas = read_file_son['nc_datas']
        # data_years = []
        # return_data = self.cdm.compare_rmse_all(files_arr, nc_datas, vali_data, land_cover, shp_geom,
        #                                         var_input,
        #                                         compute_tpye)
        # data_years = return_data['datas'][0]
        # data_org = return_data['datas'][3]
        # datas_mean = return_data['datas'][2]
        # data_month =  return_data['datas'][4]
        # # 计算scdf
        # # self.cdm.compute_scdf(files_arr, data_years, var_input)
        # #
        # datas_rmse.append(return_data['datas'][1])
        # x_aix = np.arange(1, 13, 1)
        # units = return_data['units']
        # datas.append(data_years)
        # print(datas)
        # datas_org_arr.append(data_org)
        # datas_mean_arr.append(datas_mean)
        # '月均'
        # data_combined_m = xr.DataArray(data_month, dims=['time','south_north','west_east'],name=var_input)
        # print(2)
        # sava_name_m = var_input + compute_tpye + '_month_' + self.input_path[-1:] + '.nc'
        # # self.out_path = '/Volumes/momo/op2024/op_202401008_out/rmse_percent'
        # sava_name_m = self.out_path + os.sep + sava_name_m
        #
        # ex = os.path.exists(sava_name_m)
        # if ex == False:
        #     data_combined_m.to_netcdf(sava_name_m)  # 输出合并后的nc文件
        # 'rmse'
        # data_combined = xr.concat(datas, dim='time')
        # print(2)
        # sava_name = var_input + compute_tpye + '_' + self.input_path[-1:] + '_rmse.nc'
        # # self.out_path = '/Volumes/momo/op2024/op_202401008_out/rmse_percent'
        # sava_name = self.out_path + os.sep + sava_name
        #
        # ex = os.path.exists(sava_name)
        # if ex == False:
        #     data_combined.to_netcdf(sava_name)  # 输出合并后的nc文件
        #
        # '格网均值'
        # data_combined_org = xr.concat(datas_org_arr, dim='time')
        # sava_name_org = var_input + compute_tpye + '_' + self.input_path[-1:] + '_org.nc'
        # # self.out_path = '/Volumes/momo/op2024/op_202401008_out/rmse_percent'
        # sava_name_org = self.out_path + os.sep + sava_name_org
        #
        # ex = os.path.exists(sava_name_org)
        # if ex == False:
        #     data_combined_org.to_netcdf(sava_name_org)  # 输出合并后的nc文件
        #
        # '均值'
        # data_combined_org = xr.concat(datas_org_arr, dim='time')
        # sava_name_org = var_input + compute_tpye + '_' + self.input_path[-1:] + '_org.nc'
        # # self.out_path = '/Volumes/momo/op2024/op_202401008_out/rmse_percent'
        # sava_name_org = self.out_path + os.sep + sava_name_org
        #
        # ex = os.path.exists(sava_name_org)
        # if ex == False:
        #     data_combined_org.to_netcdf(sava_name_org)  # 输出合并后的nc文件

    '''
    Save the Simulation Results as an Averaged RMSE File for Multiple Schemes to Eliminate the Need for Recalculating RMSE Each Time
    '''

    def rmse_all_percent_save_op_mean(self, compute_tpye, year, var_input, org_path):
        datas_rmse = []
        datas = []
        datas_org_arr = []
        datas_mean_arr = []
        [vali_data, land_cover, shp_geom] = self.cdm.vali_all(var_input, self.year_op_al)

        # observation
        data_change = OutInput({
            "input_path": org_path,

            "out_path": self.out_path
        })
        read_file_son = self.cdm.read_file_son(data_change, var_input)
        files_arr_org = read_file_son['files_arr']
        nc_datas_org = read_file_son['nc_datas']
        return_data_org = self.cdm.compare_rmse_all(files_arr_org, nc_datas_org, vali_data, land_cover, shp_geom,
                                                    var_input,
                                                    compute_tpye)
        data_org = return_data_org['datas'][0]

        datas.append(data_org)

        files_arr = []
        nc_datas = []
        file_name_list = os.listdir(self.input_path)
        arr_content = []

        for name in file_name_list:
            file = self.input_path + os.sep + str(name)

            data_change = OutInput({
                "input_path": file,
                "out_path": self.out_path
            })
            read_file_son = self.cdm.read_file_son(data_change, var_input)
            files_arr.append(read_file_son['files_arr'])
            nc_datas.append(read_file_son['nc_datas'])
            arr_content.append([c['attr_name'][0][var_input] for c in read_file_son['nc_datas']])
        print(1)

        # 求平均
        return_data = self.cdm.compare_mean_rmse_all(files_arr, arr_content, vali_data, land_cover, shp_geom,
                                                     var_input,
                                                     compute_tpye)

        data_years = return_data['datas'][0]
        datas_rmse.append(return_data['datas'][1])
        data_org = return_data['datas'][3]
        datas_mean = return_data['datas'][2]

        datas.append(data_years)
        datas_org_arr.append(data_org)
        datas_mean_arr.append(datas_mean)
        print(datas)
        print(datas_org_arr)
        print(datas_mean_arr)
        'rmse'
        data_combined = xr.concat(datas, dim='time')
        print(2)
        sava_name = var_input + compute_tpye + '_' + self.input_path[-1:] + '_rmse.nc'
        sava_name = self.out_path + os.sep + sava_name

        ex = os.path.exists(sava_name)
        if ex == False:
            data_combined.to_netcdf(sava_name)

        '格网均值'
        data_combined_org = xr.concat(datas_org_arr, dim='time')
        sava_name_org = var_input + compute_tpye + '_' + self.input_path[-1:] + '_org.nc'
        sava_name_org = self.out_path + os.sep + sava_name_org

        ex = os.path.exists(sava_name_org)
        if ex == False:
            data_combined_org.to_netcdf(sava_name_org)

    '''
    Extraction of Optimization Results from Different Spin-Up Strategies
    '''
    def rmse_op_diff_spinup(self, compute_tpye, year, var_input):
        datas_rmse = []
        datas = []
        # # 加入验证数据
        data_change = OutInput({
            "input_path": self.input_path,

            "out_path": self.out_path
        })
        read_file_son = self.cdm.read_file_son_var(data_change, var_input)
        nc_datas_org = read_file_son['nc_datas']
        data_mean = 0
        data_mean_arr = []
        for i, data in enumerate(nc_datas_org):
            # a = data['attr_name'][0][var_input][0]
            a = data['attr_name'][0][var_input]
            data_mean = data_mean + a
            print(np.nanmax(a), np.nanmin(a), np.nanmean(a))
            print('data:')
            data_mean_arr.append(a.values)

        '''均值1个time，网格'''
        datas.append(data_mean / len(nc_datas_org))
        data_combined = xr.concat(datas, dim='time')
        print(np.nanmax(datas), np.nanmin(datas), np.nanmean(data_combined))
        print(2)
        sava_name = var_input + compute_tpye + '_10_rmse_' + self.input_path[-1:] + '.nc'
        sava_name = self.out_path + os.sep + sava_name

        ex = os.path.exists(sava_name)
        if ex == False:
            data_combined.to_netcdf(sava_name)  # 输出合并后的nc文件


    '''
    The OP Result Compute and save to .nc
    '''
    def spin_op_out_save(self, year):
        cdst = Compute_Data_Simulation_ThreeMap(
            {
                "input_path": self.input_path,
                "out_path": r'/op2024/op_202401008_out/rmse_org_mean_20241212'
            }
        )

        for var in ['GPP', 'LH']:
            # cdst.rmse_all_percent_save_op('save', year, var)
            # cdst.rmse_all_percent_save_op_mean('save', year, var, org_path)
            cdst.rmse_op_diff_spinup('save', year, var)


if __name__ == '__main__':
    pass
