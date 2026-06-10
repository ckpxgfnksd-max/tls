# GROWTH-STRATEGY.md — Chase 的 X 定制化增长策略

> 目标:纯涨粉 + 扩大影响力。现状 1k–1万粉,中文为主,投资/经济/加密/创业领域。
> 本文 = 已验证的通用调研结论 × 仓库真实数据(x-control 算法标记 + 身份/KOL 代理数据)。
> 生成日期:2026-06-10

---

## 0. 数据来源与置信度

| 数据 | 来源 | 置信度 |
|---|---|---|
| 算法风险标记 + 信号面板 + 硬性上限 | `x-control`(公开仓库,已完整读取 `signals.py` / `queue.py` / `approve.py` / SKILL.md) | **高 — 真实代码** |
| 身份/人设 | `tls` README(Chase Wang @ChaseWang,ex-Binance listing team,审过 1,000+ 项目,2025 年上线 ~100 个 token)+ `x-control-chase` SKILL.md | **高 — 本人所写** |
| KOL 名单 | `x-control-chase/kol_list.md` 正式版(经 `chasewang-skills` 镜像的代码搜索提取) | **高 — 真实名单**:精选种子层(权重 0.7–1.0)+ 2026-05-17 自动导入的全量 following(权重 0.5,含中文区账号) |
| 文风规则 | `chase-voice` 的 SKILL.md + `style_profile.md`(经代码搜索提取核心段落;该 skill 基于全量推文存档做过 20 轮 autoresearch) | **高 — 真实规则**,细节见 §5 |
| 通用调研结论 1–10 | 用户提供,已验证 | 高 |

注:三仓库数据均已拿到。`chase-voice`/`x-control-chase` 经 GitHub 代码搜索通道提取(片段级,非整库通读),关键规则已交叉验证。

---

## 1. 身份资产(identity_hints)

人设护城河,**每条高杠杆内容都应露出其一**:

- **审过 1,000+ 项目**(样本量碾压几乎所有 KOL)
- **2025 年上线 ~100 个 token**(实操而非纸上谈兵)
- **顶级 CEX 上币团队出身**(交易所视角)
- **正在 build TLS(Token Launch Stack)**(build in public 素材,公开仓库可链)

⚠️ **硬规则修正(来自 chase-voice 6 条硬规则)**:**发帖内容里不提 Binance**(no Binance 是和"不碰中国政府/官员话题"并列的安全红线)。所以推文里的身份梗用"前顶级交易所上币团队/在交易所审过 1000+ 项目"表述;"ex-Binance"只放 bio/个人站(tls README 本来就公开写了),不进推文正文。

写入 x-control 草稿 frontmatter 的建议值:

```yaml
identity_hints: ["审过1000+项目", "2025年上线~100个token", "前顶级交易所上币团队"]
```

`x-control-chase` 的 `topic_tags` 默认值已固化为 **tokenomics / defi / ai-workflow**——这就是 30 天话题分布基线,内容支柱(§4)全部落在这三个标签内,跳出去会吃 topic-fit 低分。

> 注意:平台侧排序已由 LLM 做全语言适配,中文身份梗(如"前顶级交易所上币团队")**X 算法能正常理解并奖励**。只是 x-control 本地信号面板的 `_IDENTITY_TEASE_PATTERNS` 还是英文正则,中文梗在本地不显示得分——这是工具显示问题,不是策略问题。本地升级方向见 §8。

对应调研结论 #8(加密圈身份可信度建设)和 #6(主页转化):bio 必须一句话说清——「前顶级交易所上币团队 · 审过 1000+ 项目 · 帮 founder 把 token launch 做对」这个量级的表述。(bio 里是否写明 Binance 由你定夺——tls README 已公开写了 ex-Binance,但 chase-voice 硬规则对帖子内容是零容忍,bio 保持一致最稳。)

---

## 2. 战略回复目标名单(KOL list)

来自 `x-control-chase/kol_list.md` **正式版**。结构是两层:精选种子层(权重 0.7–1.0,与公开模板一致,本人确认过)+ 全量 following 自动导入层(权重 0.5,2026-05-17,**未经筛选**——里面连 NASA、PopBase 都有,只能当候选池不能当目标清单)。按战略回复杠杆率重新分层,调研结论 #2 说最佳猎场是**粉丝为你 2–20 倍**的账号(按 5k 粉计 = 1万–10万粉),百万级大V回复区竞争太激烈,只做选择性出击:

