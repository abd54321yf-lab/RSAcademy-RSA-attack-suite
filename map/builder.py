"""Offset map representations for reports."""
def build_map(artifacts, source_size: int) -> list[dict]:
    cursor=0; ranges=[]
    for a in sorted(artifacts, key=lambda x:x.offset):
        if a.offset > cursor: ranges.append({'start': cursor, 'end': a.offset, 'kind': 'unmapped', 'size': a.offset-cursor})
        ranges.append({'start': a.offset, 'end': a.offset+a.size, 'kind': 'artifact', 'type': a.extension, 'size': a.size})
        cursor=max(cursor, a.offset+a.size)
    if cursor < source_size: ranges.append({'start': cursor, 'end': source_size, 'kind': 'unmapped', 'size': source_size-cursor})
    return ranges

def ascii_map(ranges, width=72) -> str:
    total=max((r['end'] for r in ranges), default=1)
    line=['.']*width
    for r in ranges:
        if r['kind']=='artifact':
            start=int(r['start']/total*width); end=max(start+1,int(r['end']/total*width))
            for i in range(min(width,end)): line[i]='#'
    return ''.join(line)
