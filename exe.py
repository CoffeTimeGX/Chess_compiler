import sys 
import os
from compiler import Compiler
size = os.get_terminal_size()
width = size.columns
if width % 2 == 1:
    left= right = width // 2 - 5
else:
    left = width // 2 - 6
    right = left + 1



if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) == 1:
    print("\n"+left*'=','help page',right*'='+"""
Usage: python exe.py [options] [source file]
Options:
    -h,--help      show this help message
    -s,--start     start the chess game
    -t,--token     show token list
    -p,--pretty    show and output pretty code
        """
    )
    exit(0)
compiler = Compiler()
if "-s" in sys.argv or "--start" in sys.argv:
    compiler.output_start_game = True
    if "-s" in sys.argv:
        sys.argv.remove("-s")
    else:
        sys.argv.remove("--start")
    
elif "-t" in sys.argv or "--token" in sys.argv:
    compiler.output_token = True
    if "-t" in sys.argv:
        sys.argv.remove("-t")
    else:
        sys.argv.remove("--token")

elif "-p" in sys.argv or "--pretty" in sys.argv:
    compiler.output_pretty = True
    if "-p" in sys.argv:
        sys.argv.remove("-p")
    else:
        sys.argv.remove("--pretty")
compiler.compile(sys.argv[-1])

#except IndexError :
#quit("The arguments given don't match the correct structure. Type -h or -help to see the arguments needed and their order.")