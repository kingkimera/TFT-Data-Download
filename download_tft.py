"""
To continue downloading:

$ python3 download_tft.py --dir tmp
"""
import argparse, json, os, time
from urllib import request
pjoin = os.path.join
API_KEY = open('apikey.txt', 'r').read().strip()
STARTER_ID = open('starterID.txt', 'r').read().strip()

class Throttler:
  def __init__(self, qps):
    self.wait_time = 1. / qps
    self.last_call = time.time() - self.wait_time
  def throttle(self):
    next_time = self.last_call + self.wait_time
    time.sleep(max(next_time - time.time(), 0.0))
    self.last_call = time.time()

def readlist(path):
  with open(path, 'r') as f:
    return set([line.strip() for line in f.readlines() if len(line.strip()) > 0])

def writelist(data, path):
  with open(path, 'w') as f:
    f.write('\n'.join(data))

def fetch_history(throttler, puuid):
  throttler.throttle()
  url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=10&api_key={API_KEY}"
  try:
    return json.loads(request.urlopen(url).read())
  except:
    print(url)
    return None

def fetch_match(throttler, game_id):
  throttler.throttle()
  url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{game_id}?api_key={API_KEY}"
  try:
    return json.loads(request.urlopen(url).read())
  except:
    print(url)
    return None

argparser = argparse.ArgumentParser()
argparser.add_argument("--dir", type=str, required=True)
argparser.add_argument("--force", '-f', action='store_true')
args = argparser.parse_args()

if not os.path.exists(args.dir):
  os.mkdir(args.dir)
  os.mkdir(pjoin(args.dir, 'matches'))
  with open(pjoin(args.dir, 'open_puuids.txt'), 'w+') as f:
    f.write("""i8S1HJOXO76iTS3CDkCJKBvgkMScOC6eVxiPx2Nevk8taNQarx3o5cUo9jJpoUppHUQwh9XSY0gK1g""")
  with open(pjoin(args.dir, 'closed_puuids.txt'), 'w+') as f:
    f.write('')
  with open(pjoin(args.dir, 'open_gameids.txt'), 'w+') as f:
    f.write('')
  with open(pjoin(args.dir, 'closed_gameids.txt'), 'w+') as f:
    f.write('')


open_puuids = readlist(pjoin(args.dir, 'open_puuids.txt'))
closed_puuids = readlist(pjoin(args.dir, 'closed_puuids.txt'))
open_gameids = readlist(pjoin(args.dir, 'open_gameids.txt'))
closed_gameids = readlist(pjoin(args.dir, 'closed_gameids.txt'))

throttler = Throttler(0.5)

it = 0
numDownloaded = 0
while True:
  it += 1

  if it % 10 == 0:
    writelist(open_puuids, pjoin(args.dir, 'open_puuids.txt'))
    writelist(closed_puuids, pjoin(args.dir, 'closed_puuids.txt'))
    writelist(open_gameids, pjoin(args.dir, 'open_gameids.txt'))
    writelist(closed_gameids, pjoin(args.dir, 'closed_gameids.txt'))

  # TODO: save lists
  if len(open_gameids) > 0:
    game_id = next(iter(open_gameids))
    open_gameids.remove(game_id)
    closed_gameids.add(game_id)
    match = fetch_match(throttler, game_id)
    if match is None:
      continue

    for puuid in match['metadata']['participants']:
      if puuid not in closed_puuids:
        open_puuids.add(puuid)

    v = match['info']['game_version'].split(' ')[1]
    v = '.'.join(v.split('.')[:2])
    if not os.path.exists(pjoin(args.dir, 'matches', v)):
      os.mkdir(pjoin(args.dir, 'matches', v))
    with open(pjoin(args.dir, 'matches', v, game_id + '.json'), 'w+') as f:
      json.dump(match, f, indent=1)
    numDownloaded += 1
    print(f'saved game {numDownloaded}')
  else:
    puuid = next(iter(open_puuids))
    open_puuids.remove(puuid)
    closed_puuids.add(puuid)
    history = fetch_history(throttler, puuid)
    if history is None:
      continue

    for match in history:
      if match not in closed_gameids:
        if match > STARTER_ID:
          open_gameids.add(match)