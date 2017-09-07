'''
Author: Salil Shenoy
'''

import argparse
import datetime as dt
from datetime import timedelta
import sys
import numpy as np
import csv

'''
A class which calculates the mean and variance according to the command line arguments.
'''
class AnalyzeData(object):

    def __init__(self, args):
        self.data_file = 'investing_data.csv'
        self.price_list = list()

        try:
            self.start_date = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
            self.end_date = dt.datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

        if self.start_date > dt.datetime.today() or \
            self.end_date > dt.datetime.today() or \
            self.start_date > self.end_date:
            print ('Either Start or End Date is Incorrect')
            sys.exit()

        self.commodity = args.commodity
        self.date_range = list()
        self.calculate_date_range()

    '''
    Calculate the list of dates which lie between start and end date
    '''
    def calculate_date_range(self):

        def date_range(date1, date2):
            for n in range(int((date2 - date1).days) + 1):
                yield date1 + timedelta(n)

        for dt in date_range(self.start_date, self.end_date):
            self.date_range.append(dt.strftime("%b %d, %Y"))

        self.date_range = sorted(self.date_range, reverse=True)

    '''
    Read the data from the File createdby Scrapper.py. (investing_data.csv for this exercise)
    '''
    def read_data(self):
        i = 0
        with open(self.data_file) as f:
            #fieldnames = ['current_price', 'date', 'commodity'] for reference
            data = csv.DictReader(f)
            for line in data:
                com = line['commodity']
                if self.commodity == com:
                    cp = line['current_price']
                    # In case the float value has a , we remove it here
                    cp = "".join(cp.split(','))
                    dt_str = line['date']

                    if self.date_range[i] == dt_str:
                        self.price_list.append(cp)
                        i += 1
                        if i == len(self.date_range):
                            break

    '''
    Calculate the mean and variance using Numpy functions
    '''
    def process_data(self):
        if len(self.price_list) > 0:
            price_array = np.array(self.price_list).astype(np.float)
            print (self.commodity, np.mean(price_array, dtype=np.float64), np.var(price_array, dtype=np.float64))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("start_date", help="format: 2017-05-10", type=str)
    parser.add_argument("end_date", help="format: 2017-05-10", type=str)
    parser.add_argument("commodity", help="gold / silver", type=str)
    args = parser.parse_args()
    analyzeData = AnalyzeData(args)
    analyzeData.read_data()
    analyzeData.process_data()


'''
python data_analyser.py --help
'''