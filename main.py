#!/usr/bin/env python

import argparse
import requests
import bs4 as BeautifulSoup
import re



parser = argparse.ArgumentParser()
parser.add_argument('spot', default='''Barre-d'Etel/1211''')

args = parser.parse_args()

def fetch(spot):
  r = requests.get(url='https://www.yadusurf.com/METEO-SURF-REPORT/%s' % spot)
  if r.status_code != 200:
    raise BadFetch(r)
  return BeautifulSoup.BeautifulSoup(r.content, 'lxml')

def get_days(bs):
  for day in bs.find_all('div', class_='SurfDayV3'):
    yield day


def get_sprites(d):
  return [s for s in d.find_all('i', class_='sprite')]

content = fetch(args.spot)
assert(content)

days = [d for d in get_days(content)]
assert(days)

days = days[1:]
for d in days:
  #print(d)
  sprites = get_sprites(d)
  assert(len(sprites) == 1)
  m = re.search(r'sprite\-etoiles\-(\d+)\-bis', str(sprites[0]))
  assert(m)
  print(m.group(1))
