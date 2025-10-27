#!/usr/bin/env python3
"""
域名批量检查工具

功能：
1. 批量检查域名可用性
2. 查询域名Whois信息
3. 检查DNS解析状态
4. 生成检查报告

使用方法：
python domain-checker.py -f domains.txt -o report.csv
"""

import argparse
import csv
import time
import socket
import whois
import dns.resolver
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class DomainChecker:
    def __init__(self, timeout=10, max_workers=10):
        self.timeout = timeout
        self.max_workers = max_workers
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
    
    def check_domain_availability(self, domain):
        """检查域名是否可注册"""
        try:
            # 尝试查询域名的NS记录
            self.resolver.resolve(domain, 'NS')
            return False  # 域名已注册
        except dns.resolver.NXDOMAIN:
            return True   # 域名可注册
        except Exception:
            return None   # 查询失败
    
    def get_whois_info(self, domain):
        """获取域名Whois信息"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'name_servers': w.name_servers if w.name_servers else []
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_dns_resolution(self, domain):
        """检查DNS解析"""
        results = {}
        
        # 检查A记录
        try:
            answers = self.resolver.resolve(domain, 'A')
            results['A'] = [str(rdata) for rdata in answers]
        except Exception:
            results['A'] = []
        
        # 检查AAAA记录
        try:
            answers = self.resolver.resolve(domain, 'AAAA')
            results['AAAA'] = [str(rdata) for rdata in answers]
        except Exception:
            results['AAAA'] = []
        
        # 检查MX记录
        try:
            answers = self.resolver.resolve(domain, 'MX')
            results['MX'] = [str(rdata) for rdata in answers]
        except Exception:
            results['MX'] = []
        
        return results
    
    def check_website_status(self, domain):
        """检查网站状态"""
        try:
            # 尝试连接HTTP端口
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((domain, 80))
            sock.close()
            
            if result == 0:
                return 'HTTP_OK'
            else:
                return 'HTTP_FAIL'
        except Exception:
            return 'HTTP_ERROR'
    
    def check_single_domain(self, domain):
        """检查单个域名的完整信息"""
        print(f"正在检查域名: {domain}")
        
        result = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'available': None,
            'whois_info': {},
            'dns_records': {},
            'website_status': None
        }
        
        # 检查可用性
        result['available'] = self.check_domain_availability(domain)
        
        # 如果域名已注册，获取详细信息
        if result['available'] is False:
            result['whois_info'] = self.get_whois_info(domain)
            result['dns_records'] = self.check_dns_resolution(domain)
            result['website_status'] = self.check_website_status(domain)
        
        return result
    
    def check_domains_batch(self, domains):
        """批量检查域名"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_domain = {
                executor.submit(self.check_single_domain, domain): domain 
                for domain in domains
            }
            
            # 收集结果
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"检查域名 {domain} 时出错: {e}")
                    results.append({
                        'domain': domain,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        return results
    
    def save_results_to_csv(self, results, output_file):
        """保存结果到CSV文件"""
        fieldnames = [
            'domain', 'timestamp', 'available', 'registrar', 
            'creation_date', 'expiration_date', 'name_servers',
            'a_records', 'aaaa_records', 'mx_records', 'website_status'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = {
                    'domain': result['domain'],
                    'timestamp': result['timestamp'],
                    'available': result.get('available'),
                    'website_status': result.get('website_status')
                }
                
                # 处理Whois信息
                whois_info = result.get('whois_info', {})
                row['registrar'] = whois_info.get('registrar')
                row['creation_date'] = whois_info.get('creation_date')
                row['expiration_date'] = whois_info.get('expiration_date')
                row['name_servers'] = '; '.join(whois_info.get('name_servers', []))
                
                # 处理DNS记录
                dns_records = result.get('dns_records', {})
                row['a_records'] = '; '.join(dns_records.get('A', []))
                row['aaaa_records'] = '; '.join(dns_records.get('AAAA', []))
                row['mx_records'] = '; '.join(dns_records.get('MX', []))
                
                writer.writerow(row)
        
        print(f"结果已保存到: {output_file}")

def load_domains_from_file(filename):
    """从文件加载域名列表"""
    domains = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith('#'):
                    domains.append(domain)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filename}")
        return []
    
    return domains

def main():
    parser = argparse.ArgumentParser(description='域名批量检查工具')
    parser.add_argument('-f', '--file', required=True, help='包含域名列表的文件')
    parser.add_argument('-o', '--output', default='domain_check_results.csv', help='输出CSV文件名')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='查询超时时间（秒）')
    parser.add_argument('-w', '--workers', type=int, default=10, help='并发工作线程数')
    parser.add_argument('--delay', type=float, default=0.1, help='请求间隔时间（秒）')
    
    args = parser.parse_args()
    
    # 加载域名列表
    domains = load_domains_from_file(args.file)
    if not domains:
        print("没有找到有效的域名")
        return
    
    print(f"加载了 {len(domains)} 个域名")
    
    # 创建检查器
    checker = DomainChecker(timeout=args.timeout, max_workers=args.workers)
    
    # 开始检查
    start_time = time.time()
    print("开始批量检查域名...")
    
    results = checker.check_domains_batch(domains)
    
    # 保存结果
    checker.save_results_to_csv(results, args.output)
    
    # 统计信息
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    available_count = sum(1 for r in results if r.get('available') is True)
    registered_count = sum(1 for r in results if r.get('available') is False)
    error_count = sum(1 for r in results if 'error' in r)
    
    print(f"\n检查完成!")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"可注册域名: {available_count}")
    print(f"已注册域名: {registered_count}")
    print(f"查询错误: {error_count}")

if __name__ == '__main__':
    main()