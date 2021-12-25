from gjf23D import gjf23D
import sys

if __name__=="__main__":
    args = sys.argv
    if len(args) != 2:
        print("check arg")
        exit()
    gjf23D(args[1])
