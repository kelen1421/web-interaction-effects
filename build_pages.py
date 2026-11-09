#!/usr/bin/env python3
"""Build the public entry point from the maintained standalone preview."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
page = (ROOT / "preview/网页交互效果预览.html").read_text(encoding="utf-8")
page = page.replace('<title>网页交互效果预览</title>', '''<title>网页交互效果 · 32 项可操作演示 | KELEN</title>
<meta name="description" content="32 项网页交互原理演示：加载转场、滚动、悬停、弹簧与拖拽。直接操作预览，复制需求描述，安装可复用的 Codex skill。">
<link rel="canonical" href="https://kelen1421.github.io/web-interaction-effects/">''')
page = page.replace('<h2>网页交互效果预览</h2>', '<h1>网页交互效果</h1>')
page = page.replace('data-initial-effect="L01"', 'data-initial-effect="P04"', 1)
page = page.replace('data-use>按这个效果继续</button>', 'data-use>复制需求描述</button>')
old = "$('[data-use]').addEventListener('click',async()=>{if(window.openai?.sendFollowUpMessage){await window.openai.sendFollowUpMessage({prompt:$('#wi-brief').value,title:'继续使用 '+selected.name});}else{$('#wi-brief').focus();$('#wi-brief').select();$('[data-use-status]').textContent='需求已选中，可复制回聊天继续';}});"
new = "$('[data-use]').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#wi-brief').value);$('[data-use-status]').textContent='已复制，可粘贴到聊天或项目需求中';}catch{$('#wi-brief').focus();$('#wi-brief').select();$('[data-use-status]').textContent='需求已选中，请手动复制';}});"
if old not in page:
    raise ValueError("Preview copy handler changed; review the public-page adapter.")
page = page.replace(old, new)
page = page.replace("select(root.dataset.initialEffect||'L01',false);", "select(effects.some(e=>e.id===location.hash.slice(1))?location.hash.slice(1):(root.dataset.initialEffect||'L01'),false);")
page = page.replace("build();if(selected.group==='load')", "build();if(remember)history.replaceState(null,'','#'+selected.id);if(selected.group==='load')")
navigation = '''<header class="site-header">
<a class="site-brand" href="https://github.com/kelen1421">KELEN · 交互实验</a>
<nav aria-label="项目导航"><a href="https://github.com/kelen1421/web-interaction-effects">GitHub 源码</a><a href="https://github.com/kelen1421/web-interaction-effects#安装与调用">安装 skill</a><a href="preview/两期网页交互视频笔记.html">视频笔记</a></nav>
</header>
<p class="site-intro">选择效果，直接操作，再把需求带回你的项目。</p>'''
page = page.replace('<body><main>', '<body><main>' + navigation, 1)
page = page.replace('</head>', '''<style>
.site-header{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;margin-bottom:30px}
.site-header a{color:var(--foreground);text-decoration:none}.site-header a:hover{text-decoration:underline;text-underline-offset:4px}
.site-brand{font-weight:600}.site-header nav{display:flex;flex-wrap:wrap;gap:20px}
.site-intro{margin:0 0 30px;color:var(--muted-foreground);font-weight:400}
#web-interaction-gallery h1{font-size:clamp(28px,4vw,40px);line-height:1.2;letter-spacing:-.04em}
#web-interaction-gallery .wi-top{padding-inline-end:0}
.site-fallback{margin-block:20px}.site-fallback ul{columns:2;padding-left:22px}
@media(max-width:580px){.site-header{align-items:flex-start;flex-direction:column}.site-header nav{gap:16px}.site-intro{margin-bottom:24px}.site-fallback ul{columns:1}}
</style></head>''', 1)
effects = re.findall(r"^\['([A-Z]\d{2})','([^']+)'", page, re.MULTILINE)
if len(effects) != 32 or len({item[0] for item in effects}) != 32:
    raise ValueError("Expected 32 unique effects; update the site metadata when the catalogue changes.")
fallback = '<noscript><section class="site-fallback"><h2>完整效果目录</h2><p>请启用 JavaScript 操作演示。你仍可查看目录和视频笔记。</p><ul>' + ''.join(f'<li>{code} {name}</li>' for code, name in effects) + '</ul></section></noscript>'
page = page.replace('</main>', fallback + '</main>', 1)
(ROOT / 'index.html').write_text(page, encoding='utf-8')
(ROOT / '.nojekyll').write_text('', encoding='utf-8')
print('Built index.html: 32 effects, public navigation and shareable effect links')
