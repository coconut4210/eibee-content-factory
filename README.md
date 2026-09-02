# eibee 内容工厂（公开版）

面向平台型品牌的社媒内容规划 Skill。它帮助你把经批准的品牌事实、受众任务与营销节点，转成周度/月度排期、选题卡和平台原生内容草案。

## 安装

将本仓库克隆到 Codex 的本地 Skills 目录，并将目录命名为 `eibee`。安装后重启或刷新 Codex 的 Skill 列表。

**Windows PowerShell：**

```powershell
git clone https://github.com/coconut4210/eibee-content-factory.git "$env:USERPROFILE\.codex\skills\eibee"
```

**macOS / Linux：**

```bash
git clone https://github.com/coconut4210/eibee-content-factory.git ~/.codex/skills/eibee
```

如果已安装，需要更新时运行：

```powershell
git -C "$env:USERPROFILE\.codex\skills\eibee" pull --ff-only
```

macOS / Linux 对应命令：

```bash
git -C ~/.codex/skills/eibee pull --ff-only
```

目前 Codex CLI 没有内置的 `codex skill install` 子命令；以上 Git 命令是可复现、可审计的安装方式。

## 使用

在对话中输入 `$eibee`，然后说明你需要：周度规划、月度排期或单篇内容。开始前请提供或确认：

- 品牌与账号定位；
- 已批准的平台事实、CTA 与可用资产；
- 投放平台、时间范围和内容模态；
- 目标市场、必要时的营销日历或节点偏好。

Skill 会把外部趋势和节日仅作为创意语境，不会把它们当作平台功能的证据。请在发布前自行完成事实、版权、文化与广告披露审核。

## 包含与不包含

公开版保留内容策略、营销节点优先级、创意张力检查、平台格式与审核边界。

它不包含任何客户数据、产品截图、账号授权、自动化发布、RPA 配置、私有知识库或第三方付费工具依赖。

## 发布前检查

1. 仓库中新建的文件只有 `SKILL.md`、`README.md`、`.gitignore` 和测试文件。
2. 不要提交账号令牌、客户名单、未公开功能、产品截图、社媒素材或发布排期。
3. 选择许可证后再公开发布；未附许可证时，他人通常只能查看代码，复用权利并不明确。

## 许可证

本项目采用 [MIT License](LICENSE)，允许他人使用、修改和分发，并保留许可证与版权声明。
