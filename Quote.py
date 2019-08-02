from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as md

class Quote:
    def __init__(self, timestamp=None, open=None, close=None, dividend=None, splitCoefficient=None):
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
        self.open = float(open)
        self.close = float(close)
        self.dividend = float(dividend)
        self.splitCoefficient = float(splitCoefficient)
        self.realOpen = self.open
        self.realClose = self.close
    
    def __str__(self):
        return "%s\t%s\t%s" % (self.timestamp.strftime("%Y-%m-%d"), self.open, self.close)

    def printRealQuote(self):
        return "%s\t%s\t%s" % (self.timestamp.strftime("%Y-%m-%d"), self.realOpen, self.realClose)

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
    def findDividendDates(quotes):
        dividendsDates = []
        for q in quotes:
            if float(q.dividend) > 0.0:
                dividendsDates.append(q.timestamp)
        return dividendsDates


    @staticmethod
    def plotQuotes(config, quotes, show=True, figureNumber=1):
        # print("Config: " + str(config))
        times = list(map(lambda q: q.timestamp, quotes))
        opens = list(map(lambda q: q.open, quotes))
        closes = list(map(lambda q: q.close, quotes))

        plt.figure(figureNumber)

        if config['plotOpen']:
            plt.plot(times, opens, 'g-', label='Open')
            plt.legend(loc='best')

        if config['plotClose']:
            plt.plot(times, closes, 'b-', label='Close')
            plt.legend(loc='best')     


        if config['dividendMarker']:
            dividendsDates = Quote.findDividendDates(quotes) #Search dates with dividends
            for dD in dividendsDates:
                plt.axvline(x=dD, c='r', label='Dividend date')
                plt.legend(loc='best') 

        if 'verticalMarkers' in config:
            for vm in config['verticalMarkers']:
                plt.axvline(x=vm['date'], c=vm['color'], label=vm['label'])
            
            #print("Dividend dates: " + str(dividendsDates))
        
        if show:
            plt.show()


    @staticmethod
    def plotMultipleQuotes(config, *quotesSet):
        i = 1
        for q in quotesSet:
            Quote.plotQuotes(config, q, False, i) #False = doesn't call show
            i = i + 1
        plt.show()



    # config = {
    #     "daysBefore": 2,
    #     "daysAfter": 2,
    #     "dividendsNumber": 4
    # }
    @staticmethod
    def plotDividendDates(config, quotes):
        dividendsDates = Quote.findDividendDates(quotes) #Search dates with dividends
        latestDividendsDates = dividendsDates[-config['dividendsNumber']:]
        print(latestDividendsDates)

        subPlotNumber = 421
        for d in latestDividendsDates: # for each of the latest quote dates
            index = [ q.timestamp for q in quotes ].index(d) # finding the index
            subQuotes = quotes[ index-config['daysBefore'] : index+config['daysAfter']+1 ] # slicing the array

            print("Date of interest: " + str(d))
            #print([q.timestamp for q in subQuotes])
                        
            # ---------- PLOT ----------
            plt.figure(1)

            ax = plt.subplot(subPlotNumber)
            xfmt = md.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_formatter(xfmt)
           

            dates =[q.timestamp for q in subQuotes]
            plt.plot( dates , [q.open for q in subQuotes], 'g-', label='Open' )
            plt.plot( dates , [q.close for q in subQuotes], 'b-', label='Close' )
            plt.axvline(x=quotes[index].timestamp, c='r', label='Dividend date')
            plt.legend(loc='best')
            subPlotNumber = subPlotNumber + 1
            plt.xticks( dates, rotation=35 )

        plt.show()
        
