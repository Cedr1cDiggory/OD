# OD 互动课件部署与更新指南

本项目是纯静态网站。服务器只需要部署 `public/` 中的内容，不需要 PHP、MySQL 或 Node.js。

## 服务器信息

- 系统：OpenCloudOS 9.6
- Web 服务：Nginx 1.26.3
- 网站目录：`/usr/share/nginx/html`
- 公网地址：`http://110.42.250.133/`

## 一、上线前检查

在本地 Windows PowerShell 中执行：

```powershell
cd D:\OD
python tools/validate_units.py
```

校验通过后再上传。

服务器只需要 `public/` 的内容。以下目录和文件不要上传：

```text
content/
tools/
templates/
Agents.md
```

## 二、首次完整部署

### 1. 本地打包

```powershell
cd D:\OD
Compress-Archive -Path .\public\* -DestinationPath .\od-site.zip -Force
```

生成文件：

```text
D:\OD\od-site.zip
```

ZIP 根目录应直接包含 `index.html`、`assets/`、`levels/` 和 `units/`，不要额外套一层 `public/`。

### 2. 上传 ZIP

可使用 OrcaTerm 左侧的 SFTP，将 `od-site.zip` 上传到：

```text
/root/od-site.zip
```

也可在本地 PowerShell 中执行：

```powershell
scp D:\OD\od-site.zip root@110.42.250.133:/root/
```

### 3. 服务器解压部署

首次部署前安装解压工具：

```bash
dnf install -y unzip
```

备份 Nginx 原始网页：

```bash
cp -a /usr/share/nginx/html /usr/share/nginx/html.backup
```

解压网站：

```bash
unzip -o /root/od-site.zip -d /usr/share/nginx/html
```

修复权限和 SELinux 标签：

```bash
chown -R nginx:nginx /usr/share/nginx/html
find /usr/share/nginx/html -type d -exec chmod 755 {} \;
find /usr/share/nginx/html -type f -exec chmod 644 {} \;
restorecon -Rv /usr/share/nginx/html
```

检查并重新加载 Nginx：

```bash
nginx -t
systemctl reload nginx
```

## 三、检查部署结果

检查服务器目录：

```bash
ls -la /usr/share/nginx/html
```

应直接看到：

```text
index.html
assets/
levels/
units/
courses.html
teachers.html
```

不应出现：

```text
/usr/share/nginx/html/public/index.html
```

访问测试：

```text
http://110.42.250.133/
http://110.42.250.133/levels/od-level-1.html
http://110.42.250.133/units/od1/unit-01/
```

## 四、更新单个 Unit

完成一个新 Unit 后，不需要重新上传整个网站。

例如更新 OD1 Unit 16，先上传 Unit 目录：

```powershell
cd D:\OD
scp -r .\public\units\od1\unit-16 root@110.42.250.133:/usr/share/nginx/html/units/od1/
```

再上传更新后的 OD1 目录页：

```powershell
scp .\public\levels\od-level-1.html root@110.42.250.133:/usr/share/nginx/html/levels/
```

如果首页也有修改：

```powershell
scp .\public\index.html root@110.42.250.133:/usr/share/nginx/html/
```

如果修改了共享资源：

```powershell
scp -r .\public\assets root@110.42.250.133:/usr/share/nginx/html/
```

上传完成后在服务器执行：

```bash
chown -R nginx:nginx /usr/share/nginx/html
restorecon -Rv /usr/share/nginx/html
```

静态 HTML 和图片更新后通常不需要重启 Nginx。

## 五、整站更新

如果同时修改了多个 Unit、首页和共享资源，建议重新打包整个 `public/`：

```powershell
cd D:\OD
python tools/validate_units.py
Compress-Archive -Path .\public\* -DestinationPath .\od-site.zip -Force
scp .\od-site.zip root@110.42.250.133:/root/
```

然后在服务器执行：

```bash
unzip -o /root/od-site.zip -d /usr/share/nginx/html
chown -R nginx:nginx /usr/share/nginx/html
restorecon -Rv /usr/share/nginx/html
nginx -t
systemctl reload nginx
```

`unzip -o` 会覆盖同名文件，但不会自动删除服务器上已经废弃的旧文件。如有文件改名或删除，应同步清理对应旧文件。

## 六、浏览器缓存

如果更新后仍显示旧页面：

- Windows 浏览器：按 `Ctrl + F5`。
- iPad Safari：关闭页面后重新打开，必要时清除该网站缓存。
- 如果图片使用相同文件名替换，浏览器可能继续使用旧缓存。

## 七、Nginx 排查命令

检查 Nginx 状态：

```bash
systemctl status nginx
```

检查配置：

```bash
nginx -t
```

检查本机首页：

```bash
curl -I http://127.0.0.1/
curl http://127.0.0.1/ | head
```

检查网站根目录配置：

```bash
grep -R "root " /etc/nginx/nginx.conf /etc/nginx/conf.d
```

默认网站根目录应为：

```text
/usr/share/nginx/html
```

查看错误日志：

```bash
tail -n 100 /var/log/nginx/error.log
```

## 八、域名与 HTTPS

有域名后：

1. 添加域名 `A` 记录并指向 `110.42.250.133`。
2. 在 Nginx 或宝塔面板中绑定域名。
3. 申请 Let's Encrypt 免费 SSL 证书。
4. 放行服务器 `443` 端口。
5. 开启 HTTP 到 HTTPS 强制跳转。

如果服务器位于中国大陆，使用域名正式提供网站服务前需要完成 ICP 备案。

## 九、安全建议

- 防火墙只开放实际需要的端口：`22`、`80`、`443` 和面板端口。
- 修改宝塔默认面板端口并开启面板 SSL。
- 使用复杂密码或 SSH 密钥。
- 定期备份 `/usr/share/nginx/html`。
- 不要将服务器密码、私钥或宝塔登录信息提交到项目仓库。

## 十、推荐更新流程

每次发布按以下顺序操作：

1. 在本地完成 Unit 页面和资源。
2. 运行 `python tools/validate_units.py`。
3. 确认校验无错误。
4. 单 Unit 改动使用增量上传。
5. 多 Unit 或共享资源改动使用整站 ZIP。
6. 上传后检查权限和 SELinux 标签。
7. 在公网地址测试首页、目录页和具体 Unit。

