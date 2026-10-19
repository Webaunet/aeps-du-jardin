#!/usr/bin/env python3
"""Génère les pages HTML à partir de outils/pages/*.html (corps) + en-tête/pied communs.
Ajoute width/height/loading aux images, puis contrôle que tous les liens relatifs existent."""
import os, re, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://webaunet.github.io/allibertpaysage/'
TEL, TEL_HREF, MAIL = '06 20 27 30 80', 'tel:+33620273080', 'geoffroy.allibert@gmail.com'

PAGES = [
 ('index.html', 'Accueil', 'index', "Allibert Paysage, paysagiste à Versailles : conception, création et entretien de jardins",
  "Allibert Paysage à Versailles : conception, création et entretien d'espaces verts par une équipe unique, sans sous-traitance. Devis au 06 20 27 30 80."),
 ('nos-prestations.html', 'Nos prestations', 'prestations', "Nos prestations de paysagiste à Versailles | Allibert Paysage",
  "Conception, création d'aménagements extérieurs, entretien, élagage et abattage : toutes les prestations d'Allibert Paysage à Versailles et alentours."),
 ('nos-realisations.html', 'Nos réalisations', 'realisations', "Nos réalisations de jardins à Versailles | Allibert Paysage",
  "Conceptions, créations et entretiens de jardins par Allibert Paysage, paysagiste à Versailles : aperçu en images de nos trois métiers."),
 ('a-propos.html', 'À propos', 'apropos', "À propos d'Allibert Paysage, paysagiste à Versailles",
  "Une seule équipe, des fournisseurs français et une méthode en quatre étapes : découvrez Allibert Paysage, paysagiste à Versailles."),
 ('nous-contacter.html', 'Nous contacter', 'contact', "Contacter Allibert Paysage à Versailles | Devis paysagiste",
  "Demandez un devis à Allibert Paysage, paysagiste à Versailles : formulaire, téléphone 06 20 27 30 80 et e-mail. Du lundi au vendredi, 7 h à 19 h."),
 ('mentions-legales.html', None, 'mentions', "Mentions légales | Allibert Paysage, Versailles",
  "Mentions légales du site d'Allibert Paysage, paysagiste à Versailles (SIREN 833 518 467)."),
]

def head(title, desc, canon):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="images/logo-allibert-paysage.png">
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
    <a class="brand" href="{SITE}" aria-label="Allibert Paysage, accueil du site">
      <img src="images/logo-allibert-paysage.png" alt="Logo Allibert Paysage : cercle vert avec feuillage et champs"><span>Allibert Paysage<small>Versailles</small></span>
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
    <a class="brand" href="{SITE}" aria-label="Allibert Paysage, accueil du site"><img src="images/logo-allibert-paysage.png" alt="Logo Allibert Paysage"><span>Allibert Paysage<small>Versailles</small></span></a>
    <ul aria-label="Liens du pied de page">
      <li><a href="{TEL_HREF}">{TEL}</a></li>
      <li><a href="mailto:{MAIL}">{MAIL}</a></li>
      <li><a href="nos-prestations.html">Prestations</a></li>
      <li><a href="nous-contacter.html">Contact</a></li>
      <li><a href="mentions-legales.html">Mentions légales</a></li>
    </ul>
    <small>© Allibert Paysage · SIREN 833 518 467 · Versailles · Maquette de présentation</small>
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
        elif 'loading=' not in tag and 'logo-allibert' not in tag:
            tag = tag.replace('<img ', '<img loading="lazy" ', 1)
        return tag
    return re.sub(r'<img [^>]*>', rep, html)

def main():
    names = {}
    for f, label, key, title, desc in PAGES:
        body = open(os.path.join(ROOT, 'outils', 'pages', key + '.html'), encoding='utf-8').read()
        full = head(title, desc, f) + header(key) + body + FOOT
        full = fix_imgs(full.replace('src="images/logo-allibert-paysage.png"', 'width="128" height="128" src="images/logo-allibert-paysage.png"'))
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
