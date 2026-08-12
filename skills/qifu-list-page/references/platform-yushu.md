# 毓数平台导航基线

## 目录

- [适用范围](#1-适用范围)
- [顶部导航](#2-顶部导航)
- [侧栏菜单树](#3-侧栏菜单树)
- [侧栏图标映射](#4-侧栏图标映射)
- [组装规则](#5-组装规则)
- [输入解析示例](#6-输入解析示例)

## 1. 适用范围

当前标准数据表格页默认以毓数平台为基准。用户明确指定其他平台时，不套用本文件的菜单名称；先读取对应平台参考，缺少参考时仅询问会改变页面框架的导航信息。

平台规格使用以下字段：

```text
platform        yushu
headerActive    数据资产 | 自助查询 | 数据开发 | 指标管理 | QBI
sideActive      当前页面所在的侧栏菜单
sideExpanded[]  当前展开的父菜单；与 sideActive 分开记录
sideAncestorsActive[] 当前页的祖先菜单；从 sidePath 排除 sideActive 后自动推导
sidePath[]      从一级菜单到当前页面的完整路径
```

`sideActive` 决定唯一的当前页菜单；`sideExpanded` 决定子菜单是否可见；`sideAncestorsActive` 决定当前路径上的父级视觉高亮。展开不等于祖先激活，允许出现“探索分析已选中，同时智能分析保持展开但仍为默认黑色”的状态。

## 2. 顶部导航

使用真实组件：

- 组件集：`Navigation / HeaderMenu / Yushu Header-V2`
- 节点 ID：`3639:1529`
- 发布 Key：`13dd3304a68853196f2a683bba7ebd034e2928ee`
- 属性：`activeMenu 当前菜单`
- 画板宽度：1366px；放入宽屏页面时横向填充，保持 48px 高。

固定内容：

- 左侧 Logo；
- 菜单顺序：数据资产、自助查询、数据开发、指标管理、QBI；
- 四个中文顶部菜单文案统一使用 `PingFang SC / Regular / 14px`；不得用 `Inter` 渲染中文。若 Yushu Header-V2 实例继承了 Inter，在当前页面实例内覆盖字体但保持实例关系，并截图确认“数据资产 / 自助查询 / 数据开发 / 指标管理”均完整显示，不得只显示末尾单字或简称。
- 右侧功能图标顺序：帮助、通知、申请工单、问题上报；
- 头像使用毓数默认头像；
- 用户名固定为 `panyue`；
- 用户名右侧保留下拉箭头。

用户指定顶部入口时设置对应 `activeMenu 当前菜单`。未指定时：

1. 根据页面业务推断入口；
2. 无可靠映射时默认 QBI；
3. 不因侧栏菜单名称擅自新增顶部菜单。

## 3. 侧栏菜单树

当前已确认的一级结构：

```text
探索分析
智能分析
├── 智能探查
└── 智能报表
仪表板
图表管理
在线Excel
数据集
数据源
订阅管理
├── 订阅计划
└── 群组管理
权限管理
├── 用户授权
└── 角色授权
归因配置
```

结构属性：

| 菜单 | Level | Has Submenu | 默认展开 | 已确认子项 |
| --- | ---: | --- | --- | --- |
| 探索分析 | 1 | False | — | — |
| 智能分析 | 1 | True | True | 智能探查、智能报表 |
| 智能探查 | 2 | False | — | — |
| 智能报表 | 2 | False | — | — |
| 仪表板 | 1 | False | — | — |
| 图表管理 | 1 | False | — | — |
| 在线Excel | 1 | False | — | — |
| 数据集 | 1 | False | — | — |
| 数据源 | 1 | False | — | — |
| 订阅管理 | 1 | True | False | 订阅计划、群组管理 |
| 订阅计划 | 2 | False | — | — |
| 群组管理 | 2 | False | — | — |
| 权限管理 | 1 | True | False | 用户授权、角色授权 |
| 用户授权 | 2 | False | — | — |
| 角色授权 | 2 | False | — | — |
| 归因配置 | 1 | False | — | — |

订阅管理和权限管理的二级菜单已经确认。页面位于其中任一二级菜单时，展开对应一级父菜单并选中目标二级项；父菜单使用祖先激活样式：不出现绿色背景和指示条，但文字、图标和展开箭头均为主题色。

## 4. 侧栏图标映射

图标使用奇富本地图标组件，显示尺寸为 16×16。名称只用于定位，最终以图形语义为准。

| 一级菜单 | 图标组件 | 节点 ID | 发布 Key |
| --- | --- | --- | --- |
| 探索分析 | `Icon/dashboard` | `2312:176` | `cddd55e261b7284efe5494d80e3c2dbf09998bd5` |
| 智能分析 | `1.通用/Icon图标/QBI/智能问数`（组件卡片标签 `icon-icon_zhinengfenxi`） | `3721:11165` | `04c1d64632ac2521859af7ac7c7944e433e7c243` |
| 仪表板 | `Icon/yibiaoban1` | `2422:108` | `6a427095b3dceb7ec1bc607d8fd8a48f05113049` |
| 图表管理 | `Icon/table` | `2312:226` | `a1fd6e8cf04cc27cd41ba569c2dc5c6179f89e09` |
| 在线Excel | `Icon/xianshangexcel` | `2422:102` | `ab07f8c04fc81477141d1ad1a9abf3a70710fdb5` |
| 数据集 | `Icon/flow-manage` | `2423:444` | `b7831e070308984a7cff8e645596c627969e9973` |
| 数据源 | `Icon/shuju` | `2312:130` | `7694e996fbaa935b8cf853cea903ae1d560134bd` |
| 订阅管理 | `Icon/manage` | `2312:248` | `5099bcf783cfb7d636ee2d8bbfa721cdae565820` |
| 权限管理 | `Icon/quanxianguanli` | `2422:111` | `48a797b2fddf5e3636d610221a02772dd2584868` |
| 归因配置 | `Icon/gongdanliucheng` | `2423:82` | `8fa63bc0c95f2d7f21479b6377eaa7d578405634` |

二级和三级菜单不显示业务图标，只保留文本、层级缩进和必要的展开箭头。

## 5. 组装规则

使用真实 `Navigation / SideMenu / SideMenuItem-V2` 实例逐项组装，不创建固定业务大组件：

1. 宽度固定为 200px；一级菜单高 44px，二、三级菜单高 40px。
2. 每个实例通过 `Label`、`Level`、`Has Submenu`、`State` 设置内容。
3. 一级菜单将 `showIcon 显示图标` 设为 `true`，通过 `icon 图标` INSTANCE_SWAP 选择本文件映射的 16×16 本地图标；不得覆盖嵌套节点或绘制替代图标。
4. 二、三级菜单保持纯文本层级，不显示业务图标；`Has Submenu=True` 时仅保留组件自带的展开箭头。
5. `sideActive` 是唯一的当前页菜单并使用 `State=Selected`；如果它是无子菜单叶子，则显示绿色选中背景与右侧指示条。
6. `sideExpanded` 中的父项设置 `expanded 展开=True` 并插入其已确认子项；不在数组中的父项设置为 `False`，只显示一级项。
7. 页面落在二级或三级菜单时，从 `sidePath` 排除 `sideActive` 得到 `sideAncestorsActive`。所有祖先都使用 `State=Selected` 且保持 `expanded 展开=True`，呈现白底、文字/一级图标/展开箭头主题绿；这表示祖先路径高亮，不表示父菜单是当前页。
8. 不在 `sideAncestorsActive` 中、仅因默认展示或用户要求而展开的父项必须保持 `State=Default`；不能为了改变箭头方向或仅仅因为展开就设为绿色。
9. 菜单区域使用垂直 Auto Layout。侧栏整体填满 Header 以下高度；菜单滚动区 `layoutGrow=1`、裁切内容并允许纵向滚动。
10. 底部固定保留 `collapse-button`：使用 200×40px 横向 Auto Layout 容器，顶部 1px 分割线，左内边距 20px；内部 `Icon/shouqi` 使用组件节点 `2423:450`，固定为 16×16px、垂直居中且 `layoutSizingHorizontal=FIXED`。只有底部容器横向填充侧栏，图标实例不得设为 `FILL` 或直接 resize 到侧栏宽度；其中心线应与上方一级菜单图标一致。滚动只作用于菜单区域，不让收起按钮随菜单滚走。
11. 静态画板需要展示完整菜单时允许增加画板高度；不得压缩菜单项高度，也不得让菜单覆盖底部收起按钮。

## 6. 输入解析示例

输入：

```text
在毓数平台的权限管理 > 用户授权下新增用户授权列表页，顶部位于 QBI。
```

解析：

```text
platform=yushu
headerActive=QBI
sidePath=[权限管理, 用户授权]
sideActive=用户授权
sideExpanded=[权限管理]
sideAncestorsActive=[权限管理]
```

输入：

```text
在订阅管理 > 群组管理新增群组管理列表页。
```

解析：

```text
platform=yushu
headerActive=QBI（未提供且无可靠业务映射时的默认值）
sidePath=[订阅管理, 群组管理]
sideActive=群组管理
sideExpanded=[订阅管理]
sideAncestorsActive=[订阅管理]
```

输入：

```text
在智能分析 > 智能报表增加报表任务列表。
```

解析：

```text
platform=yushu
headerActive=QBI（未提供且无可靠业务映射时的默认值）
sidePath=[智能分析, 智能报表]
sideActive=智能报表
sideExpanded=[智能分析]
sideAncestorsActive=[智能分析]
```
