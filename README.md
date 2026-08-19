# Qifu Figma Skills

奇富科技中后台 Figma 页面生成 Skill。本仓库当前发布 `qifu-list-page`，用于根据业务描述，调用「奇富科技中后台组件库 新」中的真实组件生成标准桌面列表页。

仓库公开发布，用于降低团队协作与获取门槛。仓库包含组件名称、Figma 文件地址、节点 ID、发布 Key、毓数平台导航和页面规范；这些内容用于定位设计资产与约束生成规则，本身不提供 Figma 访问权限。实际生成仍需要使用者拥有目标文件和对应组件库的访问权限。

## 包含内容

```text
.
├── AGENTS.md
└── skills/
    └── qifu-list-page/
        ├── SKILL.md
        ├── VERSION
        ├── agents/openai.yaml
        ├── references/
        │   ├── component-invocation-contract.md
        │   ├── component-map.md
        │   ├── page-rules.md
        │   ├── platform-yushu.md
        │   └── structural-validation.md
        ├── scripts/
        │   └── validate_skill_contract.py
        └── tests/
            └── test_validate_skill_contract.py
```

## 使用前提

- 使用支持 Figma Connector / `use_figma` 的 Codex；
- 在 Codex 中完成个人 Figma 账号连接；
- 对目标业务文件拥有编辑权限；
- 对「奇富科技中后台组件库 新」拥有访问权；
- 跨文件生成时，目标文件需要能使用组件库中已发布的对应组件。

GitHub 只同步 Skill 文件，不会同步 Figma 登录状态、访问权限或个人凭证。

## 公开范围与权限边界

- 任何人都可以查看或克隆本仓库，无需单独申请仓库访问权限；
- 仓库中的 Figma 文件地址、节点 ID 和发布 Key 只用于定位组件，不等于 Figma 授权；
- 没有目标业务文件或组件库权限时，Skill 无法读取或写入对应设计资产；
- 仓库不包含 Figma Access Token、GitHub Token、Cookie、密码、真实业务数据或个人凭证。

## 使用方式一：直接打开仓库

```bash
git clone https://github.com/BitPan666/qifu-list-page.git
cd qifu-list-page
```

使用 Codex 打开仓库目录，然后在提示词中明确写：

```text
使用 qifu-list-page Skill，在毓数平台生成标准列表页……
```

这种方式会同时读取仓库中的 `AGENTS.md`，适合协作和持续更新。

## 使用方式二：安装到个人 Skills

```bash
mkdir -p ~/.codex/skills
cp -R skills/qifu-list-page ~/.codex/skills/
```

安装后重新开启一个 Codex 任务，使 Skill 被重新发现。单独安装 Skill 时，接收者项目中原有的 `AGENTS.md` 仍会生效；如需完全一致的项目规则，优先使用方式一。

## 提示词结构

复制下面模板，只替换 `【】` 中的业务内容。菜单的展开、选中、层级、箭头、组件属性 Key 和 Slot 调用规则已经写在 Skill 中，不需要重复写进提示词。

```text
使用 qifu-list-page Skill，在【Figma 地址】的【目标 Page】生成【页面名称】。

平台：【不填默认毓数；当前仅支持毓数】；页面标题：【不显示 / 显示：标题文案】。

导航模式：【不填默认使用毓数默认菜单 / 自定义菜单】；顶部菜单入口：【不填默认 QBI / 菜单名称】；当前菜单路径：【一级菜单 / 一级菜单 > 二级菜单 / 一级菜单 > 二级菜单 > 三级菜单】。

以下菜单配置仅在“自定义菜单”时填写：
一级菜单：
- 【菜单文案】，图标【组件库中完整、唯一的 Icon 组件名称】，有无子菜单【有 / 无】
当前路径所在一级菜单的二级菜单：
- 【菜单文案】，有无子菜单【有 / 无】
当前路径所在二级菜单的三级菜单：【无 / 菜单文案】。

筛选字段：【字段名称】；显示形式：【直接筛选框 / 带标题筛选项】；触发方式：【实时触发 / 按钮触发】。

列表操作栏：左侧【无 / 按钮名称】，右侧次要操作【无 / 按钮名称】；主操作：【无 / 按钮名称】，位置：【列表最左侧 / 列表最右侧】。

表格列：【列名，最多 8 个业务列；状态列和操作列计入，自动选择列不计入】；行操作：【无 / 操作名称】；特殊状态或交互：【无 / 补充要求】。

示例数据：【条数 / 不填按默认】；分页：【总数、每页条数 / 不填按默认】；画板尺寸：【不填默认 1366×768 / 1920×1080】。

完成后进行结构检查和截图检查。
```

未指定正式交付 Page 的试生成、效果验证和 Skill 回归画板统一放在目标组件库的 Figma Page `测试`。

## 提示词示例

```text
使用 qifu-list-page Skill，在 https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新 的“测试”Page 生成“机器人群组列表页”。

平台：毓数；页面标题：不显示。

导航模式：使用毓数默认菜单；顶部菜单入口：QBI；当前菜单路径：订阅管理 > 群组管理。

筛选字段：群组名称、授权用户、启用状态、创建人、更新时间；显示形式：带标题筛选项；触发方式：按钮触发。

列表操作栏：左侧“批量启用、批量停用”，右侧次要操作“刷新、导出”；主操作：“新增用户”，位置：列表最右侧。

表格列：群组名称、机器人 webhook、授权用户、启用状态、更新时间、操作；行操作：查看、编辑；特殊状态或交互：启用与禁用使用对应 Tag 组件。

示例数据：9 条；分页：总数 101、每页 20 条；画板尺寸：1366×768。

完成后进行结构检查和截图检查。
```

## 更新

维护者推送更新后，使用者在仓库中执行：

```bash
git pull
```

不要提交 Figma Access Token、GitHub Token、Cookie、密码或其他个人凭证。
