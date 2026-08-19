# 页面结构化验收契约

截图检查只能验证视觉结果，不能证明页面仍由真实组件实例组成。本文件定义交付前必须执行的结构、属性、变量和几何验收。

## 目录

- [验收顺序](#1-验收顺序)
- [PageSpec 完整性](#2-pagespec-完整性)
- [组件与实例关系](#3-组件与实例关系)
- [平台导航](#4-平台导航)
- [筛选与操作](#5-筛选与操作)
- [表格与分页](#6-表格与分页)
- [变量与几何](#7-变量与几何)
- [禁止交付特征](#8-禁止交付特征)
- [结果与交付格式](#9-结果与交付格式)

## 1. 验收顺序

严格按以下顺序执行：

```text
PageSpec 完整性
→ ComponentResolutionManifest
→ 实例属性回读
→ 页面结构计数
→ 平台导航
→ 筛选与操作
→ 表格与分页
→ 变量与几何
→ 分区截图
→ 整页截图
```

前一阶段失败时停止，不使用后续截图掩盖结构问题。

## 2. PageSpec 完整性

以下信息缺失且会改变页面结构时，状态为 `BLOCKED`：

- 目标 Figma 文件或目标 Page；
- 平台无法从用户或目标文件确定；
- 默认导航模式下 `sidePath` 指向的平台菜单不存在；
- 自定义导航没有提供完整 `sidePath`，或缺少当前一级下的二级清单、二级 `hasChildren`、必要的三级清单或一级真实 Icon 组件名；
- 需要批量操作但未确认是否显示选择列；
- 主动作与列表次要动作无法区分。

平台菜单基线不存在某业务菜单时，不把它追加为一级菜单。先询问真实完整路径，或请用户明确切换为 `navigationMode=custom` 并提供自定义菜单输入。

## 3. 组件与实例关系

验证所有必需组件均出现在 `ComponentResolutionManifest` 且状态为 `resolved`。再检查：

- Header、SideMenuItem、Filter Item、Filter Bar、Input/Select、Button、Table Shell、Header Cell、Row、Content Cell、单元格内容和 Pagination 均保持 INSTANCE；
- 每个实例的 main component 完整名称与 Component Map 一致；
- 核心真实实例不得被隐藏后再用 Frame、Group 或裸节点替代；
- 组件属性写入日志全部为 `pass`；
- Slot 内容是预期真实实例，不是截图、裸 Text 或矩形。

无法读取实例关系时状态为 `FAIL`，不是“视觉检查通过”。

## 4. 平台导航

平台导航至少验证：

- Header 真实实例数量为 1，当前入口等于 `headerActive`；
- 侧栏恰好一个菜单项为当前页，层级等于 `sidePath.length`；
- `sideActive` 等于 `sidePath` 最后一项，`sideExpanded` 与 `sideAncestorsActive` 只包含当前路径祖先；
- 不在当前路径中的一级菜单全部收起；不在当前路径中的二级菜单即使有子集也保持收起；
- 当前一级下的每个二级菜单，其 `Has Submenu` 和箭头显示与 PageSpec 的 `hasChildren` 一致；只有当前路径经过的二级菜单允许展开并显示三级菜单；
- 每个 SideMenuItem 的 Label 回读值等于业务文案，不保留“菜单项”等默认值；
- 一级菜单 `showIcon=true`；默认模式的图标 main component ID 等于平台映射，自定义模式等于 `iconComponentName` 精确解析结果；
- 二、三级菜单不显示业务图标；
- 多个一级菜单不能全部保持同一个母版默认图标；
- 未确认的菜单没有被自行追加。

## 5. 筛选与操作

筛选区至少验证：

- Filter Item-V2 实例数等于 `filters[]` 数量；
- 每个 Filter Item 的显示形式、尺寸、标题和 controlSlot 与 PageSpec 一致；
- 带标题筛选项的标题与控件几何间距为 0px；
- 非日期控件宽度符合 200px 默认或 180px 小屏例外，DateRange 按规则使用 304px；
- 按钮触发显示一个确定和一个重置；实时触发两者均不显示；
- 确定为主要按钮，重置为线框按钮；
- Filter Bar 到 List Action Bar 为 16px，List Action Bar 到 Table Shell 为 12px；
- 页面只有一个视觉最强主动作，且未同时出现在 Filter Bar 和 List Action Bar；
- 主动作只位于 List Action Bar：`listActions.left` 时为全栏最左，`listActions.right` 时为全栏最右；只有主动作时操作栏仍存在；
- 批量动作存在时 `selection=on`，零选择时按规则禁用。

## 6. 表格与分页

Data 状态使用以下计数不变量：

```text
visible Table Shell-V2 = 1
Header Cell-V2 = columns.length
Row-V2 = data.length
Content Cell-V2 per row = columns.length
Selection Cell-V2 = 0，或 data.length + 1
Pagination-V2 = showPagination ? 1 : 0
```

在 `1366 × 768` 画板中，`columns.length` 最多 8 个业务列；状态列和操作列计入，自动 Selection Cell 不计入。超过上限且未明确 1920、删列或横向滚动方案时状态为 `BLOCKED`。

同时验证：

- Table Shell 不是隐藏状态；
- `TableStyleSpec` 已同步到 Shell、Header Cell、Row、Content Cell 和 Selection Cell；
- 表头选择单元格背景绑定 `背景色/--qifu-bg-color-canvas`；
- 文本格使用 Text-V2，二元启用/禁用使用 Tag，多状态使用 Status-V2，行操作使用 Action Content-V2；
- 启用 Tag 为 `light/success/medium/square`，禁用 Tag 为 `light/danger/medium/square`，两者 `disabled=false`；
- 每列宽度数组在表头和所有行中一致，总和等于可见表宽；
- Pagination 位于 `paginationSlot`，紧跟最后一行，右边缘与表格右边缘一致；
- Table Shell 高度不裁切最后一行或 Pagination。

Loading 和 Empty 状态按组合验证对应 Slot，不套用 Data 行数不变量。

## 7. 变量与几何

检查实例继承的设计变量没有被页面级样式覆盖：

- 表头和正文文字继续使用组件内字体与文字颜色变量；
- 操作文字、状态 Tag 和选中导航继续使用组件语义变量；
- Content、Page Surface 和选择列表头背景符合页面规则；
- 不以页面级固定色修正组件内部颜色；
- 不以裸 Text 替代组件文案来修正字体。

几何检查至少覆盖：重叠、裁切、溢出、异常空白、可见区块间距、筛选换行、列连续铺满和分页对齐。

## 8. 禁止交付特征

出现任一项立即判定 `FAIL`：

```text
Navigation Text Overlay
Control Text Cover
Button Text Cover
Table / Clean（用于替代真实 Table Shell）
隐藏真实 Table Shell 后展示手绘表格
用裸 Text 覆盖组件默认文案
用矩形遮住错误内容
所有一级菜单使用同一个默认图标
实例属性仍保留“菜单项”等默认值
可见业务表格包含大量页面级裸 Text 且没有对应表格实例
```

节点名称不同但行为相同也属于失败。不要通过改名绕过检查。

## 9. 结果与交付格式

验收状态只有三种：

| 状态 | 含义 | 是否可宣称完成 |
| --- | --- | --- |
| `PASS` | 所有必需结构和视觉检查通过 | 可以 |
| `BLOCKED` | 缺少会改变页面结构的用户信息 | 不可以；提出最小问题 |
| `FAIL` | 组件解析、属性写入、Slot 或验收失败 | 不可以；报告失败位置 |

交付必须返回：

```text
skillVersion / skillCommit（可读取时）
pageNodeId / pageName
compositionName
platform / PageSpec assumptions
ComponentResolutionManifest summary
propertyReadback pass/fail summary
structuralValidation PASS|BLOCKED|FAIL
visualValidation PASS|BLOCKED|FAIL
missingComponents[]
```

只有结构验收和视觉验收均为 `PASS` 时，才能使用“完成”“已生成”或同义结论。
