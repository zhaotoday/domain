# DNS 配置最佳实践

## DNS 配置概述

DNS 配置是域名管理的核心环节，正确的 DNS 配置直接影响网站的可访问性、性能和安全性。本文档提供全面的 DNS 配置指南和最佳实践。

## 基础 DNS 记录配置

### 1. A 记录配置

#### 基本A记录
```
# 主域名指向
@       IN  A   192.168.1.1
www     IN  A   192.168.1.1

# 子域名配置
mail    IN  A   192.168.1.2
ftp     IN  A   192.168.1.3
api     IN  A   192.168.1.4
```

#### 负载均衡A记录
```
# 多个A记录实现简单负载均衡
www     IN  A   192.168.1.1
www     IN  A   192.168.1.2
www     IN  A   192.168.1.3

# 权重配置（部分DNS服务商支持）
www     IN  A   192.168.1.1  weight=10
www     IN  A   192.168.1.2  weight=5
```

### 2. AAAA记录配置

#### IPv6地址配置
```
# IPv6主记录
@       IN  AAAA    2001:db8::1
www     IN  AAAA    2001:db8::1

# 双栈配置
www     IN  A       192.168.1.1
www     IN  AAAA    2001:db8::1
```

### 3. CNAME记录配置

#### 别名配置
```
# 常用别名
www     IN  CNAME   example.com.
blog    IN  CNAME   www.example.com.
shop    IN  CNAME   www.example.com.

# CDN配置
static  IN  CNAME   cdn.example.com.
images  IN  CNAME   img.cloudfront.net.
```

#### CNAME注意事项
```
错误配置：
@       IN  CNAME   www.example.com.  # 根域名不能使用CNAME

正确配置：
@       IN  A       192.168.1.1
www     IN  CNAME   example.com.
```

### 4. MX记录配置

#### 邮件服务器配置
```
# 单个邮件服务器
@       IN  MX  10  mail.example.com.

# 多个邮件服务器（优先级不同）
@       IN  MX  10  mail1.example.com.
@       IN  MX  20  mail2.example.com.
@       IN  MX  30  mail3.example.com.

# Google Workspace配置
@       IN  MX  1   aspmx.l.google.com.
@       IN  MX  5   alt1.aspmx.l.google.com.
@       IN  MX  5   alt2.aspmx.l.google.com.
@       IN  MX  10  alt3.aspmx.l.google.com.
@       IN  MX  10  alt4.aspmx.l.google.com.
```

### 5. TXT记录配置

#### SPF记录
```
# 基本SPF配置
@       IN  TXT "v=spf1 include:_spf.google.com ~all"

# 复杂SPF配置
@       IN  TXT "v=spf1 ip4:192.168.1.0/24 include:_spf.google.com include:mailgun.org ~all"
```

#### DKIM记录
```
# DKIM选择器记录
selector1._domainkey  IN  TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC..."
```

#### DMARC记录
```
# DMARC策略
_dmarc  IN  TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

#### 域名验证记录
```
# Google验证
@       IN  TXT "google-site-verification=abc123..."

# Microsoft验证
@       IN  TXT "MS=ms123456789"
```

### 6. NS记录配置

#### 权威DNS服务器
```
# 主域名NS记录
@       IN  NS  ns1.example.com.
@       IN  NS  ns2.example.com.

# 子域名委托
subdomain   IN  NS  ns1.subdomain.example.com.
subdomain   IN  NS  ns2.subdomain.example.com.
```

## 高级DNS配置

### 1. SRV记录配置

#### 服务发现配置
```
# SIP服务
_sip._tcp       IN  SRV 10  5   5060    sip.example.com.
_sips._tcp      IN  SRV 10  5   5061    sip.example.com.

# XMPP服务
_xmpp-server._tcp   IN  SRV 5   0   5269    xmpp.example.com.
_xmpp-client._tcp   IN  SRV 5   0   5222    xmpp.example.com.

# Minecraft服务器
_minecraft._tcp     IN  SRV 0   5   25565   mc.example.com.
```

### 2. CAA记录配置

#### 证书颁发机构授权
```
# 允许Let's Encrypt颁发证书
@       IN  CAA 0   issue       "letsencrypt.org"

# 允许多个CA
@       IN  CAA 0   issue       "letsencrypt.org"
@       IN  CAA 0   issue       "digicert.com"

# 通配符证书授权
@       IN  CAA 0   issuewild   "letsencrypt.org"

# 违规报告
@       IN  CAA 0   iodef       "mailto:security@example.com"
```

### 3. PTR记录配置

#### 反向DNS配置
```
# IPv4反向DNS
1.1.168.192.in-addr.arpa.   IN  PTR mail.example.com.

# IPv6反向DNS
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. IN PTR mail.example.com.
```

## DNS安全配置

### 1. DNSSEC配置

#### 密钥生成
```bash
# 生成KSK (Key Signing Key)
dnssec-keygen -a RSASHA256 -b 2048 -f KSK example.com

# 生成ZSK (Zone Signing Key)
dnssec-keygen -a RSASHA256 -b 1024 example.com
```

#### 区域签名
```bash
# 签名区域文件
dnssec-signzone -o example.com -k Kexample.com.+008+12345.key example.com.zone Kexample.com.+008+54321.key
```

#### DS记录配置
```
# 在父域名中配置DS记录
example.com.    IN  DS  12345 8 2 1234567890ABCDEF...
```

### 2. DNS防护配置

#### 限制查询
```
# BIND配置示例
acl "trusted" {
    192.168.1.0/24;
    10.0.0.0/8;
};

