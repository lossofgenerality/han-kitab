#!/usr/bin/env python3
"""Build gallery/ (images + gallery_v001.json) from Wikimedia Commons downloads.
Usage: python3 -I make_gallery_v001.py RAW_DIR REPO_DIR
© Computational Classnotes · CC BY-NC-SA 4.0 (gallery selection and captions; each photo keeps its own licence)"""
import json, os, re, sys, html
from PIL import Image, ImageOps
RAW, REPO = sys.argv[1], sys.argv[2]
P = json.load(open(os.path.join(RAW, 'picks.json')))
D = json.load(open(os.path.join(RAW, 'cand', 'cands.json')))
C = D['cands']; ALT = D['alt']
def pick(n): return dict(P[n-1], file=os.path.join(RAW, f'g{n:02d}.jpg'))
def cand(i, j, cat, label, zh, place):
    c = dict(C[i-1][j-1]); c.update(cat=cat, label=label, zh=zh, place=place, file=os.path.join(RAW, 'cand', f'c{i:02d}_{j}.jpg')); return c
ITEMS = [  # (source, description)
 (cand(1,2,'Mosques','Huaisheng Mosque','懷聖寺','Guangzhou, Guangdong'), 'Traditionally dated to the Tang dynasty, one of the oldest mosques in China. Its smooth round minaret, the Guangta, is a Guangzhou landmark.'),
 (pick(2), 'Founded in 1009 and rebuilt in 1310; the stone gateway is in West Asian style, unlike most Chinese mosques.'),
 (pick(3), 'Laid out like a Chinese temple, with courtyards, pavilions and a pagoda-like minaret. Most of the present buildings are Ming (14th–17th century).'),
 (cand(8,2,'Mosques','Great Mosque of Xi’an, prayer hall','化覺巷清真大寺禮拜殿','Xi’an, Shaanxi'), 'Carved wooden panels with Qur’anic inscriptions line the walls of the prayer hall.'),
 (pick(4), 'Beijing’s oldest and largest mosque, founded in 996 according to tradition, at the heart of the Niujie Hui neighbourhood.'),
 (cand(13,1,'Mosques','Niujie Mosque, prayer hall','牛街禮拜寺禮拜殿','Beijing'), 'Inside the prayer hall: Chinese timber construction, painted beams and Arabic inscriptions.'),
 (pick(5), 'Founded in 1447 under the Ming, one of Beijing’s principal mosques.'),
 (pick(6), 'One of the four great early mosques of China’s coast; rebuilt in the Yuan dynasty.'),
 (pick(7), 'Founded in the Song dynasty; its plan is said to resemble a crane (仙鶴).'),
 (pick(8), 'Shanghai’s oldest mosque, built in the Yuan dynasty.'),
 (pick(9), 'Shandong’s largest mosque. Its 1528 inscription, 來復銘, is one of the earliest Chinese texts on Islam by a Muslim author.'),
 (cand(2,3,'Mosques','East Great Mosque','濟寧東大寺','Jining, Shandong'), 'On the Grand Canal; Jining was a centre of the Shandong school of scripture-hall learning.'),
 (pick(11), 'A Qing-era mosque in Chinese style in the old city of Tianjin.'),
 (pick(12), 'Ming-era mosque of Nanjing (Jinling), the city where Wang Daiyu and Liu Zhi wrote the Han Kitab.'),
 (pick(13), 'Qing-dynasty mosque joining Chinese roofs to Islamic arches.'),
 (pick(14), 'Ming-dynasty mosque of the Na clan, in a Hui village near Yinchuan.'),
 (pick(15), 'The oldest surviving mosque in Ningxia, built in Chinese style.'),
 (pick(16), 'Qinghai’s largest mosque, founded in 1380.'),
 (dict(pick(17), label='Hanjia Mosque, Linxia', zh='臨夏韓家清真寺'), 'Linxia (Hezhou), often called China’s “Little Mecca”, has dozens of mosques and Sufi shrines.'),
 (pick(18), 'Xinjiang’s largest mosque, built in 1442 at the centre of Kashgar.'),
 (cand(3,1,'Mosques','Emin Minaret','額敏塔','Turpan, Xinjiang'), 'Built in 1777–78 by Emin Khoja: 44 metres of sun-dried brick in geometric patterns.'),
 (pick(20), 'Kaifeng’s main mosque. The city’s Hui community also keeps women’s mosques (女寺), led by women.'),
 (pick(21), 'One of the oldest Muslim foundations in Kunming, Yunnan, rebuilt in modern times.'),
 (cand(10,1,'Mosques','Great Mosque of Shadian','沙甸大清真寺','Shadian, Yunnan'), 'The Hui town of Shadian rebuilt its great mosque in 2009 in a Middle Eastern style.'),
 (pick(22), 'Hong Kong’s largest mosque, opened in 1984.'),
 (pick(23), 'The principal mosque of Chengdu, Sichuan.'),
 (pick(24), 'The principal mosque of Lanzhou, Gansu.'),
 (cand(11,1,'Heritage','Tomb of Sa‘d ibn Abi Waqqas (traditional)','清真先賢古墓','Guangzhou, Guangdong'), 'Chinese Muslim tradition holds that a companion of the Prophet, Sa‘d ibn Abi Waqqas, is buried here.'),
 (pick(25), 'Traditionally the tombs of two companions of the Prophet who came to Quanzhou in the Tang dynasty.'),
 (pick(26), 'Mausoleum of the 17th-century Sufi leader Afaq Khoja and his family.'),
 (cand(4,2,'Heritage','Basmala in Sini script','清真寺經字','Qingjing Mosque, Quanzhou'), 'The basmala, “In the name of God, the Merciful, the Compassionate”, in Sini, the Chinese style of Arabic calligraphy.'),
 (cand(4,1,'Heritage','al-Ḥamdu li-llāh in Sini script','經字畫','China'), '“Praise be to God”, written in the round brush strokes of Sini calligraphy.'),
 (pick(28), 'Xi’an’s Hui quarter around the Great Mosque, known for its food streets.'),
 (cand(15,1,'Quarters','Muslim Quarter at night','回民街夜市','Xi’an, Shaanxi'), 'Evening crowds in the lanes of the Muslim Quarter.'),
 (pick(29), 'The Hui neighbourhood around Niujie Mosque in Beijing.'),
 (pick(30), 'The Uyghur old town of Kashgar; much of it has been rebuilt since 2009.'),
 (pick(31), 'Linxia city in Gansu, a historic centre of Hui, Dongxiang and Salar life.'),
 (cand(16,1,'Markets','Market street, Linxia','臨夏市場','Linxia, Gansu'), 'A street market below a mosque minaret.'),
 (pick(34), 'Spicy lamb trotters (麻辣羊蹄) and other halal snacks in Xi’an.'),
 (cand(12,1,'Markets','Yangrou paomo','羊肉泡饃','Xi’an, Shaanxi'), 'Xi’an’s signature Hui dish: flatbread broken into mutton soup.'),
 (pick(35), 'The Sunday market of Kashgar.'),
 (pick(36), 'The International Grand Bazaar of Ürümqi.'),
 (pick(37), 'A Lanzhou beef-noodle shop; Hui-run noodle restaurants are found all over China.'),
 (dict(pick(38), label='A qingzhen (halal) restaurant, early 20th century'), 'From the Japanese photograph series 亜東印画輯 (1920s–1940s); the sign 清真 marks Muslim food.'),
 (cand(7,3,'Markets','Livestock market, Hotan','和田巴扎','Hotan, Xinjiang'), 'The sheep market at the Hotan bazaar.'),
]
def clean(s):
    s = re.sub(r'<[^>]+>', '', s or ''); s = html.unescape(s); return re.sub(r'\s+', ' ', s).strip()
