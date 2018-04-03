import requests
from bs4 import BeautifulSoup
import time
import math
from random import randint
# fresh proxies here: http://proxy-daily.com/
def read_from_file():
    lines = [line.rstrip("\n") for line in open("proxies.txt")] # open("freeproxy_9896982925.txt")]
    return lines
"""
def get_proxies():
    proxy_list = []
    date = time.strftime("%Y-%m-%d", time.localtime())
    url = "http://checkerproxy.net/getProxy?date=" + date
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for ip in soup.find_all('li'):
        if not ip.has_attr("class"):
            proxy_list.append(ip.get_text())
    return proxy_list
    
""" 

def vote(offSet, proxy_list, url, sec_key, option, PROXIES_PER_PROCESS, start):
    while True:
        if start.value:
            for i in range (0,PROXIES_PER_PROCESS):
                proxy = {"https": proxy_list[offSet+i]}
                try:
                    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}# "Cookie": "__cfduid=d08c23f1413f38ee7bc613ebd74d225d41469427686; Permanent.CookieTest=1; Auth.NetworkSession=G9RJ0DCDGDGUIT87CPBYT6K7ABXN4UFS6PXHI0H5IDNX5GIM; _ceg.s=oazwib; _ceg.u=oazwib; _ga=GA1.2.991147065.1469427691;"};
                    #headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/" + str(i) + ".0"}# "Cookie": "__cfduid=d08c23f1413f38ee7bc613ebd74d225d41469427686; Permanent.CookieTest=1; Auth.NetworkSession=G9RJ0DCDGDGUIT87CPBYT6K7ABXN4UFS6PXHI0H5IDNX5GIM; _ceg.s=oazwib; _ceg.u=oazwib; _ga=GA1.2.991147065.1469427691;"};

                    # data = {'security-token':bytes.decode(sec_key.value),bytes.decode(auth_key.value):"", 'options':option.value}
                    data = {'security-token':bytes.decode(sec_key.value), 'options':option.value}
                    r = requests.post(url.value, data, headers, proxies=proxy, timeout = randint(4,6))
                    if r.text.find('"success":"success"') != -1:
                        print(r.text[:100])
                    elif r.text.find('"success":"failed"') != -1:
                        #print("already voted?")
                        print(r.text[:200])
                    else: 
                        print("cloudflare error?:") 
                        #print(r.text[:200])                        
                except requests.exceptions.Timeout:
                    pass
                    print ("  Timeout error for %s" % proxy["https"])
                except requests.exceptions.ConnectionError:
                    pass
                    print ("  Connection error for %s" % proxy["https"])
                except:
                    pass
                    print(" Proxy error " + proxy["https"])
            break
        else:
            time.sleep(1)
            #print("data = " + bytes.decode(data.value))
           # print("url = " + str(url.value))
    
if __name__ == "__main__":
    
    from multiprocessing import Process, Value, Array
    from ctypes import create_string_buffer
    from subprocess import call
    from msvcrt import getch, kbhit
    
    start = Value('i', 0)
    sec_key = Array('c', 64)
    # auth_key = Array('c', 64)
    url = Array('c', 64)
    option = Value('i', 0)
    proxy_list = read_from_file()
    amount = len(proxy_list)
    print("found " + str(amount) + " proxies")
    """ if amount < 3500:
        proxy_list = get_old_proxies()
        amount = len(proxy_list)
        print("reading old proxies")
        print("found " + str(amount) + " proxies")

    if amount < 3500:
        proxy_list = read_from_file()
        amount = len(proxy_list)
        print("read from file")
       """ 
    print(str(amount) + " proxies loaded.")
    time.sleep(1)
  
    PROXIES_PER_PROCESS = int(math.sqrt(amount))
    NumOfProcs = amount / PROXIES_PER_PROCESS
    
    procs = 0
    n = 0.01  
    
    for i in range (0,int(NumOfProcs)):
        # process = Process(target=vote, kwargs={"offSet": i*PROXIES_PER_PROCESS,"proxy_list":proxy_list,"url":url,"sec_key":sec_key,"auth_key":auth_key,"option":option,"PROXIES_PER_PROCESS":PROXIES_PER_PROCESS,"start":start})
        process = Process(target=vote, kwargs={"offSet": i*PROXIES_PER_PROCESS,"proxy_list":proxy_list,"url":url,"sec_key":sec_key,"option":option,"PROXIES_PER_PROCESS":PROXIES_PER_PROCESS,"start":start})
        #print('process ' + str(i+1) + ' created')
        time.sleep(randint(1, 3) * n)
        process.daemon = True
        process.start()
        call('cls', shell=True)
        procs += 1
        print(str(procs) + " / " + str(int(NumOfProcs)) + " procs started")
        print("press ENTER to start voting")
        if kbhit():
            key = ord(getch())
            if key == 13: #ENTER
                break
            else:
                continue
    
    id = input("Strawpoll ID: ")
    while int(id) < 0 or int(id) > 99999999:
        print("Invalid Strawpoll ID")
    #else:
    URL = "https://www.strawpoll.me/" + str(id)
    options = 0
    voteIds = []
    option_names = []
    
    req = requests.get(URL)
    soup = BeautifulSoup(req.text, 'html.parser')
    security_token = soup.find(id="field-security-token").get("value")
    # auth_token = soup.find(id="field-authenticity-token").get("name")

    for line in soup.find(id="field-options"):
        if line != '\n':
            voteIds.append(line.find("input")['value'])
            option_names.append(line.find("label").get_text())
            options += 1
        
    i=1
    for name in option_names:
        print (str(i) + ") " + str(name))
        i+=1
    
    choice = input('Select an option: ')

    if int(choice) < 0 or int(choice) > len(voteIds):
        print("Invalid option")
    else:
        #s = requests.Session() 
        url.value = str.encode(URL)
        #data.value = str.encode("security-token=" + security_token + "&" + auth_token + "=&options=" + voteIds[int(option)-1])
        sec_key.value = str.encode(security_token)
        # auth_key.value = str.encode(auth_token)
        option.value = int(voteIds[int(choice)-1])
        start.value = 1
        print("job started")
        
        for i in range (0, int(NumOfProcs)):
            if i < procs: 
                continue
            # process = Process(target=vote, kwargs={"offSet": i*PROXIES_PER_PROCESS,"proxy_list":proxy_list,"url":url,"sec_key":sec_key,"auth_key":auth_key,"option":option,"PROXIES_PER_PROCESS":PROXIES_PER_PROCESS,"start":start})
            process = Process(target=vote, kwargs={"offSet": i*PROXIES_PER_PROCESS,"proxy_list":proxy_list,"url":url,"sec_key":sec_key,"option":option,"PROXIES_PER_PROCESS":PROXIES_PER_PROCESS,"start":start})
            time.sleep(randint(1, 3) * n)
            process.daemon = True
            process.start()
            print(str(procs) + " / " + str(int(NumOfProcs)) + " procs started")
            procs += 1
            
        print ("Finished. " + str(procs) + " processes are sleeping")

        while True:
            time.sleep(1)
        
    