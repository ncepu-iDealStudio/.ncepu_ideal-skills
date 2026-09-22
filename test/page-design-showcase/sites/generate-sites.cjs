const fs=require('fs'),path=require('path');
const BASE='C:/Users/20424/WorkBuddy/前台html生成skill';
const SRC=BASE+'/page-design/designs';
const OUT=BASE+'/page-design-showcase/sites';
const write=(p,s)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,s)};

function cssBase(t,extra){
  return `:root{--bg:${t.bg};--surface:${t.surface};--text:${t.text};--muted:${t.muted};
  --primary:${t.primary};--accent:${t.accent};--border:${t.border};--radius:${t.radius};
  --shadow:${t.shadow||'none'};--head:${t.head||'inherit'};--body:${t.body||'inherit'};
  --duration:200ms;--easing:ease}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--text);font:16px/1.75 var(--body);}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
a{color:var(--primary)}a:hover{color:var(--accent)}
h1,h2,h3{font-family:var(--head);line-height:1.3;font-weight:700}
h1{font-size:clamp(30px,4.6vw,46px)}h2{font-size:24px;margin-bottom:16px}h3{font-size:18px}
p{margin-bottom:12px}
img{max-width:100%;height:auto;display:block}
.site-header{border-bottom:1px solid var(--border);background:var(--surface)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:64px;padding-top:10px;padding-bottom:10px;flex-wrap:wrap}
.brand{font-family:var(--head);font-size:19px;font-weight:700;letter-spacing:.04em}
.nav ul{display:flex;gap:22px;list-style:none;flex-wrap:wrap}
.nav a{font-size:14px;letter-spacing:.06em;text-decoration:none}
.nav a[aria-current="page"]{color:var(--accent)}
.menu{display:none}
.hero{padding:64px 0 40px}
.lead{font-size:18px;color:var(--muted);max-width:60ch;margin-bottom:20px}
section.block{padding:44px 0;border-top:1px solid var(--border)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:20px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow)}
.card h3{margin-bottom:8px}
.card p{font-size:14px;color:var(--muted);margin-bottom:8px}
.meta{font-size:12.5px;color:var(--muted);letter-spacing:.04em}
.btn{display:inline-block;background:var(--primary);color:${t.onPrimary||'#fff'};padding:11px 22px;border-radius:var(--radius);text-decoration:none;font-size:14px}
.grid-3{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}
.stat b{display:block;font-family:var(--head);font-size:32px;color:var(--primary)}
.spec{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
.spec th,.spec td{border-bottom:1px solid var(--border);padding:10px 8px;text-align:left}
.spec th{width:38%;color:var(--muted);font-weight:400}
.breadcrumb{font-size:13px;color:var(--muted);padding:16px 0}
.breadcrumb a{text-decoration:none}
.post-body{max-width:68ch;font-size:16.5px}
.post-body p{text-indent:2em}
details.faq{border-bottom:1px solid var(--border);padding:12px 0}
details.faq summary{cursor:pointer;font-weight:600;padding:4px 0}
form.contact{max-width:520px}
form.contact label{display:block;margin:14px 0 6px;font-size:14px}
form.contact input,form.contact textarea{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:var(--radius);font:inherit;background:var(--surface);color:var(--text)}
form.contact button{border:0;cursor:pointer;font:inherit}
.site-footer{border-top:1px solid var(--border);margin-top:56px;padding:26px 0 40px;font-size:13px;color:var(--muted)}
.site-footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
ul.timeline{list-style:none}
ul.timeline li{border-left:2px solid var(--primary);padding:0 0 18px 18px;margin-left:6px}
ul.timeline time{font-size:13px;color:var(--muted)}
@media(max-width:720px){
  .nav ul{display:none}
  .menu{display:block}
  .menu summary{cursor:pointer;padding:8px 0;font-size:14px}
  .menu ul{list-style:none;padding:12px 0}
  .menu li{padding:6px 0}
}
${extra||''}`;
}

function pageDoc(o){
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${o.title}</title>
<meta name="description" content="${o.desc}">
<link rel="stylesheet" href="css/base.css">
${o.head||''}
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<header class="site-header" data-component="site-header">
  <div class="wrap">
    <div class="brand"><a href="index.html" style="text-decoration:none">${o.brand}</a></div>
    <nav class="nav" aria-label="主导航">
      <ul>${o.nav.map(n=>`<li><a href="${n[0]}"${n[0]===o.file?' aria-current="page"':''}>${n[1]}</a></li>`).join('')}</ul>
    </nav>
    <details class="menu">
      <summary>菜单</summary>
      <ul>${o.nav.map(n=>`<li><a href="${n[0]}">${n[1]}</a></li>`).join('')}</ul>
    </details>
  </div>
</header>
<main>
${o.body}
</main>
<footer class="site-footer" data-component="site-footer">
  <div class="wrap">
    <span>${o.brand} · 静态站点原型（演示用样例内容）</span>
    <span>设计包 ${o.pack} · 可直接双击浏览</span>
  </div>
</footer>
${o.tail||''}
</body>
</html>`;
}

function readme(s){
  return `# ${s.name} · 设计综述（状态恢复入口）

## 需求摘要
> ${s.requirement}

## Requirement Model
- site：${s.name} / zh-CN / ${s.purpose} / ${s.audience}
- pages：${s.pages.map(p=>`${p.file}（${p.type}）`).join('、')}
- content：${s.content}
- design：${s.packName}（${s.pack}）— ${s.packReason}

## design_statement
- position：${s.ds.position}
- focus：${s.ds.focus}
- device：${s.ds.device}
- banned：${s.ds.banned}

## 采用的设计包
已复制到 \`doc/design/${s.pack}.md\`。

## 页面进度
${s.pages.map(p=>`- [x] ${p.file} · ${p.type} · ${p.title}`).join('\n')}

## 后续拆解提示
所有重复区域已标注 data-component / data-collection / data-slot，删除全部 data-* 后仍是合法语义 HTML。
`;
}

