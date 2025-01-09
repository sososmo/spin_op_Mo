import paramiko
import os
import sys
import re
import datetime
from time import sleep
import threading


class Http_CS_Conect():
    def __init__(self, data) -> None:
        self.hrldas_name = '/public1/home/scfa3271/hrl3.7'
        self.hrldas_1983 = '/hrldas-release-3.7.1'
        self.hrldas_1988 = '/hrldas_1'
        self.hrldas_2003 = '/hrldas_2'

        self.copy_org = '/hrldas/run'

        self.copy1_org = '/hrldas/run/namelist.hrldas'
        self.copy1 = '/hrldas/run/namelist.1.hrldas'

        self.copy2_org = '/hrldas/run/NoahmpTable.TBL'
        self.copy2 = '/hrldas/run//NoahmpTable.1.TBL'

        self.result_file = '/public1/home/scfa3271/soso/Noah-MP/results'
        self.copy_name_1 = 'RESTART.1984010100_DOMAIN1  0'
        self.copy_name_2 = 'RESTART.1989010100_DOMAIN1  0'
        self.copy_name_3 = 'RESTART.2004010100_DOMAIN1  0'

        self.copy4_org = '/public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/namelist.hrldas'
        self.copy4 = '/public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/namelist.hrlda.1'

        self.copy5_org = '/public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/namelist.hrldas'
        self.copy5 = '/public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/namelist.hrlda.1'
        self.inputNames = ["VCMX25", "RMF25"]
        self.input_val_org = [40.0, 1.80, 0.339, 2.790, 4.66E-05]
        self.input_soil_org = {
            'BB': [2.790, 4.260, 4.740, 5.330, 3.860, 5.250, 6.770, 8.720, 8.170, 10.730, 10.390, 11.550, 5.250, 0.000,
                   2.790, 4.260, 11.550, 2.790, 2.790],
            'DRYSMC': [0.010, 0.028, 0.047, 0.084, 0.061, 0.066, 0.069, 0.120, 0.103, 0.100, 0.126, 0.138, 0.066, 0.000,
                       0.006, 0.028, 0.030, 0.006, 0.010],
            'MAXSMC': [0.339, 0.421, 0.434, 0.476, 0.484, 0.439, 0.404, 0.464, 0.465, 0.406, 0.468, 0.468, 0.439, 1.000,
                       0.200, 0.421, 0.468, 0.200, 0.339],
            'REFSMC': [0.192, 0.283, 0.312, 0.360, 0.347, 0.329, 0.315, 0.387, 0.382, 0.338, 0.404, 0.412, 0.329, 0.000,
                       0.170, 0.283, 0.454, 0.170, 0.192],
            'SATPSI': [0.069, 0.036, 0.141, 0.759, 0.955, 0.355, 0.135, 0.617, 0.263, 0.098, 0.324, 0.468, 0.355, 0.000,
                       0.069, 0.036, 0.468, 0.069, 0.069],
            'SATDK': [4.66E-05, 1.41E-05, 5.23E-06, 2.81E-06, 2.18E-06, 3.38E-06, 4.45E-06, 2.03E-06, 2.45E-06,
                      7.22E-06,
                      1.34E-06, 9.74E-07, 3.38E-06, 0.00E+00, 1.41E-04, 1.41E-05, 9.74E-07, 1.41E-04, 4.66E-05],
            'SATDW': [2.65E-05, 5.14E-06, 8.05E-06, 2.39E-05, 1.66E-05, 1.43E-05, 1.01E-05, 2.35E-05, 1.13E-05,
                      1.87E-05,
                      9.64E-06, 1.12E-05, 1.43E-05, 0.00E+00, 1.36E-04, 5.14E-06, 1.12E-05, 1.36E-04, 2.65E-05],
            'WLTSMC': [0.010, 0.028, 0.047, 0.084, 0.061, 0.066, 0.069, 0.120, 0.103, 0.100, 0.126, 0.138, 0.066, 0.000,
                       0.006, 0.028, 0.030, 0.006, 0.010],
            'QTZ': [0.920, 0.820, 0.600, 0.250, 0.100, 0.400, 0.600, 0.100, 0.350, 0.520, 0.100, 0.250, 0.050, 0.600,
                    0.070, 0.250, 0.600, 0.520, 0.920],
            'BVIC': [0.050, 0.080, 0.090, 0.250, 0.150, 0.180, 0.200, 0.220, 0.230, 0.250, 0.280, 0.300, 0.260, 0.000,
                     1.000, 1.000, 1.000, 0.350, 0.150],
            'AXAJ': [0.009, 0.010, 0.009, 0.010, 0.012, 0.013, 0.014, 0.015, 0.016, 0.015, 0.016, 0.017, 0.012, 0.001,
                     0.017, 0.017, 0.017, 0.015, 0.009],
            'BXAJ': [0.050, 0.080, 0.090, 0.250, 0.150, 0.180, 0.200, 0.220, 0.230, 0.250, 0.280, 0.300, 0.260, 0.000,
                     1.000, 1.000, 1.000, 0.350, 0.150],
            'XXAJ': [0.050, 0.080, 0.090, 0.250, 0.150, 0.180, 0.200, 0.220, 0.230, 0.250, 0.280, 0.300, 0.260, 0.000,
                     1.000, 1.000, 1.000, 0.350, 0.150],
            'BDVIC': [0.050, 0.080, 0.090, 0.250, 0.150, 0.180, 0.200, 0.220, 0.230, 0.250, 0.280, 0.300, 0.260, 0.000,
                      1.000, 1.000, 1.000, 0.350, 0.150],
            'BBVIC': [1.000, 1.010, 1.020, 1.025, 1.000, 1.000, 1.032, 1.035, 1.040, 1.042, 1.045, 1.000, 1.000, 1.000,
                      1.000, 1.000, 1.000, 1.000, 1.000],
            'GDVIC': [0.050, 0.070, 0.130, 0.200, 0.170, 0.110, 0.260, 0.350, 0.260, 0.300, 0.380, 0.410, 0.500, 0.001,
                      0.010, 0.001, 0.001, 0.050, 0.020]
        }
        self.veg = 'USGS'
        self.vegtype = 7
        self.soiltype = 1
        self.ssh = None
        self.cp = None
        self.loop = data['loops']
        self.years = [1983, 1988, 2003]
        self.year = 2003
        self.outyear_bool = 0
        self.outyear = ''
        self.local_folder = ''
        self.python_org = '/public1/home/scfa3271/soso/python/'
        self.python_new_file = ''
        self.python_down_name = 'scdf_python_data.txt'
        self.python_down = self.python_org + self.python_down_name
        self.input_name = '/Volumes/momo'

    '''
    Connect to server
    '''
    def connect(self):
        server_address = ''
        server_port = 22
        username = ''
        password = ''
        local_port = 12345

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_address, port=server_port, username=username, password=password)

        transport = ssh.get_transport()
        transport.request_port_forward('', local_port)
        self.ssh = ssh

    '''
    Parameter Configuration Writing
    '''
    def connect_run_genAppInputFile_func(self, inputData):
        self.connect()
        ssh = self.ssh
        veg = self.veg
        vegtype = self.vegtype
        soiltype = self.soiltype
        for year in self.years:
            if year == 1983:
                copy2_org = self.hrldas_name + self.hrldas_1983 + self.copy2_org
                copy2 = self.hrldas_name + self.hrldas_1983 + self.copy2
                # 复制table文件
                stdin1, stdout1, stderr1 = ssh.exec_command(f'scp {copy2_org} {copy2}')
                exit_status = stdout1.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '执行复制tal.1文件')
                sleep(1)
                stdin2, stdout2, stderr2 = ssh.exec_command(f'cat {copy2}')
                # 等待命令执行完成
                exit_status = stdout2.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '执行复制tal文件')
                # 检查命令是否成功执行
                if exit_status == 0:
                    file_content2 = stdout2.read().decode('utf-8')
                    # 修改特定行
                    lines = file_content2.split('\n')
                    inputNames_i = 0
                    line_idx = 0
                    print(lines, 'lines')
                    for j, i in enumerate(self.inputNames):
                        print(j)
                        # pattern = i + r'\s*='
                        pattern = r'(' + re.escape(i) + r'\s*=)'
                        matching_lines = []
                        for idx, line in enumerate(lines):
                            match = re.search(pattern, line)
                            if match:
                                matching_lines.append((line, idx))
                        VEG_DATASET_DESCRIPTION = veg
                        if VEG_DATASET_DESCRIPTION == 'USGS':
                            print(matching_lines)
                            line_to_modify = matching_lines[0][1]
                            new_line_content_org = matching_lines[0][0].split(',')
                            new_line_content_org_1 = new_line_content_org[0].split('=')
                            if line_to_modify < 700:
                                new_line_content_org[vegtype - 1] = str(inputData[inputNames_i])
                                new_line_content = ','.join(new_line_content_org)
                            else:
                                for soil_index, soil_i in enumerate(new_line_content_org):
                                    var_org = self.input_soil_org[i][soil_index]
                                    if soil_index == 0:
                                        if i == 'SATDK' or i == 'SATDW':
                                            new_para_mun = var_org * inputData[inputNames_i]
                                            scientific_notation_custom_precision = "{:.{}E}".format(new_para_mun, len(
                                                str(var_org).split('.')[-1]) - 1)
                                            scientific_notation_custom_precision = "{:.2E}".format(
                                                float(scientific_notation_custom_precision))
                                            new_para = str(scientific_notation_custom_precision)
                                        else:
                                            new_para = str(round((var_org * inputData[inputNames_i]), 3))
                                        new_line_content_org[soil_index] = new_line_content_org_1[
                                                                               0].strip() + ' = ' + new_para
                                    elif soil_index == 13:
                                        new_line_content_org[soil_index] = str(var_org)
                                    else:
                                        if i == 'SATDK' or i == 'SATDW':
                                            new_para_mun = var_org * inputData[inputNames_i]
                                            scientific_notation_custom_precision = "{:.{}E}".format(new_para_mun, len(
                                                str(var_org).split('.')[-1]) - 1)
                                            scientific_notation_custom_precision = "{:.2E}".format(
                                                float(scientific_notation_custom_precision))
                                            new_para = str(scientific_notation_custom_precision)
                                        else:
                                            new_para = str(round((var_org * inputData[inputNames_i]), 3))
                                        new_line_content_org[soil_index] = new_para
                                    new_line_content = new_line_content_org
                                    new_line_content = ','.join(new_line_content)
                            lines[line_to_modify] = new_line_content
                            print(lines[line_to_modify])
                        # 重新组合文件内容
                        else:
                            # modis
                            pass
                        inputNames_i += 1

                    new_file_content = '\n'.join(lines)

                    # 写回到文件
                    with ssh.open_sftp().file(copy2, 'w') as remote_file:
                        remote_file.write(new_file_content)
                    # 修改名称
                    command = f'mv {copy2_org} {copy2_org + ".1"}'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                    print(exit_status, '改写tab的参数完成')
                    command = f'mv {copy2} {copy2_org}'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                    print(exit_status, 'tab所有内容完成')
                else:
                    print("命令执行失败")
            elif year == 1988:
                copy2_org = self.hrldas_name + self.hrldas_1988 + self.copy2_org
                copy2 = self.hrldas_name + self.hrldas_1988 + self.copy2
                # 复制table文件
                stdin1, stdout1, stderr1 = ssh.exec_command(f'scp {copy2_org} {copy2}')
                exit_status = stdout1.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '执行复制tal.1文件')
                sleep(1)
                stdin2, stdout2, stderr2 = ssh.exec_command(f'cat {copy2}')
                # 等待命令执行完成
                exit_status = stdout2.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '执行复制tal文件')
                # 检查命令是否成功执行
                if exit_status == 0:
                    file_content2 = stdout2.read().decode('utf-8')
                    # 修改特定行
                    lines = file_content2.split('\n')
                    inputNames_i = 0
                    line_idx = 0
                    print(lines, 'lines')
                    for j, i in enumerate(self.inputNames):
                        print(j)
                        # pattern = i + r'\s*='
                        pattern = r'(' + re.escape(i) + r'\s*=)'
                        matching_lines = []
                        for idx, line in enumerate(lines):
                            match = re.search(pattern, line)
                            if match:
                                matching_lines.append((line, idx))
                        VEG_DATASET_DESCRIPTION = veg
                        if VEG_DATASET_DESCRIPTION == 'USGS':
                            print(matching_lines)
                            line_to_modify = matching_lines[0][1]
                            new_line_content_org = matching_lines[0][0].split(',')
                            new_line_content_org_1 = new_line_content_org[0].split('=')
                            if line_to_modify < 700:
                                new_line_content_org[vegtype - 1] = str(inputData[inputNames_i])
                                new_line_content = ','.join(new_line_content_org)
                            else:
                                for soil_index, soil_i in enumerate(new_line_content_org):
                                    var_org = self.input_soil_org[i][soil_index]
                                    if soil_index == 0:
                                        if i == 'SATDK' or i == 'SATDW':
                                            new_para_mun = var_org * inputData[inputNames_i]
                                            scientific_notation_custom_precision = "{:.{}E}".format(new_para_mun, len(
                                                str(var_org).split('.')[-1]) - 1)
                                            scientific_notation_custom_precision = "{:.2E}".format(
                                                float(scientific_notation_custom_precision))
                                            new_para = str(scientific_notation_custom_precision)
                                        else:
                                            new_para = str(round((var_org * inputData[inputNames_i]), 3))
                                        new_line_content_org[soil_index] = new_line_content_org_1[
                                                                               0].strip() + ' = ' + new_para
                                    elif soil_index == 13:
                                        new_line_content_org[soil_index] = str(var_org)
                                    else:
                                        if i == 'SATDK' or i == 'SATDW':
                                            new_para_mun = var_org * inputData[inputNames_i]
                                            scientific_notation_custom_precision = "{:.{}E}".format(new_para_mun, len(
                                                str(var_org).split('.')[-1]) - 1)
                                            scientific_notation_custom_precision = "{:.2E}".format(
                                                float(scientific_notation_custom_precision))
                                            new_para = str(scientific_notation_custom_precision)
                                        else:
                                            new_para = str(round((var_org * inputData[inputNames_i]), 3))
                                        new_line_content_org[soil_index] = new_para
                                    new_line_content = new_line_content_org
                                    new_line_content = ','.join(new_line_content)
                            lines[line_to_modify] = new_line_content
                            print(lines[line_to_modify])
                        # 重新组合文件内容
                        else:
                            # modis
                            pass
                        inputNames_i += 1

                    new_file_content = '\n'.join(lines)

                    # 写回到文件
                    with ssh.open_sftp().file(copy2, 'w') as remote_file:
                        remote_file.write(new_file_content)
                    # 修改名称
                    command = f'mv {copy2_org} {copy2_org + ".1"}'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                    print(exit_status, '改写tab的参数完成')
                    command = f'mv {copy2} {copy2_org}'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                    print(exit_status, 'tab所有内容完成')
                else:
                    print("命令执行失败")
            elif year == 2003:
                copy2_org = self.hrldas_name + self.hrldas_2003 + self.copy2_org
                copy2 = self.hrldas_name + self.hrldas_2003 + self.copy2
                # 复制table文件
                stdin1, stdout1, stderr1 = ssh.exec_command(f'scp {copy2_org} {copy2}')
                exit_status = stdout1.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '执行复制tal.1文件')
                sleep(1)
                stdin2, stdout2, stderr2 = ssh.exec_command(f'cat {copy2}')
                # 等待命令执行完成
                exit_status = stdout2.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '执行复制tal文件')
                # 检查命令是否成功执行
                if exit_status == 0:
                    file_content2 = stdout2.read().decode('utf-8')
                    # 修改特定行
                    lines = file_content2.split('\n')
                    inputNames_i = 0
                    line_idx = 0
                    print(lines, 'lines')
                    for j, i in enumerate(self.inputNames):
                        print(j)
                        # pattern = i + r'\s*='
                        pattern = r'(' + re.escape(i) + r'\s*=)'
                        matching_lines = []
                        for idx, line in enumerate(lines):
                            match = re.search(pattern, line)
                            if match:
                                matching_lines.append((line, idx))
                        VEG_DATASET_DESCRIPTION = veg
                        if VEG_DATASET_DESCRIPTION == 'USGS':
                            print(matching_lines)
                            line_to_modify = matching_lines[0][1]
                            new_line_content_org = matching_lines[0][0].split(',')
                            new_line_content_org_1 = new_line_content_org[0].split('=')
                            if line_to_modify < 700:
                                new_line_content_org[vegtype - 1] = str(inputData[inputNames_i])
                                new_line_content = ','.join(new_line_content_org)
                            else:
                                for soil_index, soil_i in enumerate(new_line_content_org):
                                    var_org = self.input_soil_org[i][soil_index]
                                    if soil_index == 0:
                                        if i == 'SATDK' or i == 'SATDW':
                                            new_para_mun = var_org * inputData[inputNames_i]
                                            scientific_notation_custom_precision = "{:.{}E}".format(new_para_mun, len(
                                                str(var_org).split('.')[-1]) - 1)
                                            scientific_notation_custom_precision = "{:.2E}".format(
                                                float(scientific_notation_custom_precision))
                                            new_para = str(scientific_notation_custom_precision)
                                        else:
                                            new_para = str(round((var_org * inputData[inputNames_i]), 3))
                                        new_line_content_org[soil_index] = new_line_content_org_1[
                                                                               0].strip() + ' = ' + new_para
                                    elif soil_index == 13:
                                        new_line_content_org[soil_index] = str(var_org)
                                    else:
                                        if i == 'SATDK' or i == 'SATDW':
                                            new_para_mun = var_org * inputData[inputNames_i]
                                            scientific_notation_custom_precision = "{:.{}E}".format(new_para_mun, len(
                                                str(var_org).split('.')[-1]) - 1)
                                            scientific_notation_custom_precision = "{:.2E}".format(
                                                float(scientific_notation_custom_precision))
                                            new_para = str(scientific_notation_custom_precision)
                                        else:
                                            new_para = str(round((var_org * inputData[inputNames_i]), 3))
                                        new_line_content_org[soil_index] = new_para
                                    new_line_content = new_line_content_org
                                    new_line_content = ','.join(new_line_content)
                            lines[line_to_modify] = new_line_content
                            print(lines[line_to_modify])
                        # 重新组合文件内容
                        else:
                            # modis
                            pass
                        inputNames_i += 1

                    new_file_content = '\n'.join(lines)

                    # 写回到文件
                    with ssh.open_sftp().file(copy2, 'w') as remote_file:
                        remote_file.write(new_file_content)
                    # 修改名称
                    command = f'mv {copy2_org} {copy2_org + ".1"}'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                    print(exit_status, '改写tab的参数完成')
                    command = f'mv {copy2} {copy2_org}'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                    print(exit_status, 'tab所有内容完成')
                else:
                    print("命令执行失败")

        # 关闭SSH连接
        # ssh.close

    '''
     Writing .namelist 
     '''
    def connect_run_runApplication_func(self):
        # self.connect()
        ssh = self.ssh
        veg = self.veg
        sftp = ssh.open_sftp()
        # 清空文件夹
        result_file = sftp.listdir(self.result_file)
        clean_file = ''
        for file in result_file:
            if file[-2:] != result_file:
                if self.loop < 10:
                    new_file = self.result_file + '/' + 'test_0' + str(self.loop)
                else:
                    new_file = self.result_file + '/' + 'test_' + str(self.loop)
                mk_folder_command = f'mkdir {new_file} '
                stdin, stdout, stderr = ssh.exec_command(mk_folder_command)
                exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
                print(exit_status, '创建输出文件')
                clean_file = new_file
            else:
                clean_file = file
        self.python_new_file = new_file
        # clear_folder_command = f'rm -r {clean_file}/*'
        # stdin, stdout, stderr = ssh.exec_command(clear_folder_command)
        # exit_status = stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
        # print(exit_status, '清除文件完成，--上次运行的数据')
        sleep(1)
        # 修改namelist
        for index, year in enumerate(self.years):
            if year == 1983:
                copy1_org = self.hrldas_name + self.hrldas_1983 + self.copy1_org

                with sftp.file(copy1_org, 'r') as remote_file:
                    content = remote_file.read().decode('utf-8')
                    lines = content.split('\n')
                    for idx, line in enumerate(lines):
                        if 'START_YEAR' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            b = a + ' ' + str(year)
                            lines[idx] = b
                        if 'KDAY' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            if year % 4 == 0:
                                kday = 366
                            else:
                                kday = 365
                            b = a + ' ' + str(kday)
                            lines[idx] = b
                        if 'SPINUP_LOOPS' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            b = a + ' ' + str(0)
                            lines[idx] = b
                        if 'RESTART_FILENAME_REQUESTED' in line:
                            a = line[:-2]
                            b = a[-2:]
                            c = line[-1:]
                            d = line.rfind('/')
                            if int(b) >= 10:
                                if self.loop - 1 >= 10:
                                    content_new = line[:-4] + str(self.loop - 1) + '"' + c
                                else:
                                    content_new = line[:-4] + ' ' + str(self.loop - 1) + '"' + c
                            else:
                                if self.loop - 1 >= 10:
                                    content_new = line[:-4] + str(self.loop - 1) + '"' + c
                                else:
                                    content_new = line[:-4] + ' ' + str(self.loop - 1) + '"' + c
                            out_d = content_new[d + 1:]
                            h = content_new[:d].rfind('/')
                            # single-year
                            # content_new = content_new[:h + 1] + str(self.year - 1) + '_50/' + out_d
                            # mulit-year
                            if self.outyear == '':
                                content_new = content_new[:h + 1] + str(year - 1) + '_50/' + out_d
                            else:
                                content_new = content_new[:h + 1] + str(self.outyear) + '_' + str(
                                    year - 1) + '_50/' + out_d
                            f = content_new.rfind('/')
                            content_new = content_new[:f + 1] + 'RESTART.' + str(
                                year) + '010100_DOMAIN1' + content_new[
                                                           -5:]
                            if content_new.find('!') != -1:
                                content_new = content_new.replace('!', '')
                            # if content_new.find('!') == -1:
                            #     content_new = '!' + content_new
                            lines[idx] = content_new
                        if 'HRLDAS_SETUP_FILE' in line:
                            d = line.rfind('/')
                            # single-year
                            # b = line[:d - 4] + str(self.year - 1) + '/' + line[d + 1:]
                            # mulit-year
                            if self.outyear == '':
                                b = line[:d - 4] + str(year - 1) + '/' + line[d + 1:]
                            else:
                                b = line[:d - 4] + str(self.outyear) + '/' + line[d + 1:]
                            lines[idx] = b

                        if 'OUTDIR' in line:
                            index_file = line.find('"')
                            a = line[:index_file + 1]
                            c = line[-1:]
                            b = a + clean_file + '/"' + c
                            lines[idx] = b
                print(content_new, 'restar name')
                content_new_all = '\n'.join(lines)
                with sftp.file(copy1_org, 'w') as remote_file:
                    remote_file.write(content_new_all)
            elif year == 1988:
                copy1_org = self.hrldas_name + self.hrldas_1988 + self.copy1_org

                with sftp.file(copy1_org, 'r') as remote_file:
                    content = remote_file.read().decode('utf-8')
                    lines = content.split('\n')
                    for idx, line in enumerate(lines):
                        if 'START_YEAR' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            b = a + ' ' + str(year)
                            lines[idx] = b
                        if 'KDAY' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            if year % 4 == 0:
                                kday = 366
                            else:
                                kday = 365
                            b = a + ' ' + str(kday)
                            lines[idx] = b
                        if 'SPINUP_LOOPS' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            b = a + ' ' + str(0)
                            lines[idx] = b
                        if 'RESTART_FILENAME_REQUESTED' in line:
                            a = line[:-2]
                            b = a[-2:]
                            c = line[-1:]
                            d = line.rfind('/')
                            if int(b) >= 10:
                                if self.loop - 1 >= 10:
                                    content_new = line[:-4] + str(self.loop - 1) + '"' + c
                                else:
                                    content_new = line[:-4] + ' ' + str(self.loop - 1) + '"' + c
                            else:
                                if self.loop - 1 >= 10:
                                    content_new = line[:-4] + str(self.loop - 1) + '"' + c
                                else:
                                    content_new = line[:-4] + ' ' + str(self.loop - 1) + '"' + c
                            out_d = content_new[d + 1:]
                            h = content_new[:d].rfind('/')
                            # single-year
                            # content_new = content_new[:h + 1] + str(self.year - 1) + '_50/' + out_d
                            # mulit-year
                            if self.outyear == '':
                                content_new = content_new[:h + 1] + str(year - 1) + '_50/' + out_d
                            else:
                                content_new = content_new[:h + 1] + str(self.outyear) + '_' + str(
                                    year - 1) + '_50/' + out_d
                            f = content_new.rfind('/')
                            content_new = content_new[:f + 1] + 'RESTART.' + str(
                                year) + '010100_DOMAIN1' + content_new[
                                                           -5:]
                            if content_new.find('!') != -1:
                                content_new = content_new.replace('!', '')
                            # if content_new.find('!') == -1:
                            #     content_new = '!' + content_new
                            lines[idx] = content_new
                        if 'HRLDAS_SETUP_FILE' in line:
                            d = line.rfind('/')
                            # single-year
                            # b = line[:d - 4] + str(self.year - 1) + '/' + line[d + 1:]
                            # mulit-year
                            if self.outyear == '':
                                b = line[:d - 4] + str(year - 1) + '/' + line[d + 1:]
                            else:
                                b = line[:d - 4] + str(self.outyear) + '/' + line[d + 1:]
                            lines[idx] = b

                        if 'OUTDIR' in line:
                            index_file = line.find('"')
                            a = line[:index_file + 1]
                            c = line[-1:]
                            b = a + clean_file + '/"' + c
                            lines[idx] = b
                print(content_new, 'restar name')
                content_new_all = '\n'.join(lines)
                with sftp.file(copy1_org, 'w') as remote_file:
                    remote_file.write(content_new_all)
            elif year == 2003:
                copy1_org = self.hrldas_name + self.hrldas_2003 + self.copy1_org

                with sftp.file(copy1_org, 'r') as remote_file:
                    content = remote_file.read().decode('utf-8')
                    lines = content.split('\n')
                    for idx, line in enumerate(lines):
                        if 'START_YEAR' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            b = a + ' ' + str(year)
                            lines[idx] = b
                        if 'KDAY' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            if year % 4 == 0:
                                kday = 366
                            else:
                                kday = 365
                            b = a + ' ' + str(kday)
                            lines[idx] = b
                        if 'SPINUP_LOOPS' in line:
                            index_file = line.find('=')
                            a = line[:index_file + 1]
                            b = a + ' ' + str(0)
                            lines[idx] = b
                        if 'RESTART_FILENAME_REQUESTED' in line:
                            a = line[:-2]
                            b = a[-2:]
                            c = line[-1:]
                            d = line.rfind('/')
                            if int(b) >= 10:
                                if self.loop - 1 >= 10:
                                    content_new = line[:-4] + str(self.loop - 1) + '"' + c
                                else:
                                    content_new = line[:-4] + ' ' + str(self.loop - 1) + '"' + c
                            else:
                                if self.loop - 1 >= 10:
                                    content_new = line[:-4] + str(self.loop - 1) + '"' + c
                                else:
                                    content_new = line[:-4] + ' ' + str(self.loop - 1) + '"' + c
                            out_d = content_new[d + 1:]
                            h = content_new[:d].rfind('/')
                            # single-year
                            # content_new = content_new[:h + 1] + str(self.year - 1) + '_50/' + out_d
                            # mulit-year
                            if self.outyear == '':
                                content_new = content_new[:h + 1] + str(year - 1) + '_50/' + out_d
                            else:
                                content_new = content_new[:h + 1] + str(self.outyear) + '_' + str(
                                    year - 1) + '_50/' + out_d
                            f = content_new.rfind('/')
                            content_new = content_new[:f + 1] + 'RESTART.' + str(
                                year) + '010100_DOMAIN1' + content_new[
                                                           -5:]
                            if content_new.find('!') != -1:
                                content_new = content_new.replace('!', '')
                            # if content_new.find('!') == -1:
                            #     content_new = '!' + content_new
                            lines[idx] = content_new
                        if 'HRLDAS_SETUP_FILE' in line:
                            d = line.rfind('/')
                            # single-year
                            # b = line[:d - 4] + str(self.year - 1) + '/' + line[d + 1:]
                            # mulit-year
                            if self.outyear == '':
                                b = line[:d - 4] + str(year - 1) + '/' + line[d + 1:]
                            else:
                                b = line[:d - 4] + str(self.outyear) + '/' + line[d + 1:]
                            lines[idx] = b

                        if 'OUTDIR' in line:
                            index_file = line.find('"')
                            a = line[:index_file + 1]
                            c = line[-1:]
                            b = a + clean_file + '/"' + c
                            lines[idx] = b
                print(content_new, 'restar name')
                content_new_all = '\n'.join(lines)
                with sftp.file(copy1_org, 'w') as remote_file:
                    remote_file.write(content_new_all)
        # 运行程序
        print('准备运行模拟')
        time_log = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        # command = f'./hrldas.exe >./log/20231115_8.log'
        # command = f'/public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/hrldas.exe>/public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/log/20231115_8.log'
        # command = f'sbatch /public1/home/scfa3271/hrl3.7/hrldas-release-3.7.1/hrldas/run/sub.sh'
        # stdin, stdout, stderr = ssh.exec_command(command)

        threads = []

        # 添加每个模型的运行到线程
        # for year in self.years:
        #     copy_org = getattr(self, f'hrldas_name') + getattr(self, f'hrldas_{year}') + getattr(self, 'copy_org')
        #     command2 = 'sbatch sub.sh'
        #     thread = threading.Thread(target=self.run_command, args=(ssh, copy_org, command2, year))
        #     threads.append(thread)
        #     thread.start()
        # # 等待所有线程完成
        # for thread in threads:
        #     thread.join()

        while 1:
            # print('Check result at Time: ' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
            sys.stdout.flush()
            remote_files = sftp.listdir(clean_file)
            arr_end_sim = [self.copy_name_1, self.copy_name_2, self.copy_name_3]
            all_files_present = all(file in remote_files for file in arr_end_sim)

            if all_files_present == True:
                print('simulate over')
                break
            else:
                continue
        # 关闭SSH连接
        # ssh.close()

    '''
    Run model
    '''
    def run_command(self, ssh, directory, command, year):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'cd {directory} && {command}')
        error = ssh_stderr.read().decode()
        if error:
            print(f'Error running model in {directory}: {error}')
        else:
            print(f'{year}开始运行模型 in {directory}')

    '''
    Get Output Data
    '''
    def getOutput(self):
        # self.connect()
        sleep(3)
        print('开始计算')
        '''！！！改变预热次数时间，服务器上需要修改python文件！！！'''
        ssh = self.ssh
        sftp = ssh.open_sftp()
        load_py = f'module load python/3.9.6'
        command = f'python3 compute_scdf.py >./2025python.log'
        # command = f'python3 compute_scdf.py --input_path {self.python_new_file}'
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'{load_py} && cd {self.python_org} && {command}')
        # 读取输出
        output = ssh_stdout.read().decode()
        error = ssh_stderr.read().decode()

        print("Output:", output)
        print("Error:", error)

        exit_status = ssh_stdout.channel.recv_exit_status()  # 这会阻塞，直到命令完成
        print(exit_status, '计算scdf')
        # 检查命令是否成功执行
        time_now = str(datetime.datetime.now().strftime('%d_%H_%M_'))
        local_folder = self.input_name + '/pro/py_conda/uq/uqofrun/UQ/optimization/scdf_txt/20241110/' + time_now + os.sep
        ex = os.path.exists(local_folder)
        if not ex:
            os.makedirs(local_folder)
        if exit_status == 0:
            download_thread = threading.Thread(
                target=self.download_files(sftp, self.python_down, local_folder))
            download_thread.start()
            # 下载后清除服务器上的文件
            clear_folder_command = f'rm -r {self.python_down}/*'
            stdin, stdout, stderr = ssh.exec_command(clear_folder_command)
        else:
            print('scdf计算失败')
        ssh.close()

    def download_files(self, sftp, remote_folder, local_folder):
        remote_file_path = remote_folder
        local_file_path = os.path.join(local_folder, self.python_down_name)
        self.local_folder = local_file_path
        try:
            sftp.get(remote_file_path, local_file_path)
            if os.path.exists(local_file_path):
                print(f"文件下载成功: {local_file_path}")
            else:
                print(f"下载失败，文件不存在: {local_file_path}")
        except Exception as e:
            print(f"下载过程中发生错误: {e}")

    '''
    Calculate the objective function
    '''

    def getOutput_data(self):
        local_folders = self.local_folder
        # local_folders = '/Volumes/momo/pro/py_conda/nc_py/compute_nc/scdf_python_data.txt'
        data_return = []
        with open(local_folders, "r") as lines:
            for line in lines:
                line = float(line.strip())
                data_return.append(line)
        print(data_return, 'SCDF')
        # print(data_return_rmse, 'RMSE')
        return data_return

    def evaluate(self, values, names):
        print(values, names)
        self.inputNames = names
        f = open('invalidtest.txt', 'w')
        inputData = values
        sys.stdout.flush()
        # genAppInputFile(inputData, appInputTmplt, appInputFiles, nInputs, inputNames)
        # self.local_folder = ''
        self.connect_run_genAppInputFile_func(inputData)
        self.connect_run_runApplication_func()
        self.getOutput()

        Y = self.getOutput_data()
        print(Y, 'Y-out')

        sys.stdout.flush()
        #    print 'Noah-MP End Time: ' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        # 每次的结果输出
        for i in Y:
            if i < 0:
                f.write(str(i) + '\n')
        f.close()
        return {'modelout': Y, 'sampleout': values}


if __name__ == '__main__':
    pass
