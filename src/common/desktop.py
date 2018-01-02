# coding: utf-8
from PIL import Image
import win32api, win32con, win32gui
import os


def set_wallpaper_from_bmp(bmp_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)


def set_wallpaper(img_path):
    # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
    img_dir = os.path.dirname(img_path)
    bmpImage = Image.open(img_path)
    new_bmp_path = os.path.join(img_dir, 'wallpaper.bmp')
    bmpImage.save(new_bmp_path, "BMP")
    set_wallpaper_from_bmp(new_bmp_path)


def desktop_icon():
    hwnd = win32gui.FindWindow("Progman", None)
    hwnd = win32gui.FindWindowEx(hwnd, None, 'SHELLDLL_DefView', None)
    hwnd = win32gui.FindWindowEx(hwnd, None, 'SysListView32', 'FolderView')
    win32gui.UpdateWindow(hwnd)



if __name__ == '__main__':
    ''''''
    #set_wallpaper('F:\\luo_tianyi.jpg')
    desktop_icon()