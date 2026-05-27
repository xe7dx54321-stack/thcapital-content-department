# P7-007 Failure Notification Report

## 本轮目标

生成失败通知报告，暂不接微信、邮件或其他真实推送。

## 新增命令

```bash
make failure-notification
```

## 报告内容

- pipeline failures
- agent failures
- live failures
- fallback count
- estimated cost warning
- recommended actions

## 当前限制

- 只生成文件型通知。
- 不发送真实通知。
