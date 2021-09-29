import config
import function
import csv
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import os
def main():
    pcap_links_list = []
    if os.path.exists("./pcap_links_list.csv"):
        with open("./pcap_links_list.csv","r") as f:
            reader = csv.reader(f)
            for row in reader:
                #print("row:",row)
                pcap_links_list.append(row)
    else:
        with open("./pcap_links_list.csv","w",newline="") as f:
            writer = csv.writer(f)
            for i in range(2013,2022):
                index_url = f"https://www.malware-traffic-analysis.net/{i}/index.html"
                link_list = function.web_links_cothey(index_url)
                for l in link_list:
                    l.append(0)
                pcap_links_list.extend(link_list)
            writer.writerows(pcap_links_list)
    pool = ThreadPoolExecutor(50)
    for i in pcap_links_list:
        #print(i)
        mal_class = i[0]
        href = i[1]
        status = i[2]
        if status == '0':
            config.num -= 1
            if config.num == 0:
                break
            save_path = f"./pcap/{mal_class}"
            pcap_url = function.pcap_href_cothey(href)
            pool.submit(function.thread_download,pcap_url,href,save_path,i)
        else:
            continue
    pool.shutdown(wait=True)
    with open("./pcap_links_list.csv","w",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(pcap_links_list)

if __name__ == '__main__':
    main()