function manifest(s){
  return JSON.stringify({
    site:{name:s.name,language:'zh-CN',designPack:s.pack,generatedAt:'2026-09-22'},
    outputRoot:s.rootRel,
    pages:s.pages.map(p=>({file:p.file,type:p.type,title:p.title})),
    components:s.components,
    collections:s.collections,
    contentSample:{generated:true,note:'所有内容为演示用样例数据，非真实机构信息'},
    modules:s.modules,
    external:{cdn:[]}
  },null,2);
}

function build(site){
  const root=OUT+'/'+site.id;
  write(root+'/doc/design/'+site.pack+'.md',fs.readFileSync(SRC+'/'+site.pack+'.md','utf8'));
  write(root+'/doc/README.md',readme(site));
  write(root+'/template/css/base.css',cssBase(site.tokens,site.extraCss));
  if(site.js) write(root+'/template/js/main.js',site.js);
  (site.images||[]).forEach(img=>write(root+'/template/image/'+img[0],img[1]));
  site.pages.forEach(p=>write(root+'/template/'+p.file,pageDoc(Object.assign({brand:site.name,pack:site.pack,nav:site.nav,tail:site.js?'<script src="js/main.js"></script>':''},p))));
  write(root+'/template/site-manifest.json',manifest(site));
  console.log('built '+site.id+' ('+site.pages.length+' pages, pack '+site.pack+')');
}

const svg=(c1,c2,label)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="${label}">
<rect width="640" height="360" fill="${c1}"/>
<rect x="40" y="120" width="560" height="120" fill="${c2}" opacity=".5"/>
<circle cx="520" cy="90" r="52" fill="${c2}" opacity=".8"/>
<text x="40" y="300" font-family="sans-serif" font-size="22" fill="${c2}">${label}</text>
</svg>`;

/* ---------- A. 个人博客 / swiss-minimal ---------- */
const posts=[
 {title:'用三十行 CSS 做一套网格系统',summary:'不依赖框架，只用 grid 与自定义属性，把版式的节奏固定下来。',date:'2026-08-12',category:'前端'},
 {title:'读完《字体设计原理》之后',summary:'字重、字距与行高三者的关系，比想象中更影响阅读耐力。',date:'2026-07-28',category:'阅读'},
 {title:'我把博客从动态站迁回了静态',summary:'一年维护成本降到几乎为零，代价是评论功能没了——值得。',date:'2026-07-03',category:'随记'},
 {title:'关于可访问性的五个误解',summary:'它不是给少数人做的额外工作，而是让所有人都能读完你的页面。',date:'2026-06-19',category:'前端'},
 {title:'深夜调试日记：一个 overflow 引发的血案',summary:'父级的 min-width:0，救了我两个小时。',date:'2026-06-02',category:'随记'},
 {title:'为什么我不再追求"炫"的个人主页',summary:'看完二十个作品集之后，我删掉了自己页面上的粒子动画。',date:'2026-05-14',category:'设计'}
];
const postCard=(p,i)=>`    <article class="card" data-component="post-card">
      <h3><a href="post.html" data-slot="post.url"><span data-slot="post.title">${p.title}</span></a></h3>
      <p data-slot="post.summary">${p.summary}</p>
      <p class="meta"><span data-slot="post.category">${p.category}</span> · <time datetime="${p.date}" data-slot="post.date">${p.date}</time></p>
    </article>`;
const postList=n=>`  <ul class="cards" style="list-style:none" data-collection="posts">
${posts.slice(0,n).map(postCard).join('\n')}
  </ul>`;

build({
  id:'blog-swiss', pack:'swiss-minimal', packName:'瑞士极简', name:'砚田笔记',
  requirement:'我想做一个个人博客，写技术笔记和读书感想，要干净一点，能放文章列表和文章页。',
  purpose:'个人写作与技术笔记', audience:'同学、同行与未来雇主',
  content:'领域：个人写作；模型：article（posts）',
  packReason:'学生要求"干净"，且内容是长文阅读；swiss-minimal 的纯白网格与单强调色最适合文字密集场景',
  ds:{position:'一个安静的阅读型个人博客，不是作品集，也不是门户',
      focus:'首页第一眼落在标题下那句自述，紧接着是三张最近文章卡片',
      device:'纯白网格 + 单一红色强调线 + 零圆角，不用卡片阴影堆叠与渐变',
      banned:'不做粒子背景、不做卡片套卡片、不放头像墙、不写"赋能/极致"式标语'},
  components:['site-header','site-footer','post-card'],
  collections:{posts:{fields:['title','summary','url','category','date'],sample:true}},
  modules:[{feature:'移动端菜单',implementation:'details/summary + CSS，无 JS'},{feature:'动效',implementation:'无刻意动效，仅 hover 变色（阅读类页面不动）'}],
  nav:[['index.html','首页'],['list.html','文章'],['about.html','关于'],['contact.html','联系']],
  rootRel:'tmp/tests/blog-swiss/',
  tokens:{bg:'#FFFFFF',surface:'#F6F6F4',text:'#141414',muted:'#5F5F5C',primary:'#E30613',accent:'#E30613',border:'#DEDEDA',radius:'0',shadow:'none',head:"'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif",body:"'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif"},
  toPrimaryWhite:'#fff',
  extraCss:`.hero{border-bottom:1px solid var(--border)}
