""" This .py file is required here. """

import pandas as pd

def error_check_fun(data, identifier, timecol, measure, mano, wt):

  # check if the Data Exist or not......
  len_msg = ''
  len_type = True

  if type(data)==type(pd.DataFrame()):  #check if the input for data is a DataFrame or not
    df_type = True
    df_msg = ''
    len_msg = ''
    len_type = True


    if identifier in data.columns.tolist(): #check the number of months for each store is > the mano or not
      if timecol in data.columns.tolist():
        if measure in data.columns.tolist():

          data_tmp = data[[identifier, timecol, measure]].copy()
          data_tmp = data_tmp.rename(columns={identifier: 'identifier', timecol: 'timecol', measure: 'measure'})
          data_tmp['timecol'] = pd.to_datetime(data_tmp['timecol'])
          data_tmp['year'] = data_tmp['timecol'].dt.year
          data_tmp['month'] = data_tmp['timecol'].dt.month
          store_list = data_tmp['identifier'].unique().tolist()

          for ID in store_list:
            str_df = data_tmp[data_tmp['identifier']==ID].copy()
            str_df = pd.DataFrame(str_df.groupby(['identifier','year','month'])[['measure']].sum())
            str_df.reset_index(inplace=True)
            len_msg = ''

            if len(str_df) > mano:
              len_msg = ''
              len_type = True
            else:
              len_msg = len_msg + '\n' + identifier + ' does not have more than ' + str(mano) + ' months to calculate MA(' + str(mano)+ ') and trend.' 
              len_type = False

            if len_type == False: break


    if identifier in data.columns.tolist():
      dfcol_identifier_type = True
      dfcol_identifier_msg = ''
    else:
      dfcol_identifier_type = False
      dfcol_identifier_msg = '\n{} column does not exist in {} DataFrame'.format(identifier, 'data')

    if timecol in data.columns.tolist():
      dfcol_timecol_type = True
      dfcol_timecol_msg = ''
    else:
      dfcol_timecol_type = False
      dfcol_timecol_msg = '\n{} column does not exist in {} DataFrame'.format(timecol, 'data')

    if measure in data.columns.tolist():
      dfcol_measure_type = True
      dfcol_measure_msg = ''
    else:
      dfcol_measure_type = False
      dfcol_measure_msg = '\n{} column does not exist in {} DataFrame'.format(measure, 'data')

  else:
    df_type = False
    df_msg = '\nNo valid data for data param is given.'

  
  if type(mano)==type(1):  #check if mano is positive integer number or not
    if mano>0:
      t1_type = True
      t1_msg = ''
    else:
      t1_type = False
      t1_msg = '\nParam mano takes only positive int.'
  else:
    t1_type = False
    t1_msg = '\nParam mano takes only positive int.'

  if type(wt)==type(True): #check if wt is bool type or not
    wt_type = True
    wt_msg = ''
  else:
    wt_type = False
    wt_msg = '\nParam wt(weight) takes only True or False'

  if df_type==True:
    final_type = dfcol_identifier_type & dfcol_timecol_type & dfcol_measure_type & len_type
    final_msg = dfcol_identifier_msg + dfcol_timecol_msg + dfcol_measure_msg + len_msg
  else:
    final_type = False
    final_msg = df_msg

  final_type = final_type & t1_type & wt_type
  final_msg = final_msg + t1_msg + wt_msg

  return [final_type, final_msg]