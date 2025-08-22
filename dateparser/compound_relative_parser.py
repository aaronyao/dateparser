"""
复合相对日期解析器
支持多语言的复合相对日期表达，如"上周五"、"last friday"、"next monday"、"上个月十七号"、"last month 17th"等
"""

import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class CompoundRelativeParser:
    """处理多语言复合相对日期表达的解析器"""
    
    def __init__(self):
        # 定义各语言的模式和映射
        self.language_patterns = {
            'zh': {
                'week_pattern': re.compile(r'(上|下|本|这)周(?:星期)?([一二三四五六日天1234567])'),
                'month_pattern': re.compile(r'(上|下|本|这)(?:个)?月([一二三四五六七八九十]+|[0-9]+)(?:号|日)'),
                'relative_map': {'上': -1, '下': 1, '本': 0, '这': 0},
                'weekday_map': {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6, '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6},
                'number_map': {
                    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
                    '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18, 
                    '十九': 19, '二十': 20, '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
                    '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30, '三十一': 31
                }
            },
            'en': {
                'week_pattern': re.compile(r'(last|next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', re.IGNORECASE),
                'month_pattern': re.compile(r'(last|next|this)\s+month\s+(\d{1,2})(?:st|nd|rd|th)?', re.IGNORECASE),
                'relative_map': {'last': -1, 'next': 1, 'this': 0},
                'weekday_map': {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
            },
            'es': {
                'week_pattern': re.compile(r'(pasado|próximo|este)\s+(lunes|martes|miércoles|jueves|viernes|sábado|domingo)', re.IGNORECASE),
                'month_pattern': re.compile(r'(pasado|próximo|este)\s+mes\s+(\d{1,2})', re.IGNORECASE),
                'relative_map': {'pasado': -1, 'próximo': 1, 'este': 0},
                'weekday_map': {'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6}
            },
            'fr': {
                'week_pattern': re.compile(r'(dernier|prochain|ce)\s+(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)', re.IGNORECASE),
                'month_pattern': re.compile(r'(dernier|prochain|ce)\s+mois\s+(\d{1,2})', re.IGNORECASE),
                'relative_map': {'dernier': -1, 'prochain': 1, 'ce': 0},
                'weekday_map': {'lundi': 0, 'mardi': 1, 'mercredi': 2, 'jeudi': 3, 'vendredi': 4, 'samedi': 5, 'dimanche': 6}
            },
            'de': {
                'week_pattern': re.compile(r'(letzten|nächsten|diesen)\s+(montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag)', re.IGNORECASE),
                'month_pattern': re.compile(r'(letzten|nächsten|diesen)\s+monat\s+(\d{1,2})', re.IGNORECASE),
                'relative_map': {'letzten': -1, 'nächsten': 1, 'diesen': 0},
                'weekday_map': {'montag': 0, 'dienstag': 1, 'mittwoch': 2, 'donnerstag': 3, 'freitag': 4, 'samstag': 5, 'sonntag': 6}
            },
            'ja': {
                'week_pattern': re.compile(r'(先|来|今)週の?(月|火|水|木|金|土|日)曜日?'),
                'month_pattern': re.compile(r'(先|来|今)月(\d{1,2})日'),
                'relative_map': {'先': -1, '来': 1, '今': 0},
                'weekday_map': {'月': 0, '火': 1, '水': 2, '木': 3, '金': 4, '土': 5, '日': 6}
            },
            'ru': {
                'week_pattern': re.compile(r'(прошлый|следующий|этот)\s+(понедельник|вторник|среда|четверг|пятница|суббота|воскресенье)', re.IGNORECASE),
                'month_pattern': re.compile(r'(прошлый|следующий|этот)\s+месяц\s+(\d{1,2})', re.IGNORECASE),
                'relative_map': {'прошлый': -1, 'следующий': 1, 'этот': 0},
                'weekday_map': {'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3, 'пятница': 4, 'суббота': 5, 'воскресенье': 6}
            },
            'it': {
                'week_pattern': re.compile(r'(scorso|prossimo|questo)\s+(lunedì|martedì|mercoledì|giovedì|venerdì|sabato|domenica)', re.IGNORECASE),
                'month_pattern': re.compile(r'(scorso|prossimo|questo)\s+mese\s+(\d{1,2})', re.IGNORECASE),
                'relative_map': {'scorso': -1, 'prossimo': 1, 'questo': 0},
                'weekday_map': {'lunedì': 0, 'martedì': 1, 'mercoledì': 2, 'giovedì': 3, 'venerdì': 4, 'sabato': 5, 'domenica': 6}
            },
            'pt': {
                'week_pattern': re.compile(r'(passado|próximo|este)\s+(segunda|terça|quarta|quinta|sexta|sábado|domingo)', re.IGNORECASE),
                'month_pattern': re.compile(r'(passado|próximo|este)\s+mês\s+(\d{1,2})', re.IGNORECASE),
                'relative_map': {'passado': -1, 'próximo': 1, 'este': 0},
                'weekday_map': {'segunda': 0, 'terça': 1, 'quarta': 2, 'quinta': 3, 'sexta': 4, 'sábado': 5, 'domingo': 6}
            },
            'ko': {
                'week_pattern': re.compile(r'(지난|다음|이번)\s*주?\s*(월|화|수|목|금|토|일)요일'),
                'month_pattern': re.compile(r'(지난|다음|이번)\s*달\s*(\d{1,2})일'),
                'relative_map': {'지난': -1, '다음': 1, '이번': 0},
                'weekday_map': {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4, '토': 5, '일': 6}
            }
        }
        
        # 语言代码映射（处理各种变体）
        self.language_code_map = {
            'zh': ['zh', 'zh-cn', 'zh-hans', 'zh-tw', 'zh-hant'],
            'en': ['en', 'en-us', 'en-gb', 'en-au'],
            'es': ['es', 'es-es', 'es-mx', 'es-ar'],
            'fr': ['fr', 'fr-fr', 'fr-ca'],
            'de': ['de', 'de-de', 'de-at'],
            'it': ['it', 'it-it'],
            'pt': ['pt', 'pt-pt', 'pt-br'],
            'ru': ['ru', 'ru-ru'],
            'ja': ['ja', 'ja-jp'],
            'ko': ['ko', 'ko-kr']
        }
    
    def parse(self, date_string, base_time=None, language=None):
        """
        解析复合相对日期表达
        
        Args:
            date_string: 日期字符串
            base_time: 基准时间，默认为当前时间
            language: 语言代码，如果未指定则自动检测
            
        Returns:
            datetime对象或None
        """
        if base_time is None:
            base_time = datetime.now()
            
        # 如果指定了语言，直接使用
        if language:
            lang_key = self._get_language_key(language)
            if lang_key:
                return self._parse_with_language(date_string, base_time, lang_key)
        
        # 尝试所有支持的语言
        for lang_key in self.language_patterns:
            result = self._parse_with_language(date_string, base_time, lang_key)
            if result:
                return result
                
        return None
    
    def _get_language_key(self, language_code):
        """根据语言代码获取内部语言键"""
        language_code = language_code.lower()
        for lang_key, codes in self.language_code_map.items():
            if language_code in codes:
                return lang_key
        return None
    
    def _parse_with_language(self, date_string, base_time, lang_key):
        """使用指定语言解析日期字符串"""
        if lang_key not in self.language_patterns:
            return None
            
        lang_config = self.language_patterns[lang_key]
        relative_map = lang_config['relative_map']
        
        # 首先尝试匹配月份+日期模式
        if 'month_pattern' in lang_config:
            month_pattern = lang_config['month_pattern']
            match = month_pattern.match(date_string.strip())
            if match:
                relative_indicator = match.group(1).lower()
                day_str = match.group(2)
                
                # 获取相对月数
                month_offset = relative_map.get(relative_indicator)
                if month_offset is None:
                    return None
                
                # 解析日期数字
                day = self._parse_day_number(day_str, lang_key)
                if day is None or day < 1 or day > 31:
                    return None
                    
                # 计算目标月份日期
                return self._calculate_month_date(base_time, month_offset, day)
        
        # 然后尝试匹配星期模式
        week_pattern = lang_config.get('week_pattern') or lang_config.get('pattern')
        if week_pattern:
            weekday_map = lang_config['weekday_map']
            
            match = week_pattern.match(date_string.strip())
            if not match:
                return None
                
            relative_indicator = match.group(1).lower()
            weekday_name = match.group(2).lower()
            
            # 获取相对周数和目标星期
            week_offset = relative_map.get(relative_indicator)
            target_weekday = weekday_map.get(weekday_name)
            
            if week_offset is None or target_weekday is None:
                return None
                
            # 计算目标日期
            return self._calculate_target_date(base_time, week_offset, target_weekday)
        
        return None
    
    def _parse_day_number(self, day_str, lang_key):
        """
        解析日期数字，支持中文数字和阿拉伯数字
        
        Args:
            day_str: 日期字符串
            lang_key: 语言键
            
        Returns:
            int: 日期数字，失败返回None
        """
        # 尝试直接解析阿拉伯数字
        try:
            return int(day_str)
        except ValueError:
            pass
        
        # 对于中文，尝试从number_map解析
        if lang_key == 'zh' and 'number_map' in self.language_patterns[lang_key]:
            number_map = self.language_patterns[lang_key]['number_map']
            return number_map.get(day_str)
        
        return None

    def _calculate_month_date(self, base_time, month_offset, day):
        """
        计算目标月份的指定日期
        
        Args:
            base_time: 基准时间
            month_offset: 月份偏移量（-1=上月, 0=本月, 1=下月）
            day: 目标日期
            
        Returns:
            datetime对象
        """
        try:
            # 计算目标月份
            target_date = base_time + relativedelta(months=month_offset)
            
            # 设置目标日期，保持原有的时分秒
            target_date = target_date.replace(day=day)
            
            return target_date
        except ValueError:
            # 处理无效日期（如2月31日）
            # 尝试设置为该月的最后一天
            try:
                target_date = base_time + relativedelta(months=month_offset)
                target_date = target_date.replace(day=1) + relativedelta(months=1) - timedelta(days=1)
                # 如果目标日期小于等于该月最后一天，使用目标日期
                if day <= target_date.day:
                    target_date = target_date.replace(day=day)
                return target_date
            except:
                return None

    def _calculate_target_date(self, base_time, week_offset, target_weekday):
        """
        计算目标日期
        
        Args:
            base_time: 基准时间
            week_offset: 周偏移量（-1=上周, 0=本周, 1=下周）
            target_weekday: 目标星期几（0=周一, 6=周日）
            
        Returns:
            datetime对象
        """
        # 获取基准时间是星期几（0=周一, 6=周日）
        current_weekday = base_time.weekday()
        
        # 计算到本周目标星期几的天数差
        days_to_target = target_weekday - current_weekday
        
        # 加上周偏移量
        total_days_offset = days_to_target + (week_offset * 7)
        
        # 计算目标日期，保持原有的时分秒
        target_date = base_time + timedelta(days=total_days_offset)
        
        return target_date
    
    def is_applicable(self, date_string, language=None):
        """检查字符串是否适用于此解析器"""
        if language:
            lang_key = self._get_language_key(language)
            if lang_key and lang_key in self.language_patterns:
                lang_config = self.language_patterns[lang_key]
                # 检查月份模式
                if 'month_pattern' in lang_config and lang_config['month_pattern'].match(date_string.strip()):
                    return True
                # 检查星期模式
                week_pattern = lang_config.get('week_pattern') or lang_config.get('pattern')
                if week_pattern and week_pattern.match(date_string.strip()):
                    return True
                return False
        
        # 尝试所有支持的语言
        for lang_key in self.language_patterns:
            lang_config = self.language_patterns[lang_key]
            # 检查月份模式
            if 'month_pattern' in lang_config and lang_config['month_pattern'].match(date_string.strip()):
                return True
            # 检查星期模式
            week_pattern = lang_config.get('week_pattern') or lang_config.get('pattern')
            if week_pattern and week_pattern.match(date_string.strip()):
                return True
                
        return False


# 创建全局实例
compound_relative_parser = CompoundRelativeParser()


def parse_compound_relative_date(date_string, base_time=None, language=None):
    """
    解析复合相对日期的便捷函数
    
    Args:
        date_string: 日期字符串
        base_time: 基准时间
        language: 语言代码
        
    Returns:
        datetime对象或None
    """
    return compound_relative_parser.parse(date_string, base_time, language)


if __name__ == "__main__":
    # 测试代码
    from datetime import datetime
    
    base_time = datetime(2024, 1, 15, 10, 0, 0)  # 2024年1月15日(星期一)
    
    test_cases = [
        # 中文 - 星期
        ('上周五', 'zh'), ('下周三', 'zh'), ('本周二', 'zh'),
        # 中文 - 月份+日期
        ('上个月十七号', 'zh'), ('上个月17号', 'zh'), ('上月十七号', 'zh'), 
        ('下月二十二号', 'zh'), ('下个月二十二号', 'zh'),
        # 英文 - 星期
        ('last friday', 'en'), ('next monday', 'en'), ('this wednesday', 'en'),
        # 英文 - 月份+日期
        ('last month 17th', 'en'), ('next month 22nd', 'en'), ('this month 15th', 'en'),
        # 西班牙文
        ('pasado viernes', 'es'), ('próximo lunes', 'es'), ('pasado mes 17', 'es'),
        # 法文
        ('dernier vendredi', 'fr'), ('prochain lundi', 'fr'), ('dernier mois 17', 'fr'),
        # 德文
        ('letzten freitag', 'de'), ('nächsten montag', 'de'), ('letzten monat 17', 'de'),
        # 意大利文
        ('scorso venerdì', 'it'), ('prossimo lunedì', 'it'), ('scorso mese 17', 'it'),
        # 葡萄牙文
        ('passado sexta', 'pt'), ('próximo segunda', 'pt'), ('passado mês 17', 'pt'),
        # 俄文
        ('прошлый пятница', 'ru'), ('следующий понедельник', 'ru'), ('прошлый месяц 17', 'ru'),
        # 日文
        ('先週の金曜日', 'ja'), ('来週の月曜日', 'ja'), ('先月17日', 'ja'),
        # 韩文
        ('지난 주 금요일', 'ko'), ('다음 주 월요일', 'ko'), ('지난 달 17일', 'ko'),
    ]
    
    print('复合相对日期解析器测试:')
    print('=' * 60)
    for case, lang in test_cases:
        result = parse_compound_relative_date(case, base_time, lang)
        if result:
            weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][result.weekday()]
            print(f'{case:20} ({lang}) -> {result.strftime("%Y-%m-%d %H:%M:%S")} ({weekday})')
        else:
            print(f'{case:20} ({lang}) -> 解析失败')

