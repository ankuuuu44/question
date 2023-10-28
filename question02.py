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



def errorsearch(logdict,N):
    errordict = {}
    
    for i in logdict:
        if(logdict[i]['ping'] == '-'):
            if logdict[i]['address'] in errordict:
                errordict[logdict[i]['address']]['counttimeout'] += 1
            else:
                errordict[logdict[i]['address']] ={
                    'errorstarttime' : logdict[i]['time'],
                    'counttimeout' : 1
                }
        elif(logdict[i]['ping'] != '-') and (logdict[i]['address'] in errordict):
            errordict[logdict[i]['address']]['errorendtime'] = logdict[i]['time']
            
        for key,value in list(errordict.items()):
            if('errorstarttime' in value) and ('errorendtime' in value):
                if(value['counttimeout'] >= int(N)):
                    errorstartdate = datetime.strptime(value['errorstarttime'], '%Y%m%d%H%M%S')
                    errorenddate = datetime.strptime(value['errorendtime'], '%Y%m%d%H%M%S')

                    errortime = errorenddate - errorstartdate
                    
                    print(f"故障状態のサーバアドレス:{key}")
                    print(f'サーバの故障期間{errortime}')

                    del errordict[key]
                else:
                    print(f'サーバアドレス{key}はタイムアウトしましたが，連続タイムアウト回数が{value['counttimeout']}であったため，故障とみなされませんでした．')
                    del errordict[key]


def main ():
    #main関数
    logdict = {}                        #logデータを格納する二次元連想配列
    log_filename = "server.log"         #読み込むlogファイル
    logdict = readfile(log_filename)    
    print("何回以上連続してタイムアウトした場合にのみ故障とみなすように設定しますか?>>")
    N = input()
    errorsearch(logdict,N)               #故障状態のサーバアドレスとサーバの故障期間を出力する関数．引数はlogデータを格納した二次元配列



    





if __name__ == "__main__":
    #ファイルの読み込み
    main()
    
        
        

            
            