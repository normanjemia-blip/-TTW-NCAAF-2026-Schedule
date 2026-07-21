from pathlib import Path
import hashlib, zipfile, xml.etree.ElementTree as ET, os, re, json
from decimal import Decimal, InvalidOperation

SRC=Path('/mnt/data/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE.xlsx')
RT=Path('/mnt/data/TTW_NCAAF_Power_Ratings_2026_v0.6.2_AUTHORITATIVE')
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','p':'http://schemas.openxmlformats.org/package/2006/relationships'}

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def c2n(c):
    n=0
    for x in c: n=n*26+ord(x)-64
    return n

def n2c(n):
    s=''
    while n:
        n,r=divmod(n-1,26); s=chr(65+r)+s
    return s

def split_ref(ref):
    m=re.match(r'([A-Z]+)(\d+)$',ref); return m.group(1),int(m.group(2))

class X:
    def __init__(self,p):
        self.p=p; self.z=zipfile.ZipFile(p); self.ss=self._ss(); self.sheets=self._sheets(); self.cells={s['name']:self._cells(s) for s in self.sheets}; self.calc=self._calc()
    def _ss(self):
        if 'xl/sharedStrings.xml' not in self.z.namelist(): return []
        root=ET.fromstring(self.z.read('xl/sharedStrings.xml')); out=[]
        for si in root.findall('m:si',NS): out.append(''.join((t.text or '') for t in si.iter('{%s}t'%NS['m'])))
        return out
    def _sheets(self):
        wb=ET.fromstring(self.z.read('xl/workbook.xml')); rel=ET.fromstring(self.z.read('xl/_rels/workbook.xml.rels'))
        mp={x.attrib['Id']:x.attrib['Target'] for x in rel}
        out=[]
        for s in wb.find('m:sheets',NS):
            rid=s.attrib['{%s}id'%NS['r']]; t=mp[rid]; path=t.lstrip('/') if t.startswith('/') else ('xl/'+t if not t.startswith('xl/') else t)
            out.append({'name':s.attrib['name'],'state':s.attrib.get('state','visible'),'sheetId':s.attrib['sheetId'],'path':os.path.normpath(path).replace('\\','/')})
        return out
    def _calc(self):
        wb=ET.fromstring(self.z.read('xl/workbook.xml')); c=wb.find('m:calcPr',NS); return dict(c.attrib) if c is not None else {}
    def _cells(self,s):
        root=ET.fromstring(self.z.read(s['path'])); out={}
        for c in root.findall('.//m:sheetData/m:row/m:c',NS):
            ref=c.attrib['r']; t=c.attrib.get('t'); f=c.find('m:f',NS); v=c.find('m:v',NS); isel=c.find('m:is',NS)
            formula=None if f is None else (f.text or ''); attrs={} if f is None else dict(f.attrib)
            val=None
            if t=='s' and v is not None:
                val=self.ss[int(v.text)]
            elif t=='inlineStr' and isel is not None:
                val=''.join((tt.text or '') for tt in isel.iter('{%s}t'%NS['m']))
            elif v is not None:
                val=v.text or ''
            out[ref]={'formula':formula,'fattrs':attrs,'value':val,'type':t,'style':c.attrib.get('s')}
        return out
    def formulas(self):
        return {(sh,ref):c['formula'] for sh,cs in self.cells.items() for ref,c in cs.items() if c['formula'] is not None}

CELL_RE=re.compile(r'(?<![A-Za-z0-9_.])(?P<sheet>(?:\'(?:(?:[^\']|\'\')*)\'|[A-Za-z_][A-Za-z0-9_.]*)!)?(?P<ca>\$?)(?P<c>[A-Z]{1,3})(?P<ra>\$?)(?P<r>\d+)(?![A-Za-z0-9_])')
def canon_seg(seg,cc,rr):
    def repl(m):
        sh=m.group('sheet') or ''; cn=c2n(m.group('c')); rn=int(m.group('r'))
        ct=('CA'+str(cn)) if m.group('ca') else ('CR%+d'%(cn-cc)); rt=('RA'+str(rn)) if m.group('ra') else ('RR%+d'%(rn-rr))
        return sh+'['+ct+','+rt+']'
    return CELL_RE.sub(repl,seg)
def canon(formula,ref):
    col,row=split_ref(ref); cc=c2n(col); out=[]; i=0; start=0; ins=False
    while i<len(formula):
        if formula[i]=='"':
            if ins and i+1<len(formula) and formula[i+1]=='"': i+=2; continue
            if not ins:
                out.append(canon_seg(formula[start:i],cc,row)); start=i; ins=True
            else:
                i+=1; out.append(formula[start:i]); start=i; ins=False; continue
        i+=1
    out.append(formula[start:] if ins else canon_seg(formula[start:],cc,row)); return ''.join(out)

def nonblank(x,sh,cols,r1,r2):
    n=0
    for col in cols:
        for r in range(r1,r2+1):
            c=x.cells[sh].get(f'{col}{r}')
            if c and c['formula'] is None and c['value'] not in (None,''): n+=1
    return n

def val(x,sh,ref):
    c=x.cells[sh].get(ref); return None if not c else c['value']

