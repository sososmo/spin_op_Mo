import os
from nc_py.out_input import OutInput
from nc_py.pyplot.display_plot_map import Display_Plot_Map
from nc_py.pyplot.display_plot_line import Display_Plot_Line
from nc_py.compute_nc.compute_data_forcing import Compute_NC_Data_Forcing
import xarray as xr
import numpy as np
from time import sleep
import matplotlib.colors as mcolors
import geopandas as gpd
import rasterio.features as features
from rasterio.transform import from_origin
from nc_py.compute_nc.simulation.simulation_monthly import Compute_Data_Simulation_Monthly
from nc_py.compute_nc.simulation.simulation_rmse_3maps import Compute_Data_Simulation_ThreeMap
from nc_py.compute_nc.simulation.simulation_obj_func import Compute_Data_Simulation_Objection_Function

rmse_line_all = False
input_name = '/Volumes/momo'
# input_name = 'F:'


class Compute_NC_Data(object):
    def __init__(self, data) -> None:
        self.default_value = "default_value"
        self.input_path = data["input_path"]
        self.out_path = data["out_path"]
        self.dis = Display_Plot_Map()
        self.dis_line = Display_Plot_Line()

        self.cp_for = Compute_NC_Data_Forcing(data)
        self.cp_sm_monthly = Compute_Data_Simulation_Monthly(data)
        self.cp_sm_3map = Compute_Data_Simulation_ThreeMap(data)
        self.cp_sm_obf = Compute_Data_Simulation_Objection_Function(data)
        self.mk_out = ''
        self.input_name = '/Volumes/momo'
        # self.input_name = 'F:'

    '''
    Reading Validation Data
    '''
    def plot_gpp_lh(self):
        arr_data = ['GPP', 'LE']
        varify_attrs = {}
        for i in arr_data:
            in_dir_verify = self.input_name + '/data_jung/test_jung_huo/' + i
            out_dir = ''
            data_varify = OutInput({
                "input_path": in_dir_verify,
                "out_path": out_dir
            })

            varify_data = data_varify.files_one('nc', False, [i])
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
    Validation Data
    '''
    def map_vali_data(self, compute_tpye, year, var_arr=['GPP']):
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
            arr_mean = []
            x_aix = []
            while j >= year_i_min and j < year_i_max:
                varify_attr_j = varify_attr[j]
                if compute_tpye == 'mean line':
                    varify_attr_mean = varify_attr_j.mean()
                    arr_mean.append(varify_attr_mean)
                    norm1 = [varify_attr_j.min(), varify_attr_j.max()]
                    norm.append(norm1)


                else:
                    var_data_1 = np.ma.filled(varify_attr_j, fill_value=0)
                    # mask_land_cover = np.isin(land_cover, [7, 8])
                    # var_data_1 = np.where(mask_land_cover, np.nan, var_data_1)
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
                unit = varify_attrs[i].units
                units.append(unit)
        print(units)
        if compute_tpye == 'compare':
            return {
                'validation': attrs,
                'land_cover': land_cover,
                'shp_geom': shp_geom
            }
        else:
            lat_name, lon_name = 'LATITUDE', 'LONGITUDE'
            lat_data, lon_data = varify_attrs[lat_name], varify_attrs[lon_name]
            lon_data = np.where(np.abs(lon_data) > 1e10, np.nan, lon_data)
            lat_data = np.where(np.abs(lat_data) > 1e10, np.nan, lat_data)
            lon_min = np.nanmin(lon_data)
            lon_max = np.nanmax(lon_data)
            lat_min = np.nanmin(lat_data)
            lat_max = np.nanmax(lat_data)
            lonlat = {
                "lon_min": lon_min,
                "lon_max": lon_max,
                "lat_min": lat_min,
                "lat_max": lat_max
            }
            name = '198212'
            sava_name = self.out_path + os.sep + 'validata' + str(name)
            pltset = {
                'title': var_arr,
                'unit': units,
                'save': sava_name,

            }

            pltset_out = self.type_gpp_lh(pltset)
            pltset_out['x'] = x_aix
            pltset_out['legend'] = var_arr
            pltset_out['norm'] = norm
            data_in = {
                "datas": attrs,
                "lonlat": lonlat,
                "name": '1982 maen line',

            }
            print(data_in)
            data_in_map = {
                "datas": attrs_map,
                "lonlat": lonlat,
                "name": name,
            }
            # sleep(1)
            # self.data_map(data_in, '1line', pltset_out)

            self.data_map(data_in_map, '1map', pltset_out)

    def data_map(self, data, type_plot, pltset):
        print('pltset_out', pltset)
        match type_plot:
            case '1map':
                self.dis.map_ini_one_simple(data['datas'], data["lonlat"], data["name"], pltset)
                pass
            case '1mapwrf':
                self.dis.map_ini_one_simple_wrf(data['datas'], data["lonlat"], data["name"], pltset)
                pass
            case '1maplegend':
                self.dis.map_ini_one_simple_legend(data['datas'], data["lonlat"], data["name"], pltset)
                pass
            case '2map':
                self.dis.map_ini_two_simple(data['datas'], data["lonlat"], data["name"], pltset)
                pass
            case '4map':
                pass
            case 'moremap':
                self.dis.map_ini_sixteen_simple_legend(data['datas'], data["lonlat"], data["name"], pltset)

                pass
            case 'moremap_12':
                self.dis.map_ini_twelve_simple_legend(data['datas'], data["lonlat"], data["name"], pltset)
                pass
            case 'maps':
                self.dis.map_ini_more_fig_1(data['datas'], data["lonlat"], data["name"], pltset)
            case '1line':
                # self.ec.line_init_more(data["name"], data['datas'], pltset)
                self.dis_line.line_init_one(data["name"], data['datas'], pltset)
                pass
            case '2line':
                # self.ec.line_init_more(data["na me"], data['datas'], pltset)
                self.dis_line.line_init_two(data["name"], data['datas'], pltset)
                pass
            case 'moreline':
                # self.ec.line_init_more(data["name"], data['datas'], pltset)
                self.dis_line.line_init_more(data["name"], data['datas'], pltset)
                pass
            case 'moreline_x':
                self.dis_line.line_init_more_x(data["name"], data['datas'], pltset)
                pass
            case 'morefigline':
                # self.ec.line_init_more(data["name"], data['datas'], pltset)
                self.dis_line.line_init_fig_more_1(data["name"], data['datas'], pltset)
                pass
            case '1linefig':
                self.dis_line.line_init_more_fig(data["name"], data['datas'], pltset)
            case 'morey':
                self.dis_line.more_y(data["name"], data['datas'], pltset)
            case 'bar':
                pass
            case 'scatter':
                self.dis_st.scatter_init(data["name"], data['datas'], pltset)
            case 'hint':
                self.dis_hist.hist_init_more(data["name"], data['datas'], pltset)
                pass
        pass

    '''
    基本样式
    '''

    def type_gpp_lh(self, pltset):
        # viridis
        cmap = mcolors.ListedColormap(['green'])
        cmap1 = mcolors.ListedColormap(['blue', 'green', 'yellow', 'red'])
        cmap2 = mcolors.ListedColormap(['blue', 'green', 'yellow', 'red'])
        cmap3 = ['OrRd', 'BrBG']
        # 定义颜色规范化对象
        # norm1 = mcolors.BoundaryNorm([0, 0.5, 0.75, 1], cmap1.N)
        # norm2 = mcolors.BoundaryNorm([0, 0.5, 0.75, 1], cmap2.N)
        norm1 = [0.0000001, 0.00000001]
        norm2 = [-2, 2]

        pltset_out = {
            'title': pltset["title"],
            'save': pltset["save"],
            'unit': pltset["unit"],
            'cmap': pltset["cmap"],
            'norm': [norm1, norm2],
            "legend": '',
            'label': ''

        }
        return pltset_out

    def type_soil(self, pltset):
        norm1 = [-1, 1]
        norm2 = [-2, 2]
        pltset_out = {
            'title': pltset["title"],
            'save': pltset["save"],
            'unit': pltset["unit"],
            'cmap': pltset["cmap"],
            'norm': [norm1, norm2],
            'legend': pltset['legend']
        }
        return pltset_out


    '''
    WRFinput Data
    '''

    def get_wrf_data(self, land_type_data):
        # 加载 NetCDF 数据
        # in_dir = input('输入文件路径：')
        # in_dir = self.input_path
        # out_dir = self.out_path
        shp_geom = self.read_shp_geom()

        in_dir = self.input_name + r'/Noah/data/wrf_out/20230505'
        out_dir = self.input_name + r'/test_pic/wrf'
        data = OutInput({
            "input_path": in_dir,
            "out_path": out_dir
        })
        nc_files = data.file_all('.nc')
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
            nc_data = xr.open_dataset(nc_file)

            name_time = nc_data.get('Times', default=self.default_value)
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
                if (str_h == 0) and (str_d == 1):
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
                    land_cover = nc_data.get(var_input, default=self.default_value)
                    land_cover = land_cover[var_index]
                    lonlat = {
                        "lon_min": lon_min,
                        "lon_max": lon_max,
                        "lat_min": lat_min,
                        "lat_max": lat_max
                    }
                    print(lonlat)
                    if land_type_data == 'land':
                        return {
                            "land_cover": land_cover,
                            'lonlat': lonlat
                        }
                    else:
                        datas = []
                        units = []
                        for i in var_arr[var_j]:
                            type(nc_data[i])
                            var_data = nc_data[i]
                            print('分界线')
                            var_data_1 = var_data[k].where(shp_geom == True)
                            is_7 = nc_data.get('IVGTYP', default=self.default_value)
                            var_data_1 = var_data_1.where(is_7 == 7)
                            land_type_no_nan = var_data_1.where(~np.isnan(var_data_1), drop=True)
                            cleaned_values = land_type_no_nan.values[~np.isnan(land_type_no_nan.values)]
                            unique_values, counts = np.unique(cleaned_values, return_counts=True)
                            total_values = np.sum(counts)
                            percentages = counts / total_values
                            legends = []
                            for value, percentage in zip(unique_values, percentages):
                                legends.append(int(value))
                                print(f"Value: {value}, Percentage: {percentage * 100:.2f}%")
                            print('属性值：', var_data_1)
                            # 获取单位
                            unit = var_data.attrs.get('units', var_data.attrs.get('unit', ''))
                            print('unit:', unit)
                            datas.append(var_data_1)
                            units.append(unit)
                    if land_type_data == 'land':
                        pass
                    else:
                        time_name = time_i.replace('-', '')[0:11]
                        sava_name = out_dir + os.sep + str(nc_file_name) + str(
                            var_arr[var_j][0]) + time_name + 'SAND-grassland_20241010.png'
                        print(sava_name)
                        print(units)
                        colors = ['#FF7F50', '#90EE90']
                        pltset = {
                            'title': [''],
                            'save': sava_name,
                            'unit': units,
                            'cmap': ['#FF7F50', '#90EE90'],

                        }
                        pltset_out = self.type_gpp_lh(pltset)
                        pltset_out['legend'] = legends

                        pltset_out['norm'] = [[0, 20]]
                        data_in = {
                            "datas": datas,
                            "lonlat": lonlat,
                            "name": name
                        }
                        self.data_map(data_in, '1mapwrf', pltset_out)
                k += 1

            nc_i += 1

    '''
    Shape mask of research area
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



    def cp_focing(self, compute_tpye):
        self.cp_for.get_data_forcing(compute_tpye)

    def cp_simulation_org(self, compute_tpye, year, year_name):
        data = self.cp_sm.get_grass_data_simulation(compute_tpye, None, year, year_name)
        return data

    def cp_simulation(self, compute_tpye, year, year_name):
        if compute_tpye == 'op_monthly_all':
            data = self.cp_sm_monthly.get_simulation_monthly(compute_tpye, None, year, year_name)
        elif compute_tpye == 'compare_years':
            data = self.cp_sm_monthly.get_simulation_monthly_loop_change(compute_tpye, None, year, year_name)
        elif compute_tpye == 'RMSE_percent_save':
            data = self.cp_sm_3map.spin_op_out_save(year)
        elif compute_tpye == 'RMSE_1map':
            data = self.cp_sm_3map.get_simulation_rmse_1maps(compute_tpye, None, year, year_name)
        return data

