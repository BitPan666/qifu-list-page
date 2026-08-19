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
- [组件调用契约](references/component-invocation-contract.md)：真实属性 Key 动态解析、属性类型、INSTANCE_SWAP、Slot 写入和回读验证。
- [结构化验收契约](references/structural-validation.md)：实例关系、数量、变量、禁止特征和交付门禁。

同时读取根目录 `VERSION`。交付时返回该版本；Git Commit 可读取时一并返回。

再根据 `platform` 只读取一个平台文件：

| `platform` | 平台资料 |
| --- | --- |
| `yushu` | [毓数平台基线](references/platform-yushu.md) |
| `dianxiao` | `references/platform-dianxiao.md`，仅在文件存在时读取 |
| `jinyumeng` | `references/platform-jinyumeng.md`，仅在文件存在时读取 |

用户明确平台时不得读取或套用其他平台的菜单、颜色和组件。平台文件不存在时，先检查目标 Figma 文件中的真实导航、同类页面和变量；仍无法确定会改变页面框架的信息时再提问，并把未确认项记录为平台缺口。不要用毓数规则临时代替其他平台。

平台文件只记录相对通用规则的差异，固定包含：平台标识、Header、侧栏菜单、视觉 Token 覆盖、组件覆盖和已知缺口。不要复制 `page-rules.md` 的筛选/表格规则或整份 `component-map.md`；没有差异的部分直接继承公共规则。

任何 `use_figma` 调用前加载并遵循 `figma-use`；创建或更新完整页面时同时加载并遵循 `figma-generate-design`。若目标项目存在 `AGENTS.md` 或项目级规则，先读取并遵循。

