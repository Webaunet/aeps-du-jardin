#!/usr/bin/env python3
"""Génère les pages HTML à partir de outils/pages/*.html (corps) + en-tête/pied communs.
Ajoute width/height/loading aux images, puis contrôle que tous les liens relatifs existent."""
import os, re, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://webaunet.github.io/aeps-du-jardin/'
TEL, TEL_HREF, MAIL = '06 12 77 91 71', 'tel:+33612779171', 'a.e.p.s.dujardin@gmail.com'
NOM, COMMUNE, LOGO = 'AEPS du Jardin', 'Évecquemont', 'images/logo-aeps-du-jardin.png'

PAGES = [
 ('index.html', 'Accueil', 'index', "AEPS du Jardin, arboriste-grimpeur et paysagiste à Évecquemont (78)",
  "AEPS du Jardin à Évecquemont (Yvelines) : élagage, abattage, soins des arbres et aménagement paysager. Devis gratuit au 06 12 77 91 71."),
 ('nos-prestations.html', 'Nos prestations', 'prestations', "Nos prestations : élagage, abattage, paysage | AEPS du Jardin",
  "Élagage, abattage, soins des arbres, aménagement paysager, destruction de guêpes, frelons et chenilles processionnaires : les prestations d'AEPS du Jardin à Évecquemont."),
 ('nos-realisations.html', 'Nos réalisations', 'realisations', "Nos réalisations d'arbres et de jardins | AEPS du Jardin à Évecquemont",
  "Aperçu en images des métiers d'AEPS du Jardin, arboriste-grimpeur et paysagiste à Évecquemont : arbres, aménagements et entretien d'espaces verts."),
 ('a-propos.html', 'À propos', 'apropos', "À propos d'AEPS du Jardin, arboriste-grimpeur à Évecquemont",
  "AEPS du Jardin, société basée à Évecquemont (78) : arboriste-grimpeur et paysagiste. Découvrez nos activités et notre façon de travailler."),
 ('nous-contacter.html', 'Nous contacter', 'contact', "Contacter AEPS du Jardin à Évecquemont | Devis gratuit",
  "Demandez un devis gratuit à AEPS du Jardin, arboriste-grimpeur et paysagiste à Évecquemont : formulaire, téléphone 06 12 77 91 71 et e-mail."),
 ('mentions-legales.html', None, 'mentions', "Mentions légales | AEPS du Jardin, Évecquemont",
  "Mentions légales du site d'AEPS du Jardin, arboriste-grimpeur et paysagiste à Évecquemont (SIREN 999 196 587)."),
]

def head(title, desc, canon):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="images/logo-aeps-du-jardin.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
'''

def header(key):
    items = ''
    for f, label, k, *_ in PAGES:
        if label is None: continue
        cur = ' aria-current="page"' if k == key else ''
        items += f'        <li><a href="{f}"{cur}>{label}</a></li>\n'
    return f'''<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{SITE}" aria-label="AEPS du Jardin, accueil du site">
      <img src="images/logo-aeps-du-jardin.png" alt="Logo AEPS du Jardin : un chêne vert dans un cercle gris"><span>AEPS du Jardin<small>Évecquemont</small></span>
    </a>
    <nav id="menu" aria-label="Navigation principale">
      <ul>
{items}      </ul>
    </nav>
    <div class="head-right">
      <a class="btn cta-head" href="{TEL_HREF}" aria-label="Appeler le {TEL}"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11 11 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.6 3.6a1 1 0 0 1-.25 1z"/></svg><span class="t">{TEL}</span><span class="t2">Appeler</span></a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span></button>
    </div>
  </div>
</header>
<main id="main">
'''

FOOT = f'''</main>
<footer>
  <div class="wrap foot">
    <a class="brand" href="{SITE}" aria-label="AEPS du Jardin, accueil du site"><img src="images/logo-aeps-du-jardin.png" alt="Logo AEPS du Jardin"><span>AEPS du Jardin<small>Évecquemont</small></span></a>
    <ul aria-label="Liens du pied de page">
      <li><a href="{TEL_HREF}">{TEL}</a></li>
      <li><a href="mailto:{MAIL}">{MAIL}</a></li>
      <li><a href="nos-prestations.html">Prestations</a></li>
      <li><a href="nous-contacter.html">Contact</a></li>
      <li><a href="mentions-legales.html">Mentions légales</a></li>
    </ul>
    <small>© AEPS du Jardin · SIREN 999 196 587 · Évecquemont · Maquette de présentation</small>
  </div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="js/main.js" defer></script>
</body>
</html>
'''

def fix_imgs(html):
    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        if not src.startswith('http'):
            w, h = Image.open(os.path.join(ROOT, src)).size
            if 'width=' not in tag: tag = tag.replace('<img ', f'<img width="{w}" height="{h}" ', 1)
        if 'data-eager' in tag:
            tag = tag.replace(' data-eager', '').replace('<img ', '<img fetchpriority="high" ', 1)
        elif 'loading=' not in tag and 'logo-aeps' not in tag:
            tag = tag.replace('<img ', '<img loading="lazy" ', 1)
        return tag
    return re.sub(r'<img [^>]*>', rep, html)

def main():
    names = {}
    for f, label, key, title, desc in PAGES:
        body = open(os.path.join(ROOT, 'outils', 'pages', key + '.html'), encoding='utf-8').read()
        full = head(title, desc, f) + header(key) + body + FOOT
        full = fix_imgs(full.replace('src="images/logo-aeps-du-jardin.png"', 'width="192" height="192" src="images/logo-aeps-du-jardin.png"'))
        open(os.path.join(ROOT, f), 'w', encoding='utf-8').write(full)
        names[f] = full
    bad = []
    for f, html in names.items():
        for u in re.findall(r'(?:href|src)="([^"]+)"', html):
            if re.match(r'(https?:|tel:|mailto:|sms:|#)', u): continue
            p = u.split('#')[0]
            if p and not os.path.exists(os.path.join(ROOT, p)): bad.append((f, u))
        ids = set(re.findall(r'id="([^"]+)"', html))
        for u in re.findall(r'href="([^"]*#[^"]+)"', html):
            page, frag = u.split('#', 1)
            if page == '' and frag not in ids: bad.append((f, u))
            elif page in names and frag not in set(re.findall(r'id="([^"]+)"', names[page])): bad.append((f, u))
    print('pages:', len(names), '| liens/ancres cassés:', bad if bad else 'aucun')
    sys.exit(1 if bad else 0)

main()
