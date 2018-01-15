
""" Created on Jan 2018 @author: Sarbadal.Pal """

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