.card{border-left:3px solid var(--primary)}
.card h3 a{text-decoration:none;color:var(--text)}
.post-body{max-width:68ch}`,
  pages:[
   {file:'index.html',type:'home',title:'砚田笔记 · 写字的地方',desc:'砚田笔记：前端、设计与阅读的个人博客。',
    body:`<div class="wrap hero">
  <h1>砚田笔记</h1>
  <p class="lead">写给两年后的自己：那些当时以为记住了、后来全忘掉的东西。</p>
  <p><a class="btn" href="list.html">读全部文章</a></p>
</div>
<section class="block"><div class="wrap">
  <h2>最近写的</h2>
${postList(3)}
</div></section>
<section class="block"><div class="wrap">
  <h2>关于这里</h2>
  <p style="max-width:60ch">一个普通开发者的公开笔记。写前端实现、字体与排印，偶尔写读完一本书之后的碎念。不追热点，不做教程搬运。</p>
</div></section>`},
   {file:'list.html',type:'list',title:'全部文章 · 砚田笔记',desc:'砚田笔记的全部文章列表，按时间倒序。',
    body:`<div class="wrap hero">
  <h1>全部文章</h1>
  <p class="lead">共 ${posts.length} 篇，按时间倒序。</p>
</div>
<section class="block"><div class="wrap">
  <h2>文章列表</h2>
${postList(6)}
</div></section>`},
   {file:'post.html',type:'detail',title:'用三十行 CSS 做一套网格系统 · 砚田笔记',desc:'不用框架，只用 CSS grid 与自定义属性搭一套可复用的网格系统。',
    body:`<div class="wrap">
  <p class="breadcrumb"><a href="index.html">首页</a> / <a href="list.html">文章</a> / 前端</p>
  <article class="post-body">
    <h1>用三十行 CSS 做一套网格系统</h1>
    <p class="meta">发布于 <time datetime="2026-08-12">2026 年 8 月 12 日</time> · 分类 前端</p>
    <p>先承认一件事：过去我每次新建项目都会从上一份代码里把 grid 相关的样式抄过来，抄了三年，从来没想过它为什么长这样。这次决定把它拆干净，看看最少需要多少行。</p>
    <p>答案是三十行左右。核心不在 grid 本身，而在把间距和列宽收敛成两个自定义属性。一旦这两件事定了，页面上的每个区块都只是同一个系统的不同组合，而不是各写一份 margin。</p>
    <p>剩下的工作反而变难了：要忍住不为某一个特别的区块破例。破例一次很轻松，三次之后系统就名存实亡。这大概是写代码和写文章共同的难处。</p>
    <p><img src="image/grid.svg" alt="网格系统示意图：12 列栅格与 24 像素间距的标注"></p>
  </article>
</div>
<section class="block"><div class="wrap">
  <h2>相关阅读</h2>
  <ul class="cards" style="list-style:none" data-collection="posts">
${posts.slice(3,5).map(postCard).join('\n')}
  </ul>
</div></section>`},
   {file:'about.html',type:'about',title:'关于 · 砚田笔记',desc:'关于作者与这个博客。',
    body:`<div class="wrap hero">
  <h1>关于这里</h1>
  <p class="lead">写东西是为了把脑子里模糊的部分逼清楚。</p>
</div>
<section class="block"><div class="wrap">
  <h2>一点来历</h2>
  <p style="max-width:60ch">2024 年开始写技术笔记，起因是把同一个问题查了三遍。写下来之后没再查过第四遍，于是继续写。</p>
  <p style="max-width:60ch">现在这里放着三十来篇笔记，内容集中在前端实现、排印与工具使用。写得慢，但每篇都尽量说清楚一件事。</p>
</div></section>`},
   {file:'contact.html',type:'contact',title:'联系 · 砚田笔记',desc:'通过邮件或留言联系作者。',
    body:`<div class="wrap hero">
  <h1>联系</h1>
  <p class="lead">看到错别字、或者有想聊的话题，都可以写信。</p>
</div>
<section class="block"><div class="wrap">
  <h2>留言</h2>
  <form class="contact" action="#" method="post">
    <label for="name">称呼</label>
    <input id="name" name="name" type="text" required autocomplete="name">
    <label for="email">邮箱</label>
    <input id="email" name="email" type="email" required autocomplete="email">
    <label for="msg">想说的话</label>
    <textarea id="msg" name="msg" rows="5" required></textarea>
    <p style="margin-top:16px"><button class="btn" type="submit">发送</button></p>
  </form>
  <p class="meta">本页为静态原型，表单不会真正提交。</p>
</div></section>`},
   {file:'404.html',type:'error',title:'页面不存在 · 砚田笔记',desc:'页面不存在。',
    body:`<div class="wrap hero">
  <h1>这个页面不存在</h1>
  <p class="lead">可能是地址写错了，也可能是文章被我删了。</p>
  <p><a class="btn" href="index.html">回首页</a> <a class="btn" href="list.html" style="margin-left:10px">看文章列表</a></p>