out = os.path.join(REPO, 'gallery'); os.makedirs(out, exist_ok=True)
data = []
for k, (it, desc) in enumerate(ITEMS, 1):
    im = ImageOps.exif_transpose(Image.open(it['file'])).convert('RGB')
    big = im.copy(); big.thumbnail((1400, 1400)); big.save(os.path.join(out, f'photo_{k:02d}.jpg'), quality=82, optimize=True, progressive=True)
    sm = im.copy(); sm.thumbnail((560, 560)); sm.save(os.path.join(out, f'thumb_{k:02d}.jpg'), quality=78, optimize=True, progressive=True)
    data.append({'n': k, 'cat': it['cat'], 'label': it['label'], 'zh': it['zh'], 'place': it['place'], 'desc': desc,
                 'artist': clean(it.get('artist')) or 'Unknown', 'license': it.get('license', ''), 'licenseUrl': it.get('licenseUrl', ''),
                 'page': it['page'], 'title': it['title'].replace('File:', ''), 'w': big.width, 'h': big.height,
                 'img': f'gallery/photo_{k:02d}.jpg', 'thumb': f'gallery/thumb_{k:02d}.jpg'})
json.dump(data, open(os.path.join(out, 'gallery_v001.json'), 'w'), ensure_ascii=False, indent=1)
print(len(data), 'photos')
