# DNS 查询工具大全

## 命令行 DNS 工具

### 1. dig (Domain Information Groper)

#### 基本用法
```bash
# 基本查询
dig example.com

# 查询特定记录类型
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT

# 查询所有记录
dig example.com ANY
```

#### 高级用法
```bash
# 指定DNS服务器
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com A

# 追踪查询路径
dig +trace example.com

# 简短输出
dig +short example.com

# 反向DNS查询
dig -x 8.8.8.8

# 批量查询
dig -f domain_list.txt

# 查询特定端口
dig @dns.server.com -p 5353 example.com
```

#### 输出格式控制
```bash
# JSON格式输出
dig +json example.com

# 详细输出
dig +all example.com

# 禁用递归
dig +norecurse example.com

# 显示查询时间
dig +stats example.com

# 多行输出
dig +multiline example.com SOA
```

### 2. nslookup

#### 交互模式
```bash
nslookup
> set type=A
> example.com
> set type=MX
> example.com
> server 8.8.8.8
> example.com
> exit
```

#### 非交互模式
```bash
# 基本查询
nslookup example.com

# 指定记录类型
nslookup -type=MX example.com

# 指定DNS服务器
nslookup example.com 8.8.8.8

# 反向查询
nslookup 8.8.8.8
```

#### 高级选项
```bash
# 调试模式
nslookup -debug example.com

# 设置超时时间
nslookup -timeout=10 example.com

# 查询类别
nslookup -class=IN example.com
```

### 3. host

#### 基本用法
```bash
# 简单查询
host example.com

# 查询特定类型
host -t MX example.com
host -t NS example.com
host -t TXT example.com

# 详细输出
host -v example.com

# 反向查询
host 8.8.8.8
```

#### 高级选项
```bash
# 指定DNS服务器
host example.com 8.8.8.8

# 查询所有记录
host -a example.com

# TCP查询
host -T example.com

# 设置重试次数
host -R 3 example.com
```

### 4. systemd-resolve (Linux)

```bash
# 基本查询
systemd-resolve example.com

# 查询特定类型
systemd-resolve --type=MX example.com

# 显示统计信息
systemd-resolve --statistics

# 刷新缓存
systemd-resolve --flush-caches

# 查看配置
systemd-resolve --status
```

## 在线 DNS 查询工具

### 1. 综合查询平台

#### DNS Checker
- **网址**: https://dnschecker.org/
- **特点**: 
  - 全球多点查询
  - 支持所有记录类型
  - 传播检查功能
- **优势**: 界面友好，结果直观

#### MX Toolbox
- **网址**: https://mxtoolbox.com/
- **特点**:
  - 专业网络诊断工具
  - 集成多种DNS工具
  - 邮件服务器测试
- **优势**: 功能全面，专业性强

#### DNS Propagation Checker
- **网址**: https://www.whatsmydns.net/
- **特点**:
  - 全球DNS传播检查
  - 实时更新状态
  - 支持IPv6查询
- **优势**: 传播检查专业

### 2. 技术导向工具

#### IntoDNS
- **网址**: https://intodns.com/
- **特点**:
  - 全面的DNS健康检查
  - 配置问题诊断
  - 性能分析报告
- **优势**: 深度分析，问题诊断

#### DNS Stuff
- **网址**: https://www.dnsstuff.com/
- **特点**:
  - 专业DNS工具套件
  - 网络诊断功能
  - 企业级服务
- **优势**: 企业级功能

#### ViewDNS
- **网址**: https://viewdns.info/
- **特点**:
  - 多种DNS查询工具
  - 网络信息收集
  - 免费服务丰富
- **优势**: 工具种类多样

## 编程语言 DNS 库

### 1. Python DNS 库

#### dnspython
```python
import dns.resolver
import dns.query
import dns.zone

# 基本查询
def dns_query(domain, record_type='A'):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except dns.resolver.NXDOMAIN:
        return "域名不存在"
    except Exception as e:
        return f"查询错误: {e}"

# 使用示例
print(dns_query('example.com', 'A'))
print(dns_query('example.com', 'MX'))

# 高级查询
def advanced_dns_query(domain, nameserver='8.8.8.8'):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [nameserver]
    
    try:
        answers = resolver.resolve(domain, 'A')
        return [(answer.address, answer.ttl) for answer in answers]
    except Exception as e:
        return f"查询失败: {e}"

# 区域传输
def zone_transfer(domain, nameserver):
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
        return zone
    except Exception as e:
        return f"区域传输失败: {e}"
```

