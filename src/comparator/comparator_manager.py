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

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime

from __init__ import __ROOT_FOLDER__
from util import create_folder, create_file

""" *************************************** """
""" **********  PUBLIC FUNCTIONS ********** """
""" *************************************** """

def start_analysis(symbol1, symbol2, fromDate, toDate):
    print('-> start_analysis - START')

    data = __download_data(symbol1, symbol2, fromDate, toDate)

    if not data.empty:

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_folder_name = __ROOT_FOLDER__ + '/../results/analysis_' + timestamp
        create_folder(output_folder_name)
        
        __process_prices_evolution(symbol1, symbol2, data, output_folder_name, timestamp, fromDate, toDate)

    print('-> start_analysis - STOP')


""" **************************************** """
""" **********  PRIVATE FUNCTIONS ********** """
""" **************************************** """

def __download_data(symbol1, symbol2, fromDate, toDate):
    print('---- Downloading data...')

    start = pd.Timestamp (fromDate)
    end = pd.Timestamp (toDate)

    data = pd.DataFrame()
    try:
        symbols = [symbol1, symbol2]
        for sym in symbols:
            data[sym] = web.DataReader(sym,'yahoo', start, end)['Adj Close']

        print('---- Data has been downloaded. Record(s): ' + str(data.size))

    except Exception as error:
        print('*** ERROR downloading data: ' + str(error))
        data = pd.DataFrame()

    return data


def __process_prices_evolution(symbol1, symbol2, data, output_folder_name, timestamp, fromDate, toDate):
    print('---- Analyzing "Prices evolution"...')
    ##
    # Analysis configuration
    ##
    text_file_data = 'ANALYSIS CONFIGURATION' + "\n\n" + \
        'timestamp: ' + timestamp + "\n" + \
        'symbol1: ' + symbol1 + "\n" + \
        'symbol2: ' + symbol2 + "\n" + \
        'fromDate: ' + fromDate + "\n" + \
        'toDate: ' + toDate
    ## Save results to file
    output_file_name = output_folder_name + '/01-analysis_configuration_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)
    print('*' * 40)
    print(text_file_data)
    print('*' * 40)

    ##
    # Yearly representation
    ##
    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    graph = (data / data.iloc[0] * 100).plot()
    plt.title('Prices normalized evolution')
    plt.ylabel('Prices')
    plt.legend([symbol1, symbol2], loc='upper left')
    plt.savefig(
        output_folder_name + '/02-yearly_prices_normalized_evolution_' + timestamp + '.png')
    plt.clf()

    ##
    # Monthly representation
    ##
    monthlyData = data.resample('BM').last()

    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    graph = monthlyData.plot()
    plt.title('Monthly Prices evolution (non-normalized)')
    plt.ylabel('Prices')
    plt.legend([symbol1, symbol2], loc='upper left')
    plt.savefig(
        output_folder_name + '/03-monthly_prices_non_normalized_evolution_' + timestamp + '.png')
    plt.clf()

    log_data = np.log(monthlyData) - np.log(monthlyData.shift(1))
    log_data = log_data.dropna()

    __process_monthly_performance(log_data, output_folder_name, timestamp)

    __process_correlations(log_data, symbol1, symbol2, output_folder_name, timestamp, fromDate, toDate)


def __process_monthly_performance(log_data, output_folder_name, timestamp):
    print('---- Analyzing "Montly performance"...')
    ##
    ## Performance
    ##
    text_file_data = str(log_data.describe())
    ## Save results to file
    output_file_name = output_folder_name + '/04-monthly_performance_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)

    ##
    # Positive months count
    ##
    posMonths = (log_data >= 0).sum()
    text_file_data = str(posMonths)
    ## Save results to file
    output_file_name = output_folder_name + '/05-monthly_positive_performance_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)
    
    ##
    # Negative months count
    ##
    negMonths = (log_data < 0).sum()
    text_file_data = str(negMonths)
    ## Save results to file
    output_file_name = output_folder_name + '/06-monthly_negative_performance_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)
    
    print('---- "Montly performance" analysis has finished.')


