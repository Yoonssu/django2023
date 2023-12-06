#  검색한 단어 색깔 변화


from django import template
from django.utils.html import mark_safe
import re

register = template.Library()


@register.filter
def highlight(text, search):
    # search가 없을 경우 원래 텍스트를 반환
    if not search:
        return text

    # 정규 표현식을 사용하여 검색어를 강조
    highlighted_text = re.sub(f'({re.escape(search)})', r'<span style="color: red;">\1</span>', text, flags=re.IGNORECASE)
    return mark_safe(highlighted_text)

