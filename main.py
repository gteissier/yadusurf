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

for d in days[1:]:
  div = d.find_all('div')
  if len(div) == 0: continue
  div = div[0]
  date = div.string.strip('\r\n').rstrip(' ')

  sprites = get_sprites(d)
  # may report no sprite instead of sprite 0 star
  if len(sprites) == 0: continue
  assert(len(sprites) == 1)
  m = re.search(r'sprite\-etoiles\-(\d+)\-bis', str(sprites[0]))
  assert(m)
  stars = m.group(1)

  img = d.find_all('img')
  if len(img) != 1: continue

  img = img[0]
  text = img['alt']

  heights = [m.group(0) for m in re.finditer(r'\dm(50)?', text)]
  heights = [float(h.replace('m', '.')) for h in heights]
  if stars == '3' and any(h >= 1.5 for h in heights):
    desc = '%s hauteurs=%r' % (date, heights)
    print(desc)
