import sys  

from pkg_resources import DistributionNotFound, VersionConflict

from core.conf import ConfigParser
from core.data import options
from core.dependencies import *
from core.dns import DNS_Scanner
from core.opt import _options
from core.scanner import Scanner

#test
if sys.version_info < (3, 10):
    sys.stdout.write("Sorry, Dirhound requires Python 3.10 or higher\n")
    sys.exit(1)


def main():   
    config = ConfigParser()
    config.read("dependencies.ini")

    if config.get_boolean("DEPENDENCIES", "check-dependencies"):
        try:
            check()
        except (DistributionNotFound, VersionConflict):
            option = input("Missing required dependencies to run.\n"
                        "Do you want to automatically install them? [Y/n] ")
        
            if option.lower() == "y":
                print("Installing dependencies ...")

                try:
                    install()
                except:
                    print("Failed to install dependencies, try doing it manually.")
                    sys.exit(1)

            else:
                config.set("DEPENDENCIES", "check-dependencies", "False")

                with open("/requirements.txt", "w") as fh:
                    config.write(fh)


    options.update(_options())
    print(1)
    if options["mode"] == "dir":
        Scanner.run()  
    elif options["mode"] == "dns":
        DNS_Scanner.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()