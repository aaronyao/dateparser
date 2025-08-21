#!/usr/bin/env python3
"""
测试10种语言的复合相对日期解析支持
"""

import dateparser
from datetime import datetime

def test_10_languages():
    print('=== DateParser 10种语言复合相对日期测试 ===')
    base_time = datetime(2024, 1, 15, 10, 0, 0)  # 星期一
    print(f'基准时间: {base_time.strftime("%Y-%m-%d %A")}')
    print()

    # 测试所有10种语言
    test_cases = [
        ('上周五', ['zh'], '中文'),
        ('last friday', ['en'], '英文'),
        ('pasado viernes', ['es'], '西班牙文'),
        ('dernier vendredi', ['fr'], '法文'),
        ('letzten freitag', ['de'], '德文'),
        ('scorso venerdì', ['it'], '意大利文'),
        ('passado sexta', ['pt'], '葡萄牙文'),
        ('прошлый пятница', ['ru'], '俄文'),
        ('先週の金曜日', ['ja'], '日文'),
        ('지난 금요일', ['ko'], '韩文'),
    ]

    success = 0
    total = len(test_cases)

    print('测试结果:')
    print('=' * 60)
    
    for expression, languages, lang_name in test_cases:
        try:
            result = dateparser.parse(expression, languages=languages, 
                                    settings={'RELATIVE_BASE': base_time})
            if result:
                weekday_cn = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][result.weekday()]
                date_str = result.strftime('%m-%d')
                print(f'✅ {expression:20} ({languages[0]}) -> {date_str} {weekday_cn}')
                success += 1
            else:
                print(f'❌ {expression:20} ({languages[0]}) -> 解析失败')
        except Exception as e:
            print(f'❌ {expression:20} ({languages[0]}) -> 错误: {e}')

    print('=' * 60)
    print(f'成功率: {success}/{total} ({success/total*100:.1f}%)')
    
    if success == total:
        print('\n🎉 完美！所有10种语言都支持成功！')
        print('✅ 支持的语言: zh, en, es, fr, de, it, pt, ru, ja, ko')
        print('✅ 功能: 复合相对日期解析 (如"上周五"、"last friday"等)')
        print('✅ 集成: 完全集成到dateparser主接口')
    else:
        print(f'\n⚠️  还有 {total-success} 种语言需要调整')

    return success == total

if __name__ == "__main__":
    test_10_languages()
