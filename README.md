# Qifu Figma Skills

奇富科技中后台 Figma 页面生成 Skill。本仓库当前发布 `qifu-list-page`，用于根据业务描述，调用「奇富科技中后台组件库 新」中的真实组件生成标准桌面列表页。

仓库为内部使用，包含组件名称、Figma 文件地址、节点 ID、发布 Key、毓数平台导航和页面规范。请保持私有，不要转为公开仓库。

## 包含内容

```text
.
├── AGENTS.md
└── skills/
    └── qifu-list-page/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/
            ├── component-map.md
            ├── page-rules.md
            └── platform-yushu.md
```

## 使用前提

- 使用支持 Figma Connector / `use_figma` 的 Codex；
- 在 Codex 中完成个人 Figma 账号连接；
- 对目标业务文件拥有编辑权限；
- 对「奇富科技中后台组件库 新」拥有访问权；
- 跨文件生成时，目标文件需要能使用组件库中已发布的对应组件。

GitHub 只同步 Skill 文件，不会同步 Figma 登录状态、访问权限或个人凭证。

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

## 推荐提示词结构

```text
使用 qifu-list-page Skill。

目标 Figma 文件：
目标 Page：
平台：
顶部入口：
侧栏路径：
页面名称：
是否显示标题：

筛选项：
列表操作：
页面主操作：
表格列：
行操作：
状态：
示例数据条数：
分页：
画板尺寸：
```

未指定正式交付 Page 的试生成、效果验证和 Skill 回归画板统一放在目标组件库的 Figma Page `测试`。

## 更新

维护者推送更新后，使用者在仓库中执行：

```bash
git pull
```

不要提交 Figma Access Token、GitHub Token、Cookie、密码或其他个人凭证。
