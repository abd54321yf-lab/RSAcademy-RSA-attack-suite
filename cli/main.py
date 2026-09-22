"""Command-line interface for RSAcademy."""
import argparse, json, logging, sys
from pathlib import Path
from rsa.pipeline import rsa_one, rsa_many, discover
VERSION='1.0.0'

def build_parser():
    p=argparse.ArgumentParser(prog='rsacademy',description='Educational digital-forensics file carving suite')
    p.add_argument('--version',action='version',version=VERSION); p.add_argument('--log-level',default='WARNING')
    sub=p.add_subparsers(dest='command',required=True)
    def common(x):
        x.add_argument('--output',default='results'); x.add_argument('--backend',choices=['python','yara'],default='python'); x.add_argument('--type',action='append',dest='types')
    c=sub.add_parser('carve',help='carve one file/image'); common(c); c.add_argument('input')
    b=sub.add_parser('batch',help='carve a directory'); common(b); b.add_argument('directory'); b.add_argument('--recursive',action='store_true'); b.add_argument('--pattern',action='append')
    l=sub.add_parser('carve-list',help='carve files listed one per line'); common(l); l.add_argument('list_file')
    r=sub.add_parser('run',help='run a JSON configuration'); r.add_argument('config')
    return p

def main(argv=None):
    args=build_parser().parse_args(argv); logging.basicConfig(level=args.log_level)
    try:
        if args.command=='carve': result=rsa_one(args.input,Path(args.output)/Path(args.input).stem,args.backend,args.types); print(json.dumps({'artifacts':len(result['artifacts']),'report':str(Path(args.output)/Path(args.input).stem/'report.html')}))
        elif args.command=='batch': result=rsa_many(discover(args.directory,args.pattern,args.recursive),args.output,args.backend,args.types); print(json.dumps(result,indent=2))
        elif args.command=='carve-list':
            paths=[Path(x.strip()) for x in Path(args.list_file).read_text().splitlines() if x.strip()]; print(json.dumps(rsa_many(paths,args.output,args.backend,args.types),indent=2))
        else:
            cfg=json.loads(Path(args.config).read_text()); paths=cfg.get('inputs',[]); print(json.dumps(rsa_many([Path(p) for p in paths],cfg.get('output','results'),cfg.get('backend','python'),cfg.get('types')),indent=2))
        return 0
    except Exception as exc:
        print(f'error: {exc}',file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
