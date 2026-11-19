"""Build a compact academic homepage in English and Chinese, without dependencies."""
from pathlib import Path
from html import escape
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
PAGES = ('index', 'news', 'publications', 'rewards')
LABELS = {
    'en': {
        'nav': ('Home', 'News', 'Publications', 'Awards'),
        'titles': ('Jun Zhang’s Homepage', 'News', 'Publications', 'Honors & Awards'),
        'about': 'About me', 'interests': 'My research interests include:',
        'recent': 'Recent news', 'all_news': 'All news', 'education': 'Education',
        'published': 'Journal papers', 'conference': 'Conference papers',
        'submitted': 'Submitted manuscripts', 'ongoing': 'Other research',
        'corresponding_author': 'Corresponding author',
        'research': 'Selected Publications', 'more_research': 'All publications and research',
        'honors': 'Honors & Awards', 'all_awards': 'All awards',
        'rank': 'Rank in major', 'average': 'Average score',
        'scholarships': 'Scholarships', 'competitions': 'Competitions',
        'portrait': 'Portrait of Jun Zhang', 'emblem': '{} emblem', 'undergraduate': 'Undergraduate',
        'masters': 'Master',
        'skip': 'Skip to content', 'navigation': 'Main navigation',
        'switch': '中文', 'switch_label': '切换到中文', 'switch_lang': 'zh-CN',
        'description': 'Jun Zhang studies Communication Engineering at Xiamen University. His research interests include image pattern recognition, post-training for vision-language models, and embodied AI safety.'
    },
    'zh': {
        'nav': ('首页', '动态', '论文', '荣誉'),
        'titles': ('张骏的个人主页', '近期动态', '论文与研究', '荣誉与奖项'),
        'about': '关于我', 'interests': '我的主要研究兴趣包括：',
        'recent': '近期动态', 'all_news': '全部动态', 'education': '教育背景',
        'published': '期刊论文', 'conference': '会议论文',
        'submitted': '已投稿论文', 'ongoing': '其他研究工作',
        'corresponding_author': '通信作者',
        'research': '代表性论文', 'more_research': '全部论文与研究',
        'honors': '荣誉与奖项', 'all_awards': '全部奖项',
        'rank': '专业排名', 'average': '课程平均分',
        'scholarships': '奖学金', 'competitions': '竞赛获奖',
        'portrait': '张骏的个人照片', 'emblem': '{}校徽', 'undergraduate': '本科',
        'masters': '硕士',
        'skip': '跳转到正文', 'navigation': '主导航',
        'switch': 'English', 'switch_label': 'Switch to English', 'switch_lang': 'en',
        'description': '张骏，厦门大学通信工程专业，研究兴趣包括图像模式识别、视觉语言模型后训练和具身智能安全。'
    }
}


def e(value):
    return escape(str(value), quote=True)


def filename(key, lang):
    return key + ('-zh' if lang == 'zh' else '') + '.html'


def external(url, label):
    if not url.startswith(('https://', 'http://', 'mailto:')):
        raise ValueError(f'Unsupported link: {url}')
    return f'<a href="{e(url)}">{e(label)}</a>'


def section(title, body, anchor=''):
    attr = f' id="{e(anchor)}"' if anchor else ''
    return f'<section{attr}><h2>{e(title)}</h2>{body}</section>'


def listing(items):
    return '<ul>' + ''.join(f'<li>{e(item)}</li>' for item in items) + '</ul>'


