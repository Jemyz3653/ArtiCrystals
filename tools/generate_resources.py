#!/usr/bin/env python3
"""Deterministic, original pixel textures and Minecraft cuboid models. Requires Pillow.
No vanilla amethyst textures/models are copied or recolored. Each mineral has its own geometry and texture motif.
"""
import json, math, random
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
ASSET=RES/'assets/articrystals'
DATA=RES/'data/articrystals'
KINDS=[
 ('ruby','Ruby','Рубин','#d53f68',6),('sapphire','Sapphire','Сапфир','#3467d5',6),
 ('rock_crystal','Rock Crystal','Горный хрусталь','#b5e2e4',8),('citrine','Citrine','Цитрин','#e8bb42',10),
 ('rose_quartz','Rose Quartz','Розовый кварц','#e88eb3',5),('topaz','Topaz','Топаз','#e88632',9),
 ('fluorite','Fluorite','Флюорит','#78c79b',12),('jade','Jade','Нефрит','#3f9c72',3),
 ('aquamarine','Aquamarine','Аквамарин','#45bdce',8),('tourmaline','Tourmaline','Турмалин','#675878',4),
 ('amber','Amber','Янтарь','#dca02d',15),('opal','Opal','Опал','#bfcee0',13),
 ('garnet','Garnet','Гранат','#922d40',4),('onyx','Onyx','Оникс','#383b46',2),
 ('malachite','Malachite','Малахит','#23975f',5),('moonstone','Moonstone','Лунный камень','#c0cbe9',11)]

# Separate event IDs per mineral, backed by the player's vanilla/resource-pack sounds.
SOUND_PITCHES={'ruby':.84,'sapphire':1.12,'rock_crystal':1.48,'citrine':1.30,
 'rose_quartz':1.24,'topaz':1.04,'fluorite':1.62,'jade':.68,'aquamarine':1.40,
 'tourmaline':.76,'amber':.94,'opal':1.54,'garnet':.60,'onyx':.50,
 'malachite':.90,'moonstone':1.74}

