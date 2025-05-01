import math

def something():
    result = 1
    return result


def main():
    result = 0
    
    for i in range(0, 10000):
        print(probe_state(result))
        result = something()
        print(probe_state(result))
        
    save_state() # where to save?


if __name__ == "__main__":
    main()