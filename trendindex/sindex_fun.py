
""" Created on Jan 2018 @author: Sarbadal.Pal """
import pandas as pd
import numpy as np

def sindex_fun(data, identifier, timecol, measure, wt):
  """ calculates and returns index for evry store """
  data_tmp = data[[identifier, timecol, measure]].copy()
  data_tmp = data_tmp.rename(columns={identifier: 'identifier', timecol: 'timecol', measure: 'measure'})
  data_tmp['timecol'] = pd.to_datetime(data_tmp['timecol'])
  data_tmp['year'] = data_tmp['timecol'].dt.year

  str_df = pd.DataFrame(data_tmp.groupby(['identifier','year'])[['measure']].sum())
  str_df.reset_index(inplace=True)

  measure_avg_yr = pd.DataFrame(str_df.groupby(['year'])[['measure']].mean()).rename(columns={'measure': 'avg_measure'})
  measure_avg_yr.reset_index(inplace=True)
  measure_avg_yr.sort_values(['year'], ascending=[True], inplace=True)
  measure_avg_yr['one'] = 1
  measure_avg_yr['wt'] = measure_avg_yr[['one']].cumsum()
  # measure_avg_yr.reset_index(inplace=True)

  str_df = pd.merge(str_df, measure_avg_yr, how='left', on=['year'], left_index=False, right_index=False, sort=False)

  if wt==False:
    str_df['sIndex'] = str_df['measure']/str_df['avg_measure']
    str_df = pd.DataFrame(str_df.groupby(['identifier'])[['sIndex']].mean())
    str_df.reset_index(inplace=True)

  if wt==True:
    str_df['ind'] = str_df['measure']/str_df['avg_measure']
    grouped = str_df.groupby(['identifier'])
    g_wavg = lambda x: np.average(x['ind'], weights=x['wt'])
    str_df = pd.DataFrame({'sIndex': grouped.apply(g_wavg)})
    str_df.reset_index(inplace=True)

  # str_df = str_df.rename(columns={'identifier': identifier})
  return str_df