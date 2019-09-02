
import ngram_tools as ngram
import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
import seaborn as sns
import utils

utils.clear_csv_folder()



words_to_query  = input('type the words to query as a comma separated list: ')
query = words_to_query.split(',')
query = list(filter(None, query))

for q in range(0,len(query)):
    query[q] = query[q].strip()

start_year     = input('type start year to override default of 1600: ')

if start_year == '':
    start_year = '1600'

arg = ' -noprint '+' -startYear='+start_year

print(query)

#query = ['rave','MDMA','techno','ketamine']
i = 0
all_words = pd.DataFrame()

csv_prefix = './csv/'
csv_suffix = '-eng_2012-'+start_year+'-2008-3-caseSensitive.csv'


# init plot / subplot
fig, axs = plt.subplots(int(len(query)/2)+1,2, constrained_layout = False)
axs = axs.flatten()

for q in query:
    ngram.runQuery(q + arg)
    csv_name = csv_prefix + q.replace(' ','') + csv_suffix
    df = pd.read_csv(csv_name,index_col=0,parse_dates=True)

    df[q] = df[q] *(10 ** utils.order_scalar(max(df[q])))
    all_words[q] = df[q]

    axs[i].plot(df[q], label = q)
    axs[int(len(query))].plot(df[q], label = q)

    df['20Y SMA'] = df[q].rolling(window=20).mean()
    axs[i].plot(df['20Y SMA'], label = q + ' 20Y SMA', linestyle = '-.')

    df['50Y SMA'] = df[q].rolling(window=50).mean()
    axs[i].plot(df['50Y SMA'], label = q + ' 50Y SMA', linestyle = ':')

    df['100Y SMA'] = df[q].rolling(window=100).mean()
    axs[i].plot(df['100Y SMA'], label = q + ' 100Y SMA', linestyle = ':')


    axs[i].set_title(label=q)
    axs[i].legend()

    i += 1

axs[int(len(query))].set_title(label = 'All')
axs[int(len(query))].legend()

corr = all_words.corr()

axs[int(len(query))+1] = sns.heatmap(corr, label = 'Correlation Matrix', annot= True, vmin=-1, vmax=1, center =0, yticklabels=1)
axs[int(len(query))+1].set_xticklabels(query, rotation=45, horizontalalignment='right')
axs[int(len(query))+1].set_yticklabels(query)
axs[int(len(query))+1].set_ylim(len(query) + 0.5, -0.5)
axs[int(len(query))+1].set_title('Correlation Matrix')

fig.suptitle(str(query) + ' usage through time', fontsize = 16)
plt.show()

