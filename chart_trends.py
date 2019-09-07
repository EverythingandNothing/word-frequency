
import ngram_tools as ngram
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import utils
from pytrends.request import TrendReq

utils.clear_csv_folder()

pytrends = TrendReq(hl='en-US', tz=360)

words_to_query  = input('type the words to query as a comma separated list: ')
query = words_to_query.split(',')
query = list(filter(None, query))

for q in range(0,len(query)):
    query[q] = query[q].strip()


print(query)

pytrends.build_payload(query, cat=0, timeframe='today 5-y', geo='', gprop='')

i = 0
all_words = pd.DataFrame()

csv_prefix = './csv/'


# init plot / subplot
fig, axs = plt.subplots(int(len(query)/2)+1,2, constrained_layout = False)
axs = axs.flatten()

payload = pytrends.interest_over_time()

for q in query:
    axs[i].plot(payload[q], label = q)
    axs[int(len(query))].plot(payload[q], label = q)

    payload['20d SMA'] = payload[q].rolling(window=20).mean()
    axs[i].plot(payload['20d SMA'], label = q + ' 20d SMA', linestyle = '-.')

    payload['50d SMA'] = payload[q].rolling(window=50).mean()
    axs[i].plot(payload['50d SMA'], label = q + ' 50d SMA', linestyle = '-.')

    payload['100d SMA'] = payload[q].rolling(window=100).mean()
    axs[i].plot(payload['100d SMA'], label = q + ' 100d SMA', linestyle = '-.')


    axs[i].set_title(label=q)
    axs[i].legend()

    i += 1

axs[int(len(query))].set_title(label = 'All')
axs[int(len(query))].legend()

corr = payload.corr()

axs[int(len(query))+1] = sns.heatmap(corr, label = 'Correlation Matrix', annot= True, vmin=-1, vmax=1, center =0, yticklabels=1)
axs[int(len(query))+1].set_xticklabels(query, rotation=45, horizontalalignment='right')
axs[int(len(query))+1].set_yticklabels(query)
axs[int(len(query))+1].set_ylim(len(query) + 0.5, -0.5)
axs[int(len(query))+1].set_title('Correlation Matrix')

fig.suptitle(str(query) + ' usage through time', fontsize = 16)
plt.show()

