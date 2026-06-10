# HANDOFF — convergence-radar × frontrun (x_live) 落地交接

把 frontrun 的取数机制落地进 convergence-radar 的交接文档。补丁已写好、
`py_compile` 通过,staged 在本文件夹。上个 session 因仓库 scope 只授权 `tls`
无法直接 push convergence-radar,故留此交接。

---

## 新 session 要 include 的仓库

**主任务必需:**
- `ckpxgfnksd-max/convergence-radar` — 要落地 + push 的目标
- `ckpxgfnksd-max/tls` — staged 补丁来源(`artifacts/convergence-radar-x-live/`)
- `ckpxgfnksd-max/chasewang-skills` — sync 镜像,验证同步链路

**若同时继续增长策略 / 改 X-auto-loop,一并加:**
- `ckpxgfnksd-max/X-auto-loop`
- `ckpxgfnksd-max/x-control`、`ckpxgfnksd-max/x-control-chase`
- `ckpxgfnksd-max/chase-voice`、`ckpxgfnksd-max/chase-funny-voice`
  (注:funny voice 实体在 chasewang-skills 镜像里)

---

## 粘给 Claude 的任务 prompt

```text
延续上个 session 的工作。背景:我在为 @ChaseWang 的 X 账号做增长基建,
上个 session 产出了一份分阶段增长策略(在 tls 仓库 claude/x-growth-strategy-custom-9pcfi4
分支的 GROWTH-STRATEGY.md),并逆向了 Xhunt / frontrun 两个 crypto 工具的 X 取数机制
(都是在登录态页面里 monkey-patch fetch/XHR/WebSocket 劫持 X 内部 GraphQL,不走官方 API;
frontrun 干净,Xhunt 有指纹外传/开放代理/钱包注入面,是反面教材)。

【本 session 的主任务】
把 frontrun 的取数机制落地进 convergence-radar,自动化它目前唯一需要人肉的源
(frontrun_trending,现在要人用 DevTools 从扩展抠 JSON 丢进 inbox)。

补丁代码已在上个 session 写好并 py_compile 通过,staged 在:
  tls 仓库 claude/x-growth-strategy-custom-9pcfi4 分支
  路径 artifacts/convergence-radar-x-live/
  含:scripts/fetchers/x_live.py、docs/X_LIVE.md、social.yaml.patch、README.md

x_live.py 用 headless Playwright 复用登录态 X profile,page.on("response") 劫持
HomeLatestTimeline/SearchTimeline/UserTweets 等 GraphQL,抽推文算 surge,写出
radar 已有 inbox adapter 能直接吃的 JSON(source 默认 frontrun_trending,可用
CR_X_SOURCE_ID 改 x_live)。只读、不外传、失败即跳过,刻意避开 Xhunt 那套脏东西。

请执行:
1. 先读 convergence-radar 现状,确认 inbox adapter 的 JSON schema 和
   sources/social.yaml 的 frontrun_trending 源行,核对 x_live.py 的输出格式
   与现有 adapter 完全对齐(字段名、source id、domain)。如有不一致以 radar
   现状为准修正 x_live.py。
2. 从 tls 分支取 staged 补丁,落进 convergence-radar 对应路径:
   scripts/fetchers/x_live.py、docs/X_LIVE.md;按需把 social.yaml.patch 的源行
   追加进 sources/social.yaml。
3. 把 x_live.fetch_x_live() 接进 radar 的 cycle/fetch 流程(一行调用,失败要
   像其它源一样 log + skip,不能 break 整个 cycle)。
4. py_compile + 跑 radar 现有测试(尤其 tests/test_inbox.py)确保没破坏。
5. commit + push 到 convergence-radar canonical 仓库。然后确认/触发 sync 链路
   (仓库的 sync workflow 镜像进 chasewang-skills → Studio skillsync cron 拉取),
   告诉我同步状态。

约束:不要无人值守发任何东西;x_live 是只读取数。push 前把要点讲给我听。
```

---

## 这批 staged 文件清单

| 文件 | 落进 convergence-radar 的位置 |
|---|---|
| `scripts/fetchers/x_live.py` | `scripts/fetchers/x_live.py` |
| `docs/X_LIVE.md` | `docs/X_LIVE.md` |
| `social.yaml.patch` | 追加到 `sources/social.yaml`(可选) |
| `README.md` | 仅交接说明,不落地 |
| `HANDOFF.md` | 本文件,仅交接说明,不落地 |

## 已知背景结论(供新 session 省去重查)

- radar 已有 `frontrun_trending` 源,adapter 是 `inbox`,读
  `$XDG_CACHE_HOME/convergence-radar/inbox/` 下的 JSON。
- inbox JSON schema:`{source, domain, items:[{url,title,body,published_at}]}`。
  x_live 默认还多写 item 级 `engagement`/`author` + 顶层 `fetched_at`;若 adapter
  严格校验 key,设 `CR_X_RICH_ITEMS=0` 只发 4 个 canonical key(step 1a 核实)。
- 已加 `tests/test_x_live.py`:不依赖 Playwright/登录态,喂合成 GraphQL payload
  走 `_walk → _trending → _write_inbox`,断言 inbox JSON 两种 shape 都对。6 个用例
  本 session 已跑通(`python tests/test_x_live.py`)。落进 radar 时放到其 tests/ 下。
- radar 的 "never fully fail" 契约:任何源出错只 log + skip,不能炸整个 cycle。
- sync 链路参照 chase-voice 的 `.github/workflows/sync-to-monorepo.yml`:
  push canonical → 镜像进 chasewang-skills → Studio skillsync cron 拉取。
- 安全红线(Xhunt 反面教材):不做设备指纹外传、background 不开放无校验 HTTP
  代理、不混淆头部、不留钱包注入面、远端 flag 要可审计。x_live 只读 X 自己
  emit 的 GraphQL 响应并写本地文件。