</div>`}
  ],
  images:[['grid.svg',svg('#F6F6F4','#E30613','Grid System / 12 columns')]]
});

/* ---------- B. 公司门户 / flat-material ---------- */
const products=[
 {name:'云枢边缘网关',model:'EG-210',summary:'工业现场数据接入网关，支持四路串口与断网续传。',img:'image/product.svg'},
 {name:'云枢时序数据库',model:'TS-800',summary:'面向设备测点优化的时序存储，单机可承载百万级写入。',img:'image/product.svg'},
 {name:'云枢可视化平台',model:'VP-300',summary:'零代码组态画布，内置二十余种工业图表与告警面板。',img:'image/product.svg'},
 {name:'云枢设备孪生',model:'DT-120',summary:'把产线设备映射为可查询对象，支持历史状态回放。',img:'image/product.svg'},
 {name:'云枢告警中心',model:'AL-500',summary:'多渠道告警分发，支持值班轮换与升级策略。',img:'image/product.svg'},
 {name:'云枢开放接口',model:'API-10',summary:'统一的 REST 与 MQTT 接入层，含沙箱环境与用量统计。',img:'image/product.svg'}
];
const pCard=p=>`    <article class="card" data-component="product-card">
      <p><img src="${p.img}" alt="${p.name} 产品示意图" data-slot="product.img"></p>
      <h3><a href="detail.html" data-slot="product.url"><span data-slot="product.name">${p.name}</span></a></h3>
      <p class="meta" data-slot="product.model">型号 ${p.model}</p>
      <p data-slot="product.summary">${p.summary}</p>
    </article>`;

build({
  id:'corp-flat', pack:'flat-material', packName:'扁平质感', name:'云枢智能',
  requirement:'我们公司做工业物联网，需要一个正式的官网，要有首页、产品列表、产品详情、关于我们和联系方式。',
  purpose:'企业对外官网与产品门户', audience:'制造业客户与合作伙伴',
  content:'领域：工业物联网；模型：product（products）、notice（notices）',
  packReason:'对外正式门户且强调产品；flat-material 的阴影分层与现代产品感最贴合，避免暗色控制台气质',
  ds:{position:'正式但不老派的工业物联网公司门户，不是电商，也不是控制台',
      focus:'首页第一眼落在深蓝实底 hero 的主张句，往下是三条能力卡与真实数字背书',
      device:'白色卡片 + 浅阴影分层替代边框，滚动淡入只有一种，不做霓虹与扫描线',
      banned:'不做浮动装饰球、不做伪造的实时产线仪表盘、不写"赋能未来"式空话、不把产品页做成促销页'},
  components:['site-header','site-footer','product-card','value-card'],
  collections:{products:{fields:['name','model','summary','url','img'],sample:true}},
  modules:[{feature:'移动端菜单',implementation:'details/summary + CSS'},{feature:'产品 FAQ 折叠',implementation:'原生 details/summary'},{feature:'联系表单校验',implementation:'原生 form 校验（required / type=email）'},{feature:'滚动淡入',implementation:'IntersectionObserver + CSS transition（fade-up-reveal，js/main.js <20 行）'}],
  nav:[['index.html','首页'],['list.html','产品'],['detail.html','产品介绍'],['about.html','关于我们'],['contact.html','联系']],
  rootRel:'tmp/tests/corp-flat/',
  tokens:{bg:'#F5F6F8',surface:'#FFFFFF',text:'#1B1F24',muted:'#5C6672',primary:'#1565D8',accent:'#0B4FA8',border:'#E2E6EC',radius:'12px',shadow:'0 2px 8px rgba(16,24,40,.08)',head:"'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif",body:"'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"},
  extraCss:`.hero{background:var(--surface);border-bottom:1px solid var(--border);padding:72px 0 56px}
.card{border:0;overflow:hidden}
.card img{border-radius:8px;margin-bottom:12px}
.card h3 a{text-decoration:none;color:var(--text)}
.btn{border-radius:8px}
.js .reveal{opacity:0;transform:translateY(20px)}
@media(prefers-reduced-motion:no-preference){
  .js .reveal.revealed{opacity:1;transform:none;transition:opacity var(--duration) var(--easing),transform var(--duration) var(--easing)}
}`,
  js:`(function(){
  'use strict';
  if (!window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.style.opacity = 1; el.style.transform = 'none'; });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('revealed'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  var sweepRaf = 0;
  function sweep() {
    sweepRaf = 0;
    var rest = document.querySelectorAll('.reveal:not(.revealed)');
    if (!rest.length) return;
    rest.forEach(function (el) {
      if (el.getBoundingClientRect().bottom < 0) { el.classList.add('revealed'); io.unobserve(el); }
    });
  }
  function onScroll() { if (!sweepRaf) sweepRaf = requestAnimationFrame(sweep); }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
})();`,
  pages:[
   {file:'index.html',type:'home',title:'云枢智能 · 工业物联网产品与方案',desc:'云枢智能提供工业现场数据接入、时序存储与可视化的一体化方案。',
    body:`<div class="hero">
  <div class="wrap">
    <h1>让每一台设备的数据，都能被用起来</h1>
    <p class="lead">从车间里的接入网关，到总部看板上的一张图，云枢提供中间完整的那一层。</p>
    <p><a class="btn" href="list.html">查看产品</a></p>
  </div>
</div>
<section class="block"><div class="wrap reveal">
  <h2>我们能做什么</h2>
  <div class="grid-3">
    <article class="card" data-component="value-card"><h3>数据接入</h3><p>兼容主流工业协议与串口设备，断网期间本地缓存，恢复后自动续传。</p></article>
    <article class="card" data-component="value-card"><h3>时序存储</h3><p>面向测点特性优化的列式存储，压缩比常见通用库高出数倍。</p></article>
    <article class="card" data-component="value-card"><h3>可视化与告警</h3><p>组态画布与多渠道告警分发，值班轮换和升级策略可配置。</p></article>
  </div>
</div></section>
<section class="block"><div class="wrap reveal">
  <h2>主要产品</h2>
  <ul class="cards" style="list-style:none" data-collection="products">
${products.slice(0,3).map(pCard).join('\n')}
  </ul>
