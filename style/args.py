import argparse
import sys

from rich_argparse import RichHelpFormatter

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=RichHelpFormatter, usage="Usage: dirhound.py [mode] [args]")
    subparsers = parser.add_subparsers(dest = "mode")

    dir_parse = subparsers.add_parser("dir", formatter_class=RichHelpFormatter, help="Directory Enumeration Options", usage="Usage: dirhound.py dir [args]")

    # mandatory arguments
    mandatory = dir_parse.add_argument_group('Mandatory Settings')
    mandatory.add_argument(
        '-u',
        '--url',
        action="store",
        metavar='URL',
        help='Target URL',
    )

    #wordlist arguments
    wordlist = dir_parse.add_argument_group("Wordlist Settings")
    wordlist.add_argument(
        "-w",
        "--wordlist",
        action="store",
        help="Files containing wordlist"
    )
    wordlist.add_argument(
        "-e",
        "--extensions",
        action="store",
        help="Extension list (separated by COMMA) (e.g. php,asp,js)"
    )
    wordlist.add_argument(
        "-X",
        "--exclude-extensions",
        action="store",
        dest="exclude_extensions",
        help="Exclude extension list (separated by COMMA)"
    )
    wordlist.add_argument(
        "-rm",
        "--remove-extension",
        action="store_true",
        dest="remove_extensions",
        help="Remove all extension"
    )
    wordlist.add_argument(
        "-L",
        "--lowercase",
        action="store_true",
        help="Lowercase all letters in wordlist"
    )
    wordlist.add_argument(
        "-U",
        "--uppercase",
        action="store_true",
        help="Uppercase all letters in wordlist"
    )
    wordlist.add_argument(
        "-C",
        "--capitalization",
        action="store_true",
        help="Capitalization formatting on wordlist"
    )


    #general arguments
    general = dir_parse.add_argument_group("General Settings")
    general.add_argument(
        "-t",
        "--threads",
        action="store",
        type=int,
        metavar="THREADS",
        help="Number of threads"
    )
    general.add_argument(
        "-i",
        "--include-status",
        action="store",
        dest="include_code",
        help="Include status codes(separated by COMMA) (default: 200,301,302,401,403,404,405,410)"
    )
    general.add_argument(
        "-x",
        "--exclude-status",
        action="store",
        dest="exclude_code",
        help="Exclude status codes (separated by COMMA)"
    )
    general.add_argument(
        "-m",
        "--http-method",
        action="store",
        dest="method",
        help="Set HTTP method (default: GET)"
    )
    general.add_argument(
        "-a",
        "--user-agent",
        action="store",
        dest="user_agent",
        help="Set user-agent on HTTP header"
    )
    general.add_argument(
        "--cookie",
        action="store",
        help="Set cookie on HTTP header"
    )
    general.add_argument(
        "-r",
        "--retries",
        action="store",
        type=int,
        help="Max retries for failed connection (default: 3)"
    )
    general.add_argument(
        "-T",
        "--timeout",
        type=float,
        action="store",
        help="Timeout request URL"
    )
    general.add_argument(
        "-M",
        "--max-rate",
        type=int,
        action="store",
        dest="max_rate",
        help="Max requests to URL per second"
    )
    general.add_argument(
        "-D",
        "--delay",
        action="store",
        type=int,
        help="Delay between each request"
    )
    general.add_argument(
        "--allow-redirect",
        action="store_true",
        dest="allow_redirect",
        help="Allow redirection on request"
    )
    general.add_argument(
        '-o',
        '--output',
        action="store",
        help="Save enumeration scan into file (output could be in txt and html)"
    )

    dns_parse = subparsers.add_parser("dns", formatter_class=RichHelpFormatter, help="DNS and Subdomain Enumeration Options", usage="dirhound.py dns [args]")

    mandatory= dns_parse.add_argument_group('Mandatory Settings')
    mandatory.add_argument(
        '-d',
        '--domain',
        action="store",
        help="Specified domain URL for enumeration"
    )

    general = dns_parse.add_argument_group('General Settings')
    general.add_argument(
        '--dns',
        action="store_true",
        help="Enumerate A, AAAA, CNAME, MX, TXT, NS, SOA, SRV, PTR records by default"
    )
    general.add_argument(
        '-ir',
        '--include-records',
        action="store",
        dest="include_records",
        help="Include DNS records (Separated by COMMA) (e.g A,AAAA,CNAME)"
    )
    general.add_argument(
        '-er',
        '--exclude-records',
        dest='exclude_records',
        action="store",
        help="Exclude DNS records (Separated by COMMA)"
    )
    general.add_argument(
        '-s',
        '--subdomain',
        action="store_true",
        help="Include subdomain enumeration in scan"
    )
    general.add_argument(
        '-C',
        '--complete',
        action="store_true",
        help="Perform complete scan"
    )
    general.add_argument(
        '-w',
        '--wordlist',
        dest='wordlist_dns',
        action='store',
        help='Subdomain enumeration wordlist'
    )
    general.add_argument(
        '-o',
        '--output',
        action="store",
        dest="output_sub",
        help="Save subdomain enumeration scan into file (output could be in txt and html)"
    )

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    return args
