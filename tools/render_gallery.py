#!/usr/bin/env python3
"""Rasterize the shipped Minecraft JSON cuboids into a model reference sheet.
This is a model render, not an in-game screenshot. Requires numpy and Pillow.
"""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from generate_resources import KINDS,ROOT,ASSET

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def render(model,size=220,scale=8):
 rgba=np.zeros((size,size,4),dtype=np.uint8);depth=np.full((size,size),-1e20)
 textures={k:np.asarray(Image.open(ASSET/'textures'/Path(v.split(':',1)[1]+'.png')).convert('RGB')) for k,v in model['textures'].items() if not v.startswith('#')}
 for elem in model['elements']:
  x0,y0,z0=elem['from'];x1,y1,z1=elem['to']
  faces={'up':[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],'down':[(x0,y0,z1),(x1,y0,z1),(x1,y0,z0),(x0,y0,z0)],'south':[(x0,y1,z1),(x1,y1,z1),(x1,y0,z1),(x0,y0,z1)],'north':[(x1,y1,z0),(x0,y1,z0),(x0,y0,z0),(x1,y0,z0)],'east':[(x1,y1,z1),(x1,y1,z0),(x1,y0,z0),(x1,y0,z1)],'west':[(x0,y1,z0),(x0,y1,z1),(x0,y0,z1),(x0,y0,z0)]}
  for face,coords in faces.items():
   if face not in elem['faces']:continue
   verts=np.array(coords,float)
   if 'rotation' in elem:
    rot=elem['rotation'];o=np.array(rot['origin']);a=math.radians(rot['angle']);c,s=math.cos(a),math.sin(a)
    if rot['axis']=='x':r=np.array([[1,0,0],[0,c,-s],[0,s,c]])
    elif rot['axis']=='y':r=np.array([[c,0,s],[0,1,0],[-s,0,c]])
    else:r=np.array([[c,-s,0],[s,c,0],[0,0,1]])
    verts=(verts-o)@r.T+o
   v=verts-np.array([8,0,8]);points=np.column_stack((size/2+(v[:,0]-v[:,2])*.707*scale,size*.84+((v[:,0]+v[:,2])*.354-v[:,1]*.866)*scale,(v[:,0]+v[:,2])*.612+v[:,1]*.5))
   tex=textures[elem['faces'][face]['texture'].removeprefix('#')]
   # Match default cuboid UV dimensions (the entire block occupies 16 texels).
   raw=np.array(coords,float)
   if face in ('up','down'):uv=raw[:,[0,2]]/16
   elif face in ('north','south'):uv=np.column_stack((raw[:,0],16-raw[:,1]))/16
   else:uv=np.column_stack((raw[:,2],16-raw[:,1]))/16
   light={'up':1.08,'down':.55,'south':.85,'north':.7,'east':.68,'west':.78}[face]
   for ids in [(0,1,2),(0,2,3)]:
    pts=points[list(ids)];uvs=uv[list(ids)]
    mn=np.maximum(np.floor(pts[:,:2].min(0)).astype(int),0);mx=np.minimum(np.ceil(pts[:,:2].max(0)).astype(int),size-1)
    if (mx<mn).any():continue
    xx,yy=np.meshgrid(np.arange(mn[0],mx[0]+1)+.5,np.arange(mn[1],mx[1]+1)+.5)
    den=(pts[1,1]-pts[2,1])*(pts[0,0]-pts[2,0])+(pts[2,0]-pts[1,0])*(pts[0,1]-pts[2,1])
    if abs(den)<1e-7:continue
    w0=((pts[1,1]-pts[2,1])*(xx-pts[2,0])+(pts[2,0]-pts[1,0])*(yy-pts[2,1]))/den
    w1=((pts[2,1]-pts[0,1])*(xx-pts[2,0])+(pts[0,0]-pts[2,0])*(yy-pts[2,1]))/den;w2=1-w0-w1
    dep=w0*pts[0,2]+w1*pts[1,2]+w2*pts[2,2]
    ys=slice(mn[1],mx[1]+1);xs=slice(mn[0],mx[0]+1);mask=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)&(dep>depth[ys,xs])
    u=(w0*uvs[0,0]+w1*uvs[1,0]+w2*uvs[2,0]);v=(w0*uvs[0,1]+w1*uvs[1,1]+w2*uvs[2,1])
    rgb=(tex[np.clip((v*16).astype(int),0,15),np.clip((u*16).astype(int),0,15)]*light).clip(0,255).astype(np.uint8)
    region=rgba[ys,xs];region[mask,:3]=rgb[mask];region[mask,3]=255;depth[ys,xs][mask]=dep[mask]
 return Image.fromarray(rgba)

def main():
 height=192+286*math.ceil(len(KINDS)/4)
 im=Image.new('RGB',(1100,height),'#111b20');d=ImageDraw.Draw(im)
 font=ImageFont.truetype(FONT,18);title=ImageFont.truetype(FONT,42);small=ImageFont.truetype(FONT,14)
 d.text((38,24),'ArtiCrystals',font=title,fill='#f2eee2');d.text((40,82),f'{len(KINDS)} минералов · отдельные модели и звуки · Minecraft 26.3 / Fabric',font=font,fill='#9bb9bc')
 for i,(kind,en,ru,c,light) in enumerate(KINDS):
  x=34+(i%4)*267;y=128+(i//4)*286
  d.rounded_rectangle((x,y,x+249,y+268),radius=12,fill='#1b2a31',outline='#31454b')
  model=json.loads((ASSET/'models/block'/f'{kind}_cluster.json').read_text());img=render(model)
  im.paste(img,(x+14,y+8),img)
  item=json.loads((ASSET/'models/item'/f'{kind}.json').read_text());gem=render(item,90,3.5);im.paste(gem,(x+160,y+122),gem)
  d.text((x+16,y+218),ru,font=font,fill='#eeeadd');d.text((x+16,y+245),f'{en} · свет {light}',font=small,fill='#91b0b4')
 d.text((38,height-40),'Рендер моделей из JAR. Это не скриншот из игры.',font=small,fill='#91b0b4')
 out=ROOT/'docs/articrystals-models.png';out.parent.mkdir(exist_ok=True);im.save(out)
 # The branded icon is maintained separately; gallery rendering must preserve it.
 print(out)
if __name__=='__main__':main()