</div></section>
<section class="block"><div class="wrap reveal">
  <h2>一些数字</h2>
  <div class="grid-3">
    <div class="stat"><b>6</b><span class="meta">条自研产品线</span></div>
    <div class="stat"><b>17</b><span class="meta">项已授权专利</span></div>
    <div class="stat"><b>12 GWh</b><span class="meta">服务的年产能规模</span></div>
  </div>
</div></section>`},
   {file:'list.html',type:'list',title:'产品中心 · 云枢智能',desc:'云枢智能六条自研产品线的列表页。',
    body:`<div class="wrap hero">
  <h1>产品中心</h1>
  <p class="lead">六条自研产品线，覆盖接入、存储、分析到展示的完整链路。</p>
</div>
<section class="block"><div class="wrap">
  <h2>全部产品</h2>
  <ul class="cards" style="list-style:none" data-collection="products">
${products.map(pCard).join('\n')}
  </ul>
</div></section>`},
   {file:'detail.html',type:'detail',title:'云枢边缘网关 EG-210 · 云枢智能',desc:'云枢边缘网关 EG-210 的规格参数与常见问题。',
    body:`<div class="wrap">
  <p class="breadcrumb"><a href="index.html">首页</a> / <a href="list.html">产品</a> / 边缘网关</p>
  <article>
    <h1>云枢边缘网关 EG-210</h1>
    <p class="lead">面向老旧设备改造的现场接入网关，四路串口，支持断网续传与本地缓存 30 天。</p>
    <p><img src="image/product.svg" alt="EG-210 网关外观示意"></p>
    <h2>规格参数</h2>
    <table class="spec">
      <caption class="meta" style="text-align:left;padding-bottom:8px">以下参数为样机实测值，批量版本以出厂报告为准。</caption>
      <tbody>
        <tr><th>型号</th><td>EG-210</td></tr>
        <tr><th>串口</th><td>4 路 RS-485 / RS-232（可配置）</td></tr>
        <tr><th>网口</th><td>2 路千兆以太网</td></tr>
        <tr><th>本地缓存</th><td>64 GB，断网可存 30 天</td></tr>
        <tr><th>工作温度</th><td>-20℃ ~ 70℃</td></tr>
      </tbody>
    </table>
    <h2>常见问题</h2>
    <details class="faq"><summary>设备断网后数据会不会丢？</summary><p>不会。断网期间数据写入本地缓存，网络恢复后按时间顺序自动补传，不需要人工介入。</p></details>
    <details class="faq"><summary>是否支持第三方协议？</summary><p>内置 Modbus、OPC UA 等常用协议；其余协议可通过开放的插件接口自行扩展。</p></details>
    <details class="faq"><summary>可以上云吗？</summary><p>可以直连云枢时序数据库，也可以通过 MQTT 转发到客户自建的消息中间件。</p></details>
  </article>
</div>
<section class="block"><div class="wrap">
  <h2>更多产品</h2>
  <ul class="cards" style="list-style:none" data-collection="products">
${products.slice(3,5).map(pCard).join('\n')}
  </ul>
</div></section>`},
   {file:'about.html',type:'about',title:'关于我们 · 云枢智能',desc:'云枢智能的团队与里程碑。',
    body:`<div class="wrap hero">
  <h1>关于我们</h1>
  <p class="lead">一家做工业数据基础设施的公司，成立于 2019 年。</p>
</div>
<section class="block"><div class="wrap">
  <h2>我们是谁</h2>
  <p style="max-width:62ch">团队三十余人，一半在现场，一半在写代码。我们相信工业场景里最难的部分不在算法，而在把脏数据稳定地搬上来。</p>
</div></section>
<section class="block"><div class="wrap">
  <h2>一路走来</h2>
  <ul class="timeline">
    <li><time datetime="2019-04">2019 年 4 月</time><p>公司成立，第一代网关 EG-100 立项。</p></li>
    <li><time datetime="2021-08">2021 年 8 月</time><p>时序数据库 TS-800 发布，单机写入突破百万测点。</p></li>
    <li><time datetime="2024-03">2024 年 3 月</time><p>可视化平台 VP-300 上线，方案补齐最后一环。</p></li>
  </ul>
</div></section>`},
   {file:'contact.html',type:'contact',title:'联系我们 · 云枢智能',desc:'联系云枢智能，获取产品资料或方案咨询。',
    body:`<div class="wrap hero">
  <h1>联系我们</h1>
  <p class="lead">留下需求，我们会在一个工作日内回复。</p>
</div>
<section class="block"><div class="wrap">
  <h2>需求登记</h2>
  <form class="contact" action="#" method="post">
    <label for="cname">公司/姓名</label>
    <input id="cname" name="cname" type="text" required autocomplete="organization">
    <label for="cemail">邮箱</label>
    <input id="cemail" name="cemail" type="email" required autocomplete="email">
    <label for="cphone">电话（选填）</label>
    <input id="cphone" name="cphone" type="tel" autocomplete="tel">
    <label for="cneed">需求描述</label>
    <textarea id="cneed" name="cneed" rows="5" required></textarea>
    <p style="margin-top:16px"><button class="btn" type="submit">提交</button></p>
  </form>
  <h2 style="margin-top:32px">其他方式</h2>
  <p class="meta">地址：某市高新区智造大道 12 号 3 号楼 · 邮箱：hello@example.com（演示用）</p>
  <p class="meta">本页为静态原型，地图与表单均未接入真实服务。</p>
</div></section>`},
   {file:'404.html',type:'error',title:'页面不存在 · 云枢智能',desc:'页面不存在。',
    body:`<div class="wrap hero">
  <h1>没有找到这个页面</h1>
  <p class="lead">链接可能已经变更，建议从产品中心重新找起。</p>
  <p><a class="btn" href="index.html">回首页</a> <a class="btn" href="list.html" style="margin-left:10px">产品中心</a></p>
