from django import template
register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.filter(name='addcss')
def addcss(field, css):
    list = [c.strip() for c in css.split(',')]
    return field.as_widget(attrs={"class":list[0],"placeholder":list[1],"rows":list[2]})
