from Quote import Quote
from Analyzer import Analyzer

MSFTQuotes = Quote.fullCSVParse("./data/daily_adjusted_MSFT.csv")
VZQuotes = Quote.fullCSVParse("./data/daily_adjusted_VZ.csv")

config = {
    "dividendMarker": True,
    "plotOpen": True,
    "plotClose": True
}

# Quote.plotQuotes(config, MSFTQuotes)
# Quote.plotMultipleQuotes(config, MSFTQuotes, VZQuotes)


config2 = {
    "daysBefore": 4,
    "daysAfter": 4,
    "dividendsNumber": 8
}

Quote.plotDividendDates(config2, MSFTQuotes)

# ToDo: Plot recovery days in istogram chart and calculate mean and standard deviation (of all the stocks not just one)