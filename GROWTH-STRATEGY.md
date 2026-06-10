# GROWTH-STRATEGY.md — Chase 的 X 定制化增长策略

> 目标:纯涨粉 + 扩大影响力。现状 1k–1万粉,中文为主,投资/经济/加密/创业领域。
> 本文 = 已验证的通用调研结论 × 仓库真实数据(x-control 算法标记 + 身份/KOL 代理数据)。
> 生成日期:2026-06-10

---

## 0. 数据来源与置信度

| 数据 | 来源 | 置信度 |
|---|---|---|
| 算法风险标记 + 信号面板 + 硬性上限 | `x-control`(公开仓库,已完整读取 `signals.py` / `queue.py` / `approve.py` / SKILL.md) | **高 — 真实代码** |
| 身份/人设 | `tls` README(Chase Wang,ex-Binance listing team,审过 1,000+ 项目,2025 年上线 ~100 个 token) | **高 — 本人所写** |
| KOL 名单 | `x-control/kol_list.example.md`(本人为自己领域写的种子名单) | **中 — 是真实方向,但 `x-control-chase` 私有仓库里的正式 `kol_list.md` 本会话无权访问,未经核对** |
| 文风规则 | `chase-voice` 私有仓库 **无权访问** | **缺失 — 本文只用 x-control 中已编码的反 AI 味规则作为文风底线** |
| 通用调研结论 1–10 | 用户提供,已验证 | 高 |

⚠️ **访问缺口**:`x-control-chase` 和 `chase-voice` 均为私有仓库,本会话的 GitHub 授权仅覆盖 `tls`。把这两个仓库加入会话授权后,可出 v2 精修版(替换 §2 种子名单、补全 §5 文风层)。

---

## 1. 身份资产(identity_hints)

从 tls README 提炼的人设,这是别人没有的护城河,**每条高杠杆内容都应露出其一**:

- **ex-Binance listing team**(顶级 CEX 上币视角)
- **审过 1,000+ 项目**(样本量碾压几乎所有 KOL)
- **2025 年上线 ~100 个 token**(实操而非纸上谈兵)
- **正在 build TLS(Token Launch Stack)**(build in public 素材,公开仓库可链)

写入 x-control 草稿 frontmatter 的建议值:

```yaml
identity_hints: ["ex-Binance listing", "审过1000+项目", "2025年上线~100个token"]
```

> 注意:`profile_click_pull` 信号的 `_IDENTITY_TEASE_PATTERNS` 正则只识别英文模式(`ex-`、`I built`、`N years at`)。中文身份梗(如"前币安上币团队")**不会被信号面板识别**,但写英文 hint `ex-Binance` 可以命中。见 §8 改进清单。

对应调研结论 #8(加密圈身份可信度建设)和 #6(主页转化):bio 必须一句话说清 ——「前币安上币团队 · 审过 1000+ 项目 · 帮 founder 把 token launch 做对」这个量级的表述。

---

## 2. 战略回复目标名单(KOL list)

来自 `x-control/kol_list.example.md`(自述"Seed list reflects a crypto / DeFi / AI niche"),按战略回复的杠杆率重新分层。调研结论 #2 说最佳猎场是**粉丝为你 2–20 倍**的账号(按 5k 粉计 = 1万–10万粉),百万级大V回复区竞争太激烈,只做选择性出击:

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

**待办**:用 `x-control-chase/kol_list.md` 的正式版替换此表;并补充 **中文区同领域 1万–10万粉账号**(目前种子名单全是英文区,与"中文为主"的定位存在缺口——中文 KOL 回复区才是中文粉丝的主要来源)。

---

## 3. 算法红线(来自 x-control 真实代码,grounded in xai-org/x-algorithm)

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
| profile-click-pull | 正文露出 identity_hints("ex-Binance…") |
| follow-author-reason | 系列标记("Day 3 / 每周复盘 / 3/7")+ 持续价值预告 |
| topic-fit | topic_tags 与自己 30 天话题分布重叠(别突然跳出领域) |

---

## 4. 分阶段作战计划

### Phase 1 · 1k → 3k 粉:「评论区猎人」(预计 2–3 个月)

精力分配 **70% 战略回复 / 30% 原创**(调研 #2)。

**每日动作:**
- 早 6:00–8:00:跑 `x-control` pulse → 扫 §2 A 层名单过去 12h 新帖 → 选 3–5 条,15 分钟窗口内回复(2–3 句:补数据 / 补 1000+ 项目样本里的反例 / 提犀利问题)。**严禁 "Great post" 类空话。**
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

## 5. 文风层(占位 — 等 chase-voice 接入)

`chase-voice` 私有仓库本会话无法读取。当前文风底线 = x-control 已编码的反 AI 味规则(§3.1 `ai_slop_openers` + §3.2 结构性标记)反推:

- 开头直接进观点/数字,不要铺垫式开场白
- 单推 ≤2 个破折号、≤4 个 emoji、不用推内编号列表(要列表就发 thread)
- 断言句优先,砍掉 hedge 词
- **待 chase-voice 接入后补全**:口癖、句长分布、中英混排习惯、禁用词表、20 轮 autoresearch 出的核心规则

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

## 8. X-auto-loop 改进清单(基于本次代码审读的发现)

1. **🔴 中文盲区(最高优先级)**:x-control 所有风险正则和信号正则均为英文模式。中文内容下 `engagement_bait`("同意请点赞")、`ai_slop_openers`("让我解释一下/说实话/没人告诉你")、`_ASSERTION`/`_HEDGE`("我觉得/大概/可能")、`_CONTRARIAN_FRAME`("不受欢迎的观点/真相是")、`_IDENTITY_TEASE`("前币安/我做过")**全部不触发**。对一个中文为主的账号,风险面板目前形同虚设——需要为每个 pattern 增加中文对照正则。
2. **🔴 回复硬上限冲突**:`HARD_CAP_REPLIES_24H = 2` 与 Phase 1 核心打法(每天 20+ 条战略回复)直接矛盾。该上限的本意是限制"对 mention 的被动回复",但代码按 `in_reply_to`/开头 `@` 判定,会卡死主动战略回复。需要区分两类回复,或对 KOL 名单内的回复豁免/单独配额。
3. **🟡 repostability 长度阈值英文偏置**:80–240 字符的"可引用长度"按英文校准;中文信息密度约 2 倍,等效区间约 40–120 字,需要按 CJK 字符占比动态调整。
4. **🟡 kol_list 缺中文区目标**:种子名单全英文区,Phase 1 主猎场需要补 1万–10万粉的中文投资/加密账号,并加 `lang` 列。
5. **🟢 接入 chase-voice 作为发帖前的文风 lint 层**(目前只有反 AI 味底线,没有"像 Chase"的正向校验)。
6. **🟢 把 §7 健康度指标(尤其回复命中率、OON 陷阱数)纳入 weekly_review 自动产出**。

---

## 9. 一句话版本

**用「审过 1000+ 项目的前币安上币人」这个无法复制的身份,在中文加密/投资 KOL 的评论区做高密度、带数据的战略回复打开曝光;原创严守 3 单推/天 + 周更 thread 系列;所有内容过 x-control 风险门;到 5k 粉切换 thread 主火力;全程盯净增长和负反馈,不碰任何互动钓鱼。**
