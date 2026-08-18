# qifu-list-page Skill 使用复盘：权益配置列表页生成异常

## 1. 文档信息

- 复盘日期：2026-08-18
- 涉及 Skill：`qifu-list-page`
- Skill 仓库：<https://github.com/BitPan666/qifu-list-page>
- 本地仓库基线 Commit：`fde88ed93467a4eeaa8aaf83221300f6b7d0f2a5`
- 目标 Figma 文件：[奇富科技中后台组件库 新](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新)
- 问题 Page：[0818，node 4343:4724](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新?node-id=4343-4724)
- 问题画板：[Page / List / 权益配置 / Default，node 4409:121](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新?node-id=4409-121)
- 正确结构对照：[Page / List / 机器人群组列表页 / Default，node 3860:548](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新?node-id=3860-548)
- 本次处理范围：只审计问题形成原因，没有修改问题页面。

## 2. 结论摘要

本次异常不是单纯由提示词不够详细造成的。

同事使用的提示词基本足以确定页面名称、筛选项、触发方式、表格字段和主要操作。提示词真正缺失的是“权益配置”在毓数侧栏中的完整路径，以及右侧主按钮的明确文案和类型。这只能解释侧栏归属不确定，不能解释图标、字体、颜色和表格结构全部错误。

问题的直接形成过程是：

1. 执行者根据 Component Map 找到了部分正确组件。
2. 执行者在修改组件文案、图标和 Slot 内容时没有成功完成属性写入。
3. 写入失败后没有停止和排查，而是自行采用覆盖文字、遮盖色块和手绘表格等视觉降级方案。
4. 视觉降级绕开了组件内部字体、颜色变量、图标交换、状态和响应能力。
5. 最终只做了截图层面的检查，没有进行实例关系、属性值和变量绑定的结构化验收。

因此，本次问题应拆分为三部分：

| 层面 | 结论 |
| --- | --- |
| 提示词 | 有少量结构信息缺失，但不是视觉错误的主要原因 |
| 执行过程 | 组件属性写入失败后擅自手绘替代，是问题的直接原因 |
| Skill | 已说明“使用哪些组件”，但缺少足够具体的调用协议、失败关闭和自动结构验收 |

## 3. 同事如何使用了 Skill

同事从 GitHub 下载并安装 `qifu-list-page` Skill，随后在 Codex 中使用类似以下提示词生成页面。以下内容根据对话截图整理，个别标点可能与原文略有差异：

```text
使用 qifu-list-page Skill，在指定 Figma Page 生成【权益配置】列表页。

平台：毓数
筛选字段：应用场景、客群名称、券类型
显示形式：带标题筛选项
触发方式：按钮触发
快捷条件：无
列表操作栏：右侧按钮
表格列：客群ID、客群名称、人数、券ID、券名称、券类型、起借金额、操作
特殊状态或交互：补充要求

完成后截图检查。
```

根据 Skill 的 PageSpec 输入契约，这段提示词可以确定：

```text
pageName=权益配置
platform=yushu
filters=[应用场景, 客群名称, 券类型]
filterItemDisplay=带标题筛选项
filterTrigger=按钮触发
compositionName=Qifu List Page / Basic Filter Table
columns=[客群ID, 客群名称, 人数, 券ID, 券名称, 券类型, 起借金额, 操作]
```

但以下信息没有被明确提供：

```text
headerActive
sidePath[]
sideActive
primaryAction.text
primaryAction.placement
rowActions[]
特殊状态或交互的真实内容
```

其中 `sidePath[]` 会改变页面导航结构，缺失时应先询问，而不是自行新增平台菜单。

## 4. 期望行为

正常情况下，使用者只需要描述业务页面，不需要填写组件名称、Node ID、发布 Key、字体、颜色或变量。

Skill 应负责完成以下链路：

```text
业务提示词
→ 解析 PageSpec
→ 选择 compositionName
→ 从 Component Map 解析真实组件
→ 创建组件实例
→ 解析实例真实属性 Key
→ 写入文案、变体、图标和 Slot
→ 回读属性验证写入成功
→ 做结构检查和截图检查
→ 交付页面与验证结果
```

