import ps

inter = ps.Interpreter()
while True:
    code = input('>>> ')
    if code == "exit()":
        break
    print(inter.runLine(code))
