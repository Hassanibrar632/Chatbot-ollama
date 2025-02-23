import sys
import time

def main():
    if len(sys.argv) != 2:
        print("Usage: python delayed_script.py <sleep_time>")
        sys.exit(1)
    
    try:
        sleep_time = int(sys.argv[1])
        time.sleep(sleep_time)
        print("Hello, world!")
    except ValueError:
        print("Invalid sleep time. Please provide an integer.")
        sys.exit(1)

if __name__ == "__main__":
    main()