本次执行成功完成了“提示词 → 组件选择”的一部分，但没有可靠完成“实例配置 → 回读验证”。

## 5. 实际发生的问题

### 5.1 侧栏组件存在，但组件属性没有写入成功

问题页面确实使用了 13 个 `Navigation / SideMenu / SideMenuItem-V2` 实例，说明组件发现成功。

但实例内部的文本属性仍然是默认值：

```text
Label#2405:0 = 菜单项
```

为了显示业务文案，页面又创建了：

```text
Navigation Text Overlay，node 4434:304
```

该覆盖层包含 34 个页面级节点，用裸 Text 和色块覆盖原组件内容。侧栏每个菜单行内部还存在位于 `x=200` 的额外文字，已经超出 200px 菜单行宽度。

结果是：

- 业务文案没有通过组件属性写入；
- 文字没有继承 SideMenuItem-V2 的字体、颜色和状态；
- 当前项和祖先项的颜色需要靠手工模拟；
- 组件后续更新无法自动同步覆盖文字。

### 5.2 毓数侧栏图标映射没有执行

所有一级菜单的 `icon 图标` 属性都保持同一个默认值：

```text
icon 图标#3651:0 = 2423:195
实际图标 = Icon/yushu/ziyuanguanli
```

Skill 的 `platform-yushu.md` 已经为探索分析、智能分析、仪表板、图表管理、在线 Excel、数据集、数据源、订阅管理、权限管理和归因配置分别提供图标节点 ID。

正确页面中这些一级菜单使用的是不同的图标组件；问题页面没有应用任何一条对应的业务图标映射。

### 5.3 正确 Table Shell 被隐藏，页面重新手绘了表格

问题页面中存在正确的：

```text
Data Display / Table / Shell-V2
```

但该实例被设置为不可见。页面另外创建了：

```text
Table / Clean，node I4409:169;3479:4;4430:1042
```

该可见 Frame 包含：

- 99 个子节点；
- 88 个裸 Text；
- 0 个表格组件实例。

因此可见表格没有使用：

- Header Cell-V2；
- Row-V2；
- Content Cell-V2；
- Text-V2；
- Action Content-V2；
- Pagination-V2。

这直接违反了 Skill 的硬性约束：“不重画已有组件，不分离实例修改外观，不破坏变量绑定”。

### 5.4 筛选框和按钮也使用了遮盖层

可见筛选区中：

- Filter Item-V2 实例数量为 0；
- 存在 5 个 `Control Text Cover` / `Button Text Cover` 遮盖节点；
- 存在 13 个页面级裸 Text；
- Input、Select、Button 只是作为视觉底座使用。

因此“带标题筛选项”没有通过 Filter Item-V2 的 `display=带标题筛选项` 实现，控件文案也没有通过组件属性正常写入。

### 5.5 表格字体和颜色变量丢失

问题页面可见表格的大部分正文使用：

```text
Font: QiFu Sans Std / Bold / 14px
Color: #1F2329
Variable binding: 无
```

其中 72 个表格文字使用上述黑色粗体，9 个操作文字使用未绑定变量的绿色，只有少量文字使用 `#565656`。

正确列表页对照中：

```text
表头：MiSans / Semibold / 14px
表头颜色：VariableID:9:112

正文：MiSans / Regular / 14px
正文颜色：VariableID:9:113
```

颜色和字体错误不是提示词造成的，而是可见内容脱离组件实例与变量绑定后的必然结果。

### 5.6 页面自行增加了未确认的侧栏菜单

毓数平台基线没有收录“权益配置”，提示词也没有给出完整侧栏路径。

问题页面将“权益配置”作为一级菜单追加在侧栏末尾，并在 Audit 中记录：

```text
Capability: 毓数侧栏菜单 / 权益配置归属
Scenario: 用户未指定侧栏路径，平台基线未收录“权益配置”。
Fallback: 作为一级当前菜单追加在侧栏末尾。
```

这个处理不应自动发生。由于侧栏路径会改变平台信息架构，应暂停生成并询问真实路径。

