filename = "/kikupico.log"
errorfilename = "/error.log"


def log(*args):
    data = " ".join([str(arg) for arg in args])
    fd = open(filename, "a")
    fd.write(data)
    print(data)
    fd.write("\n")
    fd.close()

def error(*args):
    data = " ".join([str(arg) for arg in args])
    fd = open(errorfilename, "a")
    fd.write(str(data))
    print(str(data))
    fd.write("\n")
    fd.close()