#### 安装和使用
```bash
# 安装dnspython
pip install dnspython

# 使用示例
python -c "import dns.resolver; print([str(r) for r in dns.resolver.resolve('example.com', 'A')])"
```

### 2. Node.js DNS 库

#### 内置dns模块
```javascript
const dns = require('dns');
const { promisify } = require('util');

// 异步查询
dns.resolve('example.com', 'A', (err, addresses) => {
    if (err) {
        console.error('查询失败:', err);
    } else {
        console.log('A记录:', addresses);
    }
});

// Promise化
const resolve = promisify(dns.resolve);

async function dnsQuery(domain, type = 'A') {
    try {
        const result = await resolve(domain, type);
        return result;
    } catch (error) {
        return `查询失败: ${error.message}`;
    }
}

// 使用示例
dnsQuery('example.com', 'MX').then(console.log);
```

#### dns2库
```javascript
const DNS = require('dns2');

const dns = new DNS();

// 查询示例
async function queryDNS(domain, type = 'A') {
    try {
        const result = await dns.resolveA(domain);
        return result.answers;
    } catch (error) {
        return `查询错误: ${error.message}`;
    }
}

// 自定义DNS服务器
const customDNS = new DNS({
    nameServers: ['8.8.8.8', '1.1.1.1']
});
```

### 3. Go DNS 库

#### miekg/dns
```go
package main

import (
    "fmt"
    "github.com/miekg/dns"
)

func queryDNS(domain, recordType, nameserver string) {
    c := new(dns.Client)
    m := new(dns.Msg)
    
    // 设置查询类型
    var qtype uint16
    switch recordType {
    case "A":
        qtype = dns.TypeA
    case "AAAA":
        qtype = dns.TypeAAAA
    case "MX":
        qtype = dns.TypeMX
    default:
        qtype = dns.TypeA
    }
    
    m.SetQuestion(dns.Fqdn(domain), qtype)
    
    r, _, err := c.Exchange(m, nameserver+":53")
    if err != nil {
        fmt.Printf("查询失败: %v\n", err)
        return
    }
    
    for _, ans := range r.Answer {
        fmt.Println(ans)
    }
}

func main() {
    queryDNS("example.com", "A", "8.8.8.8")
}
```

## 专业 DNS 工具

### 1. 桌面应用

#### DNS Benchmark
- **平台**: Windows
- **功能**: DNS 服务器性能测试
- **特点**: 
  - 测试响应时间
  - 可靠性分析
  - 自动推荐最佳 DNS

#### namebench
- **平台**: 跨平台
- **功能**: DNS 性能基准测试
- **特点**:
  - Google 开源项目
  - 详细性能报告
  - 历史数据分析

### 2. 网络管理工具

#### BIND utilities
```bash
# 安装BIND工具
sudo apt-get install bind9-utils  # Ubuntu/Debian
sudo yum install bind-utils       # CentOS/RHEL

# 使用工具
dig example.com
nslookup example.com
host example.com
```

#### PowerDNS工具
```bash
# pdns_control - PowerDNS控制工具
pdns_control ping
pdns_control show *
pdns_control purge example.com

# pdnsutil - 区域管理工具
pdnsutil create-zone example.com
pdnsutil add-record example.com www A 192.168.1.1
```

## DNS 监控工具

### 1. 开源监控方案

#### Nagios DNS 插件
```bash
# 检查 DNS 解析
./check_dns -H example.com -s 8.8.8.8

# 检查特定记录
./check_dns -H example.com -s 8.8.8.8 -a 192.168.1.1
```

#### Zabbix DNS 监控
```bash
# DNS 响应时间监控
net.dns[,example.com,A,2,1]

# DNS 记录检查
net.dns.record[,example.com,A,2,1]
```

### 2. 商业监控服务

#### Pingdom DNS 监控
- 全球多点监控
- 实时告警
- 详细报告

#### StatusCake DNS 监控
- 免费基础监控
- 多种告警方式
- 简单易用

## DNS 安全工具

### 1. DNSSEC 验证工具

#### dig DNSSEC 验证
```bash
# 检查 DNSSEC 签名
dig +dnssec example.com

# 验证 DNSSEC 链
dig +trace +dnssec example.com

# 检查 DS 记录
dig DS example.com
```

