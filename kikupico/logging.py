filename = "/kikupico.log"
errorfilename = "/error.log"


def log(data):
    fd = open(filename, "a")
    fd.write(data)
    print(data)
    fd.write("\n")
    fd.close()

def error(data):
    fd = open(errorfilename, "a")
    fd.write(str(data))
    print(str(data))
    fd.write("\n")
    fd.close()
