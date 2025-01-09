
import os
import xarray as xr
import time
from time import sleep
from netCDF4 import Dataset
import fsspec
import pygrib
import re
from osgeo import gdal
import geopandas as gpd

input_name = '/Volumes/momo'


class OutInput(object):
    def __init__(self, data) -> None:
        self.input_path = data["input_path"]
        self.out_path = data["out_path"]
        self.file = ''
        self.default_value = "default_value"
        pass

    '''
    Read NC File + Name
    '''
    def files_one(self, data_format, isout, attr_name, roads=None):
        if roads != None:
            file_name_list = roads
        else:
            file_name_list = os.listdir(self.input_path)
        arr_content = []
        for name in file_name_list:
            self.file = self.input_path + os.sep + str(name)
            name_idx = str(name).find('.idx')
            if name_idx != -1:
                os.remove(self.file)
            else:
                name_index_end = str(name).find(data_format)
                if name_index_end != -1:
                    content = {}
                    match data_format:
                        case 'grib':
                            content = self.ReadGRIBData(name, attr_name)
                        case '.grib':
                            content = self.ReadGRIBDataByPygrib(name, attr_name)
                        case '.nc':
                            content = self.read_nc_data(name, attr_name)
                        case 'nc':
                            content = self.read_nc_data_netcdf(name, attr_name)
                        case '.tif':
                            content = self.read_tif_data(name, attr_name)
                        case '.shp':
                            content = self.read_shp_data(name, attr_name)
                        case '.txt':
                            content = self.read_op_txt()
                        case 'txt':
                            content = self.read_gldas_txt()
                        case '.range':
                            content = self.read_param_file()

                    arr_content.append(content)
        if data_format == '.nc.loop':
            self.file = self.input_path + os.sep + '*' + data_format + '*'
            content = self.read_nc_files(name, attr_name)
            arr_content.append(content)
        if isout:
            # log
            self.WriteLog(self.out_path, arr_content)
        else:
            # return
            return arr_content

    '''
    NCPathName:org name
    '''
    def file_all(self, data_format, condition=None, match=False):
        file_name_list = os.listdir(self.input_path)
        arr_content = []
        arr_name = []
        for name in file_name_list:
            if condition != None:
                if match == True:
                    pattern = re.compile(fr'{condition}')
                    match_result = pattern.match(name)
                    if match_result:
                        file = self.input_path + os.sep + str(name)
                        arr_name.append(name)
                        arr_content.append(file)
                else:
                    if name.find(condition) != -1:
                        file = self.input_path + os.sep + str(name)
                        arr_name.append(name)
                        arr_content.append(file)

            else:
                file = self.input_path + os.sep + str(name)
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
        Reading .nc
    '''


    def read_nc_data(self, name, attr_name):
        name_index = str(name).find('.nc')
        if name_index == -1:
            OutInput.WriteToNc(self.file)
        else:
            nc_file = fsspec.open(self.file)
            # data = xr.open_dataset(nc_file.open(), decode_times=False)
            # data.dstart.attrs['calendar'] = 'proleptic_gregorian'
            # xr.decode_cf(data, decode_times=True)
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
            # 测试
            # current_time = datetime.datetime.now().time()
            # print("当前时间1：", current_time)
            # name_time = data.get('Times', default=self.default_value)
            # name_time_type = name_time.astype(str)
            # name_time_type = pd.to_datetime(name_time_type, format="%Y-%m-%d_%H:%M:%S")
            # name_time_type.astype('datetime64[ns]')
            # # name_time_type是一个DatetimeIndex
            # # 根据时间变量提取年份和月份信息
            # # year = name_time_type.year
            # month = name_time_type.month
            # # nc_data['year'] = year
            # data['month'] = month
            # group_data = data.groupby(data['month'])
            # current_time = datetime.datetime.now().time()
            # print("当前时间2：", current_time)
            # dimensions = data.dims
            # print(dimensions)
            # mean_1 = group_data[1]['GPP'].mean()
            # # mean_1 = [i['GPP'].mean() for (j, i) in group_data]
            # print(mean_1)
            # current_time = datetime.datetime.now().time()
            # print("当前时间4：", current_time)
            # 测试
            # 获取属性值，属性值为一个字符串数组
            if len(attr_name) > 0:
                attrs = self.ReadDataAttr(data, attr_name)
                content['attr_name'] = attrs
            return content

    '''Reading .nc by netcdf4'''

    def read_nc_data_netcdf(self, name, attr_name):

        name_index = str(name).find('.nc')
        if name_index == -1:
            OutInput.WriteToNc(self.file)
        else:
            print("文件为：", self.file)
            data = Dataset(self.file, "r")
            variable = data.ncattrs()
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

            }
            # 获取属性值，属性值为一个字符串数组
            # if len(attr_name) > 0:
            #     attrs = self.ReadDataAttr(data, attr_name)
            #     content['attr_name'] = attrs
            return content

    '''
        Reanding GRIB
        filter_by_keys={'typeOfLevel': 'heightAboveGround'}
        filter_by_keys={'typeOfLevel': 'surface'}
        filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'}
        filter_by_keys={'stepType': 'instant', 'typeOfLevel': 'surface'}
        filter_by_keys={'stepType': 'accum', 'typeOfLevel': 'surface'}
        filter_by_keys={'typeOfLevel': 'surface'}
        filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'}
        'stepType': '7','typeOfLevel': 'surface'
    '''

    def ReadGRIBData(self, name, attr_name):
        name_idx = str(name).find('.idx')
        if name_idx != -1:
            os.remove(self.file)
        else:
            name_index = str(name).find('.grib')
            if (name_index != -1):
                print(self.file)
                backend_kwargs = {
                    'filter_by_keys': {
                        'stepType': 'instant',
                        'typeOfLevel': 'surface',
                        "time": 378691200
                    }
                }
                data = xr.open_dataset(
                    self.file, engine="cfgrib", backend_kwargs=backend_kwargs)
                print("文件为：", data)
                variable = data.variables
                print("文件为：", self.file)
                content = {
                    "file": self.file,
                    "variable": variable,
                    "data": data,
                    "attr_name": '',
                    "backend_kwargs": backend_kwargs
                }

                if len(attr_name) > 0:
                    attrs = self.ReadDataAttr(data, attr_name)
                    content['attr_name'] = attrs
                return content
    '''
    Reanding GRIB by Pygrib
    '''
    def ReadGRIBDataByPygrib(self, name, attr_name):
        name_idx = str(name).find('.idx')
        if name_idx != -1:
            os.remove(self.file)
        else:
            name_index = str(name).find('.grib')
            if (name_index != -1):
                # data = xr.open_dataset(self.file, engine="cfgrib")
                data = pygrib.open(self.file)
                print("文件为：", data)
                data.seek(0)  # 偏移量，一般都是设置0 表示第一个变量开始读；如果设2 则从第三个变量开始读
                variable = []
                for grb in data:  # 输出文件各个变量信息
                    str_grb = str(grb) + '/\n'
                    variable.append(str_grb)
                data_one = data.select(name='U component of wind')[0]
                lat, lon = data_one.latlons()
                # 获取值
                value1 = data_one.values()
                # 根据范围获取
                # value2 = grb.data(lat1=None, lat2=None, lon1=None, lon2=None)
                print(lat, lon)
                content = {
                    "file": self.file,
                    "variable": variable,
                    "data": data,
                    "attr_name": '',
                }
                if len(attr_name) > 0:
                    attrs = self.ReadDataAttr(data, attr_name)
                    content['attr_name'] = attrs
                return content
            # 输出log日志
    '''
    Split .nc
    '''
    def split_nc_data(self, year_r=1987):
        year_str = 'output.' + str(year_r) + '.*loop0000'
        nc_files = self.file_all('.nc', year_str, True)
        # files = [data.WriteToNc(i) for i in nc_files['roads']]
        # 顺序
        files = sorted(nc_files['files'], key=lambda x: x.split('.')[1][-2:])[:50]
        data_file_arr = []
        for file in files:
            nc_file = self.input_path + os.sep + file
            print(nc_file)
            xr_data = xr.open_dataset(nc_file)
            data_file_arr.append(xr_data)

    '''File name add .nc
    '''
    def WriteToNc(self, file):
        path = file + '.nc'
        with open(file, 'rb') as contents:
            container = contents.read()
            with open(path, 'wb') as content:
                content.write(container)
                print('data name  is  changed')

    # OUTPUT LOG
    def WriteLog(self, out_path, content):
        times = time.time()
        local_time = time.localtime(times)
        local_time = time.strftime("%Y-%m-%d%H%M%S", local_time)
        path = out_path + os.sep + local_time + '.log'
        print('输出路径', path)
        string_cont = [str(x) for x in content]
        cont = bytes(str(string_cont), encoding='utf-8')
        with open(path, 'wb') as contents:
            contents.write(cont)
            print('log is outputed')


    '''
    Retrieve Attribute Values as a String Array
    '''

    def ReadDataAttr(self, data, attr_name):
        attrs = []
        for attr_one in attr_name:
            # attr = data[attr_one].values
            attr = data[attr_one]
            # i_arr = []
            # for i in attr:
            #     i_arr.append(i)
            attr_data = data[attr_one].variable.attrs
            attrs.append({
                attr_one: attr,
                'Attributes': attr_data
            })
        return attrs
    '''
    Reading TIFF
    '''
    def read_tif_data(self, name, attr_name):
        dataset = gdal.Open(self.file)
        width = dataset.RasterXSize
        height = dataset.RasterYSize
        num_bands = dataset.RasterCount
        band = dataset.GetRasterBand(1)  # 获取第一个波段（索引从 1 开始）
        data = band.ReadAsArray()
        content = {
            "file": self.file,
            "filename": str(name),
            "variable": data,
            "data": data,
            "attr_name": ''
        }
        dataset = None

        print("Width:", width)
        print("Height:", height)
        print("Number of bands:", num_bands)
        print("Data shape:", data.shape)
        print("Data:", data)
        return content
    '''
    Reading SHP
    '''
    def read_shp_data(self, name, attr_name):
        a = gpd.read_file(self.file)

    '''
    Reading files .nc
    '''
    def read_nc_files(self, name, attr_name):
        name_index = str(name).find('.nc')
        if name_index == -1:
            OutInput.WriteToNc(self.file)
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

    '''
     Reading .log
     '''
    def read_log(self, filepath):
        with open(filepath, "r") as file:
            # 逐行读取文件内容
            i = 1
            data_log = []
            for line_number, line in enumerate(file, start=1):
                if i == 1:
                    if line_number == 3:
                        data_string = line.strip('[]\n')

                        # 将逗号分隔的值拆分成列表
                        data_list = data_string.split(', ')

                        # 将字符串列表转换为浮点数列表
                        data_float_list = [float(value) for value in data_list]
                        data_log.append(data_float_list)
                        i += 1
                else:
                    if line_number == 3 * i + (i - 1):
                        data_string = line.strip('[]\n')

                        # 将逗号分隔的值拆分成列表
                        data_list = data_string.split(', ')

                        # 将字符串列表转换为浮点数列表
                        data_float_list = [float(value) for value in data_list]
                        data_log.append(data_float_list)
                        i += 1

            return data_log


    '''
    Reading Parameter Optimization Range and Name
    '''

    def read_param_file(self):

        with open(self.file, "r") as file:
            names = []
            bounds = []
            num_vars = 0

            for row in [line.split() for line in file if not line.strip().startswith('#')]:
                num_vars += 1
                names.append(row[0])
                bounds.append([float(row[1]), float(row[2])])

        return {'names': names, 'bounds': bounds, 'num_vars': num_vars}

    '''Reading OP Output .txx'''

    def read_op_txt(self):
        with open(self.file, "r") as file:
            data = file.readlines()

        # 解析数据
        data_parsed = []
        for line in data:
            values = line.split()
            data_parsed.append([float(val) for val in values])
        groups = data_parsed
        # 转置数据，使每个数组成一组
        # groups = list(zip(*data_parsed))
        return groups

    '''Reading gldas .txx'''
    def read_gldas_txt(self):
        with open(self.file, "r") as file:
            data = file.readlines()

        return data

if __name__ == '__main__':
    in_dir = input('输入文件夹目录：')
    sleep(1)
    out_dir = input_name + "/Noah/data/outlog"
    data = OutInput({
        "input_path": in_dir,
        "out_path": out_dir
    })
    data.files_one('.nc', True, ['SH2O'])
    pass
