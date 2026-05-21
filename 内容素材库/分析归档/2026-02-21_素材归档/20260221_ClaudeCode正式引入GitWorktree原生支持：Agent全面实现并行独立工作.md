

↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新

Claude Code现已原生内置Git Worktree支持。现在，多个Agent可以完全并行运行，互不干扰。每个Agent都会获得专属的独立工作区。

这项功能此前已在Claude Code桌面端应用中提供，今天正式扩展至命令行（CLI）环境。

了解Worktree底层机制：

https://git-scm.com/docs/git-worktree

以下是本次更新的核心功能拆解：

### 命令行支持一键开启隔离环境

在命令行中，启动时附带--worktree参数即可让Claude Code在专属的Git工作区中运行。你可以自行命名工作区，或者直接让Claude自动完成命名。

这项机制允许在同一个Git仓库下同时运行多个平行的Claude Code会话，彻底解决了多任务并发时的代码修改冲突问题。

同时，附加--tmux参数可以直接在专属的Tmux会话中启动Claude。

### 桌面端应用提供可视化开关

如果不习惯使用终端命令行，可以直接在Claude桌面端应用中操作。进入Code选项卡，直接勾选worktree mode即可开启工作区模式。

桌面端快速启动指南：

https://code.claude.com/docs/en/desktop-quickstart  

### 子Agent全平台打通工作区特性

子Agent现在同样利用工作区隔离机制来处理更多的并行任务。在应对大型批量修改和代码迁移任务时，这项特性极具实用性。

只需直接要求Claude为其Agent使用工作区即可调用该能力。

目前该功能已完成全生态覆盖，支持环境包括：CLI命令行、桌面端应用、IDE扩展、Web端以及Claude Code移动端App。

### 自定义Agent支持默认隔离配置

你可以让自定义子Agent始终在自己的工作区中运行。配置方式非常直接，只需在Agent的头部配置信息（frontmatter）中添加isolation: worktree即可生效。

### 全面兼容非Git版本控制系统

对于使用Mercurial、Perforce或SVN的用户，本次更新同样提供了解决方案。通过定义工作区钩子（worktree hooks），非Git用户也能完整体验到代码隔离机制带来的优势。

--end--

最后记得⭐️我，每天都在更新：如果觉得文章还不错的话可以点赞转发推荐评论