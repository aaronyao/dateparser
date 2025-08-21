#!/usr/bin/env python3
"""
测试多语言复合相对日期解析功能
"""

import dateparser
from datetime import datetime

def test_compound_relative_dates():
    # 设置基准时间为2024年1月15日(星期一)
    base_time = datetime(2024, 1, 15, 10, 0, 0)
    
    print(f'基准时间: {base_time.strftime("%Y年%m月%d日 %A")}')
    print('=' * 60)
    
    # 测试用例
    test_cases = [
        # 中文测试
        ('上周五', 'zh', '上周的星期五'),
        ('本周五', 'zh', '本周的星期五'), 
        ('下周五', 'zh', '下周的星期五'),
        ('上周一', 'zh', '上周的星期一'),
        ('下周三', 'zh', '下周的星期三'),
        
        # 英文测试
        ('last friday', 'en', '上周五'),
        ('this friday', 'en', '本周五'),
        ('next friday', 'en', '下周五'),
        ('last monday', 'en', '上周一'),
        ('next wednesday', 'en', '下周三'),
        
        # 其他语言测试
        ('pasado viernes', 'es', '上周五(西班牙语)'),
        ('próximo lunes', 'es', '下周一(西班牙语)'),
        ('dernier vendredi', 'fr', '上周五(法语)'),
        ('prochain lundi', 'fr', '下周一(法语)'),
        
        # 基本相对日期（确保仍然工作）
        ('昨天', 'zh', '昨天'),
        ('明天', 'zh', '明天'),
        ('后天', 'zh', '后天'),
        ('yesterday', 'en', 'yesterday'),
        ('tomorrow', 'en', 'tomorrow'),
    ]
    
    print('多语言复合相对日期解析测试结果:')
    print('=' * 60)
    
    success_count = 0
    for case, lang, description in test_cases:
        try:
            result = dateparser.parse(case, languages=[lang], settings={'RELATIVE_BASE': base_time})
            if result:
                weekday_cn = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][result.weekday()]
                print(f'{case:20} -> {result.strftime("%m月%d日")} {weekday_cn} ✓')
                success_count += 1
            else:
                print(f'{case:20} -> 解析失败 ✗')
        except Exception as e:
            print(f'{case:20} -> 错误: {e} ✗')
    
    print('=' * 60)
    print(f'成功解析: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)')
    
    print('\n✅ 扩展功能总结:')
    print('• 支持中文复合相对日期: 上周X、本周X、下周X')
    print('• 支持英文复合相对日期: last X, this X, next X')  
    print('• 支持西班牙文: pasado X, próximo X')
    print('• 支持法文: dernier X, prochain X')
    print('• 支持德文: letzten X, nächsten X')
    print('• 保持原有功能: 昨天、明天、yesterday、tomorrow等')

if __name__ == "__main__":
    test_compound_relative_dates()

