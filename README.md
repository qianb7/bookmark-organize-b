# bookmark-organize-b

一个用于“浏览器书签整理”的 Cursor Skill。  
核心目标：把 Edge/Chrome 导出的书签 HTML，先整理成可复核的 CSV，再在用户确认后回生成为可导入浏览器的 HTML。

## 这个仓库解决什么问题

书签通常存在这些痛点：
- 分类混乱（技术、学习、娱乐混在一起）
- 重复链接多
- 导出后难以批量整理
- 导回浏览器后结构不可控

本 Skill 提供一套标准流程：
1. 读取导出的书签 HTML
2. 提取标题/URL并去重（按完全相同 URL）
3. 先给出“大类/小类”分类草案并让用户确认
4. 逐条分类（不确定时访问页面确认）
5. 先输出带时间戳 CSV 给用户复核
6. 用户确认无误后，再输出带时间戳 HTML
7. 提示如何在 Edge/Chrome 导入

## 仓库结构

- `SKILL.md`：主流程与执行规则（中文）
- `examples.md`：典型对话与执行示例
- `reference.md`：分类词典、冲突优先级、备注模板

## 适用场景

- “帮我整理这份 Edge/Chrome 导出的书签 HTML”
- “先按规则分类，再让我确认”
- “分类拿不准时请你自己访问页面确认”
- “输出 CSV 给我检查，确认后再导出 HTML”

## 推荐分类体系（可按用户确认调整）

大类通常包括：
- AI
- 开发
- 学习
- 设计
- 社区
- 工具
- 工作
- 娱乐
- 生活

> 说明：实际执行时，以用户最终确认的分类体系为准。

## 使用方式

把这个 skill 放到 `~/.cursor/skills/bookmark-organize-b/` 后，在对话中提出如下需求即可触发：

- “请用 bookmark-organize-b 帮我整理这个书签 html”
- “按你先给分类草案、我确认后再逐条整理的流程执行”

## 导入浏览器说明（最终 HTML）

Edge/Chrome 通用步骤：
1. 打开“书签管理器”
2. 选择“从 HTML 导入书签”
3. 选择本 Skill 生成的最终 HTML

注意：
- 浏览器有时会默认导入到“其他收藏夹”
- 可手动将导入后的目录拖到“收藏夹栏/书签栏”

## 设计原则

- 不删除非重复链接
- 仅对“完全相同 URL”去重
- 先分类草案确认，再逐条落位
- 用户确认 CSV 后才生成最终 HTML
- 输出文件统一带时间戳，避免覆盖

## 配套脚本（可选但建议）

为了提升稳定性与可复用性，skill 里建议使用两个脚本完成“结构转换/文件生成”（分类逻辑仍由 skill 规则和用户确认驱动）：

1. 书签 HTML -> 提取记录 CSV（不分类）
   - `scripts/parse_bookmarks_html.py --input <source.html> --output <extracted.csv>`
   - 输出列：`标题,网址,备注`

2. 分类 CSV -> Netscape 书签 HTML（生成可导入文件）
   - `scripts/render_bookmarks_html.py --input <classified.csv> --output <out.html> [--personal-toolbar]`
   - 输入 CSV 必须包含列：`大类,小类,网站标题,备注说明,网址`
   - `--personal-toolbar`：额外生成带“收藏夹栏”容器的版本，更贴近 Edge 书签栏导入效果


