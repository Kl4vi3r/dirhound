#   MATTHEW HUANG TP058937
#   APD3F2211CS(CYB)


import concurrent.futures
import requests
import sys
import threading
import time

from core.data import options
from core.opt import _extension_check
from requests.adapters import HTTPAdapter
from style.format import FORMATTING
from style.format import OUTPUT
from style.style import *
from urllib3.util.retry import Retry


class Scanner():
    def rate_limit(limit_rate, limit_interval):
        def decorator(func):
            rate_lock = threading.Lock()
            rate_count = 0
            timer = None

            def wrapper(*args, **kwargs):
                nonlocal rate_count, timer

                # Acquire the lock to ensure thread safety
                with rate_lock:
                    # If the limit rate is 0, allow the request to proceed without rate limiting
                    if limit_rate > 0:
                        # If the rate count exceeds the limit rate, pause execution
                        while rate_count >= limit_rate:
                            time.sleep(0.1)

                        # Execute the function and update the rate count
                        result = func(*args, **kwargs)
                        rate_count += 1

                        # If the timer is active, cancel it to avoid scheduling unnecessary decrements
                        if timer is not None and timer.is_alive():
                            timer.cancel()

                        # Schedule a decrement of the rate count after the limit interval
                        timer = threading.Timer(limit_interval, decrease_rate)
                        timer.start()
                    else:
                        # If the limit rate is 0, execute the function without rate limiting
                        result = func(*args, **kwargs)

                return result

            def decrease_rate():
                nonlocal rate_count
                rate_count -= 1

            return wrapper

        return decorator
    

    @rate_limit(options["max_rate"], 1)
    def _requests(url, method="GET", headers=None, redirects=False, timeout=0.0, retries=3):

        session = requests.Session()
        retry = Retry(total=retries, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        http_method = {
            'GET': session.get,
            'POST': session.post,
            'PUT': session.put,
            'PATCH': session.patch,
            'DELETE': session.delete
        }

        response = http_method[method.upper()](url, headers=headers, allow_redirects=redirects, timeout=timeout)
        return response

    def threads():
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=options["threads"]) as executor:
                futures = {executor.submit(Scanner.scan, word): word for word in options["_wordlist"]}
                    
                time.sleep(options["delay"])

                # Wait for all futures to complete
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
        
    def scan(word=""):
        header = {
            "User-Agent":f"{options['user_agent']}"
            "Cookie:"f"{options['cookie']}"
        }
        
        if word != "":
            if options["url"].endswith("/"):
                request_url = f'{options["url"]}{word}'
            else:
                request_url = f'{options["url"]}/{word}'

            try:
                res = Scanner._requests(request_url, options["method"], header, options["allow_redirect"], options["timeout"])
                Output.response_code(res)
            except requests.exceptions.Timeout:
                pass

    def run():
        options["_wordlist"] = _extension_check(options)

        if options["output"] != None:
            if ".html" not in options["output"] :
                time_start = f"{FORMATTING.date_format()} {FORMATTING.time_format()}"  
                Output.initialize(time_start)
            else:
                Output.initialize(FORMATTING.date_format())


        DETAILS.scan_target()
        print(FORE["magenta"] + STYLE["bright"] + f'[{FORMATTING.time_format()}]  Starting scan ...\n')
        Scanner.threads()

        print(FORE["magenta"] + STYLE["bright"] + '\nScan has finished ...')


class Output():
    def response_code(response):
        msg= ""
        content_length = len(response.content)
        url = response.url
        url = url.replace(options["url"], '')
        content_length = round(FORMATTING.bytesToKB(content_length))
        if response.status_code in range(200, 300) and response.status_code in options["include_code"]:
            msg += SIGNS["success"] + f'[{FORMATTING.time_format()}]  ||  [{response.status_code:3}] - [{content_length:>4}KB] -> {url}'
            if options["output"] != None: 
                OUTPUT.run(url, response.status_code, content_length)
        if response.status_code in range(300, 400) and response.status_code in options["include_code"]:
            msg += SIGNS["redirects"] + f'[{FORMATTING.time_format()}]  ||  [{response.status_code:3}] - [{content_length:>4}KB] -> {url}'
            if options["output"] != None: 
                OUTPUT.run(url, response.status_code, content_length)
        if response.status_code in range(400, 500) and response.status_code in options["include_code"]:
            msg += SIGNS["client_error"] + f'[{FORMATTING.time_format()}]  ||  [{response.status_code:3}] - [{content_length:>4}KB] -> {url}'
            if options["output"] != None: 
                OUTPUT.run(url, response.status_code, content_length)
        if response.status_code >= 500 and response.status_code in options["include_code"]:
            msg += SIGNS["server_error"] + f'[{FORMATTING.time_format()}]  ||  [{response.status_code:3}] - [{content_length:>4}KB] -> {url}'
            if options["output"] != None: 
                OUTPUT.run(url, response.status_code, content_length)

        
        if msg == "": pass
        else: 
            print(msg)


    def initialize(time):
        OUTPUT.validate_file_output()
        OUTPUT.initialize(time)
