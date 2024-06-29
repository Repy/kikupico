filename = "/kikupico.log"


def log(data):
    fd = open(filename, "a")
    fd.write(data)
    print(data)
    fd.write("\n")
    fd.close()
