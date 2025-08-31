#!/usr/bin/env python3
import sys, argparse, csv
from pathlib import Path

TEMPLATE = """\\begin{{table}}[t]
  \\centering
  \\resizebox{{\\textwidth}}{{!}}{{%
  \\begin{{tabular}}{{{cols}}}
    {header} \\\\
    \\hline
{rows}
  \\end{{tabular}}%
  }}
  \\caption{{{caption}}}
\\end{{table}}
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True, help='Input CSV file')
    ap.add_argument('--out', required=True, help='Output LaTeX file')
    ap.add_argument('--caption', default='Proof DAG with explicit, localized losses.')
    args = ap.parse_args()
    src = Path(args.csv)
    dst = Path(args.out)
    with src.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        if not fields:
            print(f"[FAIL] {src}: missing header")
            return 1
        cols_spec = 'l' * len(fields)
        header = ' & '.join(fields)
        
        def escape_text(s: str) -> str:
            # Escape LaTeX special chars for text-mode cells
            return (s.replace('\\', '\\textbackslash{}')
                     .replace('_', '\\_')
                     .replace('%', '\\%')
                     .replace('&', '\\&')
                     .replace('#', '\\#')
                     .replace('{', '\\{')
                     .replace('}', '\\}')
                     .replace('^', '\\^{}')
                     .replace('~', '\\~{}'))

        def format_math_loss(s: str) -> str:
            t = s.strip()
            t = t.replace('log_2', '\\log_{2}')
            t = t.replace('×', '\\times')
            t = t.replace('α', '\\alpha').replace('β', '\\beta')
            return f"${t}$"

        def format_parameters(s: str) -> str:
            t = s.strip()
            if t in {'—', '-', '–', ''}:
                return '\\textemdash{}'
            t = t.replace('α', '\\alpha').replace('β', '\\beta')
            return f"${t}$"

        row_lines = []
        for row in reader:
            vals_out = []
            for k in fields:
                v = row.get(k, '') or ''
                if k == 'LossForm':
                    vals_out.append(format_math_loss(v))
                elif k == 'Parameters':
                    vals_out.append(format_parameters(v))
                else:
                    vals_out.append(escape_text(v))
            row_lines.append('    ' + ' & '.join(vals_out) + ' \\\\')
        content = TEMPLATE.format(cols=cols_spec, header=header, rows='\n'.join(row_lines), caption=args.caption)
        dst.write_text(content, encoding='utf-8')
        print(f"[OK] wrote {dst} from {src}")
    return 0

if __name__ == '__main__':
    sys.exit(main())

