
"""This is the driver program for a scanner-parser-interpreter
   system
"""

try:
  import scan
  import parse
  import interpret

  # Read input program from terminal:  (You can also read it from a file,
  # but for the simple examples we will do, this works fine....)
  print("Type program; OK to do it on multiple lines; terminate with  !")
  print("  as the first symbol on a line by itself:")
  print()
  text = ""
  line = input("")
  while line[0] != "!" :
    text = text + " " + line
    line = input("")

  wordlist = scan.scan(text)
  print()
  print("scanned program:", wordlist)
  print()

  tree = parse.parse(wordlist)
  print("parsed program:", tree)
  print()

  print("execution:")
  interpret.interpretPTREE(tree)
except:  # in case of a run-time load- or execution-error:
  import traceback
  traceback.print_exc()   # print call stack and error message

print(input("press Enter key to finish"))