def fulfill_fun(indir, out_dir, year=1983, year_name=1983, do_what='all_pic'):
    in_dir = indir
    cp = Compute_NC_Data({
        "input_path": in_dir,
        "out_path": out_dir
    })
    data = None
    # do_what = input('你要做什么：')
    if do_what == '验证':
        cp.map_vali_data()
    elif do_what == 'wrf':
        cp.get_wrf_data('soil')
    elif do_what == 'simulation':
        data3 = cp.cp_simulation('op_monthly_all', year, year_name)
        # data1 = cp.cp_simulation('RMSE_percent_save', year, year_name)
        data2 = cp.cp_simulation('RMSE_1map', year, year_name)

    elif do_what == 'forcing':
        cp.cp_focing('years')
    elif do_what == 'all_pic':
        cp.cp_simulation('compare_years', year, year_name)
    return data

'''
File Road
'''
def check_file(i):
    indir, out_dir, year = None, None, None
    match i:
        case 1982:
            indir = input_name + '/simulation_7_11/1982_50'
            out_dir = r'F:/test_pic/spn-up data/20240316/1982'
            year = 1983
        case 1983:
            indir = input_name + '/simulation_7_11/1983'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 1983
        case 1987:
            indir = input_name + '/simulation_7_11/1987_50'
            out_dir = input_name + '/test_pic/spn-up data/20240316/1987'
            year = 1988
        case 1988:
            indir = input_name + '/simulation_7_11/1988'
            out_dir = input_name + '/test_pic//spn-up data/20240805/1'
            year = 1988
        case 2002:
            indir = input_name + '/simulation_7_11/2002_50'
            out_dir = input_name + '/test_pic/spn-up data/20240316/2002'
            year = 2003
        case 2003:
            indir = input_name + '/simulation_7_11/2003'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 2003
        case 19821987:
            indir = input_name + '/simulation_7_11/1982_1987_50'
            out_dir = input_name + '/test_pic/spn-up data/20240316/1982_1987'
            year = 1988
        case 19821988:
            indir = input_name + '/simulation_7_11/1982_1988'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 1988
        case 19822002:
            indir = input_name + '/simulation_7_11/1982_2002_50'
            out_dir = input_name + '/test_pic/spn-up data/20240316/1982_2002'
            year = 2003
        case 19822003:
            indir = input_name + '/simulation_7_11//1982_2003'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 2003
        case 19822008:
            indir = r'G:/halfmonthforcing'
            out_dir = r'F:/test_pic/forcing'
            year = 1982
        case 101:
            indir = r'G:/halfmonthforcing'
            out_dir = r'F:/test_pic/forcing'
            year = 1982
        case 102:
            indir = r'G:/halfmonthforcing'
            out_dir = r'F:/test_pic/forcing'
            year = 1982
        case 198310:
            indir = input_name + '/op2024/op_20240930'
            out_dir = input_name + '/test_pic/op/op_pic_20240930'
            year = 1983
        case 198810:
            indir = input_name + '/op2024/op_20240930'
            out_dir = input_name + '/test_pic/op/op_pic_20240930'
            year = 1983
        case 200310:
            indir = input_name + '/op2024/op_20240930'
            out_dir = input_name + '/test_pic/op/op_pic_20240930'
            year = 1983
        case 1000:
            indir = input_name + '/op2024/op/ORG_spin-up10'
            out_dir = input_name + '/test_pic/op/20240615/10_org'
            year = 1983
        case 10100:
            indir = input_name + '/op2024/ORG_spinup_1'
            out_dir = input_name + '/test_pic/op/20240615/1_org'
            year = 1983
        case 1010:
            indir = input_name + '/op2024/op_20240930/1'
            out_dir = input_name + '/test_pic/op/op_pic_20241008/1'
            year = 1983
        case 1020:
            indir = input_name + '/op2024/op_20240930/2'
            out_dir = input_name + '/test_pic/op/op_pic_20241008/2'
            year = 1983
        case 1030:
            indir = input_name + '/op2024/op_20240930/3'
            out_dir = input_name + '/test_pic/op/op_pic_20241008/3'
            year = 1983
        case 1040:
            indir = input_name + '/op2024/op_20240930/4'
            out_dir = input_name + '/test_pic/op/op_pic_20241008/4'
            year = 1983
        case 11010:
            indir = input_name + '/op2024/op_20241124/1'
            out_dir = input_name + '/test_pic/op/op_pic_20241008/4'
            year = 1983
        case 1001:
            '''最优方案的rmse百分比nc'''
            indir = input_name + '/op2024/op_202401008_out/rmse_percent_3_new'
            out_dir = input_name + '/test_pic/op/op_pic_20241008'
            year = 1983
        case 100101:
            '''10次预热多个最优方案均值的rmse百分比nc'''
            indir = input_name + '/op2024/op_202401008_out/rmse_percent_mean'
            out_dir = input_name + '/test_pic/op/op_pic_20241008'
            year = 1983
        case 100102:
            '''10次预热多个最优方案均值'''
            indir = input_name + '/op2024/op_202401008_out/rmse_org_mean_20241212/10_val'
            out_dir = input_name + '/test_pic/op/op_pic_20241212'
            year = 1983
        case 1010101:
            '''1次预热多个最优方案均值的rmse百分比nc'''
            indir = input_name + '/op2024/op_20241124_01_out/rmse_percent_mean'
            out_dir = input_name + '/test_pic/op/op_pic_20241124'
            year = 1983
        case 10010101:
            '''1CI AND 10次预热多个最优方案均值的rmse百分比nc'''
            indir = input_name + '/op2024/op_20241203_1_1_10_3_rmse'
            # indir = input_name + '/op2024/op_20241201_all_rmse'
            out_dir = input_name + '/test_pic/op/op_pic_20241201_10_1'
            year = 1983
        case 10010102:
            '''1CI AND 10次预热多个最优方案均值的+观测的网格均值'''
            indir = input_name + '/op2024/op_202401008_out/rmse_org_mean_20241212/10_1_rmse'
            # indir = input_name + '/op2024/op_20241201_all_rmse'
            out_dir = input_name + '/test_pic/op/op_pic_20241212'
            year = 1983
        case 10010103:
            '''1CI AND 10次预热多个最优方案月，12time，均值的+观测的网格均值'''
            indir = input_name + '/op2024/op_202401008_out/rmse_org_mean_20241212/val_10_1_month'
            # indir = input_name + '/op2024/op_20241201_all_rmse'
            out_dir = input_name + '/test_pic/op/op_pic_20241212'
            year = 1983
        case 1011001:
            '''1次和10次的原数据'''
            indir = input_name + '/op2024/op_20241128_1_10'
            out_dir = input_name + '/test_pic/op/op_pic_20241124'
            year = 1983
        case 1011002:
            '''1次和10次合并后的数据'''
            indir = input_name + '/op2024/op_20241128_1_10_out/rmse_percent_mean'
            out_dir = input_name + '/test_pic/op/op_pic_20241124'
            year = 1983
        case 1002:
            indir = input_name + '/op2024/op_20240930'
            out_dir = input_name + '/test_pic/op/op_pic_20241008'
            year = 1983

        case 10102:
            indir = input_name + '/op2024/op_20241124'
            out_dir = input_name + '/test_pic/op/op_pic_20241124'
            year = 1983
        case 1003:
            '''最优方案的月均曲线nc'''
            indir = input_name + '/op2024/op_202401008_out/monthly_all'
            out_dir = input_name + '/test_pic/op/op_pic_20241008'
            year = 1983
        case 1004:
            '''only sand '''
            indir = input_name + '/op2024/op'
            out_dir = input_name + '/test_pic/op/20240615'
            year = 1983
        case 4010:
            indir = input_name + '/op2024/op/1'
            out_dir = input_name + '/test_pic/op/20240615/1'
            year = 1983
        case 4020:
            indir = input_name + '/op2024/op/2'
            out_dir = input_name + '/test_pic/op/20240615/2'
            year = 1983
        case 4030:
            indir = input_name + '/op2024/op/3'
            out_dir = input_name + '/test_pic/op/20240615/3'
            year = 1983
        case 10000:
            indir = input_name + '/pro/py_conda/uq/uqofrun/UQ/optimization/op_log/20241008'
            out_dir = input_name + '/test_pic/op/op_pic_20241008'
            year = 1983
        # rmse
        case 1982200300:
            indir = input_name + '/test_pic/spn-up data/20240805/nc_rmse_3'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 2003
        case 1982200308:
            indir = input_name + '/test_pic/spn-up data/20240805/nc_rmse_all'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 2003
        case 1982200308:
            indir = input_name + '/test_pic/spn-up data/20240805/nc_rmse_all'
            out_dir = input_name + '/test_pic/spn-up data/20240805/1'
            year = 2003
    return (indir, out_dir, year)

def allfile(arr=[1982, 1983, 1987, 1988, 2002, 2003]):

    for i in arr:
        (indir, out_dir, year) = check_file(i)
        many_files = ''
        if many_files != '':
            for j in os.listdir(indir):
                fulfill_fun(indir + os.sep + j, out_dir, year, i)
            # rmse_line_all = True
            # if rmse_line_all:
            #     fulfill_fun(indir, out_dir, year)
            # rmse_line_all = False
        else:
            fulfill_fun(indir, out_dir, year, i, 'simulation')




if __name__ == '__main__':
    allfile([10010102])
    pass