</div>`}
  ],
  images:[['product.svg',svg('#E8EEF8','#1565D8','Cloud Hub Product')]]
});

/* ---------- C. 高大上动画设计展示 / tech-aurora ---------- */
const works=[
 {title:'光年计划 · 主视觉',summary:'为一支独立乐队做的巡演主视觉，含动态海报与现场背景。',year:'2026',img:'image/work.svg'},
 {title:'深海信号',summary:'数据可视化短片，把一年的海洋温度记录压缩成九十秒。',year:'2025',img:'image/work.svg'},
 {title:'折叠城市',summary:'交互装置的概念设计，观众走近时建筑立面会随距离展开。',year:'2025',img:'image/work.svg'},
 {title:'回声档案',summary:'声音博物馆的导览界面，用波形替代时间轴。',year:'2024',img:'image/work.svg'},
 {title:'纸上的轨道',summary:'地铁线路图的实验性重绘，只保留换乘关系。',year:'2024',img:'image/work.svg'},
 {title:'夜行生物',summary:'一组关于夜间城市观察者的动态插画。',year:'2023',img:'image/work.svg'}
];
const wCard=w=>`    <article class="card reveal" data-component="work-card">
      <p><img src="${w.img}" alt="${w.title} 作品缩略图" data-slot="work.cover"></p>
      <h3><a href="detail.html" data-slot="work.url"><span data-slot="work.title">${w.title}</span></a></h3>
      <p data-slot="work.summary">${w.summary}</p>
      <p class="meta" data-slot="work.year">${w.year}</p>
    </article>`;

build({
  id:'showcase-aurora', pack:'tech-aurora', packName:'极光科技', name:'光年计划',
  requirement:'我想要一个高大上的作品集网站，展示我的动态设计和视觉作品，要有动画效果，看起来很酷。',
  purpose:'视觉作品集与动态设计展示', audience:'创意机构、招聘方与同行',
  content:'领域：视觉/动态设计；模型：自建 works（title, summary, cover, url, year）',
  packReason:'学生明确要"高大上 + 动画"，tech-aurora 是唯一允许视差与霓虹渐变的包，其余包无法承载该气质',
  ds:{position:'一个以动态视觉为主角的作品集，不是简历页，也不是模板站',
      focus:'首屏第一眼落在渐变标题与下方的三张作品卡，视差只出现在中段一处',
      device:'深色渐变 + 霓虹紫青双色 + 滚动淡入与分组错开进入，视差用 sticky 纯 CSS 实现',
      banned:'不做全屏粒子雨、不做鼠标跟随光斑、不做自动播放轮播、不让首屏内容先隐藏再淡入'},
  components:['site-header','site-footer','work-card'],
  collections:{works:{fields:['title','summary','cover','url','year'],sample:true}},
  modules:[{feature:'移动端菜单',implementation:'details/summary + CSS'},
           {feature:'滚动淡入',implementation:'IntersectionObserver + CSS transition（fade-up-reveal，js/main.js）'},
           {feature:'卡片分组错开进入',implementation:'CSS transition-delay calc(var(--i)*60ms)（stagger-reveal）'},
           {feature:'中段视差',implementation:'position:sticky 纯 CSS，无滚动监听（parallax，全站仅 1 处）'}],
  nav:[['index.html','首页'],['list.html','作品'],['detail.html','作品详情'],['about.html','关于']],
  rootRel:'tmp/tests/showcase-aurora/',
  tokens:{bg:'#070A18',surface:'#111633',text:'#E9ECFF',muted:'#9AA3D0',primary:'#7C4DFF',accent:'#00E5FF',border:'#262C55',radius:'14px',shadow:'0 8px 30px rgba(124,77,255,.16)',head:"'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif",body:"'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"},
  extraCss:`.hero{position:relative;padding:96px 0 72px;background:radial-gradient(900px 420px at 20% 0%,rgba(124,77,255,.34),transparent 70%),radial-gradient(700px 380px at 85% 20%,rgba(0,229,255,.22),transparent 70%)}
