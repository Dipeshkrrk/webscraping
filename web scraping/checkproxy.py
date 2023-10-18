import threading
import queue
import requests
q=queue.Queue()
valid_proxies=[]
with open("temp.txt","r") as f:
    proxies=f.read().split("\n")
    for p in proxies:
        q.put(p)

def checker():
    global q
    while not q.empty():
        proxy=q.get()
        try:
            res = requests.get('http://ipinfo.io/json', proxies={'http': proxy,
                                                           'https': proxy})
        except:
            continue
        if res.status_code==200:
            print(proxy)
for _ in range(20):
    threading.Thread(target=checker).start()