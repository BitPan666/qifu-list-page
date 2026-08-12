---
name: qifu-list-page
description: Use when creating, updating, or auditing standard Qifu desktop list pages in Figma from business descriptions, fields, screenshots, or wireframes, including platform navigation, optional titles, filters, list actions, tables, states, pagination, and component-gap checks. Do not use for dashboards, forms, detail pages, tree tables, or highly customized workbenches.
---

# Qifu List Page

把业务描述转换为结构清楚、可编辑、保持真实组件实例关系的奇富中后台列表页。页面规则跨平台复用，平台导航、视觉和组件差异按当前目标平台加载。

## 读取路由

每次完整读取：

- [通用页面规则](references/page-rules.md)：页面组合、布局、筛选、操作栏、表格、状态与验收规则。
- [公共组件映射](references/component-map.md)：真实组件名称、节点、发布键、属性、Slot 同步方式和已知缺口。

再根据 `platform` 只读取一个平台文件：

| `platform` | 平台资料 |
| --- | --- |
| `yushu` | [毓数平台基线](references/platform-yushu.md) |
| `dianxiao` | `references/platform-dianxiao.md`，仅在文件存在时读取 |
| `jinyumeng` | `references/platform-jinyumeng.md`，仅在文件存在时读取 |

用户明确平台时不得读取或套用其他平台的菜单、颜色和组件。平台文件不存在时，先检查目标 Figma 文件中的真实导航、同类页面和变量；仍无法确定会改变页面框架的信息时再提问，并把未确认项记录为平台缺口。不要用毓数规则临时代替其他平台。

平台文件只记录相对通用规则的差异，固定包含：平台标识、Header、侧栏菜单、视觉 Token 覆盖、组件覆盖和已知缺口。不要复制 `page-rules.md` 的筛选/表格规则或整份 `component-map.md`；没有差异的部分直接继承公共规则。

任何 `use_figma` 调用前加载并遵循 `figma-use`；创建或更新完整页面时同时加载并遵循 `figma-generate-design`。若目标项目存在 `AGENTS.md` 或项目级规则，先读取并遵循。

## 规则优先级

在不破坏真实组件实例和目标文件安全的前提下，按以下顺序解决冲突：

1. 用户当前明确要求；
2. 当前平台文件中的差异与覆盖规则；
3. `page-rules.md` 的通用页面规则；
4. `component-map.md` 记录的组件默认值和实现限制。

同一条规则只在其权威文件中维护。`SKILL.md` 负责流程与路由，不重复详细尺寸、组件属性或平台菜单。

## PageSpec 输入契约

接受自然语言、字段清单、截图或线框，不要求用户填写表格。提取或合理补全：

```text
pageName / pageTitle
platform / headerActive
sidePath[] / sideActive / sideExpanded[] / sideAncestorsActive[]
compositionName
filters[]: field, control, placeholder, required, defaultValue, widthTier
filterItemDisplay: 直接筛选框 | 带标题筛选项
filterTrigger: 实时触发 | 按钮触发
controlSize
primaryAction: text, placement=filterBar|listActions.right；没有时为 null
listActions.left[] / listActions.right[]；right 只记录主动作之外的次要动作
columns[] / rowActions[] / status
pagination / viewport / targetPage / data
```

解析顺序固定为：平台 → 顶部入口 → 侧栏完整路径 → 页面名称与标题 → 筛选 → 列表操作栏 → 页面主动作 → 表格 → 行操作 → 状态、数据与画板。

只在缺失信息会改变页面主结构、平台外壳或造成高风险误导时提问。其余内容按常见后台场景补全，并在交付中列出假设。用户未指定平台且目标文件没有可靠上下文时，暂按 `yushu` 形成草案并明确标注该假设；不得静默推断。

## 工作流

### 1. 形成页面规格

1. 从输入提取 `PageSpec`。
2. 按 `page-rules.md` 的组合决策表确定唯一 `compositionName`；完整名称精确匹配，未指定时按场景选择，不创造近义别名。
3. 将筛选条件映射为 Input、Search、Select、Checkbox、DatePicker 等语义控件。
4. 将动作分为查询动作、列表操作栏左侧动作、列表操作栏右侧次要动作、单一主动作和行操作；主动作通过 `primaryAction.placement` 决定位置，不重复写入 `listActions.right[]`。
5. 将列标注为 identifier、name、long-text、number、date、status、action 等语义。

### 2. 确认平台与目标位置

1. 根据读取路由只加载当前平台资料。
2. 解析 `headerActive`、`sidePath`、`sideActive`、`sideExpanded`，并从 `sidePath` 排除 `sideActive` 得到 `sideAncestorsActive`。
3. 确认目标 Figma 文件、Page 和插入位置，不默认写入第一个 Page。
4. 测试、效果验证、试生成和 Skill 回归固定复用 Page `测试`（node `3497:651`）；正式交付按用户指定。

### 3. 盘点组件

1. 按 `component-map.md` 的精确名称解析组件；节点失效时按名称重新发现，不猜测新 ID。
2. 同文件使用本地组件节点创建实例；跨文件使用发布键导入。
3. 记录 `resolved / fallback / missing`。平台专属映射优先覆盖公共映射，未完成盘点前不开始写页面。

### 4. 创建页面

1. 先创建唯一顶层画板，再组装平台 Header、SideNavigation、Content 和 Page Surface。
2. 内容区优先使用 `Templates / List Page Shell-V2` 实例，并按 `compositionName` 配置 PageHeader、Filter Bar、可选 List Action Bar、Table Shell 和 Pagination Slot。
3. 按 `page-rules.md` 完成标题、筛选、操作栏、表格、状态、数据与响应布局。
4. 按 `component-map.md` 写入真实组件属性；自定义表格 Slot 后必须按映射逐层同步 `TableStyleSpec` 并重算外壳高度。
5. 按当前平台文件组装导航、菜单、颜色和差异组件；平台文件没有声明的内容继续使用通用规则。

### 5. 处理缺口

1. 优先使用现有真实组件的合法组合。
2. 无法满足时使用页面级最小降级，命名为 `Fallback / <Capability>`，不冒充正式组件。
3. 在画板相邻位置创建 `Audit / Missing Components`，记录能力、场景、降级方案和建议属性。
4. 不擅自修改或发布组件库母版；需要补齐平台基线或公共组件时在交付中单独列出。

### 6. 验证与交付

按 `page-rules.md`、`component-map.md` 和当前平台文件的验收要求逐区截图检查，再检查整页。至少确认：

- 页面结构、组合名称、平台外壳和 PageSpec 一致；
- 所有可复用设计系统元素仍为真实实例，Slot 和属性关系正确；
- 筛选显示形式、触发方式、列表操作、选择列、数据状态和分页没有串位；
- 无文字截断、节点重叠、画板溢出、异常空白、临时截图或占位内容；
- 组件缺口与运行时假设已记录。

完成后返回：页面节点 ID 与名称、`compositionName`、主要组件及关键变体、平台与输入假设、组件缺口、视觉与结构验证结果。

## 硬性约束

- 不把参考图作为栅格图片直接交付。
- 不重画已有组件，不分离实例修改外观，不破坏变量绑定。
- 不擅自改动、补充或发布组件库母版。
- 不把页面级 List Action Bar 冒充或发布成正式组件。
- 不把一个平台的导航、颜色、组件映射复制到另一个平台。
- 不把复杂看板、编辑表单、详情页、树表或高度定制工作台硬塞进本 Skill。
- 不宣称缺失组件已经存在；明确区分正式实例、页面级组合与降级实现。
