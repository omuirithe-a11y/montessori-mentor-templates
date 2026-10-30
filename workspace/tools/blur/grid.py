"""Draw working-coordinate grid on the ORIGINAL (unblurred) full image region of a face, in the run's orientation.
usage: python3 grid.py <set.json> <tag> <dst.jpg> [step]"""
import json, cv2, numpy as np, os, sys
S=json.load(open(sys.argv[1])); tag=sys.argv[2]; dst=sys.argv[3]; step=int(sys.argv[4]) if len(sys.argv)>4 else 0
r=json.load(open(os.path.join(S['out'],'faces.json')))
name,f=[(n,f) for n,v in r.items() for f in v['faces'] if f['tag']==tag][0]
stem=name.rsplit('.',1)[0]; res=cv2.imread(os.path.join(S['out'],'images',stem+'.jpg'))
src=[x for x in os.listdir(S['media']) if x.rsplit('.',1)[0]==stem][0]; o=cv2.imread(os.path.join(S['media'],src))
if o is None or o.shape!=res.shape: o=res; print('WARNING: original differs in shape/orientation - grid on the result')
K=f['full_box'][0]/f['box'][0] if f['box'][0] else f['full_box'][2]/f['box'][2]; x0,y0,x1,y1=f['full_box']; w=x1-x0; h=y1-y0
X0=int(max(0,x0-0.6*w)); X1=int(min(o.shape[1],x1+0.6*w)); Y0=int(max(0,y0-0.4*h)); Y1=int(min(o.shape[0],y1+0.4*h))
step=step or max(2,int(round((f['box'][2]-f['box'][0])/8)))
out=[]
for im in (o,res):
    c=im[Y0:Y1,X0:X1].copy(); s=600/c.shape[0]; c=cv2.resize(c,(int(c.shape[1]*s),600))
    for wx in range(int(X0/K)//step*step, int(X1/K)+step, step):
        px=int((wx*K-X0)*s); cv2.line(c,(px,0),(px,600),(0,255,255),1); cv2.putText(c,str(wx),(px+1,12),0,0.35,(0,255,255),1)
    for wy in range(int(Y0/K)//step*step, int(Y1/K)+step, step):
        py=int((wy*K-Y0)*s); cv2.line(c,(0,py),(c.shape[1],py),(255,255,0),1); cv2.putText(c,str(wy),(1,py-1),0,0.35,(255,255,0),1)
    out.append(c)
cv2.imwrite(dst,np.hstack(out)); print(tag,'box',f['box'],'K',round(K,3))