.hero h1{font-size:clamp(34px,6vw,60px);background:linear-gradient(92deg,#fff,#00E5FF 45%,#7C4DFF);-webkit-background-clip:text;background-clip:text;color:transparent}
.card{border:1px solid var(--border);background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.02))}
.card img{border-radius:10px;margin-bottom:12px}
.btn{background:linear-gradient(92deg,var(--primary),var(--accent));color:#0A0E22;font-weight:600}
.para{height:170vh;position:relative}
.para-inner{position:sticky;top:22vh;padding:40px 0}
.para-inner p{font-size:clamp(20px,3.4vw,34px);max-width:22ch;background:linear-gradient(92deg,#00E5FF,#7C4DFF);-webkit-background-clip:text;background-clip:text;color:transparent}
.js .reveal{opacity:0;transform:translateY(20px)}
@media(prefers-reduced-motion:no-preference){
  .js .reveal.revealed{opacity:1;transform:none;transition:opacity 520ms var(--easing),transform 520ms var(--easing);transition-delay:calc(var(--i,0)*60ms)}
}`,
  js:`(function(){
  'use strict';
  if (!window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.style.opacity = 1; el.style.transform = 'none'; });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('revealed'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15 });
  var items = document.querySelectorAll('.reveal');
  items.forEach(function (el, i) { el.style.setProperty('--i', i % 6); io.observe(el); });
  var sweepRaf = 0;
  function sweep() {
    sweepRaf = 0;
    var rest = document.querySelectorAll('.reveal:not(.revealed)');
    if (!rest.length) return;
    rest.forEach(function (el) {
      if (el.getBoundingClientRect().bottom < 0) { el.classList.add('revealed'); io.unobserve(el); }
    });
  }
  function onScroll() { if (!sweepRaf) sweepRaf = requestAnimationFrame(sweep); }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
})();`,
  pages:[
   {file:'index.html',type:'landing',title:'光年计划 · 动态视觉作品集',desc:'光年计划：动态设计与视觉作品的作品集，含滚动动效与视差。',
    body:`<div class="hero">
  <div class="wrap">
    <h1>把静止的画面，做成会呼吸的东西</h1>
    <p class="lead">光年计划是一组关于时间与运动的视觉实验，包含动态海报、数据短片与交互装置概念。</p>
    <p><a class="btn" href="list.html">看全部作品</a></p>
  </div>
</div>
<section class="block"><div class="wrap">
  <h2>精选作品</h2>
  <ul class="cards" style="list-style:none" data-collection="works">
${works.slice(0,3).map(wCard).join('\n')}
  </ul>
</div></section>
<section class="para" aria-label="视差引言">
  <div class="wrap para-inner">
    <p>动效不是装饰。它是让人知道接下来该看哪一处的路标。</p>
  </div>
</section>
<section class="block"><div class="wrap reveal">
  <h2>工作方式</h2>
  <div class="grid-3">
    <article class="card"><h3>先定节奏</h3><p>动效的时长与缓动先定下来，画面再往里填。</p></article>
    <article class="card"><h3>再定焦点</h3><p>一屏只让一个东西动，其余静止，观众才不会迷路。</p></article>
    <article class="card"><h3>留一处不动</h3><p>总有一个元素全程安静，用来兜住整页的重量。</p></article>
  </div>
</div></section>
<section class="block"><div class="wrap">
  <h2>合作</h2>
  <p class="lead">接受视觉设计、动态海报与数据可视化委托。</p>
  <p><a class="btn" href="about.html">了解工作方式</a></p>
</div></section>`},
   {file:'list.html',type:'list',title:'全部作品 · 光年计划',desc:'光年计划的全部动态视觉作品列表。',
    body:`<div class="wrap hero">
  <h1>全部作品</h1>
  <p class="lead">共 ${works.length} 组，按年份倒序。</p>
</div>
<section class="block"><div class="wrap">
  <h2>作品列表</h2>
  <ul class="cards" style="list-style:none" data-collection="works">
${works.map(wCard).join('\n')}
  </ul>
</div></section>`},
   {file:'detail.html',type:'detail',title:'光年计划 · 主视觉 · 光年计划',desc:'光年计划主视觉作品的创作说明。',
    body:`<div class="wrap">
  <p class="breadcrumb"><a href="index.html">首页</a> / <a href="list.html">作品</a> / 动态视觉</p>
  <article>
    <h1>光年计划 · 主视觉</h1>
    <p class="meta">年份 2026 · 类型 动态海报 / 现场背景</p>
    <p><img src="image/work.svg" alt="光年计划主视觉：紫青渐变的波形构图"></p>
    <h2>创作说明</h2>
    <p>巡演需要一套能同时用在海报、门票和现场大屏上的视觉。约束是：印刷时必须是静止的，现场时必须是运动的，两者还得是同一个东西。</p>
    <p>最后的做法是把波形作为唯一母题。静止版本是波形的一个截面，现场版本让这个截面沿时间轴展开——同一张图，两种不同的读法。</p>
    <p>现场反馈里最有用的一条是：副歌段的展开速度应该减半。这个改动让画面在情绪最高处反而慢下来，比一味加速耐看得多。</p>
  </article>
</div>
<section class="block"><div class="wrap">
  <h2>更多作品</h2>
  <ul class="cards" style="list-style:none" data-collection="works">
${works.slice(3,5).map(wCard).join('\n')}
  </ul>
</div></section>`},
   {file:'about.html',type:'about',title:'关于 · 光年计划',desc:'关于光年计划与其工作方式。',
    body:`<div class="wrap hero">
  <h1>关于光年计划</h1>
  <p class="lead">一个做动态视觉的小工作室，2023 年开始接活。</p>
</div>
<section class="block"><div class="wrap reveal">
  <h2>我们做什么</h2>
  <p style="max-width:62ch">动态海报、数据可视化短片、交互装置概念设计。规模不大，一次只推进一个项目，交付物通常包含静态版与动态版两套。</p>
</div></section>`},
   {file:'404.html',type:'error',title:'页面不存在 · 光年计划',desc:'页面不存在。',
    body:`<div class="wrap hero">
  <h1>信号丢失</h1>
  <p class="lead">这个地址没有对应的作品。</p>
  <p><a class="btn" href="index.html">回首页</a> <a class="btn" href="list.html" style="margin-left:10px">看作品</a></p>
</div>`}
  ],
  images:[['work.svg',svg('#0B1026','#7C4DFF','Light-year Project / Key Visual')]]
});

/* ---------- D. 个人主页 / glassmorphism ---------- */
const projects=[
 {title:'课程表小程序',summary:'帮室友做的选课辅助工具，能按空余时间反查可选课程。',year:'2026'},
 {title:'校园二手书平台原型',summary:'课程设计作业，完成了从信息架构到高保真原型的全流程。',year:'2025'},
 {title:'天气数据可视化作业',summary:'把一年的本地天气数据做成可交互的时间轴。',year:'2025'}
];
const prCard=p=>`    <article class="card" data-component="project-card">
      <h3><a href="#" data-slot="project.url"><span data-slot="project.title">${p.title}</span></a></h3>
      <p data-slot="project.summary">${p.summary}</p>
      <p class="meta" data-slot="project.year">${p.year}</p>
    </article>`;

build({
  id:'homepage-glass', pack:'glassmorphism', packName:'毛玻璃', name:'林述',
  requirement:'我想做一个简单的个人主页，介绍自己，放几个我做过的项目就行，好看一点。',
  purpose:'个人介绍与作品展示', audience:'课程老师与同学',
  content:'领域：个人主页；模型：自建 projects（title, summary, url, year）',
  packReason:'学生只要"好看一点"且页面极简；glassmorphism 是强风格包，此处内容量小、单页为主，风险可控且最贴合诉求',
  ds:{position:'一张个人名片式的主页，不是博客，也不是简历长页',
      focus:'首屏第一眼落在彩色渐变背景上的那块磨砂玻璃卡片与人名',
      device:'彩色渐变底 + 半透明磨砂浮层，只有悬浮上浮一种动效',
      banned:'不做背景视频、不做鼠标跟随光效、不做滚动视差、玻璃层不超过两层'},
  components:['site-header','site-footer','project-card'],
  collections:{projects:{fields:['title','summary','url','year'],sample:true}},
  modules:[{feature:'移动端菜单',implementation:'details/summary + CSS'},{feature:'悬浮上浮',implementation:'纯 CSS transform:translateY（hover-lift）'}],
  nav:[['index.html','首页'],['list.html','项目'],['about.html','关于']],
  rootRel:'tmp/tests/homepage-glass/',
  tokens:{bg:'linear-gradient(135deg,#4B2E83 0%,#1F6F8B 48%,#7A3B6B 100%)',surface:'rgba(255,255,255,.14)',text:'#F4F6FF',muted:'rgba(244,246,255,.74)',primary:'#8EF6E4',accent:'#FFD6E8',border:'rgba(255,255,255,.24)',radius:'18px',shadow:'none',head:"'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif",body:"'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"},
  extraCss:`body{min-height:100vh}
.site-header{background:rgba(255,255,255,.10);border-bottom:1px solid var(--border);backdrop-filter:blur(14px)}
.card{backdrop-filter:blur(16px);background:var(--surface);border:1px solid var(--border);transition:transform var(--duration) var(--easing)}
@media(prefers-reduced-motion:no-preference){.card:hover{transform:translateY(-3px)}}
.hero{padding:72px 0 40px}
.glass{padding:26px 28px;border-radius:var(--radius);background:var(--surface);border:1px solid var(--border);backdrop-filter:blur(18px)}
.btn{background:var(--primary);color:#0B2230;font-weight:600}
a{color:var(--primary)}`,
  pages:[
   {file:'index.html',type:'home',title:'林述 · 个人主页',desc:'林述的个人主页：设计专业学生，展示课程项目与个人介绍。',
    body:`<div class="wrap hero">
  <div class="glass">
    <h1>林述</h1>
    <p class="lead">设计专业大三学生。喜欢把复杂的信息排得让人一眼看懂，正在学前端。</p>
    <p><a class="btn" href="list.html">看我的项目</a></p>
  </div>
</div>
<section class="block" style="border-top:1px solid var(--border)"><div class="wrap">
  <h2>正在做的事</h2>
  <div class="grid-3">
    <article class="card"><h3>课程与自学</h3><p>这学期主修信息设计，课余在补 HTML 与 CSS 的基础。</p></article>
    <article class="card"><h3>校园项目</h3><p>和同学一起做一个校内二手书的原型，负责信息架构与界面。</p></article>
    <article class="card"><h3>想做的事</h3><p>希望毕业前能完整做完一个真正有人用的小工具。</p></article>
  </div>
</div></section>
<section class="block" style="border-top:1px solid var(--border)"><div class="wrap">
  <h2>最近的项目</h2>
  <ul class="cards" style="list-style:none" data-collection="projects">
${projects.map(prCard).join('\n')}
  </ul>
</div></section>`},
   {file:'list.html',type:'list',title:'项目 · 林述',desc:'林述做过的课程项目与个人练习。',
    body:`<div class="wrap hero">
  <h1>我的项目</h1>
  <p class="lead">课程作业与课余练习，共 ${projects.length} 个。</p>
</div>
<section class="block" style="border-top:1px solid var(--border)"><div class="wrap">
  <h2>项目列表</h2>
  <ul class="cards" style="list-style:none" data-collection="projects">
${projects.map(prCard).join('\n')}
  </ul>
</div></section>`},
   {file:'about.html',type:'about',title:'关于 · 林述',desc:'关于林述。',
    body:`<div class="wrap hero">
  <h1>关于我</h1>
  <p class="lead">一个还在学、但已经能交付东西的设计学生。</p>
</div>
<section class="block" style="border-top:1px solid var(--border)"><div class="wrap">
  <h2>一点经历</h2>
  <ul class="timeline">
    <li><time datetime="2024-09">2024 年</time><p>入学，开始接触信息设计与排版。</p></li>
    <li><time datetime="2025-11">2025 年</time><p>完成第一个完整原型：校园二手书平台。</p></li>
    <li><time datetime="2026-03">2026 年</time><p>开始自学前端，把这个主页自己做出来。</p></li>
  </ul>
</div></section>`},
   {file:'404.html',type:'error',title:'页面不存在 · 林述',desc:'页面不存在。',
    body:`<div class="wrap hero">
  <h1>这里什么都没有</h1>
  <p class="lead">页面好像还没做出来。</p>
  <p><a class="btn" href="index.html">回首页</a></p>
</div>`}
  ],
  images:[['portrait.svg',svg('#4B2E83','#8EF6E4','Portrait Placeholder')]]
});

console.log('--- done ---');
