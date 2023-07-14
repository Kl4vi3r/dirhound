from colorama import init, Fore, Style
from core.data import options

FORE = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "none": "",
}

STYLE = {
    "bright": Style.BRIGHT,
    "dim": Style.DIM,
    "normal": Style.NORMAL,
    "reset": Style.RESET_ALL
}

SIGNS = {
    "success" : STYLE["bright"] + FORE['green'],
    "redirects" : STYLE["bright"] + FORE['cyan'],
    "client_error" : STYLE["bright"] + FORE['blue'],
    "server_error" : STYLE["bright"] + FORE["red"]
}

class BANNER:    
    def banner():
        version = 1.0
        print(FORE["cyan"] + STYLE["bright"])
        print(f'''
       ___      __                          __
  ____/ (_)____/ /_  ____  __  ______  ____/ /
 / __  / / ___/ __ \/ __ \/ / / / __ \/ __  / 
/ /_/ / / /  / / / / /_/ / /_/ / / / / /_/ /  
\__,_/_/_/  /_/ /_/\____/\__,_/_/ /_/\__,_/  v.{version}    

Coded By: Matthew Huang 
Welcome to dirhound []''')
        print("" + STYLE["reset"])
        print("="*79) 
        

class DETAILS:
    def scan_target():
        BANNER.banner()
        print(FORE["magenta"] + STYLE["bright"] + 'Target: ' + FORE["white"]+ STYLE["dim"] + options["url"] + STYLE["reset"] + "\n")

        print(FORE["magenta"] + STYLE["bright"] + 'Wordlist: ' + FORE["white"]+ STYLE["dim"] + options["wordlist"] + STYLE["reset"])
        print(FORE["magenta"] + STYLE["bright"] + 'Extensions: ' + FORE["white"]+ STYLE["dim"] + options["extensions"] + STYLE["reset"])
        print(FORE["magenta"] + STYLE["bright"] + 'Threads: ' + FORE["white"]+ STYLE["dim"] + str(options["threads"])+ FORE["magenta"] + STYLE["bright"] + "  |  HTTP-Method: " + FORE["white"]+ STYLE["dim"] + options["method"] + STYLE["reset"])
        
        if options["output"] != None:
            print(FORE["magenta"] + STYLE["bright"] + '\nOutput Path: ' + FORE["white"] + STYLE["dim"] + options["output"] + STYLE["reset"])
        

        print("\n")

    
    def scan_dns_target():
        BANNER.banner()
        print(FORE["magenta"] + STYLE["bright"] + 'Target: ' + FORE["white"]+ STYLE["dim"] + options["domain"] + STYLE["reset"] + "\n")
        if options["complete"] == True:
            print(FORE["magenta"] + STYLE["bright"] + 'Scan Type: ' + FORE["white"] + STYLE["dim"] + "DNS, Subdomain" + STYLE["reset"])
            print(FORE["magenta"] + STYLE["bright"] + 'Records: ' + FORE["white"]+ STYLE["dim"] + str(options["include_records"]) + STYLE["reset"])

            print(FORE["magenta"] + STYLE["bright"] + '\nWordlist for subdomain: ' + FORE["white"]+ STYLE["dim"] + options["wordlist_dns"] + STYLE["reset"])

            
        if options["dns"] == True:
            print(FORE["magenta"] + STYLE["bright"] + 'Scan Type: ' + FORE["white"] + STYLE["dim"] + "DNS" + STYLE["reset"])
            print(FORE["magenta"] + STYLE["bright"] + 'Records: ' + FORE["white"]+ STYLE["dim"] + f'{options["include_records"]}' + STYLE["reset"])

        if options["subdomain"] == True:
            print(FORE["magenta"] + STYLE["bright"] + 'Scan Type: ' + FORE["white"] + STYLE["dim"] + "Subdomain" + STYLE["reset"])
            print(FORE["magenta"] + STYLE["bright"] + 'Wordlist for subdomain: ' + FORE["white"]+ STYLE["dim"] + options["wordlist_dns"] + STYLE["reset"])
        
        print("\n")

        


init()