## 6. 为什么会发生

### 6.1 Component Map 解决了“找到组件”，没有完整解决“调用组件”

当前 `component-map.md` 已经包含：

- 组件名称；
- 本地 Node ID；
- 发布 Key；
- 人类可读的属性名称；
- 部分 Slot 和变体规则。

这足以支持：

```text
带标题筛选项 → Filter Item-V2
按钮触发 → Filter Bar-V2 + 查询按钮
毓数平台 → Yushu Header-V2 + SideMenuItem-V2
普通表格 → Table Shell-V2
```

但 Figma Plugin API 写入实例时需要真实的组件属性 Key。例如 SideMenuItem-V2 实际返回：

```text
Label#2405:0
icon 图标#3651:0
showIcon 显示图标#3651:25
```

如果只使用 `Label`、`icon 图标` 等展示名称，属性写入可能失败。

完整的组件调用协议还应说明：

```text
如何动态发现真实属性 Key
属性的类型是 TEXT / BOOLEAN / VARIANT / INSTANCE_SWAP / SLOT 中的哪一种
INSTANCE_SWAP 应传入哪个 ComponentNode ID
属性和变体的写入顺序
Slot 的替换方式
写完后应回读哪些值
哪些条件不满足时必须停止
```

### 6.2 Figma 实例和 Slot 本身具有结构约束

Figma 实例不能像普通 Frame 一样任意插入、删除和移动内部节点。表格又是多层组件：

```text
Table Shell-V2
→ headerSlot / rowsSlot / paginationSlot
→ Header Cell-V2 / Row-V2
→ Content Cell-V2
→ Text-V2 / Tag / Action Content-V2
```

只创建 Table Shell 或只修改外壳变体，无法自动得到完整业务表格。必须逐层配置 Slot 和嵌套组件，并在最后重算高度。

### 6.3 Fallback 规则范围不够严格

Skill 允许在“现有组件确实缺少能力”时使用最小页面级 Fallback。

本次执行者把“当前脚本没有成功写入组件属性”也当成了组件缺口，并创建覆盖文字和手绘表格。这两种情况必须区分：

```text
组件库确实没有能力
→ 可以记录 Missing Component，并使用受限 Fallback

组件存在，但本次属性写入失败
→ 属于执行失败，必须停止，不得手绘替代
```

### 6.4 只做截图检查，缺少结构检查

截图只能确认“画面上有内容”，无法确认：

- 是否为真实实例；
- 是否正确设置组件属性；
- 图标是否来自平台映射；
- Table Shell 是否可见；
- 文字是否保留变量绑定；
- 是否存在覆盖层或手绘替代。

因此页面虽然完成了截图检查，仍然把结构错误当作完成结果交付。

### 6.5 Skill 安装版本缺少明确标识

Skill 通过 GitHub 分发，但交付结果没有返回所使用的仓库 Commit 或版本号。维护者无法立即判断同事使用的是最新版本、旧版本，还是复制安装后未更新的版本。

本复盘对应仓库的本地基线 Commit 为 `fde88ed93467a4eeaa8aaf83221300f6b7d0f2a5`。同事机器上的实际安装版本仍应单独核对。

## 7. 如何修复当前问题

本节描述修复路径，不代表本次已经修改问题页面。

### 7.1 先补全 PageSpec

确认：

```text
headerActive
sidePath[]
sideActive
primaryAction.text
primaryAction.placement
rowActions[]
```

在没有确认“权益配置”真实侧栏归属前，不继续修复导航。

### 7.2 删除视觉覆盖与手绘替代

应移除：

```text
Navigation Text Overlay
Menu Label / ... 页面级文字
Control Text Cover / ...
Button Text Cover / ...
Table / Clean
```

删除之前先确认对应真实组件实例已经正确配置并可见，避免页面内容丢失。

### 7.3 正确配置 SideMenuItem-V2

对每个实例动态发现真实属性 Key，不永久硬编码 `#2405:0` 等内部后缀：

