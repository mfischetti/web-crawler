import sys

if __name__ == "__main__":
    if not sys.argv[1:]:
        print("Please input a starting URL.")
    else:
        print("Starting web crawling at URL: " + sys.argv[1])
        exit()