#### DNSSEC 验证器
```python
import dns.resolver
import dns.dnssec

def verify_dnssec(domain):
    try:
        # 获取 DNSKEY 记录
        dnskey_answer = dns.resolver.resolve(domain, 'DNSKEY')
        
        # 验证签名
        for rdata in dnskey_answer:
            if rdata.flags & dns.dnssec.ZONE:
                print(f"找到区域密钥: {rdata}")
        
        return True
    except Exception as e:
        print(f"DNSSEC 验证失败: {e}")
        return False
```

### 2. DNS 安全扫描

#### DNSRecon
```bash
# 安装DNSRecon
git clone https://github.com/darkoperator/dnsrecon.git

# 基本扫描
python dnsrecon.py -d example.com

# 区域传输测试
python dnsrecon.py -d example.com -t axfr

# 子域名枚举
python dnsrecon.py -d example.com -t brt -D subdomains.txt
```

#### Fierce
```bash
# 安装Fierce
pip install fierce

# 子域名发现
fierce --domain example.com

# 使用自定义字典
fierce --domain example.com --wordlist custom_list.txt
```

## DNS 性能测试工具

### 1. 响应时间测试

#### 自定义测试脚本
```python
import time
import dns.resolver

def dns_performance_test(domain, nameservers, iterations=10):
    results = {}
    
    for ns in nameservers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ns]
        
        times = []
        for _ in range(iterations):
            start_time = time.time()
            try:
                resolver.resolve(domain, 'A')
                end_time = time.time()
                times.append((end_time - start_time) * 1000)  # 转换为毫秒
            except:
                times.append(None)
        
        # 计算统计信息
        valid_times = [t for t in times if t is not None]
        if valid_times:
            results[ns] = {
                'avg': sum(valid_times) / len(valid_times),
                'min': min(valid_times),
                'max': max(valid_times),
                'success_rate': len(valid_times) / iterations * 100
            }
    
    return results

# 测试示例
nameservers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
results = dns_performance_test('example.com', nameservers)

for ns, stats in results.items():
    print(f"{ns}: 平均 {stats['avg']:.2f}ms, 成功率 {stats['success_rate']:.1f}%")
```

### 2. 批量测试工具

#### DNS 批量查询脚本
```bash
#!/bin/bash

# DNS 批量测试脚本
DOMAINS_FILE="domains.txt"
OUTPUT_FILE="dns_results.csv"

echo "Domain,A_Record,Response_Time" > $OUTPUT_FILE

while IFS= read -r domain; do
    if [ ! -z "$domain" ]; then
        start_time=$(date +%s%N)
        result=$(dig +short "$domain" A)
        end_time=$(date +%s%N)
        
        response_time=$(( (end_time - start_time) / 1000000 ))  # 转换为毫秒
        
        if [ ! -z "$result" ]; then
            echo "$domain,$result,${response_time}ms" >> $OUTPUT_FILE
        else
            echo "$domain,No_Record,${response_time}ms" >> $OUTPUT_FILE
        fi
    fi
done < "$DOMAINS_FILE"

echo "测试完成，结果保存在 $OUTPUT_FILE"
```

## 故障排查工具

### 1. DNS 路径追踪

#### 查询路径分析
```bash
# 完整查询路径
dig +trace example.com

# 分步查询
dig . NS                           # 查询根服务器
dig @a.root-servers.net com NS     # 查询.com服务器
dig @a.gtld-servers.net example.com NS  # 查询权威服务器
dig @ns1.example.com example.com A      # 最终查询
```

### 2. DNS 缓存分析

#### 缓存状态检查
```bash
# Linux 系统 DNS 缓存
sudo systemd-resolve --statistics
sudo systemd-resolve --flush-caches

# Windows DNS 缓存
ipconfig /displaydns
ipconfig /flushdns

# macOS DNS 缓存
sudo dscacheutil -flushcache
```

## 最佳实践

### 1. 工具选择建议
- **日常查询**: dig（功能最全面）
- **快速检查**: host（输出简洁）
- **Windows 用户**: nslookup（系统自带）
- **编程集成**: 各语言 DNS 库
- **性能测试**: 专业基准测试工具

### 2. 查询优化
- 使用就近的 DNS 服务器
- 合理设置超时时间
- 批量查询时控制频率
- 缓存查询结果

### 3. 安全考虑
- 使用可信的 DNS 服务器
- 验证 DNSSEC 签名
- 监控 DNS 查询异常
- 定期更新工具版本

## 总结

DNS 查询工具是网络管理和故障排查的重要工具。选择合适的工具并掌握其使用方法，可以有效提高工作效率和问题解决能力。建议根据具体需求选择工具，并结合多种工具进行综合分析。