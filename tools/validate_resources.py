#!/usr/bin/env python3
"""Check internal resource references and model geometry without launching a GPU."""
from pathlib import Path
import json,hashlib
from PIL import Image
from generate_resources import ROOT,ASSET,KINDS,SOUND_PITCHES,geometry

models={p.relative_to(ASSET/'models').with_suffix('').as_posix():json.loads(p.read_text()) for p in (ASSET/'models').rglob('*.json')}
def check_model(ref):
 if ref.startswith('articrystals:'):assert ref.split(':',1)[1] in models,ref
for key,model in models.items():
 if 'parent' in model:check_model(model['parent'])
 for tex in model.get('textures',{}).values():
  if tex.startswith('articrystals:'):assert (ASSET/'textures'/(tex.split(':',1)[1]+'.png')).is_file(),tex
 for e in model.get('elements',[]):
  assert all(-16<=v<=32 for v in e['from']+e['to']),(key,e)
  assert all(a<=b for a,b in zip(e['from'],e['to'])),(key,e)
  if 'rotation' in e:assert e['rotation']['angle'] in [-45,-22.5,0,22.5,45],key
  for face in e['faces'].values():assert face['texture'].removeprefix('#') in model['textures'],(key,face)
for p in (ASSET/'blockstates').glob('*.json'):
 for variant in json.loads(p.read_text())['variants'].values():check_model(variant['model'])
def walk(node):
 if isinstance(node,dict):
  if node.get('type')=='minecraft:model':check_model(node['model'])
  for value in node.values():walk(value)
 elif isinstance(node,list):
  for value in node:walk(value)
for p in (ASSET/'items').glob('*.json'):walk(json.loads(p.read_text()))
for p in (ASSET/'textures').rglob('*.png'):
 with Image.open(p) as im:assert im.width & (im.width-1)==0 and im.height & (im.height-1)==0,p
for folder in ['block','item']:
 digests=[hashlib.sha256((ASSET/'models'/folder/(k+('_cluster' if folder=='block' else '')+'.json')).read_bytes()).digest() for k,*_ in KINDS]
 assert len(set(digests))==len(KINDS)
 # Compare actual shapes too, so unique texture names alone cannot pass.
 assert len({json.dumps(geometry(k,folder=='item'),sort_keys=True) for k,*_ in KINDS})==len(KINDS)
for lang in ['ru_ru','en_us']:
 data=json.loads((ASSET/'lang'/(lang+'.json')).read_text())
 for k,*_ in KINDS:
  assert 'item.articrystals.'+k in data
  for suffix in ['_block','_cluster']:assert 'block.articrystals.'+k+suffix in data
for p in (ROOT/'src/main/resources').rglob('*.json'):
 if p.name=='fabric.mod.json':continue
 json.loads(p.read_text())
recipe_count=3*len(KINDS)+10
item_count=3*len(KINDS)+9
assert len(list((ROOT/'src/main/resources/data/articrystals/recipe').glob('*.json')))==recipe_count
assert len(list((ASSET/'items').glob('*.json')))==item_count
sounds=json.loads((ASSET/'sounds.json').read_text())
assert len(sounds)==7*len(KINDS)
assert set(SOUND_PITCHES)=={k for k,*_ in KINDS}
assert len(set(SOUND_PITCHES.values()))==len(KINDS)
for event,definition in sounds.items():
 kind=event.split('.')[1]
 sound=definition['sounds'][0]
 assert sound['type']=='event' and sound['name'].startswith('minecraft:block.amethyst_')
 assert sound['pitch']==SOUND_PITCHES[kind] and .5<=sound['pitch']<=2
 for lang in ['ru_ru','en_us']:
  assert definition['subtitle'] in json.loads((ASSET/'lang'/(lang+'.json')).read_text())
print(f'PASS: {len(models)} models, {item_count} item definitions, {recipe_count} recipes, {len(sounds)} sound events; references and translations resolve.')