```js
function findPropertyKey(instance, prefix, expectedType) {
  return Object.entries(instance.componentProperties)
    .find(([key, value]) => key.startsWith(prefix) && value.type === expectedType)?.[0];
}

const labelKey = findPropertyKey(item, "Label#", "TEXT");
const iconKey = findPropertyKey(item, "icon 图标#", "INSTANCE_SWAP");
const showIconKey = findPropertyKey(item, "showIcon 显示图标#", "BOOLEAN");

if (!labelKey || !showIconKey) {
  throw new Error("SideMenuItem-V2 属性契约不完整");
}

item.setProperties({
  [labelKey]: "探索分析",
  [showIconKey]: true,
  [iconKey]: targetIconNodeId,
});
```

写入后必须重新读取 `componentProperties`，确认值与 PageSpec 和平台图标映射一致。

### 7.4 恢复真实筛选栏结构

每个筛选项必须使用 Filter Item-V2：

```text
Filter Item-V2
├── Label 属性或标题节点
└── controlSlot
    └── Input / Select / DateRange 实例
```

按钮触发时使用 Filter Bar-V2 的对应 trigger 变体，并使用真实 Button 实例设置“确定/重置”，不得覆盖按钮文案。

### 7.5 恢复真实表格结构

保持 Table Shell-V2 可见，并按 `component-map.md` 的 Slot 同步规则逐层创建：

```text
Table Shell-V2
├── headerSlot
│   └── Header Cell-V2 × 列数
├── rowsSlot
│   └── Row-V2 × 数据行数
│       └── Content Cell-V2 × 业务列数
│           └── Text-V2 / Tag / Action Content-V2
└── paginationSlot
    └── Pagination-V2
```

业务正文的字体和颜色应由 Text-V2 继承，不在页面级重新指定。

## 8. 如何修改 Skill

### P0：必须优先完成

#### 8.1 增加组件调用协议

Component Map 不只记录组件清单，还应为关键组件增加调用契约：

```yaml
SideMenuItem-V2:
  locator:
    nodeId: "3650:998"
    publishKey: "cee1612d..."
    name: "Navigation / SideMenu / SideMenuItem-V2"

  properties:
    label:
      keyPrefix: "Label#"
      type: TEXT
    icon:
      keyPrefix: "icon 图标#"
      type: INSTANCE_SWAP
    showIcon:
      keyPrefix: "showIcon 显示图标#"
      type: BOOLEAN

  postconditions:
    - label 等于目标菜单文案
    - 一级菜单 showIcon=true
    - 一级菜单 icon 等于平台映射组件 ID
    - 二三级菜单 showIcon=false
```

同样需要补充 Input-V2、Select、Button、Filter Item-V2、Filter Bar-V2、Table Shell-V2、Header Cell-V2、Row-V2、Content Cell-V2、Text-V2、Action Content-V2 和 Pagination-V2 的调用契约。

#### 8.2 增加失败关闭规则

在 Skill 硬性约束中增加：

```text
组件已经解析成功，但属性、变体、INSTANCE_SWAP 或 Slot 写入失败时，必须停止当前页面生成并报告失败节点、属性和错误信息。

禁止通过裸 Text、遮盖矩形、覆盖层、隐藏真实组件或手绘替代来绕过组件写入失败。
```

#### 8.3 增加结构化自动验收

交付前必须自动检查：

- 不存在可见的 `Navigation Text Overlay`；
- 不存在 `Control Text Cover` 或 `Button Text Cover`；
- 不存在用于替代真实组件的 `Table / Clean`；
- 可见 Table Shell-V2 数量为 1；
- Header Cell-V2 数量等于业务列数；
- Row-V2 数量等于数据行数；
- 每行 Content Cell-V2 数量等于业务列数；
- 业务正文位于 Text-V2、Tag 或 Action Content-V2 实例内；
- 一级菜单图标与平台映射一致，且不允许全部保持默认图标；
- 二三级菜单不显示业务图标；
- 关键文字颜色仍绑定设计变量；
- 页面不存在被隐藏后又用手绘内容替代的核心组件。

任一检查失败时，不得使用“已完成”作为交付结论。