def dump(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def texture(name,im):
 p=ASSET/'textures'/f'{name}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def color(hex):return tuple(bytes.fromhex(hex.strip('#')))
def shade(c,f):return tuple(max(0,min(255,round(x*f))) for x in c)
def mineral_texture(kind,hex):
 c=color(hex);im=Image.new('RGB',(16,16));r=random.Random(kind)
 for y in range(16):
  for x in range(16):
   if kind=='ruby': v=.72+((x//4+y//5)%3)*.16+(.2 if x in (3,11) else 0)
   elif kind=='sapphire': v=.65+(x%5)*.08+(y//4%2)*.16
   elif kind=='rock_crystal': v=.78+((x+y//3)%7)*.04
   elif kind=='citrine': v=.7+(15-y)*.018+(.22 if x%6==1 else 0)
   elif kind=='rose_quartz': v=.84+.15*math.sin((x+y)/2)+(.14 if (x-y)%9==0 else 0)
   elif kind=='topaz': v=.7+(x//3%3)*.13+(.18 if y in (4,11) else 0)
   elif kind=='fluorite': v=.7+(y//3%3)*.16
   elif kind=='jade': v=.8+.15*math.sin(x*.9+math.sin(y))
   elif kind=='aquamarine': v=.8+(x%4)*.08+(.1 if y<3 else 0)
   elif kind=='tourmaline': v=.65+(x%3)*.25+(.25 if y>11 else 0)
   elif kind=='amber': v=.8+.13*math.sin((x-8)**2/20+(y-7)**2/23)
   elif kind=='garnet': v=.62+((x//4+y//4)%3)*.16+(.25 if (x+y)%8==0 else 0)
   elif kind=='onyx': v=.7+.17*math.sin(y*.8+x*.2)
   elif kind=='malachite': v=.66+.35*(.5+.5*math.sin(math.hypot(x-3,y-11)*1.8))
   elif kind=='moonstone': v=.84+.14*math.sin(x*.5+y*.25)
   else:v=.84+((x//3+y//3)%2)*.15
   out=shade(c,v+r.uniform(-.025,.025))
   if kind=='fluorite' and y in (5,6,11):out=shade((150,111,199),.9+x/60)
   if kind=='opal' and (x*7+y*11)%19<4:out=[(130,208,197),(203,157,210),(227,202,137),(147,180,228)][(x//4+y//4)%4]
   if kind=='jade' and (x+round(2*math.sin(y)))%11==0:out=(126,170,127)
   if kind=='amber' and ((x-6)**2+(y-9)**2<5 or (x==10 and 4<y<8)):out=(115,64,24)
   if kind=='onyx' and (y+round(2*math.sin(x*.4)))%9 in (0,1):out=(169,165,152)
   if kind=='moonstone' and (x+y//2)%13 in (0,1,2):out=(129,174,228)
   im.putpixel((x,y),out)
 d=ImageDraw.Draw(im);d.line((1,1,5,1),fill=shade(c,1.35));d.point((1,2),fill=shade(c,1.25));return im

def box(a,b,tex='crystal',rotation=None):
 out={'from':a,'to':b,'faces':{f:{'texture':'#'+tex} for f in ['up','down','north','south','east','west']}}
 if rotation:out['rotation']={'origin':rotation[0],'axis':rotation[1],'angle':rotation[2],'rescale':False}
 return out

def prism(x,z,w,h,y=1,angle=0):
 rot=([x,y,z],'y',angle) if angle else None
 return [box([x-w/2,y,z-w/2],[x+w/2,y+h-3,z+w/2],rotation=rot),
         box([x-w*.36,y+h-3,z-w*.36],[x+w*.36,y+h-1.5,z+w*.36],rotation=rot),
         box([x-w*.17,y+h-1.5,z-w*.17],[x+w*.17,y+h,z+w*.17],rotation=rot)]

def geometry(kind,single=False):
 if kind=='ruby':
  e=[box([4,2,4],[12,7,12],rotation=([8,5,8],'y',45)),box([5,7,5],[11,10,11],rotation=([8,5,8],'y',45)),box([6,10,6],[10,12,10],rotation=([8,5,8],'y',45))]
  if not single:e+=prism(3.5,4,3,6,angle=45)+prism(12.3,11,3.5,7,angle=45)
 elif kind=='sapphire':
  e=[box([5,1,5],[11,4,11]),box([4,4,4],[12,9,12]),box([5,9,5],[11,12,11]),box([6,12,6],[10,14,10])]
  if not single:e+=[box([1,1,9],[5,6,13]),box([11,1,2],[15,5,6])]
 elif kind=='rock_crystal':
  e=prism(8,8,4.5,13,angle=45)
  if not single:e+=prism(3.5,6,3,7,angle=45)+prism(11.5,11,3.5,9,angle=45)+prism(6,12,3,5,angle=45)
 elif kind=='citrine':
  e=prism(8,8,4,12)
  if not single:
   for x,z,h in [(4,5,8),(12,6,9),(5,11,6),(11,12,7)]:e+=prism(x,z,3,h)
 elif kind=='rose_quartz':
  e=[]
  for a in [0,45,-45]:e+=[box([6,1,5],[10,10,11],rotation=([8,2,8],'z',a))]
  if not single:e+=[box([5,1,6],[11,8,10],rotation=([8,2,8],'x',45)),box([5,1,6],[11,8,10],rotation=([8,2,8],'x',-45))]
 elif kind=='topaz':
  e=[box([5,1,5],[11,11,11]),box([6,11,6],[10,13,10])]
  if not single:e+=[box([1,1,3],[5,7,7]),box([10,1,10],[15,9,15]),box([2,1,10],[6,5,14])]
 elif kind=='fluorite':
  e=[box([4,3,4],[11,10,11],rotation=([8,4,8],'y',45)),box([8,9,6],[13,14,11])]
  if not single:e+=[box([1,1,8],[6,6,13]),box([10,1,1],[15,6,6])]
 elif kind=='jade':
  e=[box([3,1,4],[13,5,12]),box([4,5,5],[12,8,11]),box([5,8,6],[11,9,10])]
  if not single:e+=[box([1,1,7],[5,4,14]),box([10,1,2],[15,4,7])]
 elif kind=='aquamarine':
  e=prism(8,8,4,13)
  if not single:e+=prism(3.5,4.5,3,10)+prism(12,11,3,8)+prism(4,11,2.5,6)
 elif kind=='tourmaline':
  e=[box([7,1,6],[9,14,9]),box([6.5,14,6.5],[9.5,15,8.5])]
  if not single:
   for x,z,h,a in [(3,4,10,-22.5),(12,5,12,22.5),(4,10,9,-22.5),(11,12,8,22.5)]:e.append(box([x-1,1,z-1],[x+1,h,z+1],rotation=([x,1,z],'z',a)))
 elif kind=='amber':
  e=[box([4,1,4],[12,3,12]),box([3,3,3],[13,7,13]),box([5,7,5],[11,9,11])]
  if not single:e+=[box([1,1,9],[5,4,13]),box([11,1,1],[15,5,5])]
 elif kind=='garnet':
  # Compact, many-faced garnet grains rather than long quartz points.
  e=[box([4,2,4],[12,8,12],rotation=([8,5,8],'y',22.5)),
     box([5,1,5],[11,10,11],rotation=([8,5,8],'y',-22.5)),
     box([6,10,6],[10,11,10],rotation=([8,5,8],'y',22.5))]
  if not single:e+=[box([1,1,9],[5,5,13],rotation=([3,3,11],'y',45)),box([11,1,2],[15,5,6])]
 elif kind=='onyx':
  # Banded blades of unequal width and height.
  e=[box([4,1,6],[8,12,10]),box([8,1,5],[11,10,11]),box([5,12,7],[7,14,9])]
  if not single:e+=[box([1,1,3],[4,8,6]),box([11,1,9],[14,6,12])]
 elif kind=='malachite':
  # A low fan of green, banded blades.
  e=[box([6,1,6],[10,10,10])]
  # Each blade has a distinct depth, so its broad faces never share a plane.
  for i,a in enumerate([-45,-22.5,22.5,45],1):
   e.append(box([7,1,6-i*.15],[9,9,10+i*.15],rotation=([8,1,8],'z',a)))
  if not single:e+=[box([2,1,3],[7,4,7]),box([10,1,10],[14,5,14])]
 elif kind=='moonstone':
  # Pearly, interlocking feldspar plates with stepped ends.
  e=[box([3,1,5],[13,4,11]),box([4,4,6],[12,7,10]),box([5,7,6],[11,8,10])]
  if not single:e+=[box([2,1,2],[8,5,6],rotation=([5,2,4],'y',22.5)),box([9,1,10],[14,6,14],rotation=([11,2,12],'y',-22.5))]
 else:
  e=[box([5,1,5],[11,3,11]),box([3,3,3],[13,7,13]),box([4,7,4],[12,10,12]),box([6,10,6],[10,12,10])]
  if not single:e+=[box([1,1,10],[5,5,14]),box([11,1,2],[15,6,6])]
 if not single:e=[box([2,0,2],[14,1,14],'matrix')]+e
 return e

DISPLAY={'gui':{'rotation':[25,225,0],'translation':[0,0,0],'scale':[.8,.8,.8]},'ground':{'rotation':[0,0,0],'translation':[0,3,0],'scale':[.4,.4,.4]},'fixed':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[.6,.6,.6]},'thirdperson_righthand':{'rotation':[75,45,0],'translation':[0,2.5,0],'scale':[.375,.375,.375]},'firstperson_righthand':{'rotation':[0,45,0],'translation':[0,2,0],'scale':[.5,.5,.5]}}
def item_definition(name,model=None):dump(ASSET/'items'/f'{name}.json',{'model':{'type':'minecraft:model','model':model or 'articrystals:item/'+name}})
def shaped(name,pattern,key,result,count=1):dump(DATA/'recipe'/f'{name}.json',{'type':'minecraft:crafting_shaped','category':'misc','pattern':pattern,'key':key,'result':{'id':result,'count':count}})
def shapeless(name,ingredients,result,count=1):dump(DATA/'recipe'/f'{name}.json',{'type':'minecraft:crafting_shapeless','category':'misc','ingredients':ingredients,'result':{'id':result,'count':count}})
def loot(name):dump(DATA/'loot_table/blocks'/f'{name}.json',{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'articrystals:'+name}],'condition':{'type':'minecraft:survives_explosion'}}]})
def simple_block(name,model):
 dump(ASSET/'blockstates'/f'{name}.json',{'variants':{'':{'model':'articrystals:block/'+name}}});dump(ASSET/'models/block'/f'{name}.json',model);item_definition(name,'articrystals:block/'+name);loot(name)

def main():
 langs={'en_us':{'itemGroup.articrystals':'ArtiCrystals','block.articrystals.crystal_synthesizer':'Crystal Synthesizer','gui.articrystals.recipes':'Synthesis guide','gui.articrystals.shapeless':'Any arrangement','gui.articrystals.one_each':'One per slot'},'ru_ru':{'itemGroup.articrystals':'ArtiCrystals','block.articrystals.crystal_synthesizer':'Синтез кристаллов','gui.articrystals.recipes':'Рецепты синтеза','gui.articrystals.shapeless':'Порядок любой','gui.articrystals.one_each':'По одному в слот'}}
 matrix=Image.new('RGB',(16,16));r=random.Random(185)
 for y in range(16):
  for x in range(16):matrix.putpixel((x,y),shade((88,91,98),r.uniform(.8,1.2)))
 texture('block/matrix',matrix)
 for kind,en,ru,hex,light in KINDS:
  im=mineral_texture(kind,hex);texture('block/'+kind,im)
  # Storage blocks have individual mineral pattern plus a cut-stone border.
  tile=im.copy();d=ImageDraw.Draw(tile);d.rectangle((0,0,15,15),outline=shade(color(hex),.52));d.line((1,1,14,1),fill=shade(color(hex),1.32));d.line((1,1,1,14),fill=shade(color(hex),1.2));d.line((2,14,14,14),fill=shade(color(hex),.65));texture('block/'+kind+'_block',tile)
  common={'ambientocclusion':False,'textures':{'crystal':'articrystals:block/'+kind,'matrix':'articrystals:block/matrix','particle':'articrystals:block/'+kind},'display':DISPLAY}
  dump(ASSET/'models/block'/f'{kind}_cluster.json',{**common,'elements':geometry(kind)})
  dump(ASSET/'models/item'/f'{kind}.json',{**common,'elements':geometry(kind,True)});item_definition(kind)
  item_definition(kind+'_cluster','articrystals:block/'+kind+'_cluster')
  variants={}
  for face,x,y in [('up',0,0),('down',180,0),('north',90,0),('south',90,180),('east',90,90),('west',90,270)]:
   variants['facing='+face]={'model':'articrystals:block/'+kind+'_cluster','x':x,'y':y}
  dump(ASSET/'blockstates'/f'{kind}_cluster.json',{'variants':variants});loot(kind+'_cluster')
  simple_block(kind+'_block',{'parent':'minecraft:block/cube_all','textures':{'all':'articrystals:block/'+kind+'_block'}})
  shaped(kind+'_block',['###','###','###'],{'#':'articrystals:'+kind},'articrystals:'+kind+'_block')
  shapeless(kind+'_from_block',['articrystals:'+kind+'_block'],'articrystals:'+kind,9)
  shaped(kind+'_cluster',[' # ','###',' S '],{'#':'articrystals:'+kind,'S':'minecraft:stone'},'articrystals:'+kind+'_cluster')
  for lang,n in [('en_us',en),('ru_ru',ru)]:
   langs[lang]['item.articrystals.'+kind]=n
   langs[lang]['block.articrystals.'+kind+'_cluster']=n+' Cluster' if lang=='en_us' else 'Кластер: '+n.lower()
   langs[lang]['block.articrystals.'+kind+'_block']=n+' Block' if lang=='en_us' else 'Блок: '+n.lower()
 # Workbench surface: copper frame, pale ceramic 3x3 reagent tray, a teal instrument panel.
 for side in ['top','side','bottom']:
  im=Image.new('RGB',(16,16),(55,75,76));d=ImageDraw.Draw(im)
  d.rectangle((0,0,15,15),outline=(113,66,43));d.rectangle((1,1,14,14),outline=(192,125,76))
  if side=='top':
   d.rectangle((2,2,13,13),fill=(193,201,190))
   for yy in [3,7,11]:
    for xx in [3,7,11]:d.rectangle((xx,yy,xx+2,yy+2),fill=(71,97,98));d.point((xx,yy),fill=(39,60,65))
  elif side=='side':
   d.rectangle((3,3,12,7),fill=(29,46,52));d.line((4,5,7,5),fill=(91,202,178));d.rectangle((10,4,11,6),fill=(225,183,85));d.rectangle((3,10,12,13),fill=(112,81,60));d.line((7,11,9,11),fill=(205,184,137))
  texture('block/synthesizer_'+side,im)
 simple_block('crystal_synthesizer',{'parent':'minecraft:block/cube','textures':{'up':'articrystals:block/synthesizer_top','down':'articrystals:block/synthesizer_bottom','north':'articrystals:block/synthesizer_side','south':'articrystals:block/synthesizer_side','east':'articrystals:block/synthesizer_side','west':'articrystals:block/synthesizer_side','particle':'articrystals:block/synthesizer_side'}})
 shaped('crystal_synthesizer',['CGC','ATA','SSS'],{'C':'minecraft:copper_ingot','G':'minecraft:glass','A':'minecraft:amethyst_shard','T':'minecraft:crafting_table','S':'minecraft:smooth_stone'},'articrystals:crystal_synthesizer')
 for name,en,ru,c in [('clear_lens','Clear Lens','Прозрачная линза',(169,223,227)),('focus_lens','Focusing Lens','Фокусирующая линза',(94,161,225)),('prismatic_lens','Prismatic Lens','Призматическая линза',(175,132,218))]:
  im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im);d.polygon([(5,1),(10,1),(14,5),(14,10),(10,14),(5,14),(1,10),(1,5)],fill=(90,59,38),outline=(224,169,98));d.ellipse((3,3,12,12),fill=(*c,255));d.line((5,5,8,4),fill=(243,255,255),width=1)
  if name=='focus_lens':d.ellipse((6,6,10,10),outline=(222,244,255))
  if name=='prismatic_lens':
   for yy,cc in [(8,(225,139,168)),(9,(222,204,112)),(10,(137,216,169))]:d.line((5,yy,11,yy),fill=cc)
  texture('item/'+name,im);dump(ASSET/'models/item'/f'{name}.json',{'parent':'minecraft:item/generated','textures':{'layer0':'articrystals:item/'+name}});item_definition(name)
  langs['en_us']['item.articrystals.'+name]=en;langs['ru_ru']['item.articrystals.'+name]=ru
 shaped('clear_lens',[' C ','CRC',' C '],{'C':'minecraft:copper_nugget','R':'articrystals:rock_crystal'},'articrystals:clear_lens')
 shapeless('focus_lens',['articrystals:clear_lens','articrystals:sapphire','articrystals:aquamarine'],'articrystals:focus_lens')
 shapeless('prismatic_lens',['articrystals:clear_lens','articrystals:opal','articrystals:fluorite'],'articrystals:prismatic_lens')
 shaped('spyglass',['L','C','C'],{'L':'articrystals:clear_lens','C':'minecraft:copper_ingot'},'minecraft:spyglass')
 shaped('crystal_spyglass',['L','C','C'],{'L':'articrystals:focus_lens','C':'minecraft:copper_ingot'},'articrystals:crystal_spyglass')
 # The prismatic lens turns low-light crystal blocks into bright lamps.
 for kind in ['ruby','sapphire','rose_quartz','jade']:
  name=kind+'_lamp'
  im=mineral_texture(kind,dict((a,d) for a,b,c,d,e in KINDS)[kind]);d=ImageDraw.Draw(im);d.rectangle((0,0,15,15),outline=(120,77,44));d.rectangle((1,1,14,14),outline=(221,168,100));d.line((0,0,4,4),fill=(221,168,100));d.line((15,0,11,4),fill=(221,168,100));texture('block/'+name,im)
  simple_block(name,{'parent':'minecraft:block/cube_all','textures':{'all':'articrystals:block/'+name}})
  shapeless(name,['articrystals:'+kind+'_block','articrystals:prismatic_lens','minecraft:glowstone_dust'],'articrystals:'+name)
  langs['en_us']['block.articrystals.'+name]=dict((a,b) for a,b,c,d,e in KINDS)[kind]+' Lamp'
  langs['ru_ru']['block.articrystals.'+name]='Лампа: '+dict((a,c) for a,b,c,d,e in KINDS)[kind].lower()
 # Item and held model for the copper-and-aquamarine telescope.
 im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im);d.polygon([(2,11),(10,3),(13,6),(5,14)],fill=(180,115,61),outline=(86,58,38));d.line((4,11,10,5),fill=(241,185,107),width=2);d.polygon([(9,3),(11,1),(15,5),(13,7)],fill=(74,158,174),outline=(180,226,229));texture('item/crystal_spyglass',im)
 dump(ASSET/'models/item/crystal_spyglass.json',{'parent':'minecraft:item/generated','textures':{'layer0':'articrystals:item/crystal_spyglass'}})
 held=Image.new('RGB',(16,16),(182,115,65));hd=ImageDraw.Draw(held);hd.rectangle((0,0,1,1),fill=(105,221,229));hd.line((0,2,0,12),fill=(230,183,115));hd.rectangle((0,5,1,7),fill=(66,148,164));hd.rectangle((0,12,1,14),fill=(66,148,164));texture('item/crystal_spyglass_model',held)
 dump(ASSET/'models/item/crystal_spyglass_in_hand.json',{'parent':'minecraft:item/spyglass_in_hand','textures':{'spyglass':'articrystals:item/crystal_spyglass_model','particle':'articrystals:block/aquamarine'}})
 dump(ASSET/'items/crystal_spyglass.json',{'model':{'type':'minecraft:select','property':'minecraft:display_context','cases':[{'when':['gui','ground','fixed'],'model':{'type':'minecraft:model','model':'articrystals:item/crystal_spyglass'}}],'fallback':{'type':'minecraft:model','model':'articrystals:item/crystal_spyglass_in_hand'}}})
 langs['en_us']['item.articrystals.crystal_spyglass']='Crystal Spyglass';langs['ru_ru']['item.articrystals.crystal_spyglass']='Кристальная подзорная труба'
 sounds={}
 actions={'break':'block.amethyst_block.break','cluster_break':'block.amethyst_cluster.break',
  'step':'block.amethyst_block.step','place':'block.amethyst_block.place',
  'hit':'block.amethyst_block.hit','fall':'block.amethyst_block.fall','chime':'block.amethyst_block.chime'}
 verbs={'break':('breaks','разбивается'),'cluster_break':('cluster breaks','кластер разбивается'),
  'step':('footsteps','шаги'),'place':('placed','установка'),'hit':('hit','удар'),
  'fall':('landing','приземление'),'chime':('chimes','звенит')}
 for kind,en,ru,*_ in KINDS:
  for action,base in actions.items():
   event=f'crystal.{kind}.{action}';subtitle='subtitles.articrystals.'+event
   sounds[event]={'subtitle':subtitle,'sounds':[{'name':'minecraft:'+base,'type':'event','pitch':SOUND_PITCHES[kind]}]}
   langs['en_us'][subtitle]=en+' '+verbs[action][0]
   langs['ru_ru'][subtitle]=ru+': '+verbs[action][1]
 dump(ASSET/'sounds.json',sounds)
 for lang,data in langs.items():dump(ASSET/'lang'/f'{lang}.json',data)
 blocks=['articrystals:crystal_synthesizer']+[f'articrystals:{k}_{suffix}' for k,*_ in KINDS for suffix in ['block','cluster']]+['articrystals:'+k+'_lamp' for k in ['ruby','sapphire','rose_quartz','jade']]
 dump(RES/'data/minecraft/tags/block/mineable/pickaxe.json',{'replace':False,'values':blocks})
 dump(RES/'data/minecraft/tags/block/needs_stone_tool.json',{'replace':False,'values':[f'articrystals:{k}_block' for k,*_ in KINDS]})
 # Discover ordinary recipes when the workstation is crafted or obtained.
 for recipe in (DATA/'recipe').glob('*.json'):
  dump(DATA/'advancement/recipes'/f'{recipe.stem}.json',{'parent':'minecraft:recipes/root','criteria':{'has_synthesizer':{'trigger':'minecraft:inventory_changed','conditions':{'items':[{'items':('minecraft:amethyst_shard' if recipe.stem=='crystal_synthesizer' else 'articrystals:crystal_synthesizer')}]}}},'requirements':[['has_synthesizer']],'rewards':{'recipes':['articrystals:'+recipe.stem]}})
 print(f'Generated resources for {len(KINDS)} minerals, 4 lamps and the synthesizer; {len(sounds)} sound events.')
if __name__=='__main__':main()
