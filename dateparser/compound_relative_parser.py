"""
复合相对日期解析器
支持多语言的复合相对日期表达，如"上周五"、"last friday"、"next monday"等
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
                'pattern': re.compile(r'(上|下|本|这)周([一二三四五六日天])'),
                'relative_map': {'上': -1, '下': 1, '本': 0, '这': 0},
                'weekday_map': {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6}
            },
            'en': {
                'pattern': re.compile(r'(last|next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', re.IGNORECASE),
                'relative_map': {'last': -1, 'next': 1, 'this': 0},
                'weekday_map': {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
            },
            'es': {
                'pattern': re.compile(r'(pasado|próximo|este)\s+(lunes|martes|miércoles|jueves|viernes|sábado|domingo)', re.IGNORECASE),
                'relative_map': {'pasado': -1, 'próximo': 1, 'este': 0},
                'weekday_map': {'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6}
            },
            'fr': {
                'pattern': re.compile(r'(dernier|prochain|ce)\s+(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)', re.IGNORECASE),
                'relative_map': {'dernier': -1, 'prochain': 1, 'ce': 0},
                'weekday_map': {'lundi': 0, 'mardi': 1, 'mercredi': 2, 'jeudi': 3, 'vendredi': 4, 'samedi': 5, 'dimanche': 6}
            },
            'de': {
                'pattern': re.compile(r'(letzten|nächsten|diesen)\s+(montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag)', re.IGNORECASE),
                'relative_map': {'letzten': -1, 'nächsten': 1, 'diesen': 0},
                'weekday_map': {'montag': 0, 'dienstag': 1, 'mittwoch': 2, 'donnerstag': 3, 'freitag': 4, 'samstag': 5, 'sonntag': 6}
            },
            'ja': {
                'pattern': re.compile(r'(先|来|今)週の?(月|火|水|木|金|土|日)曜日?'),
                'relative_map': {'先': -1, '来': 1, '今': 0},
                'weekday_map': {'月': 0, '火': 1, '水': 2, '木': 3, '金': 4, '土': 5, '日': 6}
            },
            'ru': {
                'pattern': re.compile(r'(прошлый|следующий|этот)\s+(понедельник|вторник|среда|четверг|пятница|суббота|воскресенье)', re.IGNORECASE),
                'relative_map': {'прошлый': -1, 'следующий': 1, 'этот': 0},
                'weekday_map': {'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3, 'пятница': 4, 'суббота': 5, 'воскресенье': 6}
            },
            'it': {
                'pattern': re.compile(r'(scorso|prossimo|questo)\s+(lunedì|martedì|mercoledì|giovedì|venerdì|sabato|domenica)', re.IGNORECASE),
                'relative_map': {'scorso': -1, 'prossimo': 1, 'questo': 0},
                'weekday_map': {'lunedì': 0, 'martedì': 1, 'mercoledì': 2, 'giovedì': 3, 'venerdì': 4, 'sabato': 5, 'domenica': 6}
            },
            'pt': {
                'pattern': re.compile(r'(passado|próximo|este)\s+(segunda|terça|quarta|quinta|sexta|sábado|domingo)', re.IGNORECASE),
                'relative_map': {'passado': -1, 'próximo': 1, 'este': 0},
                'weekday_map': {'segunda': 0, 'terça': 1, 'quarta': 2, 'quinta': 3, 'sexta': 4, 'sábado': 5, 'domingo': 6}
            },
            'ko': {
                'pattern': re.compile(r'(지난|다음|이번)\s*주?\s*(월|화|수|목|금|토|일)요일'),
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
        pattern = lang_config['pattern']
        relative_map = lang_config['relative_map']
        weekday_map = lang_config['weekday_map']
        
        match = pattern.match(date_string.strip())
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
                return bool(self.language_patterns[lang_key]['pattern'].match(date_string.strip()))
        
        # 尝试所有支持的语言
        for lang_key in self.language_patterns:
            if self.language_patterns[lang_key]['pattern'].match(date_string.strip()):
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
        # 中文
        ('上周五', 'zh'), ('下周三', 'zh'), ('本周二', 'zh'),
        # 英文
        ('last friday', 'en'), ('next monday', 'en'), ('this wednesday', 'en'),
        # 西班牙文
        ('pasado viernes', 'es'), ('próximo lunes', 'es'),
        # 法文
        ('dernier vendredi', 'fr'), ('prochain lundi', 'fr'),
        # 德文
        ('letzten freitag', 'de'), ('nächsten montag', 'de'),
        # 意大利文
        ('scorso venerdì', 'it'), ('prossimo lunedì', 'it'),
        # 葡萄牙文
        ('passado sexta', 'pt'), ('próximo segunda', 'pt'),
        # 俄文
        ('прошлый пятница', 'ru'), ('следующий понедельник', 'ru'),
        # 日文
        ('先週の金曜日', 'ja'), ('来週の月曜日', 'ja'),
        # 韩文
        ('지난 주 금요일', 'ko'), ('다음 주 월요일', 'ko'),
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

