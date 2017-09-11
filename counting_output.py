#!python3

import subprocess
import traceback
import sys

proc_out = {} #{string, int}

def reaction(line):
  return line


def each_line(line, porc):
  count = proc_out.get(line, 0)
  count = count + 1;
  proc_out[line] = count;

  print(repr(line))

  if proc != None:
    rline = reaction(line)
    if rline != None:
      proc.stdin.write(rline)

def counting_lines(proc):
  try:
    while True:
      line = proc.stdout.readline()
      if len(line) == 0:
        print("---proc exit---")
        return
      each_line(line, proc)
  except:
    print()
    print('---porc except---')
    traceback.print_exc()


def print_result():
  line_sum = sum([k for v,k in proc_out.items()])
  for k,v in sorted(proc_out.items(), key=lambda item: -item[1]):
    print(v, '\t', repr(k), sep='')
  print()
  print('total lines:', line_sum)

if __name__=='__main__':
  cmd = ['ls', '-al']
  if len(sys.argv) >= 2:
    cmd = sys.argv[1:]
  proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  counting_lines(proc)
  print()
  print('------')
  print_result()
