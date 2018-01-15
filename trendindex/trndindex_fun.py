
""" Created on Jan 2018 @author: Sarbadal.Pal """
import pandas as pd
from trendindex import trend_fun as trend_fun
from trendindex import sindex_fun as sindex_fun
from trendindex import error_check as error_check

def trendindex_fun(data=None, identifier='identifier', timecol='timecol', measure='measure', mano=12, wt=False):
  """ combines trend and index together and creates the final DataFrame"""
  final_type, final_msg = error_check.error_check_fun(data=data, identifier=identifier, timecol=timecol, measure=measure, mano=mano, wt=wt)

  if final_type:
    t = trend_fun.trend_fun(data=data, identifier=identifier, timecol=timecol, measure=measure, mano=mano, wt=wt)
    ind = sindex_fun.sindex_fun(data=data, identifier=identifier, timecol=timecol, measure=measure, wt=wt)
    tind_df = pd.merge(t, ind, how='inner', on=['identifier'], left_index=False, right_index=False, sort=False)
    tind_df = tind_df.rename(columns={'identifier': identifier})
    tind_df.reset_index(inplace=True)
    tind_df = tind_df[[identifier,'sIndex','Trend']]
    
    return tind_df

  else:
    print(final_msg)
    return pd.DataFrame({'msg': [final_msg]})