def __process_correlations(log_data, symbol1, symbol2, output_folder_name, timestamp, fromDate, toDate):
    print('---- Analyzing "Correlations"...')

    ##
    # Correlations
    ##
    text_file_data = str(log_data.corr())
    ## Save results to file
    output_file_name = output_folder_name + '/07-correlations_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)

    ##
    # Histogram
    ##
    symbol1_data = log_data.eval(symbol1)
    symbol2_data = log_data.eval(symbol2)

    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    plt.title('Histogram')
    plt.hist(symbol1_data, bins=50,alpha=0.5, label=symbol1)
    plt.hist(symbol2_data, bins=50, alpha=0.5, label=symbol2)
    plt.legend([symbol1, symbol2], loc='upper left')
    #plt.ylim([0, 16])
    plt.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    plt.savefig(
        output_folder_name + '/08-histogram_' + timestamp + '.png')
    plt.clf()

    ##
    # Cummulated Histogram
    ##
    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()
    ax.hist(symbol1_data, bins=50, histtype='step', cumulative=True, density=True, label=symbol1)
    ax.hist(symbol2_data, bins=50, histtype='step', cumulative=True,density=True, label=symbol2)
    plt.legend([symbol1, symbol2], loc='upper left')
    ax.set_title('Cummulated Histogram')
    ax.set_xlabel('Performance')
    ax.set_ylabel('Probability')
    plt.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    plt.savefig(
        output_folder_name + '/09-cummulated_histogram_' + timestamp + '.png')
    plt.clf()

    ##
    # Correlation returns
    ##
    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    plt.scatter(symbol1_data, symbol2_data)
    plt.xlabel(symbol1 + ' returns')
    plt.ylabel(symbol2 + ' returns')
    plt.savefig(
        output_folder_name + '/10-returns_' + timestamp + '.png')
    plt.clf()

    ##
    # Rolling correlation
    ##
    start = pd.Timestamp(fromDate)
    end = pd.Timestamp(toDate)
    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    graph = symbol1_data.rolling(12).corr(symbol2_data).plot()
    plt.hlines(0, start, end, color='r')
    plt.ylabel('Correlation');
    plt.savefig(
        output_folder_name + '/11-rolling_correlation_' + timestamp + '.png')
    plt.clf()

    ##
    # Monthly frequency
    ##
    text_file_data = \
        '# months ' + symbol2 + ' >=0 and ' + symbol1 + ' >= 0 is: ' + str(len(log_data[(symbol2_data >= 0) & (symbol1_data >= 0)])) + "\n" + \
        '# months ' + symbol2 + ' < 0 and ' + symbol1 + ' < 0 is: ' + str(len(log_data[(symbol2_data < 0) & (symbol1_data < 0)]))  + "\n" + \
        '# months ' + symbol2 + ' >= 0 and ' + symbol1 + ' < 0 is: ' + str(len(log_data[(symbol2_data >= 0) & (symbol1_data < 0)]))  + "\n" + \
        '# months ' + symbol2 + ' < 0 and ' + symbol1 + ' >= 0 is: ' + str(len(log_data[(symbol2_data < 0) & (symbol1_data >= 0)]))
    ## Save results to file
    output_file_name = output_folder_name + '/12-monthly_frequency_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)

    ##
    # Correlations details
    ##
    symbol1_when_negative_symbol2 = log_data[symbol2_data < 0]
    symbol1_when_positive_symbol2 = log_data[symbol2_data >= 0]

    symbol2_when_negative_symbol1 = log_data[symbol1_data < 0]
    symbol2_when_positive_symbol1 = log_data[symbol1_data >= 0]

    fig, axes = plt.subplots(nrows=2, ncols = 2)

    axes[0,0].plot(symbol2_when_negative_symbol1.eval(symbol2))
    axes[0,0].set_title(symbol2 + ' if ' + symbol1 + ' < 0')
    axes[0,0].hlines(0, start, end, color= 'r')

    axes[1,0].plot(symbol2_when_positive_symbol1.eval(symbol2))
    axes[1,0].set_title(symbol2 + ' if ' + symbol1 + ' >= 0')
    axes[1,0].hlines(0, start, end, color= 'r')

    axes[0,1].plot(symbol1_when_negative_symbol2.eval(symbol1))
    axes[0,1].set_title(symbol1 + ' if ' + symbol2 + ' < 0')
    axes[0,1].hlines(0, start ,end, color= 'r')

    axes[1,1].plot(symbol1_when_positive_symbol2.eval(symbol1))
    axes[1,1].set_title(symbol1 + ' if ' + symbol2 + ' >= 0')
    axes[1,1].hlines(0,start,end, color= 'r')

    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    plt.savefig(
        output_folder_name + '/13-correlation_details_' + timestamp + '.png')
    plt.clf()

    ##
    # Correlations details Histogram
    ##
    fig = plt.figure()

    img1= fig.add_subplot(221)
    plt.hist(symbol2_when_negative_symbol1.eval(symbol2), bins=20, density=True)
    plt.title(symbol2 + ' if ' + symbol1 + ' < 0')
    plt.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    plt.ylim([0, 18])
    plt.xlim([-0.20, 0.20])

    img2 = fig.add_subplot(223)
    plt.hist(symbol2_when_positive_symbol1.eval(symbol2), bins=20, density=True)
    plt.title(symbol2 + ' if ' + symbol1 + ' >= 0')
    plt.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    plt.ylim([0, 18])
    plt.xlim([-0.20, 0.20])

    img3= fig.add_subplot(222)
    plt.hist(symbol1_when_negative_symbol2.eval(symbol1), bins=20, density=True)
    plt.title(symbol1 + ' if ' + symbol2 + ' < 0')
    plt.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    plt.ylim([0, 18])
    plt.xlim([-0.20, 0.20])

    img4 = fig.add_subplot(224)
    plt.hist(symbol1_when_positive_symbol2.eval(symbol1), bins=20, density=True)
    plt.title(symbol1 + ' if ' + symbol2 + ' >= 0')
    plt.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    plt.ylim([0, 18])
    plt.xlim([-0.20, 0.20])

    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    plt.savefig(
        output_folder_name + '/14-correlation_details_histogram_' + timestamp + '.png')
    plt.clf()

    ##
    ## How much symbol1 wins when symbol2 loss
    ##
    ## Table
    text_file_data = str((log_data[(symbol1_data >=0) & (symbol2_data < 0)]).describe())
    text_file_data = text_file_data + '\n\n' + str((log_data[(symbol1_data >=0) &(symbol2_data < 0)]).sum())
    ## Save results to file
    output_file_name = output_folder_name + '/15-symbol1_profit_vs_symbol2_losses_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)

    ## Graph
    symbol1_profit_vs_symbol2_losses = ((log_data[(symbol1_data >= 0) & (symbol2_data < 0)])).cumsum()
    symbol1_profit_vs_symbol2_losses.plot()
    plt.hlines(0,start,end, color= 'r')
    plt.ylabel('Cummulated')
    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    plt.savefig(
        output_folder_name + '/16-symbol1_profit_vs_symbol2_losses_graph_' + timestamp + '.png')
    plt.clf()

    ##
    ## How much symbol2 wins when symbol1 loss
    ##
    ## Table
    text_file_data = str((log_data[(symbol2_data >=0) & (symbol1_data < 0)]).describe())
    text_file_data = text_file_data + '\n\n' + str((log_data[(symbol2_data >=0) &(symbol1_data < 0)]).sum())
    ## Save results to file
    output_file_name = output_folder_name + '/17-symbol2_profit_vs_symbol1_losses_' + timestamp + '.txt'
    create_file(output_file_name, text_file_data)

    ## Graph
    symbol2_profit_vs_symbol1_losses = ((log_data[(symbol2_data >= 0) & (symbol1_data < 0)])).cumsum()
    symbol2_profit_vs_symbol1_losses.plot()
    plt.hlines(0,start,end, color= 'r')
    plt.ylabel('Cummulated')
    plt.rcParams['figure.figsize']= 16,10
    plt.style.use('seaborn-darkgrid')
    plt.savefig(
        output_folder_name + '/18-symbol2_profit_vs_symbol1_losses_graph_' + timestamp + '.png')
    plt.clf()

    print('---- "Correlations" analysis has finished.')
