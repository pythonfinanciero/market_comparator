# MIT License
#
# Copyright (c) 2022 Gonzalo Castelao Escobar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import sys

from __init__ import __ROOT_FOLDER__
from comparator import comparator_manager

""" **************************************** """
""" **********  PRIVATE FUNCTIONS ********** """
""" **************************************** """

def __register_global_paths():
    # Register paths to allow app run from IDE or Command Line.
    sys.path.append(os.path.dirname("."))
    # Register root folder to allow refer files (configs)
    sys.path.append(__ROOT_FOLDER__)
    print('-> Global paths regstered.')


def __read_arguments():
    parser = argparse.ArgumentParser(description='Market Comparator')
    # Add arguments

    # Symbol 1
    parser.add_argument('-s1','--symbol1', dest='symbol1', help='Enter symbol1', default='SPY')

    # Symbol 2
    parser.add_argument('-s2','--symbol2', dest='symbol2', help='Enter symbol2', default='TLT')

    # From Date
    parser.add_argument('-f','--fromDate', dest='fromDate', help='Enter fromDate for data comparison', default='2012-01-01')

    # To Date
    parser.add_argument('-t','--toDate', dest='toDate', help='Enter toDate for data comparison', default='2022-01-01')

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return all variable values
    return args.symbol1, args.symbol2, args.fromDate, args.toDate

def __main():
    print('-> main - START')
    """ Read arguments """
    symbol1, symbol2, fromDate, toDate = __read_arguments()

    comparator_manager.start_analysis(symbol1, symbol2, fromDate, toDate)
    
    print('-> main - STOP')


""" *************************************** """
""" **********  PUBLIC FUNCTIONS ********** """
""" *************************************** """

if __name__ == '__main__':
    print('-' * 80)
    print('Market Comparator - START')
    print('-' * 80)
    
    __register_global_paths()
    __main()
    
    print('-' * 80)
    print('Market Comparator - STOP')
    print('-' * 80)
