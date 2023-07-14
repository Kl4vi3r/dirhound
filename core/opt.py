import dns.resolver
import os
import requests
import re
import socket
import sys
import validators

from core.conf import ConfigParser
from fake_useragent import UserAgent
from style.args import parse_args
from style.style import *


def _args_parse_dir(args):
    config = ConfigParser()
    config.read("config.ini")

    args.threads = args.threads or config.get_int("GENERAL", "threads")

    args.include_code = args.include_code or config.get_string("REQUEST", "include-status")

    args.exclude_code = args.exclude_code or config.get_string("REQUEST", "exclude-status")

    args.method = (args.method or config.get_string("REQUEST", "http-method")).upper()
    
    args.retries = args.retries or config.get_int("CONNECTION", "max-retries")

    ua = UserAgent()
    user_agent = ua.random
    args.user_agent = args.user_agent or user_agent

    args.cookie = args.cookie

    args.timeout = args.timeout or config.get_float("CONNECTION", "timeout")

    args.max_rate = args.max_rate or config.get_int("CONNECTION", "max-rate")

    args.delay = args.delay or config.get_int("CONNECTION", "delay")

    args.allow_redirect = args.allow_redirect or config.get_boolean("CONNECTION", "allow-redirect")


    #Wordlist
    args.wordlist = args.wordlist or config.get_string("DICTIONARY", "default-path")

    args.extensions = args.extensions or config.get_string("DICTIONARY", "default-extensions")

    args.exclude_extensions = args.exclude_extensions

    args.remove_extensions = args.remove_extensions or config.get_string("DICTIONARY", "remove-extension")

    args.lowercase = args.lowercase or config.get_boolean("DICTIONARY", "lowercase")

    args.uppercase = args.uppercase or config.get_boolean("DICTIONARY", "uppercase")

    args.capitalization = args.capitalization or config.get_boolean("DICTIONARY", "capitalization")
    
    args.output = args.output

    return args

def _args_parse_dns(args):
    config = ConfigParser()
    config.read("config.ini")

    args.domain = args.domain

    args.dns = args.dns or config.get_boolean("DNS", "dns")
    
    args.subdomain = args.subdomain or config.get_boolean("DNS", "subdomain")

    args.complete = args.complete or config.get_boolean("DNS", "complete")

    args.default_path = config.get_string("DNS", "dns-default-record")

    args.include_records = args.include_records 

    args.exclude_records = args.exclude_records

    args.wordlist_dns = args.wordlist_dns or config.get_string("DICTIONARY_DNS", "wordlist-default-path")

    args.output_sub = args.output_sub

    return args

