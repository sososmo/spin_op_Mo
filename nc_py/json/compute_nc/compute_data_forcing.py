import os
from nc_py.out_input import OutInput
import numpy as np
import nc_py.compute_nc.unit as unit


class Compute_NC_Data_Forcing(object):
    def __init__(self, data) -> None:
        self.data = data
        self.input_path = data["input_path"]
        self.out_path = data["out_path"]
        self.unit_data = unit.get_unit()
        self.lonlat = {
            "lon_min": -124.9375,
            "lon_max": -67.0625,
            "lat_min": 25.0625,
            "lat_max": 52.9375
        }

        pass

    '''
    Reading Forcing Data
    '''
    def get_data_forcing(self, compute_tpye, dataset=None):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        # 加载 NetCDF 数据
        cn = Compute_NC_Data(self.data)
        shp_geom = cn.read_shp_geom({'x': 'ny', 'y': 'nx'})
        data = OutInput(self.data)
        var_input = 'PRCP'
        var_input = 'QAIR'
        time_arr = list(np.arange(1982, 2011, 1))
        datas = []
        x_aix = list(np.arange(1, 13, 1))
        time_i = 0
        for time1 in time_arr:
            nc_files = data.file_all('.nc', str(time1))
            # 倒序
            files = sorted(nc_files['files'], key=lambda x: x.split('.')[0])
            nc_datas = data.files_one('.nc', False, [var_input], files)
            mean_datas = []
            if compute_tpye == 'years':
                i = 0
                mean_datas_year = 0
                while i < len(nc_datas):
                    var_data = nc_datas[i]['attr_name'][0][var_input]
                    var = var_data.sum(dim='time')
                    var = var.where(shp_geom == True)
                    # var = var.where(land == 7)
                    var = var / len(var)
                    mean_data = np.nanmean(var)
                    mean_datas_year = mean_datas_year + mean_data
                    i += 1
                print(mean_datas_year, 'mean_datas_year')
                datas.append(mean_datas_year / 100)
                x_aix = time_arr
            else:
                i, j = 0, 0
                var_data = nc_datas[0]['attr_name'][0][var_input]
                while i < len(nc_datas) - 1:
                    var = var_data[i].where(shp_geom == True)
                    var1 = var_data[i + 1].where(shp_geom == True)
                    mean_data_0 = np.nanmean(var * 360)
                    mean_data_1 = np.nanmean(var1 * 360)
                    mean_data = mean_data_0 + mean_data_1
                    mean_datas.append(mean_data)
                    x_aix.append(j)
                    i += 2
                    j += 1
                print(mean_datas)
                datas.append(mean_datas)
        print(datas)
        axhline = np.mean(datas)
        units = [self.unit_data[var_input]['unit']]
        path_name = self.input_path[self.input_path.rfind('\\') + 1:]

        sava_name = self.out_path + os.sep + var_input + compute_tpye + path_name + '0409.png'
        title = ['{} '.format(str(i)) for i in time_arr]
        pltset = {
            'title': title,
            'save': sava_name,
            'unit': units,
            # 'cmap': ['blue', 'green', 'orange'],]
            'cmap': ['coolwarm', 'coolwarm', 'coolwarm'],
            'legend': var_input

        }
        pltset_out = cn.type_gpp_lh(pltset)
        data_in = {"datas": [datas], "lonlat": self.lonlat, "name": 'Annual precipitation in Grassland'}
        pltset_out['x'] = x_aix

        if compute_tpye == 'years':
            name = 'Annual precipitation in Grassland'
            if var_input == 'PRCP':
                name = 'Annual precipitation'
            elif var_input == 'QAIR':
                name = 'Annual humidity index'
            elif var_input == 'TAIR':
                name = 'Annual temperature'

            pltset_out['label'] = name
            pltset_out['legend'] = name
            pltset_out['axhline'] = axhline
            pltset_out['xunit'] = ['Year']
            pltset_out['highlight'] = [1982, 1983, 1987, 1988, 2002, 2003]
            data_in['name'] = name
            cn.data_map(data_in, '1line', pltset_out)
        else:
            pltset_out['label'] = title
            pltset_out['legend'] = var_input
            cn.data_map(data_in, 'moreline', pltset_out)
if __name__ == '__main__':
    pass