S=X(SRC); R=X(RT); sf=S.formulas(); rf=R.formulas()
checks={}
checks['source_sha256']=sha256(SRC); checks['roundtrip_sha256']=sha256(RT)
checks['sheet_count_source']=len(S.sheets); checks['sheet_count_roundtrip']=len(R.sheets)
checks['sheet_order_states_equal']=[(s['name'],s['state']) for s in S.sheets]==[(s['name'],s['state']) for s in R.sheets]
checks['formula_count_source']=len(sf); checks['formula_count_roundtrip']=len(rf); checks['formula_coordinates_equal']=set(sf)==set(rf)
# exact formula diffs should be precisely shared-formula followers
exact_diffs=[k for k in sf if sf[k]!=rf[k]]
shared_bases=[]; shared_followers=0; shared_ok=True
for sh,cs in R.cells.items():
    for ref,c in cs.items():
        if c['formula'] is not None and c['fattrs'].get('t')=='shared':
            if c['formula']:
                shared_bases.append((sh,ref,c['fattrs']['ref'],c['fattrs']['si']))
            else: shared_followers+=1
for sh,base,rng,si in shared_bases:
    st,en=rng.split(':'); col,r1=split_ref(st); _,r2=split_ref(en); basecanon=canon(sf[(sh,base)],base)
    for r in range(r1,r2+1):
        ref=f'{col}{r}'; c=R.cells[sh].get(ref)
        if not c or c['fattrs'].get('t')!='shared' or c['fattrs'].get('si')!=si or canon(sf[(sh,ref)],ref)!=basecanon:
            shared_ok=False; break
checks['exact_formula_text_differences']=len(exact_diffs)
checks['shared_formula_groups']=len(shared_bases); checks['shared_formula_followers']=shared_followers
checks['shared_formula_semantics_equal']=shared_ok and len(exact_diffs)==shared_followers
# target ranges
clean_exact=True
for col in ['C','D']:
    for r in range(6,1006):
        k=('CLEAN',f'{col}{r}')
        if sf.get(k)!=rf.get(k): clean_exact=False
checks['clean_C6_D1005_exact']=clean_exact
# ADJ J exact, K semantic via canonicalization
adjJ=True; adjK=True
for r in range(6,256):
    if sf[('ADJUSTMENTS',f'J{r}')]!=rf[('ADJUSTMENTS',f'J{r}')]: adjJ=False
    if canon(sf[('ADJUSTMENTS',f'K{r}')],f'K{r}')!=canon(sf[('ADJUSTMENTS','K6')],'K6'): adjK=False
checks['adjustments_J_unchanged']=adjJ; checks['adjustments_K_semantics_unchanged']=adjK
checks['start_here_A1']=val(R,'START HERE','A1')
checks['start_here_has_v062']='v0.6.2' in (val(R,'START HERE','A1') or '')
checks['changelog_v062_exact']=all(S.cells['CHANGELOG'].get(f'{c}57',{}).get('value')==R.cells['CHANGELOG'].get(f'{c}57',{}).get('value') for c in ['A','B','C','D'])
checks['source_calc_props']=S.calc; checks['roundtrip_calc_props']=R.calc
checks['native_recalc_evidence']={
  'games_loaded':val(R,'DATA QUALITY','B6'), 'blocked':val(R,'DATA QUALITY','B7'), 'pending_line':val(R,'DATA QUALITY','B8'),
  'data_incomplete':val(R,'DATA QUALITY','B12'), 'fcs_no_play':val(R,'DATA QUALITY','B21'), 'audit_failures':val(R,'DATA QUALITY','B20')
}
checks['market_line_input_cells_nonblank']=nonblank(R,'MARKET LINES',list('ABCDEFGH'),6,1005)
checks['adjustment_input_cells_nonblank']=nonblank(R,'ADJUSTMENTS',list('ABCDEFGHI'),6,255)
checks['stats_input_cells_nonblank']=nonblank(R,'IMPORT STATS',[n2c(i) for i in range(1,11)],6,205)
checks['bet_toggle']=val(R,'SETTINGS','B11')
# constants semantic compare allowing normal Google numeric serialization / float rounding
substantive=[]; repr_only=0
for sh in [s['name'] for s in S.sheets]:
    refs=set(S.cells[sh])|set(R.cells[sh])
    for ref in refs:
        a=S.cells[sh].get(ref); b=R.cells[sh].get(ref)
        if (a and a['formula'] is not None) or (b and b['formula'] is not None): continue
        av=None if not a else a['value']; bv=None if not b else b['value']
        if av==bv: continue
        try:
            if av is not None and bv is not None and abs(float(av)-float(bv))<=1e-12*max(1,abs(float(av)),abs(float(bv))): repr_only+=1; continue
        except: pass
        substantive.append((sh,ref,av,bv))
checks['constant_numeric_serialization_differences']=repr_only
checks['substantive_constant_differences']=len(substantive)
checks['substantive_constant_difference_samples']=substantive[:10]
# overall: calcPr removal is explicitly classified as Google package-level because native results are recalculated.
checks['overall_pass']=all([
 checks['sheet_count_source']==21, checks['sheet_count_roundtrip']==21, checks['sheet_order_states_equal'],
 checks['formula_count_source']==123011, checks['formula_count_roundtrip']==123011, checks['formula_coordinates_equal'], checks['shared_formula_semantics_equal'],
 checks['clean_C6_D1005_exact'],checks['adjustments_J_unchanged'],checks['adjustments_K_semantics_unchanged'],checks['start_here_has_v062'],checks['changelog_v062_exact'],
 checks['native_recalc_evidence']=={'games_loaded':'888','blocked':'0','pending_line':'761','data_incomplete':'0','fcs_no_play':'127','audit_failures':'0'},
 checks['market_line_input_cells_nonblank']==0,checks['adjustment_input_cells_nonblank']==0,checks['stats_input_cells_nonblank']==0,checks['bet_toggle']=='N',
 checks['substantive_constant_differences']==0
])
print(json.dumps(checks,indent=2,ensure_ascii=False))
Path('/mnt/data/v062_roundtrip_verification.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False),encoding='utf-8')
