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


def loadserver(logdict,m,t):
    loaddict = {}

    for i in reversed(logdict):
        if logdict[i]['ping'] != '-':
            if logdict[i]['address'] in loaddict:
                count = len(loaddict[logdict[i]['address']]) + 1
                if count <= int(m):
                    loaddict[logdict[i]['address']][count] = {
                        'time': logdict[i]['time'],
                        'ping': logdict[i]['ping']
                    }
                else:
                    pass
            else:
                loaddict[logdict[i]['address']] = {
                    1: {
                        'time': logdict[i]['time'],
                        'ping': logdict[i]['ping']
                    }
                }
        else : 
            pass

    
    
    for key,value in loaddict.items():
        print(f'key: {key}, value: {value}')
        sum_ping =  sum(int(addressvalue['ping']) for addressvalue in value.values())
        ave_ping = sum_ping / len(value)
        print(f'key: {key}, total_ping: {sum_ping},ave_ping:{ave_ping}')

        if ave_ping > float(t):
            starttime = datetime.strptime(value[int(m)]['time'], '%Y%m%d%H%M%S')
            endtime = datetime.strptime(value[1]['time'], '%Y%m%d%H%M%S')
            loadtime = starttime - endtime
            print(f'サーバー{key}は過負荷状態であり，期間は{loadtime}')
        else:
            print(f'サーバー{key}は過負荷状態ではありません．')

            
        
    
        


def main ():
    #main関数
    logdict = {}                        #logデータを格納する二次元連想配列
    log_filename = "server.log"         #読み込むlogファイル
    logdict = readfile(log_filename)    
    print("直近m回の平均応答時間がtミリ秒を超えた場合は、サーバが過負荷状態になっているとみなします．mとtの入力を行てください")
    print("m>>")
    m = input()
    print("t>>")
    t = input()
    loadserver(logdict,m,t)



    





if __name__ == "__main__":
    #ファイルの読み込み
    main()
    
        
        

            
            