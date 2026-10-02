import time
import sys
from attacks.escape_attack import run_escape_simulation

def main():
    print("==================================================")
    print("       SPECTRE-AGENT: Adversary Simulator        ")
    print("==================================================")
    print("[+] Agent initialized. Waiting for trigger cycles...")

    while True:
        try:
            print("\n[>] Executing attack cycle...")
            run_escape_simulation()
            print("[+] Attack cycle completed. Sleeping for 30 seconds...")
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n[-] Stopping adversary simulator.")
            sys.exit(0)
        except Exception as e:
            print(f"[-] Attack execution error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()