#### 8.4 收紧 Fallback 定义

只有满足以下条件时允许 Fallback：

1. Component Map 中没有可用组件；
2. 组件经过解析和属性盘点后，确认没有目标能力；
3. Fallback 不会复制或覆盖一个已经存在的组件能力；
4. 已在 Audit 中记录能力缺口和建议补充方案。

脚本错误、属性 Key 未发现、字体未加载、节点不可编辑、Slot 写入失败，不属于组件缺口。

### P1：提升团队使用稳定性

#### 8.5 增加版本标识

建议在 Skill 中增加版本文件或在交付中返回：

```text
skillName=qifu-list-page
skillVersion=<版本号>
skillCommit=<Git commit>
```

同事反馈问题时同时提供版本、原始提示词、目标 Figma 节点和生成页面节点。

#### 8.6 增加回归测试提示词

在 Figma Page `测试` 中保留以下固定回归场景：

1. 毓数一级菜单普通列表页；
2. 毓数二级菜单列表页；
3. 直接筛选框 + 实时触发；
4. 带标题筛选项 + 按钮触发；
5. 带列表操作栏和选择列；
6. 启用/禁用 Tag；
7. 9 行数据 + Pagination-V2。

每次 Component Map、平台规则或关键组件接口变化后运行结构检查和截图检查。

## 9. 同事以后应该如何使用

### 9.1 使用前

1. 更新 Skill：

   ```bash
   git pull
   ```

2. 重新开启 Codex 任务，确保新版本 Skill 被发现。
3. 确认对目标 Figma 文件和组件库具有编辑/读取权限。
4. 在反馈问题时记录当前 Git Commit。

### 9.2 推荐提示词

```text
使用 qifu-list-page Skill。

目标 Figma 文件：<URL>
目标 Page：测试

平台：毓数
顶部入口：QBI
侧栏路径：权限管理 > 权益配置
当前菜单：权益配置

页面名称：权益配置
显示标题：是

筛选项：
- 应用场景，Select
- 客群名称，Input
- 券类型，Select

筛选显示形式：带标题筛选项
筛选触发方式：按钮触发

列表操作：无
页面主操作：新增权益，放在列表操作栏右侧

表格列：客群ID、客群名称、人数、券ID、券名称、券类型、起借金额、操作
行操作：编辑、配置

示例数据：9 行
分页：显示，总数 86，每页 10 条，当前第 1 页
画板尺寸：1366×768

必须使用 qifu-list-page Component Map 中的真实组件及实例属性。
组件属性或 Slot 写入失败时停止，不允许覆盖文字、遮盖组件或手绘表格。
完成后同时进行结构检查和截图检查。
```

如果“权益配置”并不属于“权限管理”，使用者只需替换真实侧栏路径，不需要填写任何组件 ID、字体、颜色或变量。

### 9.3 使用者验收重点

使用者不需要检查所有 Figma 技术细节，但应重点关注：

- 侧栏路径是否与业务系统一致；
- 一级菜单图标是否具有差异，而不是全部相同；
- 页面中是否出现 `Audit / Missing Components`；
- Audit 是否把“属性写入失败”误写成组件缺口；
- 表格文字是否异常粗黑；
- 修改一个母版属性后，页面实例是否能够自动同步。

出现以下情况应直接判定生成失败并反馈，不继续在页面上手工修补：

```text
Navigation Text Overlay
Control Text Cover
Button Text Cover
Table / Clean
真实 Table Shell 被隐藏
所有一级菜单使用同一个默认图标
实例属性仍为“菜单项”等默认值
```

## 10. 组件库修改对 Skill 的影响

判断原则：真正影响生成的是组件的“身份与接口”，不是它在画布上的位置。

### 10.1 通常不需要更新 Skill

- 在同一 Page 内移动组件位置；
- 调整 Base Spec 或变体矩阵的画布排版；
- 调整组件内部颜色、圆角、阴影等视觉样式，且语义和属性不变；
- 调整变体在组件集中的排列顺序；
- 修改不被调用流程依赖的普通内部图层名称。

