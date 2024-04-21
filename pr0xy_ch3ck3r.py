class colors:
    # Regular text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bold text colors
    BOLD_BLACK = '\033[30;1m'
    BOLD_RED = '\033[31;1m'
    BOLD_GREEN = '\033[32;1m'
    BOLD_YELLOW = '\033[33;1m'
    BOLD_BLUE = '\033[34;1m'
    BOLD_MAGENTA = '\033[35;1m'
    BOLD_CYAN = '\033[36;1m'
    BOLD_WHITE = '\033[37;1m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # End of color code
    END = '\033[0m'


import requests
import concurrent.futures
import random
import argparse

def usage():
    logo=f"""{colors.BOLD_GREEN}
    ____                           ________              __            
   / __ \_________  _  ____  __   / ____/ /_  ___  _____/ /_____  _____
  / /_/ / ___/ __ \| |/_/ / / /  / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
 / ____/ /  / /_/ />  </ /_/ /  / /___/ / / /  __/ /__/ ,< /  __/ /    
/_/   /_/   \____/_/|_|\__, /   \____/_/ /_/\___/\___/_/|_|\___/_/     
                      /____/                                           


Developer : Zed G.U.I
Telegram : t.me/ZedGUI
GitHub : https://github.com/ZawRib

Usage : python pr0xy_ch3ck3r.py -pl proxyfile.txt -t 10
Help : python pr0xy_ch3ck3r.py -h
{colors.END}"""
    
    
    print(logo)





def main():
    
    global proxies,thread_count,timeout
    
    parser = argparse.ArgumentParser(description='Proxy Checker')

    parser.add_argument('-pl', '--proxyList', default="Default", help='Proxy Link or ProxyFile to check')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Number of threads for concurrency')
    parser.add_argument('-to', '--timeout', type=int,default=10, help='Setting connection timeout')

    args = parser.parse_args()
    
    usage()

    print("Time Out:", args.timeout)
    print("Threads:", args.threads)
    print("Proxies:", args.proxyList)
    timeout=args.timeout
    thread_count=args.threads
#q    var=['http://','https://','socks4://','socks5://']
    if args.proxyList != "Default":
    	    if '://' in args.proxyList :
    	    	plist = requests.get(args.proxyList)
    	    	if plist.status_code == 200:
    	    		proxies = plist.text.splitlines()

    	    	else:
    	    		print(colors.RED+'Error While Fetching Proxies')
    	    		exit()
    	    else:
    	    	with open(args.proxyList,'r') as plist:
    	    		proxies = plist.read().splitlines()
	
	
    else:
    	response = requests.get('https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt')
    	if response.status_code == 200:
    		proxies = response.text.splitlines()
    	else:
    		print(colors.RED+'Error While Fetching Proxies')
    		exit()


#I Used Multiple Website To Check Proxies Because Requesting One Specific Target May Cause Dos or DDos
websites=['https://google.com','https://github.com','https://findall.xyz','https://knauf.co.th','https://sia.unm.ac.id','https://www.pseb.ac.in/','https://www.amritacademy.in','https://gmtpublicschoolludhiana.com','https://tpsldh.com','https://erp.bvmschools.com']

def check_proxy(proxy, website):
    
    if not '://' in proxy:
    	proxy='http://'+proxy
    
    try:
        response = requests.get(website, proxies={'http': proxy, 'https': proxy,'socks4': proxy,'socks5': proxy}, timeout=timeout)
        if response.ok:
#            return proxy
            return f"{colors.BG_GREEN}Proxy {proxy} is alive {colors.END}"
#            return proxy
        else:
            return f"{colors.RED}Proxy {proxy} WebServer Error{colors.END}"
    except Exception as e:
        return f"{colors.RED}Proxy {proxy} encountered{colors.END}"




main()
#worked proxies
worked=[]

def check_proxies_for_random_website(proxy):
    random_website = random.choice(websites)
    
    return check_proxy(proxy, random_website)

# Set the number of threads for concurrency
num_threads = thread_count  # Adjust as needed

# Check proxies concurrently for randomly chosen websites with increased concurrency

try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit requests for each proxy to check its status for randomly chosen websites
        future_to_proxy = {executor.submit(check_proxies_for_random_website, proxy): proxy for proxy in proxies}
    
    # Iterate over completed futures as they finish
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            result = future.result()
            if 'alive' in result:
            	liveprox=result.split(' ')
            	worked.append(liveprox[1])
            print(result)

except:
	pass
	
finally:
	print('\n\n\nShowing Alive Proxies From Results')
	print('**********************************\n')
	for liveprox in worked:
		print(colors.BG_BLUE+liveprox+colors.END)
	print('\n\n')


