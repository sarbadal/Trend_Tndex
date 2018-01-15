
""" Created on Jan 2018 @author: Sarbadal.Pal """

# from trendindex import moving_avg as ma
import pandas as pd

def moving_avg_fun(list, N):
  cumsum, moving_avg, time_id = [0], [], []

  for i, x in enumerate(list):
    cumsum.append(cumsum[i] + x)
    if i >= N-1:
      moving_average = (cumsum[i+1] - cumsum[i-N+1])/N
      moving_avg.append(moving_average)
      time_id.append(i-1)
  return [moving_avg, time_id]

def linreg_fun(X, Y):
  """ returns a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized """
  N = len(X)
  Sx = Sy = Sxx = Syy = Sxy = 0.0
  for x, y in zip(X, Y):
    Sx = Sx + x
    Sy = Sy + y
    Sxx = Sxx + x*x
    Syy = Syy + y*y
    Sxy = Sxy + x*y
  det = Sxx * N - Sx * Sx
  return [(Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det]

def trend_fun(data, identifier, timecol, measure, mano):
  """ returns trend for every store """
  data_tmp = data[[identifier, timecol, measure]].copy()
  data_tmp = data_tmp.rename(columns={identifier: 'identifier', timecol: 'timecol', measure: 'measure'})
  data_tmp['timecol'] = pd.to_datetime(data_tmp['timecol'])
  data_tmp['year'] = data_tmp['timecol'].dt.year
  data_tmp['month'] = data_tmp['timecol'].dt.month
  store_list = data_tmp['identifier'].unique().tolist()

  store, trend = [], []
  for str_id in store_list:
    str_df = data_tmp[data_tmp['identifier']==str_id].copy()
    str_df = pd.DataFrame(str_df.groupby(['identifier','year','month'])[['measure']].sum())
    str_df.reset_index(inplace=True)

    ma, t = moving_avg_fun(str_df['measure'].tolist(), mano)
    a, b = linreg_fun(range(len(ma)),ma)

    store.append(str_id)
    trend.append(a)
  return pd.DataFrame({'identifier': store, 'Trend': trend})

def sindex_fun(data, identifier, timecol, measure):
  """ calculates and returns index for evry store """
  data_tmp = data[[identifier, timecol, measure]].copy()
  data_tmp = data_tmp.rename(columns={identifier: 'identifier', timecol: 'timecol', measure: 'measure'})
  data_tmp['timecol'] = pd.to_datetime(data_tmp['timecol'])
  data_tmp['year'] = data_tmp['timecol'].dt.year

  str_df = pd.DataFrame(data_tmp.groupby(['identifier','year'])[['measure']].sum())
  str_df.reset_index(inplace=True)

  measure_avg_yr = pd.DataFrame(str_df.groupby(['year'])[['measure']].mean()).rename(columns={'measure': 'avg_measure'})
  measure_avg_yr.reset_index(inplace=True)

  str_df = pd.merge(str_df, measure_avg_yr, how='left', on=['year'], left_index=False, right_index=False, sort=False)
  str_df['sIndex'] = str_df['measure']/str_df['avg_measure']
  str_df = pd.DataFrame(str_df.groupby(['identifier'])[['sIndex']].mean())
  str_df.reset_index(inplace=True)
  # str_df = str_df.rename(columns={'identifier': identifier})
  return str_df

  def trendindex_fun(data=None, identifier='identifier', timecol='timecol', measure='measure', mano=12):
    """ combines trend and index together and creates the final DataFrame"""
    t = trend_fun(data=data, identifier=identifier, timecol=timecol, measure=measure, mano=mano)
    ind = sindex_fun(data=data, identifier=identifier, timecol=timecol, measure=measure)
    tind_df = pd.merge(t, ind, how='inner', on=['identifier'], left_index=False, right_index=False, sort=False)
    return tind_df