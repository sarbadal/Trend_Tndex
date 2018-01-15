
""" Created on Jan 2018 @author: Sarbadal.Pal """
from trendindex import ma_fun as ma_fun
from trendindex import linreg_fun as lreg
from trendindex import error_check as error_check
import pandas as pd

def trend_fun(data, identifier, timecol, measure, mano, wt):
  """ returns trend for every store """
  final_type, final_msg = error_check.error_check_fun(data=data, identifier=identifier, timecol=timecol, measure=measure, mano=mano, wt=wt)

  if final_type:
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
      str_df.sort_values(['identifier','year','month'], ascending=[True, True, True], inplace=True)

      ma, t = ma_fun.moving_avg_fun(str_df['measure'].tolist(), mano)
      a, b = lreg.linreg_fun(range(len(ma)),ma)

      store.append(str_id)
      trend.append(a)
    return pd.DataFrame({'identifier': store, 'Trend': trend})