class Site:
    def __init__(self, lang):
        self.lang = lang
        base = json.loads((ROOT / 'content/profile.json').read_text(encoding='utf-8'))
        self.d = {**base, **json.loads((ROOT / 'content/profile.en.json').read_text(encoding='utf-8'))} if lang == 'en' else base
        self.t = LABELS[lang]

    def more(self, key, label):
        return f'<p>[<a href="{filename(key, self.lang)}">{e(label)}</a>]</p>'

    def news(self, items):
        rows = []
        for item in items:
            message = e(item['text'])
            if item.get('emphasis'):
                emphasis = e(item['emphasis'])
                message = message.replace(emphasis, f'<strong>{emphasis}</strong>', 1)
            rows.append(f'<li><time>{e(item["date"])}</time>: {message}</li>')
        return '<ul>' + ''.join(rows) + '</ul>'

    def research(self, items, *, show_role=False):
        result = '<ol class="research-list">'
        for item in items:
            authors = e(item.get('authors', ''))
            if authors:
                corresponding = item.get('corresponding_author')
                if corresponding:
                    marker = f'<sup title="{e(self.t["corresponding_author"])}">†</sup>'
                    authors = authors.replace(e(corresponding), e(corresponding) + marker)
                authors = authors.replace('Jun Zhang', '<strong>Jun Zhang</strong>')
            else:
                authors = f'<strong>{e(self.d["name"])}</strong>'
            if show_role and item.get('role'):
                authors += f' · {e(item["role"])}'
            venue = item.get('citation', item.get('status', ''))
            rank = item.get('journal_rank')
            rank_html = f' <strong>{e(rank)}</strong>' if rank else ''
            title = e(item['title'])
            for link in item.get('links', []):
                title += f' <span class="paper-link">[{external(link["url"], link["label"])}]</span>'
            result += f'''<li id="{e(item['id'])}"><article><h3>{title}</h3>
            <p>{authors}.<br><em>{e(venue)}</em>{rank_html}</p></article></li>'''
        return result + '</ol>'

    def publications(self):
        result = ''
        for group in ('published', 'conference', 'submitted', 'ongoing'):
            items = [r for r in self.d['research'] if r['group'] == group]
            if items:
                result += section(self.t[group], self.research(items))
        return result

    def awards(self):
        return '<ol>' + ''.join(f'<li><time>{e(a["date"])}</time>: {e(a["name"])} — <strong>{e(a["award"])}</strong>.</li>' for a in self.d['awards']) + '</ol>'

    def education(self):
        profile, t = self.d, self.t
        degree = profile['education']
        colon = '：' if self.lang == 'zh' else ': '
        graduate_details = (
            f'<p>{e(profile["department"])}<br>{e(t["masters"])} · {e(profile["school_period"])}</p>'
        )
        undergraduate_details = (
            f'<p>{e(degree["department"])}<br>{e(t["undergraduate"])} · {e(degree["period"])}</p>'
            f'<p>{e(t["rank"])}{colon}{e(degree["rank"])} · GPA{colon}{e(degree["gpa"])}<br>'
            f'{e(t["average"])}{colon}{e(degree["average"])} · {e(degree["english"])}</p>'
        )
        entries = [
            (profile['school'], profile['headline'], profile['school_logo'], graduate_details),
            (degree['school'], degree['major'], degree['logo'], undergraduate_details),
        ]
        rows = []
        for school, major, logo, details in entries:
            alt = t['emblem'].format(school)
            rows.append(
                f'<article class="education"><img src="{e(logo)}" alt="{e(alt)}" '
                f'width="85" height="85" loading="lazy"><div>'
                f'<h3>{e(school)} · {e(major)}</h3>{details}</div></article>'
            )
        return ''.join(rows)

    def home(self):
        d, t = self.d, self.t
        name = f'{e(d["name"])} ({e(d["native_name"])})' if self.lang == 'en' else e(d['name'])
        socials = ' '.join('[' + external(x['url'], x['label']) + ']' for x in d['social_links'])
        profile = f'''<div class="profile"><img class="portrait" src="{e(d['portrait'])}" alt="{e(t['portrait'])}" width="1199" height="1312" fetchpriority="high">
        <div><p>{name}<br>{e(d['headline'])}</p><p>{external(d['department_url'], d['school'])}</p>
        <p>E-mail: {external('mailto:' + d['email'], d['email'])}</p>{f'<p>{socials}</p>' if socials else ''}</div></div>'''
        about = ''.join(f'<p>{e(p)}</p>' for p in d['about']) + f'<p>{e(t["interests"])}</p>' + listing(d['interests'])
        return (profile + section(t['about'], about)
                + section(t['recent'], self.news(d['news'][:5]) + self.more('news', t['all_news']))
                + section(t['education'], self.education(), 'education')
                + section(t['research'], self.research(d['research'], show_role=True) + self.more('publications', t['more_research']))
                + section(t['honors'], listing(d['education']['scholarships']) + self.more('rewards', t['all_awards'])))

    def body(self, key):
        t = self.t
        if key == 'index': return self.home()
        if key == 'news': return section(t['recent'], self.news(self.d['news']))
        if key == 'publications': return self.publications()
        return section(t['competitions'], self.awards()) + section(t['scholarships'], listing(self.d['education']['scholarships']))

    def page(self, key):
        t, d = self.t, self.d
        other = 'zh' if self.lang == 'en' else 'en'
        title = t['titles'][PAGES.index(key)]
        language = 'zh-CN' if self.lang == 'zh' else 'en'
        nav = ''.join(f'<a href="{filename(k, self.lang)}" {"aria-current=page" if key == k else ""}>{e(t["nav"][i])}</a>' for i, k in enumerate(PAGES))
        return f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(t['description'])}"><meta name="theme-color" content="#ffffff"><title>{e(title)}</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css">
<link rel="alternate" hreflang="{t['switch_lang']}" href="{filename(key, other)}"></head>
<body><a class="skip-link" href="#main">{e(t['skip'])}</a><div class="layout">
<aside class="sidebar"><a class="site-name" href="{filename('index', self.lang)}">{e(d['name'])}</a><nav aria-label="{e(t['navigation'])}">{nav}</nav></aside>
<main id="main"><header class="page-header"><h1>{e(title)}</h1><a class="language-switch" lang="{t['switch_lang']}" hreflang="{t['switch_lang']}" aria-label="{e(t['switch_label'])}" href="{filename(key, other)}">{e(t['switch'])}</a></header>{self.body(key)}
</main></div></body></html>'''


def build():
    DIST.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'assets', DIST / 'assets', dirs_exist_ok=True)
    for lang in ('en', 'zh'):
        site = Site(lang)
        for key in PAGES:
            (DIST / filename(key, lang)).write_text(site.page(key), encoding='utf-8')
    (DIST / '.nojekyll').touch()
    print(f'Built {2 * len(PAGES)} pages (English + Chinese).')


if __name__ == '__main__':
    build()