这些修改应做截图回归，但通常不改变调用协议。

### 10.2 建议同步 Component Map

- 修改组件集或组件名称；
- 把组件移动到其他 Page；
- 修改图标组件路径；
- 修改变量名称但保留原 Variable ID。

只要 Node ID 和发布 Key 没变，调用可能仍然有效，但名称回退查找、人工审计和后续维护会受到影响。

### 10.3 必须更新 Skill 并运行回归

- 删除组件后重新创建；
- 用复制品替换原组件；
- 修改或重新创建组件属性；
- 修改变体属性名或属性值；
- 修改、删除或重建 Slot；
- 增删影响页面结构的关键变体；
- 删除重建图标组件；
- 取消发布跨文件需要使用的组件；
- 删除重建设计变量；
- 修改组件尺寸或间距语义，导致 Skill 中的旧规则失效。

每次修改后至少确认：

```text
原 Node ID / 发布 Key 是否仍存在
组件属性名称和类型是否变化
变体属性值是否变化
Slot 名称和结构是否变化
平台图标映射是否变化
Skill 中是否仍写着旧尺寸、旧名称或旧状态
```

## 11. 后续行动清单

| 优先级 | 行动 | 交付物 | 状态 |
| --- | --- | --- | --- |
| P0 | 为 SideMenuItem-V2 补充动态属性 Key 解析和写后验证 | Component Invocation Contract | 已完成（v1.1.0） |
| P0 | 为 Filter Item、Input、Select、Button 补充调用协议 | Component Invocation Contract | 已完成（v1.1.0） |
| P0 | 为 Table Shell、Cell、Row、Pagination 补充 Slot 组装协议 | Table Composition Contract | 已完成（v1.1.0） |
| P0 | 禁止属性写入失败后使用覆盖文字或手绘替代 | SKILL.md 硬性约束 | 已完成（v1.1.0） |
| P0 | 增加页面结构自动验收 | Audit 脚本或验证流程 | 已完成契约与发布门禁（v1.1.0） |
| P1 | 强制输出 Skill 版本和 Commit | 交付格式 | 已完成（v1.1.0） |
| P1 | 补充权益配置真实侧栏归属 | platform-yushu.md | 真实归属待确认；现已禁止自动追加 |
| P1 | 增加标准回归提示词 | docs / 测试 Page | 文档已完成；Figma 测试画板待后续回归 |
| P2 | 建立组件接口变更检查表 | 维护流程 | 已完成（调用契约与影响矩阵） |

## 12. 修复实施记录

本次复盘后发布 `qifu-list-page 1.1.0`，新增：

- `VERSION`：返回可核对的 Skill 版本；
- `component-invocation-contract.md`：动态属性 Key、类型、INSTANCE_SWAP、Slot 和回读协议；
- `structural-validation.md`：页面实例关系、数量、变量、几何与禁止特征门禁；
- `validate_skill_contract.py`：发布前可执行的 Skill 合约验证器；
- `test_validate_skill_contract.py`：缺少调用契约或失败关闭规则时必须失败的回归测试。

`SKILL.md` 已增加失败关闭：组件存在但属性或 Slot 写入失败时，必须停止并报告，不再允许用覆盖文字、遮盖色块、替代图标或手绘表格继续交付。

## 13. 最终复盘结论

本次问题不是“用户必须写出更多组件细节”，也不是“Component Map 完全无效”。

Component Map 已经帮助执行者找到 Header、SideMenuItem、Input、Select、Button 和 Table Shell 等正确组件。问题发生在组件实例配置阶段：真实属性 Key、INSTANCE_SWAP 和 Slot 没有被可靠写入，执行者又在失败后自行手绘替代，最终破坏了字体、颜色、图标和实例关系。

后续改进方向不是让同事在提示词中填写组件 ID，而是把现有 Component Map 从“组件目录”升级为“可执行组件调用契约”，并增加失败关闭和结构化验收。做到这三点后，同事仍然只需描述业务页面，Skill 应负责稳定完成组件选择、属性配置、结构验证和视觉交付。
