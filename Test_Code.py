import pandas as pd
from trendindex import trndindex_fun as tind

path = r'F:\Python_Modules\TrendIndex_version_1_0_1\Data\sales_data.txt'
sales_df = pd.read_csv(path, sep='\t', header=0, low_memory=False, encoding='latin-1', error_bad_lines=False)


tind_df = tind.trendindex_fun(data=sales_df, identifier='Identifier', timecol='Period', measure='Measure', mano=12, wt=True)
tind_df.head(10)



for i in range(len(tind_df)):
    if i == 0: print('')
    if i == 0: print(tind_df.columns.tolist()[0], '\t', 
                     tind_df.columns.tolist()[1], '\t\t', 
                     tind_df.columns.tolist()[2])
    print(tind_df.loc[tind_df.index==i,:].values[0][0], '\t\t', 
          tind_df.loc[tind_df.index==i,:].values[0][1], '\t', 
          tind_df.loc[tind_df.index==i,:].values[0][2])