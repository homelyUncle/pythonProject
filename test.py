with open("setting.txt", "r") as setf:
        for line in setf:
            if line.startswith("addresses: "):
                print(line.split(": ")[1].rstrip("\n"))
