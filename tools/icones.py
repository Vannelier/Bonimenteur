"""Favicon et icônes d'application : le sceau de cire rouge, traversé de la plume
dorée du faussaire, sur le cuir vert du sous-main (docs/direction-artistique.md).

Une seule source, le SVG dessiné ici, écrit dans prototype/favicon.svg puis rendu
par Chromium : prototype/favicon.ico (16, 32, 48 px), prototype/img/icon-192.png,
prototype/img/icon-512.png (fond transparent : le sceau et la plume seuls, demande de
l'auteur, 25/11/2026) et prototype/img/apple-touch-icon.png (180 px sur le cuir, plein
cadre : iOS remplit de noir ce qui est transparent, et arrondit lui-même).
Même méthode que tools/icones.py de Discoverium : ICO à frames BMP 32 bits (le
décodeur d'icônes de Bing lit mal les frames PNG, constaté sur Vocabulium).

    pip install playwright pillow
    python tools/icones.py [--chrome /opt/pw-browsers/chromium]
"""
import argparse
import io
import struct
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

RACINE = Path(__file__).resolve().parent.parent
PAGE = RACINE / "prototype"


def icone(cuir: bool) -> str:
    """SVG 64 × 64. `cuir` : sur le cuir vert, plein cadre (icône iOS) ; sinon fond
    transparent (favicon, icônes du manifeste)."""
    fond = '<rect width="64" height="64" fill="url(#cuir)"/>' if cuir else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <title>Bonimenteur</title>
  <!-- Généré par tools/icones.py : le sceau de cire rouge et la plume dorée du
       faussaire (fond transparent ; le cuir vert du sous-main pour iOS). -->
  <defs>
    <radialGradient id="cuir" cx="50%" cy="12%" r="95%">
      <stop offset="0" stop-color="#2c4a3a"/><stop offset=".6" stop-color="#15281f"/>
      <stop offset="1" stop-color="#0b1712"/>
    </radialGradient>
    <linearGradient id="or" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff1bf"/><stop offset=".5" stop-color="#e7c869"/>
      <stop offset="1" stop-color="#b8973f"/>
    </linearGradient>
  </defs>
  {fond}
  <g transform="translate(5 6) scale(.9)">
    <path fill="#9e2e25" d="M30 3c4 0 5 3 8.5 4s6.5-1 9 1.7.8 6.2 2.5 9.3 5 4 5 8-3 5.2-4 8.6 1 6.6-1.7 9.3-6.2.8-9.3 2.5S34 57 30 57s-5.2-3-8.6-4-6.6 1-9.3-1.7-.8-6.2-2.5-9.3S4 34 4 30s3-5.2 4-8.6-1-6.6 1.7-9.3 6.2-.8 9.3-2.5S26 3 30 3z" transform="translate(1.5 2)"/>
    <path fill="#d24a3c" d="M30 3c4 0 5 3 8.5 4s6.5-1 9 1.7.8 6.2 2.5 9.3 5 4 5 8-3 5.2-4 8.6 1 6.6-1.7 9.3-6.2.8-9.3 2.5S34 57 30 57s-5.2-3-8.6-4-6.6 1-9.3-1.7-.8-6.2-2.5-9.3S4 34 4 30s3-5.2 4-8.6-1-6.6 1.7-9.3 6.2-.8 9.3-2.5S26 3 30 3z"/>
    <circle cx="30" cy="30" r="18" fill="none" stroke="#b23a2e" stroke-width="2"/>
    <ellipse cx="21" cy="15" rx="7" ry="3" fill="#fff" opacity=".3" transform="rotate(-30 21 15)"/>
  </g>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M55 7C37 8 26 19 21.5 36L18 52" stroke="#5a3a10" stroke-width="6.5" opacity=".7"/>
    <path d="M55 7C55.5 23 46 34 28.5 37" stroke="#5a3a10" stroke-width="6.5" opacity=".7"/>
    <path d="M55 7C37 8 26 19 21.5 36L18 52" stroke="url(#or)" stroke-width="3.6"/>
    <path d="M55 7C55.5 23 46 34 28.5 37" stroke="url(#or)" stroke-width="3.6"/>
    <path d="M34 22L45 22M30 29L40 30" stroke="url(#or)" stroke-width="2.4"/>
  </g>
</svg>
"""


def ico(images: list[Image.Image]) -> bytes:
    """ICO à frames BMP 32 bits (BITMAPINFOHEADER + masque AND), sans PNG.

    Le masque AND porte la même transparence que l'alpha : un masque tout à zéro dit
    « tout opaque », et les décodeurs qui le suivent plutôt que l'alpha affichaient le
    pourtour du sceau en noir (carré noir derrière l'icône, signalé le 26/11/2026).
    Discoverium ne le voyait pas : son icône est un carré plein."""
    entetes, corps = [], []
    decalage = 6 + 16 * len(images)
    for im in images:
        w, h = im.size
        im = im.convert("RGBA")
        lignes, bits = [], []
        for y in range(h - 1, -1, -1):                       # de bas en haut
            ligne = []
            for x in range(w):
                r, g, b, a = im.getpixel((x, y))
                lignes.append(bytes((b, g, r, a)))
                ligne.append(0 if a >= 128 else 1)            # 1 = pixel transparent
            ligne += [0] * (-len(ligne) % 32)                # lignes du masque alignées sur 4 octets
            bits.append(bytes(int("".join(map(str, ligne[i:i + 8])), 2) for i in range(0, len(ligne), 8)))
        pixels = b"".join(lignes)
        masque = b"".join(bits)
        bih = struct.pack("<IiiHHIIiiII", 40, w, h * 2, 1, 32, 0, len(pixels) + len(masque), 0, 0, 0, 0)
        blob = bih + pixels + masque
        entetes.append(struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(blob), decalage))
        corps.append(blob)
        decalage += len(blob)
    return struct.pack("<HHH", 0, 1, len(images)) + b"".join(entetes) + b"".join(corps)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default="/opt/pw-browsers/chromium")
    args = ap.parse_args()
    transparent, plein = icone(False), icone(True)
    (PAGE / "favicon.svg").write_text(transparent, encoding="utf-8")
    (PAGE / "img").mkdir(exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=args.chrome if Path(args.chrome).exists() else None)

        def png(svg: str, taille: int) -> Image.Image:
            page = nav.new_page(viewport={"width": taille, "height": taille})
            page.set_content("<style>html,body{margin:0;background:transparent}"
                             f"svg{{display:block;width:{taille}px;height:{taille}px}}</style>{svg}")
            data = page.screenshot(omit_background=True)
            page.close()
            return Image.open(io.BytesIO(data)).convert("RGBA")

        (PAGE / "favicon.ico").write_bytes(ico([png(transparent, t) for t in (16, 32, 48)]))
        png(transparent, 192).save(PAGE / "img" / "icon-192.png")
        png(transparent, 512).save(PAGE / "img" / "icon-512.png")
        png(plein, 180).convert("RGB").save(PAGE / "img" / "apple-touch-icon.png")
        nav.close()
    print("écrit : favicon.svg, favicon.ico, img/icon-192.png, img/icon-512.png, img/apple-touch-icon.png")


if __name__ == "__main__":
    main()
