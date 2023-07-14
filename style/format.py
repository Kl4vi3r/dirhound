import datetime
import os
import sys
import time


from core.data import options 
from .style import *

class FORMATTING:
    def bytesToKB(bytes):
        kb = bytes/1024
        return kb

    def time_format():
        current_time = time.strftime("%H:%M:%S")
        return current_time
    
    def date_format():
        return datetime.date.today()


class OUTPUT:

    def validate_file_output():
        if options["output"]:
            path = options["output"] 

        elif options["output_sub"]:
            path = options["output_sub"]

        directory, filename = os.path.split(path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        output_file_path = os.path.join(directory, filename)

        if os.path.exists(output_file_path):
            print(FORE["red"] + STYLE["dim"] + "File exists. Please choose another name." + STYLE["reset"])
            sys.exit()

        else:
            pass

    def output_txt(url_requested, response, length):    
        message = f"[{response}] - [{length}KB] --> {url_requested}"  
        with open(options["output"], 'a+') as f:
            f.write(f"{message}\n")


    def output_html(url_requested, response, length):
        content = ""
        with open(options["output"], "r") as f: 
            content = f.readlines()
        text=f"""

                    <tr>
                        <td>{url_requested}</td>
                        <td>{response}</td>
                        <td>{length}KB</td>
                    </tr>

"""
        idx = len(content) - 6
        content.insert(idx, text)

        with open(options["output"], 'w') as a:
            content = "".join(content)
            a.write(content)
            
        a.close()
        

    def output_header_html():
        if ".html" in options["output"]:
            head=f'''
<html>
	<head>
  		<meta charset="utf-8">
  		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Dirhound Report</title>
		<style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                text-align: left;
                padding: 8px;
            }}
            tr:nth-child(even) {{background-color: #f2f2f2;}}
        </style>
	</head>
	<body>
		<div class="main" style="overflow-x: auto;">
			<h1 class="text-center">Dirhound v1.0 - Web Directories enumeration </h1>
            <h3>Target URL: {options["url"]}</h3>
			<table class="table">
   		 		<head>
      				<tr>
        				<th>URL</th>
        				<th>RESPONSE</th>
                        <th>CONTENT-LENGTH</th>
      				</tr>
    			</thead>
    			<tbody>

    			</tbody>
  			</table>
		</div>
	</body>
</html>'''    
             
            with open(options["output"], 'w') as f:
                f.write(head)


    def initialize(time_start):
        if ".html" not in options["output"]:
            with open(options["output"], 'a+') as f:
                f.write(f"{time_start} \nDIRHOUND Web Directory Scan\n")
                f.write(f"URL: {options['url']}  |  METHOD: {options['method']}\n\n")
        else:
            OUTPUT.output_header_html()

    def run(url, resp, length):
        if ".html" not in options["output"] :
            OUTPUT.output_txt(url, resp, length)
        else:
            OUTPUT.output_html(url, resp, length)


class OUTPUT_SUBDOMAIN:
    def validate_file_output():
        OUTPUT.validate_file_output()

    def output_txt(message, ip_addr):    
        with open(options["output_sub"], 'a+') as f:
            f.write(f"{message} -> {ip_addr}\n")

    def output_header_html():
        if ".html" in options["output_sub"]:
            head=f'''
<html>
	<head>
  		<meta charset="utf-8">
  		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Dirhound Report</title>
		<style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                text-align: left;
                padding: 8px;
            }}
            tr:nth-child(even) {{background-color: #f2f2f2;}}
        </style>
	</head>
	<body>
		<div class="main" style="overflow-x: auto;">
			<h1 class="text-center">Dirhound v1.0 - Subdomain enumeration </h1>
            <h3>Target DOMAIN: {options["domain"]}</h3>
			<table class="table">
   		 		<head>
      				<tr>
        				<th>SUBDOMAIN</th>
        				<th>IP ADDRESS</th>
    			</thead>
    			<tbody>

    			</tbody>
  			</table>
		</div>
	</body>
</html>'''    
             
            with open(options["output_sub"], 'w') as f:
                f.write(head)

    def output_html(message, ip_addr):
        content = ""
        with open(options["output_sub"], "r") as f: 
            content = f.readlines()
        text=f"""
                    <tr>
                        <td>{message}</td>
                        <td>{ip_addr}</td>
                    </tr>
"""
        idx = len(content) - 6
        content.insert(idx, text)

        with open(options["output_sub"], 'w') as a:
            content = "".join(content)
            a.write(content)
            
        a.close()

        
    def initialize(time_start):
        if ".html" not in options["output_sub"]:
            with open(options["output_sub"], 'a+') as f:
                f.write(f"{time_start} \nDIRHOUND Subdomain Scan\n")
                f.write(f"DOMAIN: {options['domain']}\n\n")
        else:
            OUTPUT_SUBDOMAIN.output_header_html()

    def run(message, ip_addr):
        if ".html" not in options["output_sub"] :
            OUTPUT_SUBDOMAIN.output_txt(message, ip_addr)
        else:
            OUTPUT_SUBDOMAIN.output_html(message, ip_addr)