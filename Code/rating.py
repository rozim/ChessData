
def expectation(r1, r2):
  return  1.0 / (1.0 + 10.0 ** ((r2-r1)/400.0))

# https://medium.com/mlearning-ai/how-to-calculate-elo-score-for-international-teams-using-python-66c136f01048
def rating_gain(r1, r2, result, k=24):
  assert result in [1.0, 0.5, 0.0]
  assert 0 < r1 < 3000
  assert 0 < r2 < 3000

  return k * (result - expectation(r1, r2))

# Performance Rating = Average Opponents' Rating + [(PctScore - 0.50) * 850]
# https://github.com/sublee/glicko/blob/master/glicko2.py

# https://www.chessprogramming.org/Match_Statistics#SPRT
