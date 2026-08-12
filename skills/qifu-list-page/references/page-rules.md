# 奇富标准列表页通用规则

本文件是列表页结构、组合选择与页面级布局的唯一权威来源。平台导航、颜色与差异组件由当前 `platform-*.md` 覆盖；精确组件名称、节点、属性和 Slot 同步方法见 `component-map.md`。

## 目录

- [页面组合注册表](#1-页面组合注册表)
- [画板与页面骨架](#2-画板与页面骨架)
- [上下文导航与标题](#3-上下文导航与标题)
- [筛选条件](#4-筛选条件)
- [列表操作栏](#5-列表操作栏)
- [表格与列](#6-表格与列)
- [数据、状态与分页](#7-数据状态与分页)
- [响应规则](#8-响应规则)
- [节点命名](#9-节点命名)
- [页面级验收](#10-页面级验收)

## 1. 页面组合注册表

`compositionName` 描述 `List Page Shell-V2 + Filter Bar-V2 + 可选 List Action Bar + Table Shell-V2` 的稳定结构，不是 Figma 组件母版名称。

| `compositionName` | 适用场景 | Filter Bar | List Action Bar | Table Shell | `rowsSlot` | Pagination |
| --- | --- | --- | --- | --- | --- | --- |
| `Qifu List Page / Basic Table` | 无筛选条件的普通数据列表 | 隐藏 | 按 `listActions` 显示 | `selection=off` | 数据行 | 默认显示 |
| `Qifu List Page / Basic Filter Table` | 1–4 个常用筛选条件；默认组合 | 单行，`expanded=false` | 按 `listActions` 显示 | `selection=off` | 数据行 | 默认显示 |
| `Qifu List Page / Advanced Filter Table` | 5 个以上筛选条件或明确要求更多筛选 | 两行，`expanded=true` | 按 `listActions` 显示 | `selection=off` | 数据行 | 默认显示 |
| `Qifu List Page / Selectable Filter Table` | 需要行选择或批量操作 | 1–4 项单行，更多时两行 | 批量动作存在时显示 | `selection=on` | 数据行 | 默认显示 |
| `Qifu List Page / Loading Table` | 首次加载或刷新状态 | 按筛选需求显示 | 默认隐藏 | `selection=off` | Loading | 隐藏 |
| `Qifu List Page / Empty Table` | 无数据、无结果、无权限或加载失败 | 按筛选需求显示 | 默认隐藏 | `selection=off` | Empty 与对应状态 | 隐藏 |

选择顺序：Loading/Empty → 需要选择或批量操作 → 5 个以上筛选 → 1–4 个筛选 → 无筛选。未指定且无法区分时使用 `Qifu List Page / Basic Filter Table`。

组合名称只决定稳定骨架。标题、筛选显示形式、触发方式、业务字段、操作、列、数据、表格 `size/type` 和分页总数继续来自 `PageSpec`；不要为这些独立配置新增组合名。新场景先用最接近组合并记录缺口，只有确认需要长期复用后才扩展注册表。

每次内部解析：

```text
compositionName
showFilterBar / filterBarExpanded
showListActionBar
tableSelection
rowsState
showPagination
```

## 2. 画板与页面骨架

默认只生成桌面端：

| 场景 | 画板 | 规则 |
| --- | ---: | --- |
| 常规中后台页面 | 1366 × 768 | 默认选择；先压缩非关键列，不压缩组件真实高度 |
| 宽屏或高信息密度 | 1920 × 1080 | 长文本列弹性扩展；必要时横向滚动 |

测试、效果验证、试生成和 Skill 回归统一放入既有 Figma Page `测试`（node `3497:651`）；正式交付且用户明确目标 Page 时例外。

使用以下结构：

```text
Page / List / <pageName> / Default
├── Header（当前平台真实组件）
└── Workspace
    ├── SideNavigation（当前平台真实组件）
    └── Content（灰色背景）
        └── Page Surface（白色，距 Content 四周 12px）
            ├── ContextNavigation（按需）
            └── List Page Shell-V2 Instance（距 Page Surface 四周 16px）
                ├── pageHeaderSlot
                ├── filterBarSlot → Filter Bar-V2 Instance
                └── tableSlot
                    ├── 无列表操作：Table Shell-V2 Instance
                    └── 有列表操作：Data Region（Vertical，gap 12）
                        ├── List Action Bar（页面级组合）
                        └── Table Shell-V2 Instance
                            ├── headerSlot
                            ├── rowsSlot
                            └── paginationSlot
Audit / Missing Components（仅有缺口时，放在画板外侧）
```

Page Surface 的 16px 是唯一页面内容外边距。Filter Bar 可见底边到 List Action Bar 顶边固定为 16px；List Action Bar 到 Table Shell、以及其他相邻可见区块保持 12px。内部区块不得再次叠加外层 padding。Pagination 只存在于 Table Shell 的 `paginationSlot`。

先创建外层，再实例化 List Page Shell-V2，最后替换 Slot。组合只控制 Slot 状态，不取代组件正式名称；组件实现全部按 `component-map.md`。

## 3. 上下文导航与标题

先读取当前平台文件确定 Header、SideNavigation、菜单、颜色与平台组件，再判断内容区导航：

- 单一路径、无同级切换：按业务需要使用标题；
- 多层路径：使用 Breadcrumb；标题仍独立服从 PageSpec；
- 同级视图切换：使用 Tabs；标题仍独立服从 PageSpec；
- 多任务可关闭页签：需要 WorkspaceTabs，普通 Tabs 不得冒充。

一张默认页面只允许一个叶子菜单处于当前选中状态。父菜单展开、当前页选中和祖先路径高亮必须分别处理，具体样式由平台文件定义。

标题不是必选项。需要时为 16px，PageHeader padding 为 0，标题落在 Page Surface 左上 16px 内容边界；不需要时关闭整个 PageHeader，不保留空白占位。整页只保留一个视觉最强主动作，使用“动词 + 对象”文案。

## 4. 筛选条件

| 字段语义 | 控件 |
| --- | --- |
| 实时模糊文本 | Search |
| 按钮触发的模糊文本、精确文本或编号 | Input |
| 单选/多选枚举 | Select Single / Multiple |
| 独立布尔条件 | Checkbox |
| 单日/日期范围 | DatePicker / DateRange |
| 组织、地区、类目层级 | Cascader |

页面规则：

- 1–4 项使用单行；5–8 项允许两行；更多时首屏保留 3–5 个高频项并提供更多筛选。小屏不论直接筛选框还是带标题筛选项，均优先尝试保持 4 项一行。
- 每个字段使用 Filter Item-V2 包裹真实控件。常规宽度使用 `120 / 160 / 200 / 304 / 408px`，默认 200px；日期范围和长文本使用 304/408px。小屏为容纳 4 项时，非日期控件允许统一缩至 180px，日期范围仍保持 304px。
- Filter Item 与内部控件为 FIXED，不使用 FILL 拉伸。筛选 Slot 使用水平 Auto Layout 并开启 WRAP；常规横向/换行间距为 12px。小屏 4 项一行时，4 个筛选项的剩余横向空间通过 `SPACE_BETWEEN` 或等效方式均分到项间，控件自身宽度不得被均分。
- `直接筛选框` 总宽度等于控件宽度；`带标题筛选项` 为“标题 HUG + 0px + 控件宽度”，标题与控件紧贴，以实际几何间距验证。
- 普通页面统一使用 32px 控件；同一筛选栏不得混用显示形式、标题字号或控件高度。
- Filter Bar padding 为 0；首个筛选项与页面主操作直接对齐 Page Surface 左右 16px 内容边界。
- `实时触发` 不显示确定/重置，文本模糊搜索使用 Search；`按钮触发` 统一显示确定/重置，文本筛选使用 Input。两种触发只能选择一种。
- 按钮触发时，确定/重置跟随筛选项最后一行；页面主操作固定在第一行最右侧，不与查询按钮混为一组。
- `showQuickFilters`、`showPrimaryAction` 默认关闭，只有 PageSpec 明确需要时开启。

精确组件属性、尺寸映射、文本属性和 Slot 最小高度见 `component-map.md`。

## 5. 列表操作栏

只有 `listActions.left[]` 或 `listActions.right[]` 非空时才创建：

```text
tableSlot → Data Region（Vertical, Fill, gap 12）
├── List Action Bar（Horizontal, Fill, height 32, padding 0）
│   ├── List Actions / Left（Hug, gap 8）
│   ├── Flexible Spacer（Fill）
│   └── List Actions / Right（Hug, gap 8）
└── Table Shell-V2 Instance
```

Filter Bar 可见底边到 List Action Bar 顶边固定为 16px；Data Region 内 List Action Bar 到 Table Shell 的间距仍为 12px。

- 左侧放与选择或当前数据相关的批量动作；依赖选择的动作在零选择时可见但禁用，危险动作需要确认。
- 右侧先放 `listActions.right[]` 中的刷新、导入、导出、列设置等次要动作，再放 `primaryAction`；主动作只通过 `primaryAction.placement=listActions.right` 表达，不重复写入右侧数组，唯一 Primary 固定在最右侧。
- 确定/重置只属于 Filter Bar；查看、编辑、删除等单条动作只属于表格行。
- 操作栏出现时关闭 Filter Bar 的 `showPrimaryAction`，同一动作不得重复。
- 操作过多时保留高频项并使用已有更多菜单；无可复用能力时记录缺口，不换行或缩小按钮。

## 6. 表格与列

先由组合确定 `selection` 与 `rowsSlot` 状态，再形成唯一 `TableStyleSpec={size,type,selection}`。未指定时默认 `size=large 大 44px`、`type=basic 基础`，`selection` 由组合决定。自定义 Slot 后必须按 `component-map.md` 逐层同步所有 Header Cell、Row、Content Cell 与 Selection Cell，并重算 Table Shell 高度。

列宽按语义分配：

| 语义 | 行为 |
| --- | --- |
| 序号、短 ID | 窄列 |
| 名称 | 中等宽度，保持可读 |
| 长文本、URL | 弹性列，单行省略，配 Tooltip 或查看 |
| 数字 | 右对齐，必要时千分位 |
| 日期时间 | 稳定宽度与格式 |
| 状态 | 稳定宽度 |
| 操作 | 动作组右对齐，右侧 20px；表头左边缘对齐第一个动作文案 |

所有列宽之和等于表格可用宽度，表头与每行使用同一列宽数组；第一列贴左、最后一列贴右，不使用 `SPACE_BETWEEN` 制造空白带。

行操作 1–4 个时使用 Action Content-V2；超过 4 个收纳低频操作。删除、解绑、停用等高风险操作需要确认。状态切换动作必须随记录状态变化：启用记录显示“停用”，禁用记录显示“启用”。

## 7. 数据、状态与分页

- 默认展示 5–10 行有差异的虚构或脱敏示例数据；`1366 × 768` 常规结构优先 9 行，空间允许时 10 行。
- 名称长短有差异，至少覆盖两种状态；长文本至少一条触发省略，不使用真实个人敏感信息。
- 二元状态使用 Tag：启用为 success，禁用为 danger；精确变体见 `component-map.md`。多状态场景使用 Status Content-V2。
- 默认画面只交付 Data、Loading 或 Empty 中的一种状态，不同时堆叠。
- Pagination 紧跟最后一行；根据 `pageCount=ceil(total/pageSize)` 选择页数变体。Loading、Empty 或明确无分页时按组合隐藏。
- 分页可见右边缘必须与 Table Shell 可见右边缘一致；母版 Slot 过宽时使用右侧补偿，不拉伸分页填空。

## 8. 响应规则

- Header 填充宽度，SideNavigation 保持平台规定宽度，Content 填充剩余空间。
- Filter Bar 允许整项换行；List Action Bar 不换行。
- 表格关键列保持稳定，长文本列承担收缩；必要时明确横向滚动，不缩小字号或控件高度。
- 从 1366 切换到 1920 时必须显式调整 Page Surface、List Page Shell、Table Shell 和列宽，不能只 resize 根画板。
- 只在用户明确要求时制作窄屏或移动端。

## 9. 节点命名

```text
Page / List / <Object> / Default
Header / Global
Workspace
Navigation / Side
Content
ContextNavigation
PageHeader
FilterToolbar
Filter / <field>
Action / Primary
DataRegion
List Action Bar
List Actions / Left
List Actions / Right
Table
Column / <field>
Row / <index>
Cell / <field>
Pagination-V2
Audit / Missing Components
Fallback / <capability>
```

## 10. 页面级验收

- `compositionName` 与注册表完全一致，筛选栏、展开方式、操作栏、选择列、状态和分页符合组合。
- 平台、顶部入口、侧栏路径、唯一当前页、祖先激活与展开组符合 PageSpec 和当前平台文件。
- 页面外壳、Filter Bar、Table Shell 及可复用元素保持真实实例关系；缺口才使用命名明确的页面级 Fallback。
- Content 为灰色，Page Surface 为白色；12px 外间距、16px 内容边距正确；筛选区到列表操作栏为 16px，列表操作栏到表格为 12px。
- 标题开关、筛选显示形式、触发方式、查询动作、列表操作、主动作和行操作没有重复或错位。
- 筛选项宽度属于规定阶梯或小屏 180px 例外，32px 控件及父 Row/Slot 不裁切；小屏优先 4 项一行且剩余空间均分到项间，带标题筛选项的标题到控件为 0px。
- 表头与数据行列宽一致并连续铺满；选择列数量、危险操作语义、状态文案与 PageSpec 一致；表头选择单元格背景使用 `背景色/--qifu-bg-color-canvas`。
- Table Shell 高度包住表头、全部数据行和分页；分页紧跟数据行且右边缘对齐。
- 无文字截断、节点重叠、画板溢出、异常空白、placeholder shimmer、临时截图或参考图栅格。
- 存在缺口时已创建 `Audit / Missing Components`，并且只记录当前页面实际遇到的缺口。
