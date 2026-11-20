# Motion Library（动效模式库）

动效独立于设计包：设计包只定义"气质参数"（duration / easing / 允许的动效强度），本库提供**可复用的动效模式**。生成时按页面需求从本库挑选 1–2 种组合，模式继承设计包的 duration/easing，并在 site-manifest.json 的 `modules` 中登记。

## 总原则

1. **每页最多 2 种动效模式**，组合使用，不要全上
2. **首屏内容直接可见**：hero 与首屏内元素禁止做 reveal（防止用户看到白屏/闪入）
3. **渐进增强（硬性）**：reveal 类动效的隐藏态必须挂在 `html.js` 之下——`<head>` 里写一行 `document.documentElement.classList.add('js')`，CSS 写成 `.js .reveal { opacity: 0 }` 而不是 `.reveal { opacity: 0 }`。否则 JS 未执行（加载失败、被拦截、脚本报错）时，所有待入场元素会永久停在 `opacity: 0`，页面出现成片空白。无 JS 时内容必须默认可见
4. **尊重 reduced-motion**：所有动效必须包裹 `@media (prefers-reduced-motion: no-preference)`，用户开了减弱动效则内容直接呈现
5. **原生优先**：纯 CSS 能实现的（hover、scroll-snap、details）不引入 JS；需要 JS 的自写轻量实现（< 30 行），不为动效引动画库
6. **登记义务**：每个动效在 manifest.modules 写一条 `{ "feature": "...", "implementation": "..." }`
7. **跳转兜底（硬性）**：IntersectionObserver 只在交叉状态**变化**时回调。当用户按 End 跳页尾、点锚点或快速拖动滚动条跨过一整屏时，中间的 reveal 元素从未进入视口，也永远不会回调，结果永久停在隐藏态。必须补一个滚动兜底：把 `getBoundingClientRect().bottom < 0`（即已滚过视口上沿）的待入场元素直接置为已入场。判定条件要用"已滚过"，不能用"top < innerHeight"——后者会在正常滚动时抢在 IntersectionObserver 之前触发，把入场效果整个抵消掉

## 模式清单

### fade-up-reveal（滚动淡入上移）★ 企业/产品站默认

元素首次滚入视口时，从透明 + 下移 20px 状态淡入到位。企业官网、产品站的推荐默认动效。

实现：IntersectionObserver + CSS transition（自写 JS，无依赖）。

```css
.js .reveal { opacity: 0; transform: translateY(20px); }
@media (prefers-reduced-motion: no-preference) {
  .js .reveal.revealed { opacity: 1; transform: none;
    transition: opacity var(--motion-duration, .5s) ease,
                transform var(--motion-duration, .5s) ease; }
}
```

```js
// 给 section/卡片加 .reveal，滚入后加 .revealed
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('revealed'); io.unobserve(e.target); }
}), { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// 兜底：跳转（End / 锚点 / 快速拖动）跨过的元素不会触发回调，必须补入场
let raf = 0;
const sweep = () => {
  raf = 0;
  const rest = document.querySelectorAll('.reveal:not(.revealed)');
  if (!rest.length) return;
  rest.forEach(el => {
    if (el.getBoundingClientRect().bottom < 0) { el.classList.add('revealed'); io.unobserve(el); }
  });
};
addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(sweep); }, { passive: true });
```

manifest 登记：`{ "feature": "区块滚动淡入", "implementation": "IntersectionObserver + 滚动兜底 + CSS transition（fade-up-reveal）" }`

### count-up（数字滚动）

统计数字从 0 滚到目标值。属于数据展示增强而非装饰，可与其他两种模式共存，但**每处嵌入式只允许出现一组**。

**渐进增强写法（硬性）**：HTML 里写的必须是最终值，JS 启动时才置 0 再滚动，结束时还原原文（保留千分位等格式）。写成 `<span data-count="1842">0</span>` 是错的——JS 失效或被拦截时页面上会永久显示 0。

```html
<b><span data-count="1842">1,842</span></b>
```

```js
var finalText = el.textContent;                  // 无 JS 时已经是正确数字
if (reduced) { el.textContent = finalText; return; }
el.textContent = (0).toFixed(decimals);
// ...rAF 滚动结束后 el.textContent = finalText;
```

manifest 登记：`{ "feature": "统计数字滚动", "implementation": "requestAnimationFrame 自写 count-up，尊重 prefers-reduced-motion" }`

### stagger-reveal（分组依次进入）

卡片网格/列表逐个错开进入。与 fade-up 同构，`transition-delay: calc(var(--i) * 60ms)`，JS 里给子元素写 `--i`。每页最多一组使用。

### hover-lift（悬浮上浮）

纯 CSS。卡片 `transition: transform, box-shadow; :hover { transform: translateY(-2~4px) }`。与 flat-material / corporate-clean 默认搭配。

### scroll-snap-deck（PPT 翻页）

纯 CSS：`main { scroll-snap-type: y mandatory } section { scroll-snap-align: start; min-height: 100vh }`。用于 landing 原型，禁用于多内容页面。

### accordion（折叠面板）

原生 `<details>+<summary>`，见 html-contract.md。CSS 可加展开动画，但保持原生交互语义不变。

### parallax（视差，慎用）

仅 tech-aurora / retro-futuristic 等强风格包允许，且每页 ≤ 1 处。transform 驱动，不监听 scroll 做逐帧计算（用 `position: sticky` 或 rAF 节流）。

## 模式 × 设计包推荐组合

| 场景 | 推荐组合 |
|------|---------|
| 企业官网（corporate-clean / flat-material） | fade-up-reveal + hover-lift |
| 科技发布页（tech-aurora） | stagger-reveal + parallax（一处） |
| 电商（commerce-rich） | hover-lift（图片放大）+ 角标 CSS 动画 |
| PPT 落地页（landing） | scroll-snap-deck + 页内 fade-up |
| 资讯媒体（editorial） | 仅 hover-lift（阅读类不动） |
| 毛玻璃（glassmorphism） | fade-up-reveal（慢档 400ms） |
