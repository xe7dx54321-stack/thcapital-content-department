# Windows 侧运行说明

## 推荐运行方式

在 Windows 副机上运行：

```bat
run_wechat_bridge_consumer.bat
```

建议把这个 `.bat` 配到 **任务计划程序 / 登录后自动启动**，让副机长期保持监听。

如果要正式进入自治运行，推荐直接安装我们准备好的计划任务：

```powershell
PowerShell -ExecutionPolicy Bypass -File D:\THCapital\wechat-bridge-outbox\tools\install_wechat_bridge_consumer_task.ps1 -RunNow
```

安装后会创建计划任务 `THCapital-WeChat-Bridge-Consumer`，并启动一个带自恢复的 runner：

- `run_wechat_bridge_consumer_forever.ps1`
- consumer 异常退出后会自动重拉
- 日志写入 `D:\THCapital\wechat-bridge-outbox\logs\wechat_bridge_consumer.log`
- runner 现在带**单实例保护**：计划任务、Startup、手动双击、手动 `py --watch` 同时触发时，只保留一个存活实例，避免双开锁文件
- 手动移除任务可运行：

```powershell
PowerShell -ExecutionPolicy Bypass -File D:\THCapital\wechat-bridge-outbox\tools\remove_wechat_bridge_consumer_task.ps1
```

安装脚本会先尝试“登录 + 开机”双触发的高权限模式；如果当前账户没有管理员权限，会自动降级成“当前用户登录后自启动”的普通模式。
降级时会**自动额外安装 Startup 启动项兜底**，避免某些受限环境下任务计划程序起不来。

如果连普通计划任务也被系统策略拦截，还可以退回到“Startup 启动文件夹”模式：

```powershell
PowerShell -ExecutionPolicy Bypass -File D:\THCapital\wechat-bridge-outbox\tools\install_wechat_bridge_consumer_startup.ps1
```

它会在当前用户的 Startup 文件夹中创建一个快捷方式，保证登录后自动拉起 watchdog runner。

watchdog 内部会优先尝试：

- `py -3 wechat_bridge_consumer.py --watch --interval 20`
- 如果没有 `py` 启动器，再退回 `python wechat_bridge_consumer.py --watch --interval 20`

## 密钥读取顺序

1. 环境变量：
   - `TH_WECHAT_APPID`
   - `TH_WECHAT_APPSECRET`
2. 本机本地配置文件：
   - `%LOCALAPPDATA%\\THCapital\\wechat-bridge\\credentials.json`

## 本地配置文件格式

```json
{
  "appid": "wx...",
  "secret": "your-secret"
}
```

这个文件要存放在 **Windows 本地**，不要放进同步目录。