**A 层 — 日常主猎场(发帖 15 分钟内抢前排,每条 2–3 句补洞见/数据)**

| handle | 类别 | 备注 |
|---|---|---|
| jefftokenomics | defi-founder | $HYPE Hyperliquid(原表权重 1.0,需核对 handle) |
| nathanallman | defi-founder | $ONDO |
| gdog97_ | defi-founder | $ENA Ethena |
| paulframbot | defi-founder | $MORPHO |
| weremeow | defi-founder | $JUP Jupiter |
| PrimordialAA | defi-founder | $ZRO LayerZero |
| a1lon9 | platform-ops | pump.fun |
| StarXu_ | cex-ops | OKX — 与你的 CEX 背景天然对话 |
| grapeot | ai-builder | 工作流/AI benchmark(原表权重 1.0) |

**B 层 — 选择性出击(只在你有独家视角时回复:上币/tokenomics/listing 话题)**

| handle | 类别 |
|---|---|
| VitalikButerin | l1-founder |
| aeyakovenko | l1-founder (SOL) |
| SergeyNazarov | $LINK |
| StaniKulechov | $AAVE |
| RuneKek | $SKY |
| karpathy | ai-builder |

**C 层 — 中文区主猎场(新增,从 following 导入层挖出的真实关注)**

正式名单的 following 层里已有中文区加密账号:`daobase_ai`、`awsbclub_cn`、`tmel0211`、`Uncle_Kai_CN` 等。这层是中文粉丝的主要来源,但目前全部躺在 0.5 权重的未筛选池里。**待办**:把 following 层里 1万–10万粉的中文投资/加密账号筛出来,提权到 0.8–1.0 并标 `lang: zh`,作为 Phase 1 的日常主猎场(优先级高于 A 层英文区——中文回复在中文 KOL 评论区的转化远高于在英文区)。

---

## 3. 算法红线(来自 x-control 真实代码,grounded in xai-org/x-algorithm)

> **语言适配前提**:X 排序已用 LLM 做全用户语言适配,内容理解是语义级、语言无关的。下表正则是 x-control 本地镜像(英文写法),但**红线以"类别"为准,不以英文字面为准**——中文版互动钓鱼("同意请点赞")、中文喊单、中文点名开战,平台侧同样识别、同样惩罚。

### 3.1 风险标记 — 高危(直接映射 block/mute/report/not_interested 负反馈头;调研结论 #1:拉黑 -74、举报 -369)

| 标记 | 触发条件 | 对策 |
|---|---|---|
| `engagement_bait` | "RT if / like if / comment yes / do you agree / am I wrong / prove me wrong / who else…?" | 调研 #7 的互动钓鱼红线,代码已强制执行 |
| `callout_named_account` | `@某人 is wrong/lying/grifting/cooked…` | 点名开战 = 被对方粉丝集体拉黑;争议观点只对事不对人 |
| `ai_slop_openers` | 开头 "Let me explain / Here's the thing / In this thread / The truth is / Nobody talks about…" | AI 味开场白 = "not interested" 高风险 |
| `shill_keywords` | 100x / 1000x / moonshot / to the moon / degen play / presale | 调研 #8:喊单词触发 spam 标记 |
| `guarantee_lang` | guaranteed / 100% / definitely / will hit | 同上,且有合规风险 |
| `dm_solicitation` | "DM me / DMs are open" | 典型骗子模式词 |

### 3.2 风险标记 — 中危(结构性 AI 味)

