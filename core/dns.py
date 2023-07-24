#   MATTHEW HUANG TP058937
#   APD3F2211CS(CYB)

import concurrent.futures
import dns.resolver
import dns.query
import dns.zone
import requests
import sys

from core.data import options
from core.opt import _extension_check
from style.format import FORMATTING
from style.format import OUTPUT_SUBDOMAIN
from style.style import *

class DNS:
    def main(record_type):
        try:
            answers = dns.resolver.resolve(options["domain"], record_type)
            message = (FORE["magenta"] + STYLE["bright"] + f'\n{record_type} Records')
            message += '\n' + '-'*50
            print(message)
            for server in answers:
                message += '\n' + FORE["white"] + STYLE["bright"] + server.to_text()
                print(FORE["white"] + STYLE["bright"] + server.to_text())
    
        except dns.resolver.NXDOMAIN:
            print(FORE["red"] + STYLE["bright"] + f'\n[warn] {options["domain"]} domain does not exist.\n')
            quit()
        except dns.resolver.NoAnswer:
            print(FORE["blue"] + STYLE["bright"] + f'\nNo {record_type} records found.\n')
        except dns.rdatatype.UnknownRdatatype:
            pass
        except dns.resolver.NoNameservers:
            pass
        except dns.resolver.NoAnswer:
            pass
        except Exception:
            pass
    def threads():

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(DNS.main, record_type) for record_type in options["include_records"]]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

class subdomain:
    def main(subdoms):
        try:

            ip_value = dns.resolver.resolve(f'{subdoms}.{options["domain"]}', 'A')

            for ip_addr in ip_value:
                ip = ip_addr.to_text()
                try:
                    # url = f'https://{ip}'
                    # response = requests.get(url)

                    # if response.status_code == 200:
                        message = f'{subdoms}.{options["domain"]}' 
                        print(FORE["green"] + STYLE["bright"] + message + f' -> {ip_addr}')

                        if options["output_sub"] != None:
                            OUTPUT_SUBDOMAIN.run(message, ip_addr)
                except requests.exceptions.RequestException:
                    pass
                    

        except requests.ConnectionError:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NoNameservers:
            pass
        except dns.exception.Timeout:
            pass
        
    def threads():
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                futures = [executor.submit(subdomain.main, subdoms) for subdoms in options["_wordlist_dns"]]

                for future in concurrent.futures.as_completed(futures):
                        try:
                            future.result()
                        except KeyboardInterrupt:
                            print(FORE["white"] + STYLE["dim"] + "\\nCtrl + C detected, cancelling tasks ...")
                            for future in futures:
                                future.cancel()
                            break

        except KeyboardInterrupt:
            print(FORE["white"] + STYLE["dim"] + "\\nCtrl + C detected, exiting the program ...")
            sys.exit(0)

            # concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

            # for future in futures:
            #     future.cancel()

            # # Shutdown the executor
            # executor.shutdown()

            # # for future in concurrent.futures.as_completed(futures):
            # #     future.result()

class DNS_Scanner:
    def run():
        options["_wordlist_dns"] = _extension_check(options)

        print(options["_wordlist_dns"])

        if options["output_sub"] != None:
            if ".html" not in options["output_sub"] :
                time_start = f"{FORMATTING.date_format()} {FORMATTING.time_format()}"  
                OUTPUT_SUBDOMAIN.validate_file_output()
                OUTPUT_SUBDOMAIN.initialize(time_start)
            else:
                OUTPUT_SUBDOMAIN.validate_file_output()
                OUTPUT_SUBDOMAIN.initialize(FORMATTING.date_format())

        DETAILS.scan_dns_target()

        if options["dns"] == True:
            print(FORE["magenta"] + STYLE["bright"] + f'[{FORMATTING.time_format()}]    Starting DNS enumeration...')
            DNS.threads()

            print(FORE["magenta"] + STYLE["bright"] + '\nScan has finished ...')


        elif options["subdomain"] == True:
            print(FORE["magenta"] + STYLE["bright"] + f'[{FORMATTING.time_format()}]    Starting subdomain enumeration...\n')
            subdomain.threads()

            print(FORE["magenta"] + STYLE["bright"] + '\nScan has finished ...')


        elif options["complete"] == True:
            print(FORE["magenta"] + STYLE["bright"] + f'[{FORMATTING.time_format()}]    Starting DNS enumeration...')
            DNS.threads()
            print("\n")

            print(FORE["magenta"] + STYLE["bright"] + f'[{FORMATTING.time_format()}]    Starting subdomain enumeration...\n')
            print(1)
            subdomain.threads()

            print(FORE["magenta"] + STYLE["bright"] + '\nScan has finished ...')


