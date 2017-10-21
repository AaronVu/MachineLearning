import zipfile
import os
import gzip
import tarfile


# 解压zip
def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names, file_name + "_files/")
    zip_file.close()


# 解压gz
def un_gz(file_name):
    """ungz zip file"""
    f_name = file_name.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name)
    # 创建gzip对象
    open(f_name, "w+").write(g_file.read())
    # gzip对象用read()打开后，写入open()建立的文件中。
    g_file.close()
    if f_name.endswith('.tar'):
        un_tar(f_name)
        # 关闭gzip对象


# 解压tar
def un_tar(file_name):
    """untar zip file"""
    tar = tarfile.open(file_name)
    names = tar.getnames()
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
        # 由于解压后是许多文件，预先建立同名文件夹
    for name in names:
        tar.extract(name, file_name + "_files/")
    tar.close()


def unpack(file_name, name):
    if file_name.endswith('zip'):
        un_zip(name)
    elif file_name.endswith('gz'):
        un_gz(name)
    elif file_name.endswith('tar'):
        un_tar(name)
    else:
        print("Error File...")
    print("Unpack Success...")


def main():
    file_name = input("请输入文件路径: ")
    files = file_name.split(os.sep)
    name = files[len(files)-1]
    print("File Name Is %s ..."%(name))
    unpack(file_name)