| 标记 | 触发条件 |
|---|---|
| `em_dash_overuse` | 单条推文 ≥3 个全角破折号 — AI 生成痕迹 |
| `emoji_spam` | 单条推文 ≥5 个 emoji |
| `numbered_list_in_one_tweet` | 单条推内 "1. … 2. … 3. …" 压缩列表 |
| `price_target` | "$X price/target by EOY" 价格预测句式 |
| `contains_url_$0.20_per_post` | 正文含 URL(调研 #7:外链放评论区) |

### 3.3 节奏硬上限(AuthorDiversityDecay,approve.py 强制)

- **单推 ≤3 条 / 24h**(超出 = 算法指数衰减,代码直接拒发,`--override` 才能绕过)
- **4h 窗口内 ≥2 条单推即触发 burst 警告**
- **Thread 整串只算 1 次作者事件,不受上限约束** ← 这是关键漏洞利用点:想多发就发串
- 工具内回复 ≤2 条 / 24h(此上限与增长策略冲突,见 §8)

### 3.4 OON 陷阱(dashboard 自动标旗)

回复 ≥3 但点赞 ≤1 的推 = 吵架树,无圈内放大,被 `OON_WEIGHT_FACTOR` 结构性压制。**争议内容的健康形态是"点赞与回复同涨",只涨回复不涨赞 = 在吵架,立刻停止恋战。**

### 3.5 正向信号面板(发帖前自查清单,对应 ranking_scorer.rs 各头)

| 信号 | 满分条件 |
|---|---|
| repostability | 80–240 字符 + 陈述句断言 + 反共识框架;忌 hedge 词("我觉得可能大概") |
| reply-worthiness | 结尾开放式提问 / 反共识框架(与 engagement_bait 一线之隔,问真问题不求互动) |
| dwell-potential | ≥6 条的 thread 最强;单推则多行结构 + ≥2 个具体数字 |
| profile-click-pull | 正文露出 identity_hints("审过1000+项目…",注意 §5.1 硬规则:不提 Binance) |
| follow-author-reason | 系列标记("Day 3 / 每周复盘 / 3/7")+ 持续价值预告 |
| topic-fit | topic_tags 与自己 30 天话题分布重叠(别突然跳出领域) |

---

## 4. 分阶段作战计划

### Phase 1 · 1k → 3k 粉:「评论区猎人」(预计 2–3 个月)

精力分配 **70% 战略回复 / 30% 原创**(调研 #2)。

**每日动作:**
- 早 6:00–8:00:跑 `x-control` pulse → 扫 §2 C/A 层名单过去 12h 新帖 → 选 3–5 条,15 分钟窗口内回复(2–3 句:补数据 / 补 1000+ 项目样本里的反例 / 提犀利问题)。**严禁 "Great post" 类空话。**(注意:这一步无法自动化——Typefully 被 X 政策禁止发回复,见 §8——是每天必须本人到场的动作)
- 午 12:00–13:00:1 条原创单推(中文,带数字,带身份梗)。
- 晚 20:00–22:00:1 条原创 + 回复每一条自己帖子下的评论(调研 #1:作者回复≈点赞 150 倍权重,这是免费杠杆,一条都别漏)。
- 单推全天 ≤3 条,间隔 ≥4h(刚好对齐三个中文活跃时段,自然规避 burst 警告)。

**每周动作:**
- 1 条 thread(5–7 推):「审过 1000+ 项目」系列复盘 / token launch 失败案例拆解。Thread 不占单推配额。
- 固定栏目标记:"上币周记 #N" —— 喂 `follow-author-reason` 信号。

**内容支柱(按身份资产展开):**
1. 上币视角内幕(不点名、讲机制):交易所怎么筛项目、为什么 90% 被拒
2. Tokenomics 拆解:用真实数据图复盘热门项目的解锁/分配
3. 风险清单体(调研 #4 最稳):「launch 前 founder 必查的 N 件事」
4. Build in public:TLS 工具本身的进展(repo 公开,可信度+开源人设)

**Phase 1 目标指标**:互动率 ≥1.5%(互动÷曝光),周净增 ≥80,负反馈≈0。

### Phase 2 · 3k → 5k 粉:「系列化 + 声音」(预计 2 个月)

- 回复:原创调到 **50/50**。回复继续做,但从"广撒"转向"深耕"——重点经营已回复过 3 次以上、对方有回应的 KOL 关系。
- 每周 2 条 thread + 开 1 个固定 Spaces 栏目(周更,邀 §2 名单里有过互动的嘉宾,剪 60s 片段二次分发——调研 #9 冷启动放大器第一梯队)。
- 置顶 thread 换成转化率最高的身份梗串(调研 #6:每 3–6 月轮换)。
- 开 X Premium(长文 + 回复加权,Phase 1 末期即可开)。
- 开始做数据图帖:链上数据 / 解锁日历可视化(调研 #3 格式优先级第三档,但在加密圈尤其能涨粉)。

**Phase 2 目标指标**:互动率 ≥2%,周净增 ≥150,主页访问→关注 ≥10%。

### Phase 3 · 5k → 10k 粉:「Thread 火力全开」(预计 2–3 个月)

- 调研 #3:**~5K 粉是算法大力推 thread 的门槛**,此阶段 thread 升为主武器:每周 3 条,首推按 §3.5 满分标准打磨(首推决定整串生死)。
- 原创:回复 = 60/40。
- 长文(Premium Article)月更 1–2 篇:深度 launch 复盘,评论区放 TLS 链接(正文永不放链接)。
- Spaces 固定栏目 + 跨场客串(去别人的 Spaces 当嘉宾)。
- 争议单推 + 投票每周 1 次:反共识观点(对机制不对人,盯 OON 陷阱旗,赞跟不上回复就撤)。

**Phase 3 目标指标**:互动率 ≥2.5%,周净增 ≥300,thread 首推曝光 ≥粉丝数 3 倍。

### 全程红线(任何阶段不破)

- §3.1 高危标记 = 0 容忍,x-control 审批门已强制
- 不买粉、不互关圈、不 pod 互推(调研 #7)
- 新内容不突推单一 token,不晒无风险披露的盈利(调研 #4/#8)
- hashtag ≤2,外链只进评论区
- 每天看负反馈数,连续两天 >0 就复盘内容

---

## 5. 文风层(chase-voice 真实规则,20 轮 autoresearch 提炼自全量推文存档)

### 5.1 六条硬规则(任何情况不破,硬规则 #1 压倒一切包括时效)

1. **不编造数据**(lived/qualitative specificity only,永不发明数字)
2. **不碰中国政府/官员话题**
3. **不提 Binance**
4. **超过 2 行的帖子必须有 hook**
5. **AI 话题的论断必须先对照 landscape-ai-workflow + yage.ai 验证**
6. **不直接攻击具名个人**(与 §3.1 `callout_named_account` 同源)

### 5.2 语言形态

- **永远中文为主**,没有英文推文路径;英文素材消化成中文帖,不直译
- **Crypto-native 中英混排是声音本体**:DeFi、harness、real yield、agentic、perps 这类 terms of art 内嵌在中文句子里,**不过度汉化**
- **禁 `#` hashtag**(2022–24 存档里的 #财富密码 风格已过时,是 Grok slop 筛查的负分项);`$` cashtag($BTC)保留
- 融资数据格式:`$43M` / `$1B FDV`,日期 `YYYY.MM`,轮次英文内嵌(`Series A`),领投方括注(`a16z 领投`)

### 5.3 去AI味的两半(对齐 X 的 Grok slop_score)

**一半:像真人说话**——口语颗粒(了/的/吧/呢)、软化词(大概率/感觉/好像)、口癖转折(话说回来/仔细想想/毕竟/反正/说到底/难怪/居然)、省略号、网络slang;**招牌动作 = 成语收尾**("刻舟求剑大概率要被打脸了"),比任何干净的总结句都更像 Chase。同时检测翻译腔:抽象名词当主语、「很+形容词+冒号」、物理动词配抽象推理、"结构性"滥用。

**另一半:不是 generic**——每帖至少一个 first-party anchor:亲历的 founder/builder 细节、一个不显然的具名 specific、或带推理的反共识观点。slop 检测打的是"同质化/低成本",不是工具本身。

**最高纯度的去AI味 = 网感**:黑色幽默 + 荒诞 + 自嘲 + meme 素养 + degen 粗口边缘(以存档上限为准)。真正好笑的帖子本身就是 first-party anchor,不需要论点——X 的 banger 筛查直接奖励它。但 meme 必须当下,不冻结;安全线(无歧视语/不点名攻击/不碰官员/不提Binance)永远在上。

**禁用 tells**:不是…而是…、自问自答、铺垫式开场、中英 buzzword、方法论命名、报告腔开头。

### 5.4 八分支决策树(按内容形态选格式)

| 分支 | 形态 | 规则要点 |
|---|---|---|
| 1 | 配图说一句 | 一行裸 caption,无收尾无分析 |
| 2 | 平行对比(A vs B) | 恰好 N 行,无开头无收尾,标签中文为主英文内嵌 |
| 3 | 利空/利好信号清单 | 每行主语开头、一行一信号,收尾"大家注意风险。"/"标志性的XX" |
| 4 | 读古文有感 | `观察一,观察二,是个不可能三角,读《X》有感`(逗号不用破折号,引文收尾是签名) |
| 5 | 政策/监管长分析 | 定位动词开场("比较值得注意的是"),保留实体名 |
| 6 | 项目/TGE/launch 公告 | 单段中文,融资格式见 §5.2,一句中文 punchline 收尾 |
| 7 | **快讯观察**(对具体事件的反应) | 事实先行、2–4 短段、数字/入口/身份/动作密集、干冷后果收尾;先跑四问(第一问:这件事里最反常识的事实是什么?);breaking 子模式需 ≥2 独立信源 |
| 8 | 多点感想 | "讲几点感想:"+ 编号(有排序)或 dash(无排序),每点 ≤25 字,平收 |

开场三式:受 X 启发… / 第一行直接放最挑衅的论点再展开 / 个人下场("我自己也踩过这个坑…")。

### 5.5 与增长策略的咬合点

- 分支 7(快讯观察)+ breaking 子模式 = 调研 #5 时效内容的执行规范;**速度永远不压倒硬规则 #1**
- 分支 3(风险清单)= 调研 #4 最稳选题的格式落地
- 成语 punchline + 网感 = repostability 信号(§3.5)的中文版实现路径
- style_profile 自述:first-party 锚点的力度**留给 x-auto-loop 按真实表现数据校准**——正好对上 §8 的 feedback loop 设计

---

## 6. 一周节奏样板(Phase 1)

| 时段 | 一 | 二 | 三 | 四 | 五 | 六 | 日 |
|---|---|---|---|---|---|---|---|
| 早 6–8 | 回复×4 | 回复×4 | 回复×4 | 回复×4 | 回复×4 | 回复×3 | 回复×3 |
| 午 12–13 | 单推(数据) | 单推(观点) | **Thread** | 单推(风险清单) | 单推(观点) | 单推(BIP*) | 复盘周记 |
| 晚 20–22 | 单推+清评论区 | 单推+清评论区 | 清评论区 | 单推+清评论区 | 单推+清评论区 | 清评论区 | 清评论区 |

*BIP = build in public。每条原创发出后 2h 内回到评论区回复每一条。

---

## 7. 健康度仪表盘(周复盘指标)

| 指标 | 公式 | Phase 1 / 2 / 3 及格线 |
|---|---|---|
| 互动率 | 互动数 ÷ 曝光 | 1.5% / 2% / 2.5% |
| 净增长 | 新关注 − 取关 | +80 / +150 / +300 每周 |
| 主页转化 | 关注数 ÷ 主页访问 | — / 10% / 12% |
| 负反馈 | mute+block+report+not_interested | ≈0(任何阶段) |
| OON 陷阱数 | dashboard 旗标数 | 0 |
| 回复命中率 | 获 KOL 本人回应的回复 ÷ 总战略回复 | ≥10% |

---

## 8. X-auto-loop 能力核对 + 修订后的改进清单

> 2026-06-10 对 `X-auto-loop` 仓库逐项核对后的版本。先说结论:**这个 loop 比 §8 v2 假设的先进得多**——LLM 安全筛查、贝叶斯 bandit 学习回路、维度限定的 directive 闭环验证(`verify_prior`,apply 锚定的不相交队列)、结构性 dunk 杀开关都已在线。原清单 6 项里:2 项已基本建成、1 项失效、1 项被 X 政策封死要换地方做、2 项保留且框架就绪。

### 现有架构(核对所得)

radar 选题(last30days / kol / trending / marquee / convergence 多源,x-control-chase 作为 system 加载)→ chase-voice 起草(codex CLI,ollama 兜底)→ `guard.py` 正则守门 + **pre-publish LLM safety screen**(管判断型规则:编造数据/未验证 AI 论断/人身攻击)+ `judge.py`(substance/format/overall)→ 人工 pick → Typefully 发布(链接自动剥离到回复位,chase-voice Rule 7 已自动化)→ 2 天 impression 锁定 → **日度 postmortem**(top/bottom 20% voice 范例)+ **周度 analyst**(bandit 选臂 → 有界自动 directive → 下周验证,Chase 审计周报)。

### 逐项判定

| 原清单 | 判定 | 现状与动作 |
|---|---|---|
| #1 LLM 风险评审层 | **已基本建成** | guard.py(含 Binance + listing-desk 第一人称叙事拦截,2026-06-08 真实事故后加固)+ safety LLM screen + judge 三层已在线。剩余缺口:把 §3.1 的加密负反馈类别(engagement_bait / shill / price_target / dm_solicitation / callout)显式并入 safety screen 的检查单——一次 prompt 级小改 |
| #2 回复配额 feedback loop | **loop 做不了,移到 x-control** | Typefully **无法发布回复**(X 政策,GROWTH_ENGINE_PLAN 风险表里文档化的限制"no auto-reply actuator")。战略回复只能走 x-control(官方 API 可写)或手动。动作:参数化 `HARD_CAP_REPLIES_24H`→`reply_quota_daily` 改在 **x-control**,命中率从官方 API 的 mentions 读;X-auto-loop 不动 |
| #3 CJK 长度阈值 | **对 loop 失效,降级** | loop 的 judge 是 LLM,语言原生,没有这个问题。只剩 x-control 审批 UI 的显示层小修,优先级降到最低 |
| #4 kol_list 提纯 | **保留,双重收益** | 该文件同时喂 x-control monitor 和 loop 的 `kol` topic source,提纯一次两边受益。动作不变(中文区账号提权 + `lang: zh`,NASA/PopBase 类降噪),改在 x-control-chase 仓库 |
| #5 anchor 校准回路 | **框架全就绪,最高 ROI** | bandit 维度已有 hook_type / structure / length_bucket / cluster / job / archetype / lane / voice_variant / timing,新维度有 shadow→live 上线模式(archetype/lane 的 forab 集成就是先例)。缺口仅是 **anchor_type 不在维度列表**。动作:起草时打 anchor_type 标签(亲历/具名 specific/反共识/网感),注册为 bandit 维度,走 shadow gate 上线 |
| #6 健康度指标入周报 | **大部分已有** | 周度 analyst 报告(Chase 审计)、follower snapshots、**结构性 dunk 杀开关**(replies+quotes 高/likes 低的比例检测 = §3.4 OON 陷阱的自动化版,且零 prompt-injection 面)、dead-man ping 都在线。缺口:mute/block 在 Typefully 读不到(已用 dunk 比例兜底);回复命中率依赖 #2 在 x-control 侧落地 |

### 修订后的行动清单(按优先级)

1. **anchor_type 进 bandit**(原 #5):唯一"框架就绪、只差接线"的高 ROI 项,照 archetype/lane 的 shadow 先例做。
2. **x-control 侧:reply_quota_daily 参数化**(原 #2 移址):战略回复是 Phase 1 的 70%,但它在自动化栈里只有 x-control 这一条腿——配额、命中率统计、周度调节全做在那边。
3. **safety screen 检查单扩容**(原 #1 收尾):并入 x-control 风险类别,顺手把 §5.1 六条硬规则和它对齐成同一份清单。
4. **kol_list 提纯**(原 #4):一次改动,monitor 和 radar 双收益。
5. deconstruct.py(emotion-first 角度生成,Nora 挖矿成果)还在 shadow——攒够样本后评估转 live,对应调研 #4"逆向/争议观点"选题的自动化供给。

### ⚠️ 对策略本体的反作用修正

- **Phase 1 的 70% 战略回复是人肉动作**:自动回路只覆盖原创那 30%(选题→起草→审→发→学习)。每天早间的 KOL 评论区突击没有自动化兜底,必须进你本人的日程;x-control 只能做"找目标 + 审文案 + 官方 API 代发"的半自动。
- **身份梗措辞必须先过 guard.py**:2026-06-08 事故后,第一人称"上币桌/台/listing desk"叙事被高精度拦截(泛指的"$X 在 OKX 上线"不拦)。`identity_hints` 里 **"审过1000+项目"最安全**;"前顶级交易所上币团队"接近被拦的身份叙事边缘,启用前先拿 guard.py 跑一遍。

---

## 9. 一句话版本

**用「在顶级交易所审过 1000+ 项目」这个无法复制的身份,以 chase-voice 的中文口语+成语 punchline+网感写作,在中文加密/投资 KOL 的评论区做高密度、带数据的战略回复打开曝光;原创严守 3 单推/天 + 周更 thread 系列;所有内容过 x-control 风险门和 6 条硬规则(不编数据、不提币安、不碰官员、不点名攻击);到 5k 粉切换 thread 主火力;全程盯净增长和负反馈,不碰任何互动钓鱼。**
