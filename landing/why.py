"""«Почему ONEFLOW» — the advantages as a bento grid (by request, 2026-11-11), in place of the tabbed «Возможности»
section: cheaper, a balance that does not burn, one account; then the three advertising tools (adaptation to the ad
cabinets, the click-appeal score, the marketplace card) and one tile for everything else with the main button.

The markup is why_section.html and the styles why.css (plain files, so they open in an editor as they are). The
pictures are the page's own: the «made in ONEFLOW» ads (--mi0…) and the product photo (--img-airbuds), no new files.
The section has its own id (#why), so texts edited in /admin for the old #modes section never land on these.
The scores and the product in the pictures are examples, not data.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def why_html():
    return open(os.path.join(HERE, 'why_section.html'), encoding='utf-8').read().strip()


def why_css():
    return '\n/* «Почему ONEFLOW»: the advantages, a bento grid */\n' + open(os.path.join(HERE, 'why.css'), encoding='utf-8').read()
