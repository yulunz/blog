from typing import Optional

import dataclasses
import datetime
import os
import pathlib
import re
import sys


TIME = re.compile(r'date:\s*(.*)\n')
TITLE = re.compile(r'title:\s*(.*)\n')
HIDE = re.compile(r'hide:\s*(true|false)\n')
IS_ZH_CN = re.compile(r'is_zh_cn:\s*(true|false)\n')


META_SPLITTER = '---'


@dataclasses.dataclass(frozen=True)
class Meta:
  title: str
  wrote_at: Optional[str] = None
  hide: Optional[bool] = None
  is_zh_cn: Optional[bool] = None


def make_title(text):
  i = j = 0
  seq = []
  is_cap_ct = 0
  while j < len(text):
    is_cap = text[j].isupper()
    if is_cap:
      if is_cap_ct == 0:
        seq.append(text[i:j].title())
        i = j
      is_cap_ct += 1
    else:
      if is_cap_ct > 1:
        seq.append(text[i:j])
        i = j
      is_cap_ct = 0

    j += 1

  final_part = text[i:j]
  if is_cap_ct <= 1:
    final_part = final_part.title()
  seq.append(final_part)
  return ''.join(seq)


def _gen_index(metas):
  blog_list = ['<ul class="blog-list">']
  by_date = sorted(metas.items(), key=lambda x: x[1].wrote_at, reverse=True)
  for href, meta in by_date:
    if meta is None or meta.hide is True:
      continue
    item = ['<li class="blog-item">']
    item.extend([f'<a href="{href}">', meta.title, '</a>'])
    if meta.wrote_at:
      item.extend(['<span>', meta.wrote_at, '</span>'])
    item.append('</li>')
    blog_list.extend(item)
  blog_list.append('</ul>')
  blog_list_content = '\n'.join(blog_list)

  return f"""\
<h1>The Responsible Adult</h1>
<i>A personal blog.</i>
<h2>Posts</h2>
{blog_list_content}
"""

def _extract_meta_field(pattern, content):
  match = re.search(pattern, content)
  if not match:
    return None

  field = match.group(1)
  if field == 'true':
    field = True
  elif field == 'false':
    field = False
  return field


def _parse(file_content):
  if META_SPLITTER not in file_content:
    return None, file_content

  meta_content, blog_content = file_content.split('---', maxsplit=1)

  wrote_at = _extract_meta_field(TIME, meta_content)
  title = _extract_meta_field(TITLE, meta_content)
  hide = _extract_meta_field(HIDE, meta_content)
  is_zh_cn = _extract_meta_field(IS_ZH_CN, meta_content)

  meta = Meta(
    wrote_at=wrote_at,
    title=make_title(title),
    hide=hide,
    is_zh_cn=is_zh_cn,
  )
  return meta, blog_content


def _add_title(blog_content, meta):
  if meta is None or meta.title is None:
    return blog_content

  titles = [f'<h1>{meta.title}</h1>']
  if meta.wrote_at:
    titles.append(f'<i>{meta.wrote_at}</i>')
  title_content = '\n'.join(titles)
  return f'{title_content}\n{blog_content}'


def _gen_html(blog_content, template, meta=None):
  page_title = 'The Responsible Adult'
  if meta and meta.title:
    page_title = f'{meta.title} | {page_title}'
  replacements = [
    ('{{content}}', blog_content),
    ('{{main_class}}', 'zh-cn' if meta and meta.is_zh_cn else ''),
    ('{{page_title}}', page_title),
    ('{{year}}', str(datetime.datetime.now().year)),
  ]
  for src, dst in replacements:
    template = template.replace(src, dst)
  return template


def _cp_statics(srcs, dst_dir):
  statics_dir = dst_dir / 'static'
  if not statics_dir.exists():
    statics_dir.mkdir()
  for src in srcs:
    dst = statics_dir / src.name
    dst.write_bytes(src.read_bytes())
    print(f'copied {src} to {dst}')


def main():
  cwd = pathlib.Path(os.getcwd())
  executable = cwd / pathlib.Path(sys.argv[0])
  base_dir = executable.parent / '..'

  out_dir = base_dir / 'out'
  if not out_dir.exists():
    out_dir.mkdir()
  if not out_dir.is_dir():
    print(f'{out_dir} must be a directory')
    os.exit(1)

  blog_dir = base_dir / 'blog'
  if not blog_dir.exists():
    print(f'cannot find blog directory at {blog_dir}')
    os.exit(1)

  template = (base_dir / 'assets' / 'template.html').read_text()

  metas = {}
  for blog_file in blog_dir.iterdir():
    if blog_file.suffix != '.html':
      print(f'[WARNING] skipping non-HTML file: {blog_file}')
      continue

    meta, blog_content = _parse(blog_file.read_text())
    metas[blog_file.name] = meta

    blog_content = _add_title(blog_content, meta)
    gen_content = _gen_html(blog_content, template, meta)
    gen_file = out_dir / blog_file.name
    gen_file.write_text(gen_content)  # Overrides existing.
    print(f'wrote {gen_file.resolve()}')

  index_content = _gen_index(metas)
  index_html = _gen_html(index_content, template)
  (out_dir / 'index.html').write_text(index_html)

  _cp_statics([
    base_dir / 'assets' / 'static' / 'blog.css',
    base_dir / 'assets' / 'static' / 'favicon.ico',
  ], out_dir)


if __name__ == '__main__':
  main()
