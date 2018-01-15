
""" Created on Jan 2018 @author: Sarbadal.Pal """

def moving_avg_fun(list, N):
  cumsum, moving_avg, time_id = [0], [], []

  for i, x in enumerate(list):
    cumsum.append(cumsum[i] + x)
    if i >= N-1:
      moving_average = (cumsum[i+1] - cumsum[i-N+1])/N
      moving_avg.append(moving_average)
      time_id.append(i-1)
  return [moving_avg, time_id]