from django import template

register=template.Library()

@register.filter(name='chunk')
def chunk(list_data,chunk_size):
    chunk=[]
    i=0
    for x in list_data:
        chunk.append(x)
        i+=1
        if i==chunk_size:
            yield chunk
            chunk=[]
            i=0
    if chunk:
        yield chunk