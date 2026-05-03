''' Stopwatch (from borrowed from https://www.codespeedy.com/how-to-create-a-stopwatch-in-python/)'''
def time_lapsed(start, end):
  sec = end - start
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))