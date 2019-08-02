from Quote import Quote

class Analyzer:
    def __init__(self, quotes: [Quote]):
        self.quotes = quotes

    def printTime(time):
        return str(time.strftime("%Y-%m-%d"))

    @staticmethod
    def analyze(quotes):
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



        totalDividends = 0

        dayBeforeAvg = 0.0
        dayBeforeSum = 0.0

        dayAvg = 0.0
        daySum = 0.0

        dayAfterAvg = 0.0
        dayAfterSum = 0.0

        recoversIn = [0] * 9999 #vector of 9999 zeros

        indx = 1
        while indx+1 < len(quotes)-1:
            if quotes[indx].dividend > 0: #identifies a day with dividend
                quote = quotes[indx]
                pQuote = quotes[indx-1] #previous Quote
                nQuote = quotes[indx+1] #next Quote

                dayBefore = pQuote.close - pQuote.open
                day = quote.close - pQuote.close
                dayAfter = nQuote.close - quote.close

                totalDividends += 1
                dayBeforeSum += dayBefore
                daySum += day
                dayAfterSum += dayAfter

                recoverCounter = 0
                recoverIndx = indx
                while (recoverIndx < len(quotes)) and (quotes[recoverIndx].close <= quotes[indx].close):
                    recoverCounter += 1
                    recoverIndx += 1

                recoversIn[recoverCounter] += 1

                print("%s(%0.2f $) - "
                    "Day before: %0.2f$   "
                    "Day: %0.2f$   "
                    "Day after: %0.2f$   "
                    "Recover after: %d" % (Analyzer.printTime(quote.timestamp), quote.dividend, dayBefore, day, dayAfter, recoverCounter))
            indx += 1

        dayAvg = daySum/totalDividends
        dayBeforeAvg = dayBeforeSum/totalDividends
        dayAfterAvg = dayAfterSum/totalDividends

        print("\n\nDayBeforeAvg: %0.2f   DayAvg: %0.2f   DayAfterAvg: %0.2f" % (dayBeforeAvg, dayAvg, dayAfterAvg))

        print("\nTotal dividends: %d" % (totalDividends))
        i = 0
        cumulativePerc = 0
        while i < len(recoversIn):
            if recoversIn[i] > 0:
                perc = (recoversIn[i]*1.0/totalDividends)*100
                cumulativePerc += perc
                print("%d recovered in %d days (%0.2f%%)[%0.2f%%]" % (recoversIn[i], i, perc, cumulativePerc))
            i += 1


    # ---------- PROCESS ----------
    # 1) Buy on Ex-diffDate
    # 2) It recovers in X days?
    #
    # 2.yes) Look at the slope
    # 2.yes.>30%) Hold and go back to (2.yes)
    # 2.yes.<=30%) Sell and take profit
    #
    # 2.no) Look at the slope
    # 2.no.>0%) Hold and go back to (2.no)
    # 2.no.<=0%) Sell & take loss

    # config = {
    #     "recoverAfter": 10,
    # }
    @staticmethod
    def simulate(config, quotes):
        print("\n---------- SIMULATION ----------\n")
        indx = 0
        verticalMarkers = []
        newQuotes = quotes[-config['nQuotes']:]
        while indx < len(newQuotes):
            if newQuotes[indx].dividend > 0: # Dividend date => buy (at closing price)
                
                buyQuote = newQuotes[indx] # buy (at closing price)
                print("Buying at " + str(buyQuote.close))

                indx2 = indx
                recovered = None
                while indx2 < len(newQuotes): # Let's find when it recovers
                    if newQuotes[indx2].close > buyQuote.close: #Recovered
                        recovered = newQuotes[indx2]
                        break
                    
                    if indx2 - indx > config['recoverAfter']: #Didn't recover in time
                        break

                    indx2 = indx2 + 1

                verticalMarkers.append({"date": buyQuote.timestamp, "color": "y", "label":"Buy"})
                if recovered is None: # Didn't recover
                    print("Didn't recover")
                else:
                    print("Recovered -> " + str(buyQuote) + " " + str(recovered))
                    verticalMarkers.append({"date": recovered.timestamp, "color": "c", "label":"Sell"})
                        
                    

            indx = indx + 1
    

        config = {
        "dividendMarker": True,
        "plotOpen": True,
        "plotClose": True,
        "verticalMarkers": verticalMarkers
        }
        Quote.plotQuotes(config, newQuotes)
