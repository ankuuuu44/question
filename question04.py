from datetime import datetime

def readfile(filename):
    #fileの読み込みを行うプログラム
    log_filename = filename
    count = 0       #logfileの行数を取得するカウント変数
    logdict ={}      #fileを行ごとに取得する配列
    
    with open(log_filename,"r",encoding="utf-8") as f:
        for line in f:
            
            str = line.split(",")
            logdict[count] = {
                'time' : str[0],
                'address' : str[1],
                'ping' : str[2].replace('\n','')
            }

            count += 1
        print(f'ログファイルの行数:{count}')
    return logdict

def makeipgroup(logdict,N):
    ipgroup = {}

    for ip in logdict:
        ipaddress,subnet = logdict[ip]['address'].split('/')
        if subnet in ipgroup:
            pass
        else:
            ipgroup[subnet] = {}

        a,b,c,d = ipaddress.split('.')
        ab16 = a + '.' + b
        abc24 = a + '.' + b + '.' + c

        if logdict[ip]['ping'] == '-':
            if (int(subnet) == 8) :
                if(a not in ipgroup[subnet]):
                    ipgroup[subnet][a] = {}
                else:
                    pass
                if(logdict[ip]['address'] in ipgroup[subnet][a]):
                    ipgroup[subnet][a][logdict[ip]['address']]['counttimeout'] += 1
                else:
                    ipgroup[subnet][a][logdict[ip]['address']] = {
                        'errorstarttime' : logdict[ip]['time'],
                        'counttimeout' : 1
                    }
            elif (int(subnet) == 16):
                if(ab16 not in ipgroup[subnet]):
                    ipgroup[subnet][ab16] = {}
                else:
                    pass
                if(logdict[ip]['address'] in ipgroup[subnet][ab16]):
                    ipgroup[subnet][ab16][logdict[ip]['address']]['counttimeout'] += 1
                else:
                    ipgroup[subnet][ab16][logdict[ip]['address']] = {
                        'errorstarttime' : logdict[ip]['time'],
                        'counttimeout' : 1
                    }

            elif (int(subnet) == 24):
                if(abc24 not in ipgroup[subnet]):
                    ipgroup[subnet][abc24] = {}
                else:
                    pass
                if(logdict[ip]['address'] in ipgroup[subnet][abc24]):
                    ipgroup[subnet][abc24][logdict[ip]['address']]['counttimeout'] += 1
                else:
                    ipgroup[subnet][abc24][logdict[ip]['address']] = {
                        'errorstarttime' : logdict[ip]['time'],
                        'counttimeout' : 1
                    }

        elif logdict[ip]['ping'] != '-':
            if (int(subnet) == 8) :
                ipgroup[subnet][a][logdict[ip]['address']]['errorendtime'] = logdict[ip]['time']
            elif(int(subnet) == 16):
                if(ab16 in ipgroup[subnet]):
                    if(logdict[ip]['address'] in ipgroup[subnet][ab16]):
                        ipgroup[subnet][ab16][logdict[ip]['address']]['errorendtime'] = logdict[ip]['time']
            elif(int(subnet) == 24):
                if(abc24 in ipgroup[subnet]):
                    if(logdict[ip]['address'] in ipgroup[subnet][abc24]):
                        ipgroup[subnet][abc24][logdict[ip]['address']]['errorendtime'] = logdict[ip]['time']


    #print(ipgroup)
        max_errorstarttime = 0
        max_errorendtime = 0

        for prefix,subnetmask in list(ipgroup.items()):
            for key,value in list(subnetmask.items()):
                for ipad,valuend in list(value.items()):
                    if all('errorstarttime' in  itemvalue and 'errorendtime' in itemvalue and itemvalue['counttimeout'] >= int(N) for itemvalue in valuend.values()):
                        for itemvalue1 in valuend.values(): 
                            currentmaxerrorstarttime = int(itemvalue1['errorstarttime'])
                            currentmaxerrorendtime = int(itemvalue1['errorendtime'])
                            if  currentmaxerrorstarttime > max_errorstarttime:
                                max_errorstarttime = currentmaxerrorstarttime
                            if  currentmaxerrorendtime > max_errorendtime:
                                max_errorendtime = currentmaxerrorendtime
                            
                        
                        errorstartdate = datetime.strptime(max_errorstarttime, '%Y%m%d%H%M%S')
                        errorenddate = datetime.strptime(max_errorendtime, '%Y%m%d%H%M%S')

                        errortime = errorenddate - errorstartdate
                        
                        print(f"故障状態のサブネットマスク:{key}")
                        print(f'サーバの故障期間{errortime}')
                    else:
                        print('破損しているサブネットはありませんでした．')

                 
            
                





def main ():
    #main関数
    logdict = {}                        #logデータを格納する二次元連想配列
    log_filename = "server.log"         #読み込むlogファイル
    logdict = readfile(log_filename)    
    print("何回以上連続してタイムアウトした場合にのみ故障とみなすように設定しますか?>>")
    N = input()
    makeipgroup(logdict,N)
    


    





if __name__ == "__main__":
    #ファイルの読み込み
    main()
    
        
        

            
            