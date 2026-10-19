# Optimise les images sources (dossier Paysagiste) vers images/ : WebP q78-80, 800 px (cartes) ou 1280 px (hero). Jamais agrandi.
import sys, os
from PIL import Image, ImageDraw
SRC = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/Maquettes/Images/Paysagiste/imgi_'
LOGO = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/uploads/1792446843231_image.png'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
M = {'7_entretien-jardin':('jardin-maison-pierre',1280,78),'4_creation-espace-vert':('creation-massifs-allee',720,78),
'6_plantation':('plantation-arbuste',720,78),'7_terrassement':('terrassement-jardin',720,78),'8_nivellement':('nivellement-terrain',720,78),
'2_tonte':('tonte-pelouse',720,78),'1_taille-haies':('taille-haie-laurier',720,78),'4_desherbage':('desherbage-massif',720,78),
'5_feuilles':('ramassage-feuilles',720,78),'1_elagage-chene':('elagage-chene',720,78),'3_dessouchage':('rognage-souche',720,78),
'7_dechets-verts':('evacuation-dechets-verts',720,78),'10_nettoyage':('nettoyage-jardin',720,78),'3_entretien-general':('entretien-general',720,78),
'1_hero-elagage-chene':('elagage-maison-briques',720,78),'4_taille-haies':('taille-haie-allee',720,78)}
for k,(n,w,q) in M.items():
    im = Image.open(SRC+k+'.jpg').convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, n+'.webp'), 'WEBP', quality=q, method=6)
    print(n, im.size)
lg = Image.open(LOGO).convert('RGBA'); cx, cy, r = 330, 345, 253
c = lg.crop((cx-r-4, cy-r-4, cx+r+4, cy+r+4)); m = Image.new('L', c.size, 0)
ImageDraw.Draw(m).ellipse((2, 2, c.width-2, c.height-2), fill=255)
o = Image.new('RGBA', c.size, (0,0,0,0)); o.paste(c, (0,0), m); o = o.resize((128,128), Image.LANCZOS)
o.save(os.path.join(OUT, 'logo-allibert-paysage.png'), optimize=True)
