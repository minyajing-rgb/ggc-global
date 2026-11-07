#!/usr/bin/env python3
"""Build original, product-specific SVG editorial illustrations for the public Lab.

These are concept illustrations, not screenshots or claims of released features.
Keep the scenes text-free so the same art works on the Chinese and English pages.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "product-art"
OUT.mkdir(parents=True, exist_ok=True)


def card(x, y, w, h, body='', fill='#fff', r=22, opacity=1):
    return f'<g opacity="{opacity}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#d8d6f6" stroke-width="2"/>{body}</g>'


def line(x1, y1, x2, y2, color='#9d81ed', width=5, dash=''):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash_attr}/>'


def dot(x, y, r=12, fill='#7a4ee3'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def bars(x, y, heights, color='#7953e6'):
    return ''.join(f'<rect x="{x+i*32}" y="{y-h}" width="19" height="{h}" rx="7" fill="{color}" opacity="{.48+i*.11}"/>' for i, h in enumerate(heights))


SCENES = {
    'intelligence': (
        '#ddd9ff', '#8556e9',
        card(80, 128, 210, 250, bars(125, 320, [57, 95, 133, 82]) + line(120, 340, 246, 340, '#ced1ed', 3))
        + card(340, 94, 265, 318, ''.join(line(389, 165+i*56, 551, 165+i*56, '#dfdcf3', 14) for i in range(4)) + dot(390, 165, 16, '#eb55ae') + dot(500, 221, 16, '#7a4ee3') + dot(430, 277, 16, '#398ed8'))
        + card(656, 146, 210, 226, '<path d="M704 291l49 35 73-110" fill="none" stroke="#25a79a" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
        + line(290, 253, 339, 253) + line(606, 253, 655, 253),
    ),
    'creative': (
        '#ffe0f1', '#ec58a7',
        ''.join(card(85+i*270, 120+(i%2)*28, 218, 262,
            f'<rect x="{107+i*270}" y="{145+(i%2)*28}" width="174" height="120" rx="14" fill="{["#decfff", "#f7c1de", "#c6e9fa"][i]}"/>'
            + f'<circle cx="{160+i*270}" cy="{207+(i%2)*28}" r="28" fill="white" opacity=".85"/>'
            + line(112+i*270, 301+(i%2)*28, 254+i*270, 301+(i%2)*28, '#cab9dc', 10)
            + line(112+i*270, 328+(i%2)*28, 210+i*270, 328+(i%2)*28, '#ded4ed', 8)) for i in range(3)),
    ),
    'outbound': (
        '#dceeff', '#527de4',
        card(86, 135, 223, 244, dot(158, 203, 32, '#a3ccfa') + dot(237, 203, 32, '#bfa4f7') + line(132, 275, 270, 275, '#c6d2eb', 12) + line(132, 307, 235, 307, '#dce4f3', 10))
        + card(369, 97, 223, 320, dot(440, 174, 32, '#f4b9d7') + dot(518, 174, 32, '#b6d3f8') + line(406, 251, 550, 251, '#c6d2eb', 12) + line(406, 285, 508, 285, '#dce4f3', 10) + line(406, 319, 538, 319, '#dce4f3', 10))
        + card(651, 137, 223, 244, '<path d="M704 251l42 40 74-98" fill="none" stroke="#31b79e" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>')
        + line(309, 257, 368, 257) + line(592, 257, 650, 257),
    ),
    'copilot': (
        '#e2e1ff', '#7f64e9',
        card(110, 90, 740, 340,
            '<rect x="110" y="90" width="740" height="56" rx="22" fill="#34316f"/>'
            + card(150, 178, 290, 205, bars(192, 341, [59, 108, 76, 136, 98]), '#f8f8ff', 14)
            + card(465, 178, 345, 87, dot(506, 221, 17, '#41baa8') + line(542, 221, 767, 221, '#c9c6e9', 12), '#f8f8ff', 14)
            + card(465, 283, 345, 100, '<path d="M505 337l53-25 51 16 55-40 57 17 53-9" fill="none" stroke="#e05db4" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>', '#f8f8ff', 14)),
    ),
    'steam': (
        '#dce8ff', '#4a71ce',
        card(125, 80, 700, 360,
            '<rect x="125" y="80" width="700" height="64" rx="22" fill="#1d3159"/>'
            + '<rect x="160" y="174" width="365" height="212" rx="13" fill="#5772c9"/>'
            + '<path d="M210 332l84-99 49 55 59-79 79 123z" fill="#a0baf0"/>'
            + line(563, 196, 777, 196, '#bbbfe5', 16)
            + line(563, 238, 755, 238, '#d7d8ec', 10)
            + line(563, 268, 730, 268, '#d7d8ec', 10)
            + '<rect x="563" y="326" width="165" height="40" rx="10" fill="#3aade5"/>'),
    ),
    'intel': (
        '#e0e9ff', '#588de3',
        card(120, 86, 720, 360,
            '<circle cx="480" cy="265" r="146" fill="#f1f5ff" stroke="#d5def6" stroke-width="3"/>'
            + '<circle cx="480" cy="265" r="91" fill="none" stroke="#c9d8f4" stroke-width="3"/>'
            + '<circle cx="480" cy="265" r="39" fill="none" stroke="#c9d8f4" stroke-width="3"/>'
            + line(480, 265, 622, 162, '#6b75df', 8)
            + dot(622, 162, 21, '#eb5cac') + dot(380, 193, 15, '#45bdb4') + dot(533, 321, 13, '#697de4')
            + bars(168, 381, [34, 56, 76, 47], '#8b6de8')),
    ),
    'casino': (
        '#fce0ed', '#cf5d9f',
        card(145, 92, 670, 350,
            '<rect x="190" y="132" width="580" height="198" rx="24" fill="#432c78"/>'
            + ''.join(f'<rect x="{218+i*184}" y="156" width="152" height="150" rx="19" fill="white"/>' for i in range(3))
            + ''.join(f'<circle cx="{294+i*184}" cy="232" r="43" fill="{["#f8be5b", "#ef83b4", "#8f83ed"][i]}"/>' for i in range(3))
            + '<rect x="390" y="349" width="180" height="42" rx="21" fill="#f4b958"/>')
            + dot(113, 368, 30, '#f2c15d') + dot(846, 375, 24, '#f2c15d'),
    ),
    'simulation': (
        '#ddf2e4', '#71b98c',
        '<path d="M155 342l331-170 322 170-322 156z" fill="#a8ddaa"/>'
        + '<path d="M302 335l180-93 177 93-177 88z" fill="#d4b991"/>'
        + '<path d="M379 210l106-58 104 58v129l-104 54-106-54z" fill="#fff4dd" stroke="#bfa387" stroke-width="3"/>'
        + '<path d="M359 215l126-90 126 90-126 71z" fill="#9b6fa6"/>'
        + '<rect x="448" y="300" width="72" height="88" rx="5" fill="#b77e87"/>'
        + ''.join(f'<circle cx="{210+i*130}" cy="{330+i%2*53}" r="31" fill="#78b79b"/>' for i in range(5))
        + dot(720, 282, 21, '#eaa2b5'),
    ),
    'arcade': (
        '#dbe8ff', '#7788e9',
        '<rect x="223" y="84" width="514" height="365" rx="42" fill="#373369" stroke="#827ce0" stroke-width="8"/>'
        + '<rect x="263" y="126" width="434" height="217" rx="20" fill="#a6c8f0"/>'
        + '<path d="M285 306l106-122 94 109 88-83 101 96" fill="none" stroke="#fff1a2" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/>'
        + dot(570, 401, 20, '#f58cbe') + dot(629, 401, 20, '#8b82ec')
        + line(318, 405, 406, 405, '#bbbef1', 15) + line(362, 366, 362, 442, '#bbbef1', 15),
    ),
    'bunny': (
        '#e9dcff', '#9f62d8',
        '<rect x="246" y="82" width="468" height="374" rx="32" fill="#26133e" stroke="#b67de5" stroke-width="8"/>'
        + '<rect x="279" y="115" width="402" height="308" rx="22" fill="#5b3b92"/>'
        + '<path d="M419 254q-42-91-9-111 37-10 56 76 19-87 54-76 34 20-9 111" fill="#f7e7fa"/>'
        + '<circle cx="465" cy="292" r="76" fill="#f7e7fa"/>'
        + dot(439, 282, 7, '#40305d') + dot(490, 282, 7, '#40305d')
        + '<path d="M453 309q12 13 24 0" fill="none" stroke="#a777b2" stroke-width="5" stroke-linecap="round"/>'
        + '<path d="M620 170l25 39-25 39-25-39z" fill="#e5cafa" stroke="#fff" stroke-width="3"/>'
        + '<path d="M317 350l18-23 18 23-18 23z" fill="#eac5f5"/>'
        + dot(760, 150, 17, '#f9d083') + dot(183, 380, 13, '#e7b5ed'),
    ),
    'plot': (
        '#ffe5ed', '#db729b',
        card(152, 110, 307, 250,
            '<circle cx="258" cy="206" r="50" fill="#e8bdd5"/>'
            + '<path d="M201 302q56-70 114 0" fill="#9d74ab"/>'
            + line(348, 185, 418, 185, '#d4c6df', 11)
            + line(348, 221, 400, 221, '#e2d6e7', 9))
        + card(523, 151, 291, 250,
            '<circle cx="633" cy="244" r="45" fill="#a6b8e9"/>'
            + '<path d="M579 345q53-66 107 0" fill="#6376b9"/>'
            + line(714, 229, 779, 229, '#d4c6df', 11))
        + '<path d="M445 375q45-33 92 0" fill="none" stroke="#de72ad" stroke-width="9" stroke-linecap="round"/>',
    ),
    'atlas': (
        '#e2eff5', '#4ca8af',
        '<circle cx="464" cy="268" r="180" fill="#d2e7e8" stroke="#90c5c5" stroke-width="5"/>'
        + '<ellipse cx="464" cy="268" rx="90" ry="180" fill="none" stroke="#83b6ba" stroke-width="4"/>'
        + line(285, 268, 643, 268, '#83b6ba', 4)
        + '<path d="M335 167q130 60 260 0M335 369q130-60 260 0" fill="none" stroke="#83b6ba" stroke-width="4"/>'
        + card(100, 321, 242, 98, '<path d="M135 351q84-24 84 44 0-68 88-44" fill="none" stroke="#7894bc" stroke-width="9"/>', '#fff9ee', 12)
        + dot(686, 131, 18, '#edbc6b') + dot(721, 364, 13, '#e07fa5'),
    ),
    'memo': (
        '#f0e4dc', '#bb8e76',
        '<path d="M273 113l413 33 53 291-480-38z" fill="#fff8ee" stroke="#d9c9bb" stroke-width="5"/>'
        + '<path d="M687 146l52 291-74-14z" fill="#e5d3c9"/>'
        + ''.join(line(330, 222+i*41, 625-i*20, 222+i*41, '#d0b9bc', 8) for i in range(4))
        + '<circle cx="632" cy="351" r="70" fill="#f2c6bf" opacity=".8"/>'
        + '<path d="M595 352l26 25 54-60" fill="none" stroke="#aa6885" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>',
    ),
}


def svg(name, pale, accent, scene):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540" role="img" aria-label="{name} editorial illustration">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#fff"/><stop offset=".55" stop-color="{pale}"/><stop offset="1" stop-color="#f3e8fa"/></linearGradient>
<radialGradient id="glow"><stop stop-color="{accent}" stop-opacity=".3"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<rect width="960" height="540" fill="url(#bg)"/><circle cx="752" cy="92" r="276" fill="url(#glow)"/>
<path d="M0 470Q230 358 482 491T960 443" fill="none" stroke="{accent}" stroke-opacity=".14" stroke-width="34"/>
{scene}<rect x="20" y="20" width="920" height="500" rx="28" fill="none" stroke="{accent}" stroke-opacity=".15" stroke-width="2"/>
</svg>'''


for name, (pale, accent, scene) in SCENES.items():
    (OUT / f'{name}.svg').write_text(svg(name, pale, accent, scene), encoding='utf-8')
