from datetime import datetime
import csv
import matplotlib.pyplot as plt

class Quote:
    def __init__(self, timestamp=None, open=None, close=None, dividend=None, splitCoefficient=None):
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
        self.open = float(open)
        self.close = float(close)
        self.dividend = float(dividend)
        self.splitCoefficient = float(splitCoefficient)
    
    def __str__(self):
        return "%s\t%s\t%s" % (self.timestamp.strftime("%Y-%m-%d"), self.open, self.close)

    @staticmethod
    def parseCSV(filePath):
        with open(filePath, 'r') as csvfile:
            #print("Opening file: " + filePath)
            reader = csv.DictReader(csvfile)
            quotes = []
            for row in reader:
                #print row['timestamp']+" "+row['close']
                quotes.append(Quote(row['timestamp'], row['open'], row['close'], row['dividend_amount'], row['split_coefficient']))
        return quotes

    @staticmethod
    def sort(quotes, reverse=False):
        quotes.sort(key=lambda x: x.timestamp, reverse=reverse) #Sorting
    
    @staticmethod
    def adjustSplits(quotes):
        # Rebasing stock prices with splits
        # TODO: Should handle reverse split
        indx = 0
        indx2 = 0
        while indx < len(quotes):
            if quotes[indx].splitCoefficient != 1.0:
                indx2 = indx
                while indx2 < len(quotes):
                    quotes[indx2].open *= quotes[indx].splitCoefficient
                    quotes[indx2].close *= quotes[indx].splitCoefficient
                    indx2 += 1
            indx += 1

    @staticmethod
    def fullCSVParse(filePath):
        with open(filePath, 'r') as csvfile:
            #print("Opening file: " + filePath)
            reader = csv.DictReader(csvfile)
            quotes = []
            for row in reader:
                #print row['timestamp']+" "+row['close']
                quotes.append(Quote(row['timestamp'], row['open'], row['close'], row['dividend_amount'], row['split_coefficient']))

        Quote.sort(quotes, False)
        Quote.adjustSplits(quotes)
        return quotes

    @staticmethod
    def plotQuotes(config, quotes, show=True, figureNumber=1):
        # print("Config: " + str(config))
        times = list(map(lambda q: q.timestamp, quotes))
        opens = list(map(lambda q: q.open, quotes))
        closes = list(map(lambda q: q.close, quotes))

        plt.figure(figureNumber)

        if config['plotOpen']:
            plt.plot(times, opens, 'g-', label='Open')

        if config['plotClose']:
            plt.plot(times, closes, 'b-', label='Close')       


        if config['dividendMarker']:
            #Search dates with dividends
            dividendsDates = []
            for q in quotes:
                if float(q.dividend) > 0.0:
                    dividendsDates.append(q.timestamp)
            for dD in dividendsDates:
                plt.axvline(x=dD, c='r')
            
            print("Dividend dates: " + str(dividendsDates))
        
        if show:
            plt.show()

    @staticmethod
    def plotMultipleQuotes(config, *quotesSet):
        i = 1
        for q in quotesSet:
            Quote.plotQuotes(config, q, False, i) #False = doesn't call show
            i = i + 1
        plt.show()
        
