# 奇富标准列表页 Skill 协作说明

## 仓库用途

本仓库用于分发 `qifu-list-page` Skill，使具备相同 Figma 组件库权限的协作者，可以根据业务提示词生成结构、组件和视觉规则一致的奇富中后台标准列表页。

- 奇富科技目标文件：<https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新>
- 试生成统一目标 Page：`测试`，node id `3497:651`
- 核心 Skill：`skills/qifu-list-page/SKILL.md`

## 每次生成前

创建、更新或审查标准列表页时，必须完整读取并执行 `qifu-list-page` Skill。Skill 会继续路由到：

- `references/page-rules.md`
- `references/component-map.md`
- 当前平台资料，例如 `references/platform-yushu.md`

使用 Figma 写入工具前，还必须加载该工具要求的官方 Figma Skill。

## 目标位置

- 所有试生成、效果验证和 Skill 回归画板统一放入既有 Figma Page `测试`（node `3497:651`）。
- 不得自行创建 `Test`、`Skill Test` 等近义 Page。
- 用户明确指定正式交付目标 Page 时，以用户要求为准。
- 不覆盖已有画板；新画板放在不重叠的空白区域。

## 组件使用规则

- 优先使用「奇富科技中后台组件库 新」中的真实组件实例和已发布组件。
- 不分离实例后重画，不用截图冒充可编辑页面。
- 同文件优先按组件映射中的 Node ID 定位；跨文件按发布 Key 导入。
- 节点失效时按精确组件名称重新发现，不猜测新 ID，并更新映射。
- 不擅自修改、补充或发布组件库母版。发现组件缺口时，按 Skill 规则使用页面级最小降级并记录 Audit。
- 原版组件保持不动；如后续获得明确授权修改组件，已有 V2 时直接调整 V2，没有 V2 时从原版复制为 V2，不继续新增 V3、V4。

## 验证要求

- 写入后逐区截图检查，再检查整页。
- 验证真实实例关系、Slot、组件属性、平台导航、间距、尺寸、表格、分页和示例数据。
- 不得留下文字截断、节点重叠、画板溢出、异常空白、临时截图或 placeholder。
- 完成时返回画板名称、节点 ID、页面组合、主要组件、假设、缺口和验证结果。

## 安全

- 不向仓库提交 Figma Access Token、GitHub Token、Cookie、密码或其他个人凭证。
- 仓库包含内部组件结构、节点 ID、发布 Key 和平台规范，应保持私有。