def _options():   
    args = parse_args()

    print(1)

    if args.mode == "dir":
        args = _args_parse_dir(args)

        if not args.url:
            print(FORE["red"] + "[warn] Missing target URL (-u <URL>)")
        
        if not validators.url(args.url):
            print(FORE["red"] + "[warn] Invalid URL")
            sys.exit()
        
        try:
            header = {
                "User-Agent":f"{args.user_agent}"
                "Cookie:"f"{args.cookie}"
            }

            res = requests.get(args.url, headers=header)

        except requests.exceptions.TooManyRedirects:
            print(5)
            sys.exit()

        except requests.exceptions.ConnectionError:
            print(6)
            sys.exit()

        except requests.exceptions.RequestException:
            print(7)
            sys.exit()
            
        if args.exclude_extensions != None:
            for exclude in args.exclude_extensions.split(","):
                if exclude not in args.extensions:
                    pass
                else:
                    args.extensions = args.extensions.remove(exclude)

        if not args.wordlist:
            print(FORE["red"] + "[warn] Missing wordlist (-w <WORDLIST>)")
            sys.exit()
        
        _file_check(args.wordlist)

        print(4)


        if not 1 < args.threads < 50:
            print(FORE["red"] + "[warn] thread number must be in range between 1 - 100")
            sys.exit()
        
        args.include_code = _status_code_sets(args.include_code, args.exclude_code)

        http_method = ["get", "head", "patch", "post", "put", "delete"]

        print(3)

        if args.method.lower() not in http_method:
            print(FORE["red"] + f"[warn] http {args.method} method does not exists")
            sys.exit()
            
        print(2)

        return vars(args)



    elif args.mode == "dns":

        args = parse_args()
        args = _args_parse_dns(args)

        try:
            pattern = r"^(?!:\/\/)([a-zA-Z0-9_-]+\.)*[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}$"

            if not re.match(pattern, args.domain):
                print(FORE["red"] + "[warn] unknown domain, try checking again")
                sys.exit()

            args.domain = args.domain

            dns.resolver.resolve(args.domain, 'A')

        except IndexError:
            print(FORE["red"] + "[warn] no domain is entered.")
            sys.exit()

        except dns.resolver.NXDOMAIN:
            print(FORE["red"] + f'\n[warn] {args.domain} domain does not exist.\n')
            sys.exit()

        if not args.wordlist_dns:
            print(FORE["red"] + "[warn] Missing wordlist (-w <WORDLIST>)")
            sys.exit()
        

        _file_check(args.wordlist_dns)


        if args.include_records:
            for rec in args.include_records.split(","):
                if _record_check(args.domain, None, rec):
                    pass
                else:
                    print(FORE["red"] + f"[warn] {rec} record for {args.domain} is not valid, try checking again")
                    sys.exit()
            
        args.include_records = _record_sets(args)

        return vars(args)

def _file_check(path):
    if not os.path.exists(path):
        print(FORE["red"] + f"[warn] {path} doesn't exists")
        sys.exit()

    if not os.path.isfile(path):
        print(FORE["red"] + f"[warn] {path} is not valid")
        sys.exit()

    try:
        with open(path): pass

    except IOError: 
        print(FORE["red"] + f"[warn] {path} can't be read")
        sys.exit()


def _status_code_sets(str_include, str_exclude):
    config = ConfigParser()
    config.read("config.ini")

    sets = set()
    sc = config.get_string("REQUEST", "status-code")

    for default in sc.split(","):
        sets.add(int(default))

    if str_include != None:
        for code in str_include.split(","):
            sets.add(int(code.strip()))

    if str_exclude != None:
        for code in str_exclude.split(","):   
            sets.discard(int(code.strip()))

    return sets

def _record_sets(args):
    sets = set()
    sc = args.default_path

    for default in sc.split(","):
        sets.add(str(default))

    if args.include_records != None:
        for include in args.include_records.split(","):
            if include not in sets:
                sets.add(str(include.strip()))
        
    if args.exclude_records != None:
        for exclude in args.exclude_records.split(","):
            if exclude in sets:
                sets.discard(str(exclude.strip()))

    
    return sets

def _record_check(domain, rec):
    try:
        answers = socket.getaddrinfo(domain, None, rec)
        return len(answers) > 0
    except socket.gaierror:
        return False


def _extension_check(opt):
    list_word = set()

    _ext = r"%ext%"
    regex_ext_pattern = re.compile(_ext, re.IGNORECASE)

    if opt["mode"] == "dir":
        f = open(opt["wordlist"], "r")
    
        for word in f.read().split("\n"):

            word = word.lstrip("/")
            
            if _ext in word.lower():
                if opt["remove_extensions"] == True:
                    word = word.split(".")[0]
                
                for extension in opt["extensions"].split(","):
                    word_with_ext = regex_ext_pattern.sub(extension, word)
                    list_word.add(word_with_ext)

            else:
                list_word.add(word)


        if opt["lowercase"] == True:
            return list(map(list_word.str.lower()))
        
        elif opt["uppercase"] == True:
            return list(map(list_word.str.upper()))
        
        elif opt["capitalization"] == True:
            return list(map(list_word.str.capitalize()))
        
        else:
            return list(list_word)
    
    elif opt["mode"] == "dns":
        f = open(opt["wordlist_dns"], "r")

        for word in f.read().split("\n"):
            list_word.add(word)

        return list(list_word)


    
        












    