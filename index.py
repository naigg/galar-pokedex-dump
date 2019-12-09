import requests
import json
from bs4 import BeautifulSoup, NavigableString, Tag

url  = 'https://www.serebii.net/swordshield/galarpokedex.shtml'
r    = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.content, 'html5lib')

trTable = soup.find_all("tr")

pokemonList = []

def removeSpecialCharacter(string):
  new_text = string.replace('\n', '')
  new_text = new_text.replace('\t', '')
  return new_text

def removeJapaneseCharacters(string):
  new_text = string.split('\\u', 1)[0]
  return new_text

def getPokemonTypes(types):
  new_types = []
  for type in types:
    # Don't both with NavigableString
    if isinstance(type, NavigableString):
      continue
    if isinstance(type, Tag):
      type = type.img['src'].split('/')[-1].split('.')[0]
      new_types.append(type)
  return new_types

for table in trTable:
  tableFooInfo = table.find_all("td", class_="fooinfo")
  if tableFooInfo:
    td_dexNum = tableFooInfo[0].text
    td_dexName = tableFooInfo[2].text
    td_dexTypes = getPokemonTypes(tableFooInfo[4])
    pokemon = dict()

    td_dexNum = removeSpecialCharacter(td_dexNum)
    td_dexName = removeJapaneseCharacters(removeSpecialCharacter(td_dexName))
    pokemon['dexNumber'] = td_dexNum
    pokemon['dexName'] = td_dexName
    pokemon['dexTypes'] = td_dexTypes
    pokemonList.append(pokemon)

with open('data.json', 'w') as outfile:
  json.dump(pokemonList, outfile, ensure_ascii=True, indent=4)
