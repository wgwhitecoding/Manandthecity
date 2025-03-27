from django import template

register = template.Library()

@register.simple_tag
def render_replies(reply_list):
    output = ""
    for reply in reply_list:
        output += f"<div class='ms-4 mt-3 border-start ps-3'>{reply.body}</div>"
    return output

