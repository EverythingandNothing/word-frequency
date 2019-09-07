

from pytrends.request import TrendReq
import pandas

pytrends = TrendReq(hl='en-US', tz=360)


kw_list = ["juul"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

test = pytrends.interest_over_time()



#un = 'jwebost@gmail.com'
#pw = 'b33#kn33GMAIL'

#pyGtrends(un,pw)

#test = trends.request_report('juul',hl='en-US')

print(test)