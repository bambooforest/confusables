#!/usr/bin/env python3

import os


def gen_confusables_table(f, cf):
  confusables = {}

  max_tgt_size = 0

  for line in cf:
    line = line.decode('utf-8').lstrip('\ufeff')

    try:
      i = line.index('#')
    except ValueError:
      pass
    else:
      line = line[:i]

    line = line.strip()
    if not line:
      continue

    src, tgt, _ = line.split(' ;\t')

    src = int(src, 16)
    tgt = tuple(int(t, 16) for t in tgt.split(' '))

    confusables[src] = tgt
    max_tgt_size = max(len(tgt), max_tgt_size)

  f.write("""#include <stdint.h>

static uint32_t const CONFUSABLES[][{}] = {{
""".format(max_tgt_size + 1))

  for i in range(max(confusables.keys()) + 1):
    confusable = confusables.get(i, ())
    f.write("    {{{}}},\n".format(", ".join("0x{:x}".format(t)
                                             for t in confusable + (0,))))

  f.write("};\n")