业务提示词首句必须显式调用 `@figma` 插件。在 Codex 输入框输入 `@figma` 并选择当前用户已连接的 Figma Connector；不同用户的 Connector ID 可能不同，因此提示词、示例和 Skill 不得写死 `app://connector_*`。未连接或无法调用 Figma 时停止并报告，不把网页访问或手绘内容当作替代。

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
navigationMode=yushuPreset|custom；未填时为 yushuPreset
sidePath[] / sideActive / sideExpanded[] / sideAncestorsActive[] / sideActiveLevel
customSideMenu.level1[]: label, iconComponentName, hasChildren
customSideMenu.activeLevel1Children[]: label, hasChildren
customSideMenu.activeLevel2Children[]: label
compositionName
filters[]: field, control, placeholder, required, defaultValue, widthTier
filterItemDisplay: 直接筛选框 | 带标题筛选项
filterTrigger: 实时触发 | 按钮触发
controlSize
primaryAction: text, placement=listActions.left|listActions.right；没有时为 null
listActions.left[] / listActions.right[]；right 只记录主动作之外的次要动作
columns[] / rowActions[] / status
tableSelection=true|false；对应提示词“左侧是否有多选框：是/否”，未填写时为 false
pagination / viewport / targetPage / data
```

解析顺序固定为：平台 → 顶部入口 → 侧栏完整路径 → 页面名称与标题 → 筛选 → 列表操作栏 → 页面主动作 → 表格列 → 表格多选框 → 行操作 → 状态、数据与画板。

只在缺失信息会改变页面主结构、平台外壳或造成高风险误导时提问。其余内容按常见后台场景补全，并在交付中列出假设。用户未指定平台且目标文件没有可靠上下文时，暂按 `yushu` 形成草案并明确标注该假设；不得静默推断。

`navigationMode=yushuPreset` 时，`sidePath` 必须存在于毓数默认菜单基线；不在基线且没有切换为 `custom` 时，必须先询问真实父级，不得把新菜单自动追加为一级菜单。`navigationMode=custom` 时按平台文件要求校验完整路径、一级菜单、当前一级下的二级菜单、必要的三级菜单和一级真实 Icon 组件名；缺少会改变层级、箭头或选中状态的信息时停止提问，不自行补树。

## 工作流

### 1. 形成页面规格

1. 从输入提取 `PageSpec`。
2. 按 `page-rules.md` 的组合决策表确定唯一 `compositionName`；完整名称精确匹配，未指定时按场景选择，不创造近义别名。
3. 将筛选条件映射为 Input、Search、Select、Checkbox、DatePicker 等语义控件。
4. 将动作分为查询动作、列表操作栏左侧动作、列表操作栏右侧次要动作、单一主动作和行操作；主动作通过 `primaryAction.placement` 决定列表操作栏最左或最右，不重复写入左右次要动作数组。列表操作文案只决定按钮，不推断表格是否可选择。
5. 将列标注为 identifier、name、long-text、number、date、status、action 等语义；1366px 画板最多保留 8 个业务列，操作列和状态列计入，自动选择列不计入。
6. 只从“左侧是否有多选框”解析 `tableSelection`：是=`true`，否或未填写=`false`；不得根据“批量”等按钮文案自动开启选择列。

### 2. 确认平台与目标位置

1. 根据读取路由只加载当前平台资料。
2. 解析 `navigationMode`、`headerActive` 和 `sidePath`；`sideActive` 固定为路径最后一项，`sideActiveLevel=sidePath.length`，`sideExpanded` 与 `sideAncestorsActive` 固定为路径中除最后一项外的祖先，不允许额外展开其他菜单。
3. 确认目标 Figma 文件、Page 和插入位置，不默认写入第一个 Page。
4. 测试、效果验证、试生成和 Skill 回归固定复用 Page `测试`（node `3497:651`）；正式交付按用户指定。

### 3. 盘点组件

1. 按 `component-map.md` 的精确名称解析组件；节点失效时按名称重新发现，不猜测新 ID。
2. 同文件使用本地组件节点创建实例；跨文件使用发布键导入。
3. 按 `component-invocation-contract.md` 建立 `ComponentResolutionManifest`，记录来源、组件 ID、实例 ID 和 `resolved / missing / ambiguous / failed`。
4. 平台专属映射优先覆盖公共映射。所有必需组件均为 `resolved` 后才开始写页面。

### 4. 创建页面

1. 先创建唯一顶层画板，再组装平台 Header、SideNavigation、Content 和 Page Surface。
2. 内容区优先使用 `Templates / List Page Shell-V2` 实例，并按 `compositionName` 配置 PageHeader、Filter Bar、可选 List Action Bar、Table Shell 和 Pagination Slot。
3. 按 `page-rules.md` 完成标题、筛选、操作栏、表格、状态、数据与响应布局。
4. 每个实例都按“读取 `componentProperties` → 解析唯一真实 Key → 校验类型和值域 → 写入 → 回读”的闭环配置；不得直接假设 `Label`、`text` 等展示名称就是可写 Key。
5. 按 `component-invocation-contract.md` 完成 INSTANCE_SWAP 和 Slot；自定义表格 Slot 后按 `component-map.md` 逐层同步 `TableStyleSpec` 并重算外壳高度。
6. 每完成一个实例就记录属性回读结果。出现 `PROPERTY_READBACK_MISMATCH` 或其他必需写入失败时立即进入“失败关闭”。
7. 按当前平台文件组装导航、菜单、颜色和差异组件；默认模式使用已确认菜单预设，自定义模式严格使用 PageSpec 菜单数据，并以完整、唯一的 Icon 组件名解析一级图标。平台文件没有声明的内容继续使用通用规则。

### 5. 处理缺口

1. 优先使用现有真实组件的合法组合。
2. 只有 `COMPONENT_MISSING`，即组件库经盘点确认没有目标能力时，才评估页面级最小降级，命名为 `Fallback / <Capability>`，不冒充正式组件。
3. 属性 Key 未找到、属性写入失败、INSTANCE_SWAP 失败、Slot 写入失败、权限不足、字体未加载或节点不可编辑都属于执行失败，不属于组件缺口。
4. 在画板相邻位置创建 `Audit / Missing Components`，只记录真实能力缺口、场景、降级方案和建议属性。
5. 不擅自修改或发布组件库母版；需要补齐平台基线或公共组件时在交付中单独列出。

## 失败关闭

任一必需组件、属性、INSTANCE_SWAP、Slot 或写后验证失败时：

1. 停止组装依赖该结果的后续页面内容；
2. 保留错误节点 ID、组件名、逻辑属性、真实候选 Key、期望值、实际值和错误代码；
3. 将结果标记为 `FAIL`，不使用“完成”“已生成”或同义结论；
4. 不创建覆盖文字、遮盖矩形、替代图标或手绘表格；
5. 不隐藏真实组件后用 Frame、Group、裸 Text 或截图替代；
6. 向用户报告可修复的最小阻塞项。

`Navigation Text Overlay`、`Control Text Cover`、`Button Text Cover` 和用于替代真实 Table Shell 的 `Table / Clean` 均是禁止交付特征。改名不改变其失败性质。

只有 Component Map 中确实不存在目标能力时，才按“处理缺口”进入受限 Fallback。

## 验证与交付

先按 `structural-validation.md` 执行结构化验收；结构状态为 `PASS` 后，再按 `page-rules.md`、`component-map.md` 和当前平台文件逐区截图检查并检查整页。至少确认：

- 页面结构、组合名称、平台外壳和 PageSpec 一致；
- 导航只有一个当前菜单，仅当前路径祖先展开；自定义一级图标均通过真实 INSTANCE_SWAP 写入并回读成功；
- 所有可复用设计系统元素仍为真实实例，Slot 和属性关系正确；
- 筛选显示形式、触发方式、列表操作、显式表格选择列、数据状态和分页没有串位；列表操作不会隐式开启 Checkbox；
- 无文字截断、节点重叠、画板溢出、异常空白、临时截图或占位内容；
- 组件缺口与运行时假设已记录。

只有结构验收和视觉验收均为 `PASS` 时才交付完成结果。返回：Skill 版本与可读取的 Git Commit、页面节点 ID 与名称、`compositionName`、主要组件及关键变体、平台与输入假设、组件解析摘要、属性回读摘要、组件缺口、结构与视觉验证结果。

## 硬性约束

- 不把参考图作为栅格图片直接交付。
- 不重画已有组件，不分离实例修改外观，不破坏变量绑定。
- 不用裸 Text、色块或覆盖层修正组件属性写入失败。
- 不隐藏 Header、Filter Bar、Table Shell 等真实核心组件后用手绘内容替代。
- 不擅自改动、补充或发布组件库母版。
- 不把页面级 List Action Bar 冒充或发布成正式组件。
- 不把一个平台的导航、颜色、组件映射复制到另一个平台。
- 不把复杂看板、编辑表单、详情页、树表或高度定制工作台硬塞进本 Skill。
- 不宣称缺失组件已经存在；明确区分正式实例、页面级组合与降级实现。