options {
    allow-query { trusted; };
    allow-recursion { trusted; };
    allow-transfer { none; };
};
```

#### 隐藏版本信息
```
# BIND配置
options {
    version "DNS Server";
    hostname "ns.example.com";
};
```

## 性能优化配置

### 1. TTL优化

#### TTL设置策略
```
# 静态内容 - 长TTL
www     86400   IN  A   192.168.1.1

# 动态内容 - 短TTL
api     300     IN  A   192.168.1.2

# 负载均衡 - 中等TTL
lb      1800    IN  A   192.168.1.3

# 故障切换 - 很短TTL
backup  60      IN  A   192.168.1.4
```

### 2. 地理位置DNS

#### GeoDNS配置示例
```
# 美国用户
www.us      IN  A   192.168.1.1

# 欧洲用户
www.eu      IN  A   192.168.2.1

# 亚洲用户
www.asia    IN  A   192.168.3.1

# 默认
www         IN  CNAME   www.us.example.com.
```

### 3. 负载均衡配置

#### DNS轮询
```
# 简单轮询
www     IN  A   192.168.1.1
www     IN  A   192.168.1.2
www     IN  A   192.168.1.3
```

#### 加权轮询
```
# 使用SRV记录实现加权
_http._tcp  IN  SRV 10  60  80  server1.example.com.
_http._tcp  IN  SRV 10  30  80  server2.example.com.
_http._tcp  IN  SRV 10  10  80  server3.example.com.
```

## 监控和维护

### 1. DNS监控脚本

#### Python监控脚本
```python
import dns.resolver
import time
import smtplib
from email.mime.text import MIMEText

class DNSMonitor:
    def __init__(self, domains, expected_records):
        self.domains = domains
        self.expected_records = expected_records
    
    def check_dns_records(self, domain):
        results = {}
        for record_type in ['A', 'AAAA', 'MX', 'NS']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                results[record_type] = [str(rdata) for rdata in answers]
            except dns.resolver.NXDOMAIN:
                results[record_type] = []
            except Exception as e:
                results[record_type] = [f"Error: {e}"]
        return results
    
    def monitor_loop(self):
        while True:
            for domain in self.domains:
                current = self.check_dns_records(domain)
                expected = self.expected_records.get(domain, {})
                
                for record_type, expected_values in expected.items():
                    current_values = current.get(record_type, [])
                    if set(current_values) != set(expected_values):
                        self.send_alert(domain, record_type, expected_values, current_values)
            
            time.sleep(300)  # 5分钟检查一次
    
    def send_alert(self, domain, record_type, expected, current):
        message = f"""
        DNS记录变化警告:
        域名: {domain}
        记录类型: {record_type}
        期望值: {expected}
        当前值: {current}
        """
        print(message)
        # 这里可以添加邮件发送逻辑
```

### 2. 健康检查

#### DNS健康检查脚本
```bash
#!/bin/bash

DOMAIN="example.com"
EXPECTED_IP="192.168.1.1"

# 检查A记录
CURRENT_IP=$(dig +short $DOMAIN @8.8.8.8)

if [ "$CURRENT_IP" != "$EXPECTED_IP" ]; then
    echo "警告: $DOMAIN 的IP地址已变更"
    echo "期望: $EXPECTED_IP"
    echo "当前: $CURRENT_IP"
    # 发送告警
fi

# 检查DNS响应时间
RESPONSE_TIME=$(dig $DOMAIN @8.8.8.8 | grep "Query time" | awk '{print $4}')
if [ $RESPONSE_TIME -gt 1000 ]; then
    echo "警告: DNS响应时间过长: ${RESPONSE_TIME}ms"
fi
```

## 故障排查

### 1. 常见DNS问题

#### 解析失败
```bash
# 检查DNS配置
dig example.com
dig @8.8.8.8 example.com

# 检查权威DNS
dig example.com NS
dig @ns1.example.com example.com
```

#### 传播延迟
```bash
# 检查全球DNS传播
dig example.com @8.8.8.8
dig example.com @1.1.1.1
dig example.com @208.67.222.222
```

### 2. 调试工具

#### 命令行工具
```bash
# dig - 详细DNS查询
dig example.com ANY +trace

# nslookup - 交互式查询
nslookup
> set type=MX
> example.com

# host - 简单查询
host -t MX example.com
```

#### 在线工具
- DNS Checker
- MX Toolbox
- DNS Propagation Checker
- IntoDNS

## 最佳实践总结

### 1. 配置原则
- 使用多个DNS服务器
- 设置合理的TTL值
- 定期备份DNS配置
- 监控DNS变化

### 2. 安全原则
- 启用DNSSEC
- 限制区域传输
- 隐藏DNS版本信息
- 定期更新DNS软件

### 3. 性能原则
- 优化TTL设置
- 使用CDN和负载均衡
- 选择就近的DNS服务器
- 监控DNS性能指标

### 4. 维护原则
- 建立变更管理流程
- 定期审查DNS配置
- 制定应急响应计划
- 培训运维人员

## 总结

正确的DNS配置是网站稳定运行的基础。通过遵循最佳实践，可以提高网站的可用性、性能和安全性。定期监控和维护DNS配置，及时发现和解决问题，是确保服务质量的关键。