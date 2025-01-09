import numpy as np
import nc_py.compute_nc.unit as unit
from scipy.stats import norm


class Compute_Data_Simulation(object):
    def __init__(self, data) -> None:
        self.data = data
        self.input_path = data["input_path"]
        self.out_path = data["out_path"]
        self.title_name = ''
        self.var_read = ''
        self.unit_d5ata = unit.get_unit()
        self.vali_year = [1983, 1988, 2003]
        self.x_aix = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        pass

    '''
    Reading file
    '''

    def read_file_son(self, data, var_input):
        files_arr = []
        for year_r in self.vali_year:
            year_str = 'output.' + str(year_r)
            nc_files = data.file_all('.nc', year_str, True)
            files = sorted(nc_files['files'], key=lambda x: x.split('.')[1])
            files_arr.extend(files)
        nc_datas = data.files_one('.nc', False, [var_input], files_arr)
        return {
            "files_arr": files_arr,
            "nc_datas": nc_datas
        }

    '''
    Reading file only filter Variables
    '''

    def read_file_son_var(self, data, var_input):
        files_arr = []
        format_str = var_input
        nc_files = data.file_all('.nc', format_str, True)
        files = sorted(nc_files['files'], key=lambda x: x.split('.')[0])
        files_arr.extend(files)
        nc_datas = data.files_one('.nc', False, [var_input], files_arr)
        return {
            "files_arr": files_arr,
            "nc_datas": nc_datas
        }


    '''Reading RMSE file'''

    def read_file_rmse(self, data, var_input):
        year_str = var_input
        nc_files = data.file_all('.nc', year_str, True)
        # files = sorted(nc_files['files'], key=lambda x: x.split('.')[0])
        files = sorted(nc_files['files'], key=lambda x: x.split('.')[0][-1])

        nc_datas = data.files_one('.nc', False, [var_input], files)
        return {
            "files_arr": files,
            "nc_datas": nc_datas
        }

    '''
    CDF
    '''
    def cdf_op_fun(self, data_change, var_input, compute_tpye):
        import nc_py.compute_nc.compute_data as cp
        read_file_son = self.read_file_son(data_change, var_input)
        files_arr = read_file_son['files_arr']
        nc_datas = read_file_son['nc_datas']
        # 倒序
        return_data = self.compute_compare_all_scdf(files_arr, nc_datas,
                                                    var_input,
                                                    compute_tpye)
        if compute_tpye == 'SCDF_RMSE_percent':
            x_aix = return_data['x_aix']
            datas = return_data['datas'][0]
        else:
            x_aix = return_data['datas'][0][0]
            datas = return_data['datas'][0][1]
        units = return_data['units']
        return {
            "x_aix": x_aix,
            "datas": datas,
            "units": units,
        }

    '''
    Validation
    '''

    def vali_all(self, var_input, vali_year):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        cn = Compute_NC_Data(self.data)
        vali_datas_out = []
        for vali_y in vali_year:
            vali_data_return = cn.map_vali_data('compare', vali_y, [var_input])
            land_cover = vali_data_return['land_cover']
            shp_geom = vali_data_return['shp_geom']
            vali_data = vali_data_return['validation']
            vali_datas_out.append(vali_data)
        vali_datas_out = np.concatenate(vali_datas_out, axis=0)
        return [vali_datas_out, land_cover, shp_geom]
    '''
    Monthly MEAN
    '''
    def out_month_mean(self, out_datas, valdata, land_cover, shp_geom, vail=False, dim_time=True):
        from nc_py.compute_nc.compute_data import Compute_NC_Data
        outdata = None
        var_data_1 = None
        out_data_sq = None
        out_datas = out_datas.where(out_datas != -1.000e+33)
        out_datas = out_datas.where(out_datas != -9.999e+03)
        print('1', np.nanmin(out_datas), ',', np.nanmax(out_datas))
        data_sim = out_datas.where(shp_geom == True)
        data_sim = data_sim.where(land_cover == 7)
        if dim_time is True:
            data_sim = data_sim.mean(dim='Time')
            # data_sim = (data_sim / len(out_datas))

        # data_sim = data_sim.where((land_cover == 7) | (land_cover == 11))
        if self.var_read == 'LH':
            # data_sim = (data_sim / len(out_datas))
            data_sim = data_sim

        else:
            # 计算均值时，已经是day了，不需要*day
            if dim_time is True:
                data_sim = data_sim * 86400
            else:
                data_sim = data_sim

        datas = data_sim

        print('最大最小', np.nanmax(datas), ',', np.nanmin(datas))
        # 验证数据
        if vail == True:
            var_data_1 = valdata
            outdata = np.sqrt(((datas - var_data_1) ** 2))
            out_data_sq = (datas - var_data_1) ** 2
            print(np.nanmean(out_data_sq), ':out_data_sq', np.nanmean(var_data_1), ':var_data_1')
            # print('maxrmse', np.sum(outdata > 2), np.sum(outdata > 1), np.nanmax(outdata),
            #       'np.sum((~np.isnan(data_sim)) & (data_sim == 0))')
        # cn.write_to_excel(self.title_name, datas)
        return {
            'simdata': datas,
            'valdata': var_data_1,
            'outdata': outdata,
            'out_data_sq': out_data_sq
        }

    '''
    Monthly MEAN from Validation
    '''
    def out_month_mean_vail(self, vali_data):
        var_data_arr = []
        var_data_arr_mean = []
        for valdata in vali_data:
            var_data_1 = valdata
            var_data_arr.append(var_data_1)
            valdata_mean = np.nanmean(var_data_1)
            var_data_arr_mean.append(valdata_mean)
        return {
            'valdata': var_data_arr,
            'valdata_mean': var_data_arr_mean,
        }

    '''
        RMSE
    '''

    def compare_rmse(self, files, nc_datas, vali_data, land_cover, shp_geom, var_input, compute_tpye):
        i = 0
        valdata_out = 0
        data_funcs = 0
        data_vals = 0
        data_funcs_arr_sim = 0

        valdata_out_arr = []
        data_funcs_arr = []

        datas = []
        units = []
        x_aix = []
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_data[i]
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
            print('计算中' + str(i) + '...')
            return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
            data_func = return_data['out_data_sq']
            data_funcs = data_funcs + data_func
            i += 1

        data_funcs = np.sqrt(data_funcs / len(nc_datas))
        datas.append(data_funcs)

        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }

    '''
      MEAN
    '''

    def compare_mean(self, files, nc_datas, vali_data, land_cover, shp_geom, var_input, compute_tpye):
        i = 0
        data_funcs_arr = []
        data_org_arr = []
        datas = []
        units = []
        x_aix = []
        self.var_read = var_input
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_data[i]
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
            print('计算中' + str(i) + '...')
            return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, False)
            data_org = return_data['simdata']
            data_func = np.nanmean(data_org)
            data_funcs_arr.append(data_func)
            data_org_arr.append(data_org)
            i += 1

        datas.append(data_funcs_arr)
        datas.append(data_org_arr)
        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }

    '''
    MEAN + RMSE
    '''

    def compare_mean_rmse(self, files, nc_datas, vali_data, land_cover, shp_geom, var_input, compute_tpye):
        i = 0
        data_funcs_arr = []
        data_vals = 0

        datas = []
        units = []
        x_aix = []
        self.var_read = var_input
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_data[i]
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
            print('计算中' + str(i) + '...')
            return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
            data_func = np.nanmean(return_data['simdata']).values
            data_funcs_arr.append(data_func)
            data_val = return_data['out_data_sq']
            data_vals = data_vals + data_val
            i += 1

        valdata_out = np.nanmean(np.sqrt((data_vals / len(nc_datas))))
        datas.append(data_funcs_arr)
        datas.append(valdata_out)

        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }

    '''
    RMSE + RMSE MEAN+ RESULT MEAN
    '''

    def compare_rmse_all(self, files, nc_datas, vali_data, land_cover, shp_geom, var_input, compute_tpye):
        i = 0
        data_funcs_arr = []
        data_vals = 0

        datas = []
        units = []
        x_aix = []
        data_org = 0
        data_month = []

        self.var_read = var_input
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_data[i]
            # org:i==0
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
            print('计算中' + str(i) + '...')
            return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
            data_val = return_data['out_data_sq']
            data_vals = data_vals + data_val
            data_func = np.nanmean(return_data['simdata'])

            data_funcs_arr.append(data_func)
            data_org = data_org + return_data['simdata']
            data_month.append(return_data['simdata'].values)
            i += 1

        data_funcs = np.sqrt(data_vals / len(nc_datas))
        valdata_out = np.nanmean(np.sqrt(data_vals / len(nc_datas)))
        data_orgs = data_org / len(nc_datas)
        print('data_orgs:',np.nanmax(data_orgs), np.nanmin(data_orgs), np.nanmean(data_orgs))
        data_month = np.array(data_month)
        data_month_out = data_month.reshape(3, 12, 224, 464).mean(axis=0)
        datas.append(data_funcs)
        datas.append(valdata_out)
        datas.append(data_funcs_arr)
        datas.append(data_orgs)
        datas.append(data_month_out)

        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }

    '''
       RMSE + RMSE MEAN 
       '''

    def compare_mean_rmse_all(self, files, nc_datas, vali_data, land_cover, shp_geom, var_input, compute_tpye):
        i = 0
        data_funcs_arr = []
        data_vals = 0

        datas = []
        units = []
        x_aix = []
        self.var_read = var_input
        data_val = []
        for n in range(len(nc_datas[0])):
            a = 0
            for m in range(len(nc_datas)):

                c = nc_datas[m][n]
                if n % 12 == 0:
                    c = c[1:]
                else:
                    pass
                return_data = self.out_month_mean(c, None, land_cover, shp_geom, False)
                b = return_data['simdata']
                print(np.nanmax(b), 'b的最大值')
                a += b

            a = a / len(nc_datas)
            data_val.append(a)
        while i < len(data_val):
            title_name = files[0][i].split('.')[1]
            self.title_name = title_name
            val1 = vali_data[i]
            out_datas = data_val[i]
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
            print('计算中' + str(i) + '...')
            return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True, False)
            data_val_1 = return_data['out_data_sq']
            data_vals = data_vals + data_val_1
            data_func = np.nanmean(return_data['simdata']).values
            data_funcs_arr.append(data_func)

            i += 1

        data_funcs = np.sqrt(data_vals / len(data_val))
        valdata_out = np.nanmean(np.sqrt(data_vals / len(data_val)))
        data_org = data_vals / len(nc_datas)

        datas.append(data_funcs)
        datas.append(valdata_out)
        datas.append(data_funcs_arr)
        datas.append(data_org)

        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }

    '''
       SCDF of Multiple OP Schemes
       '''

    def compute_scdf(self, files, nc_datas, var_input):
        datas = []
        data_funcs = nc_datas
        # 使用正态分布计算理论上的累积分布
        sorted_data = np.sort(data_funcs.values.flatten())
        sorted_data = sorted_data[~np.isnan(sorted_data)]
        y_equals_1 = np.ones_like(sorted_data)
        theoretical_cdf = norm.cdf(sorted_data, loc=np.nanmean(data_funcs), scale=np.nanstd(data_funcs))
        area_under_curve = np.trapz(y_equals_1 - theoretical_cdf, sorted_data)
        print(area_under_curve, 'area_under_curve')
        # print(np.trapz(1 - theoretical_cdf, sorted_data,), 'area_under_curve0')
        # print(np.trapz(1 - theoretical_cdf[1:], sorted_data[1:],), 'area_under_curve1')
        # print(np.trapz(1 - theoretical_cdf[3:], sorted_data[3:],), 'area_under_curve3')
        # print(np.trapz(1 - theoretical_cdf[5:], sorted_data[5:],), 'area_under_curve5')
        # print(np.trapz(1 - theoretical_cdf[10:], sorted_data[10:],), 'area_under_curve10')
        # print(np.trapz(1 - theoretical_cdf[50:], sorted_data[50:],), 'area_under_curve50')
        # print(np.trapz(1 - theoretical_cdf[100:], sorted_data[100:],), 'area_under_curve100')
        # print(np.trapz(1 - theoretical_cdf[-100:], sorted_data[-100:],), 'area_under_curve-100')
        # print(np.trapz(1 - theoretical_cdf[-500:], sorted_data[-500:],), 'area_under_curve-500')

        datas.append([sorted_data, theoretical_cdf])
        units = [self.unit_data[var_input]['unit']]
        return {
            "datas": datas,
            'units': units,
            "x_aix": self.x_aix
        }

    '''
    Calculation of Simulation and Validation Comparison
    '''

    def compute_compare_all(self, files, nc_datas, vali_data, land_cover, shp_geom, var_input, compute_tpye):
        self.var_read = var_input

        i = 0
        valdata_out = 0
        data_funcs = 0
        data_vals = 0
        data_funcs_arr_sim = 0

        valdata_out_arr = []
        data_funcs_arr = []

        datas = []
        units = []
        x_aix = []
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_data[i]
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            dataset = nc_datas[i]["data"]
            # units.append(nc_datas[i]['attr_name'][0]['Attributes']['units'])
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
            print('计算中' + str(i) + '...')
            if compute_tpye == 'compare_map':
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom)
                data_func = return_data['simdata']
                data_funcs = data_funcs + data_func
                data_funcs_arr = [data_funcs]
                data_val = return_data['valdata']
                valdata_out = valdata_out + data_val
                valdata_out_arr = [valdata_out_arr]


            elif compute_tpye[-7:] == 'monthly':
                if compute_tpye.find('RMSE') != -1:
                    return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                    data_func = return_data['outdata']
                    data_funcs_arr.append(data_func)
                else:
                    return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                    data_func = return_data['simdata']
                    data_funcs_arr.append(data_func)
                    data_val = return_data['valdata']
                    valdata_out_arr.append(data_val)

            elif compute_tpye == 'compare_years' or compute_tpye == 'RMSE_all':
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                data_func = np.nanmean(return_data['simdata'])
                data_funcs_arr.append(data_func)
                # print(xr.where(data_func >= 0, 1, np.nan).count().item(),'simdata conut')
                data_val = return_data['out_data_sq']
                data_vals = data_vals + data_val
            elif compute_tpye == 'RMSE_lines':
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                data_func = np.nanmean(return_data['simdata'])
                data_funcs_arr.append(data_func)
            elif compute_tpye == 'RMSE' or compute_tpye == 'RMSE_return' or compute_tpye == 'SCDF' or compute_tpye == 'CDF' or compute_tpye == 'RMSE_3year_single':
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                data_func = return_data['out_data_sq']
                data_funcs = data_funcs + data_func
            elif compute_tpye == 'compare_line_monthly':
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                data_func = np.nanmean(return_data['simdata'])
                data_funcs_arr.append(data_func)
                data_val = np.nanmean(return_data['valdata'])
                valdata_out_arr.append(data_val)
            else:
                return_data = self.out_month_mean(out_datas, val1, land_cover, shp_geom, True)
                data_func = return_data['outdata']
                data_funcs = data_funcs + data_func
                data_funcs_arr = [data_funcs]
            i += 1

        if compute_tpye[-7:] == 'monthly':
            if compute_tpye.find('RMSE') != -1:
                datas.append([valdata_out_arr, data_funcs_arr])
            else:
                datas.append([valdata_out_arr, data_funcs_arr])

        if compute_tpye == 'compare_map':
            data_funcs = data_funcs / len(nc_datas)
            valdata_out = valdata_out / len(nc_datas)
            datas.append([valdata_out, data_funcs])
        elif compute_tpye == 'RMSE_line':
            data_funcs = np.nanmean(np.sqrt(data_funcs))
            datas.append([data_funcs])
        elif compute_tpye == 'RMSE' or compute_tpye == 'RMSE_return' or compute_tpye == 'RMSE_3year_single':
            data_funcs = np.sqrt(data_funcs / len(nc_datas))
            datas.append(data_funcs)
        elif compute_tpye == 'CDF':
            data_funcs = np.sqrt(data_funcs / len(nc_datas))
            # 使用正态分布计算理论上的累积分布
            sorted_data = np.sort(data_funcs.values.flatten())
            sorted_data = sorted_data[~np.isnan(sorted_data)]
            y_equals_1 = np.ones_like(sorted_data)
            theoretical_cdf = norm.cdf(sorted_data, loc=np.nanmean(data_funcs), scale=np.nanstd(data_funcs))
            area_under_curve = np.trapz(y_equals_1 - theoretical_cdf, sorted_data)
            print(area_under_curve, 'area_under_curve')
            datas.append([sorted_data, theoretical_cdf])

        elif compute_tpye == 'RMSE_all':
            data_funcs = np.sqrt(data_vals / len(nc_datas))
            valdata_out = np.nanmean(np.sqrt(data_vals / len(nc_datas)))
            datas.append(data_funcs)
            datas.append(valdata_out)
        elif compute_tpye == 'compare_years' or compute_tpye == 'RMSE_lines':
            valdata_out = np.nanmean(np.sqrt(data_vals / len(nc_datas)))
            # print(valdata_out, ':valdata_out',
            #       xr.where(np.sqrt(data_vals / len(nc_datas)) >= 0, 1, np.nan).count().item())
            datas.append(data_funcs_arr)
            datas.append(valdata_out)
        elif compute_tpye == 'compare_line_monthly':
            datas.append([valdata_out, data_funcs])

        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }

    '''SCDF'''
    def compute_compare_all_scdf(self, files, nc_datas, var_input, compute_tpye):
        i = 0
        data_funcs = 0
        datas = []
        units = []
        x_aix = []
        [vali_datas_out, land_cover, shp_geom] = self.vali_all(var_input)
        while i < len(nc_datas):
            title_name = files[i].split('.')[1]
            self.title_name = title_name
            val1 = vali_datas_out[i]
            if i % 12 == 0:
                out_datas = nc_datas[i]['attr_name'][0][var_input][1:]
            else:
                out_datas = nc_datas[i]['attr_name'][0][var_input]
            units.append(self.unit_data[var_input]['unit'])
            # 筛选条件
            x_aix.append(i)
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
        elif compute_tpye == 'SCDF_RMSE' or compute_tpye == 'SCDF_RMSE_percent':
            data_funcs = np.sqrt(data_funcs / len(nc_datas))
            datas.append(data_funcs)
        elif compute_tpye == 'CDF_all':
            data_funcs = np.sqrt(data_funcs / len(nc_datas))
            # 使用正态分布计算理论上的累积分布
            sorted_data = np.sort(data_funcs.values.flatten())
            sorted_data = sorted_data[~np.isnan(sorted_data)]
            y_equals_1 = np.ones_like(sorted_data)
            theoretical_cdf = norm.cdf(sorted_data, loc=np.nanmean(data_funcs), scale=np.nanstd(data_funcs))
            area_under_curve = np.trapz(y_equals_1 - theoretical_cdf, sorted_data)
            print(area_under_curve, 'area_under_curve')
            datas.append([sorted_data, theoretical_cdf])
        return {
            "datas": datas,
            'units': units,
            "x_aix": x_aix
        }


if __name__ == '__main__':
    pass
