import schedule
import time
import shutil
import os
import subprocess

SOURCE = "/Users/sanadshalabi/Downloads/btcFreshData"
REPO   = "/Users/sanadshalabi/Downloads/btc-data"

def sync():
    try:
        if not os.path.exists(SOURCE):
            print(f"[{time.strftime('%H:%M:%S')}] Folder not found: {SOURCE}")
            return

        files = os.listdir(SOURCE)
        csvs  = [f for f in files if f.endswith('.csv')]

        if not csvs:
            print(f"[{time.strftime('%H:%M:%S')}] No CSV files in folder yet")
            return

        copied = 0
        for f in csvs:
            src = os.path.join(SOURCE, f)
            dst = os.path.join(REPO, f)
            shutil.copy2(src, dst)
            copied += 1

        subprocess.run(['git', '-C', REPO, 'add', '.'], check=True)
        subprocess.run(['git', '-C', REPO, 'commit', '-m',
                       f'auto {time.strftime("%Y-%m-%d %H:%M")}'], check=True)
        subprocess.run(['git', '-C', REPO, 'push'], check=True)
        print(f"[{time.strftime('%H:%M:%S')}] Pushed {copied} files ✓")

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")

print("=== BTC Data Sync Started ===")
print(f"Source: {SOURCE}")
print(f"Repo:   {REPO}")
print("Syncing now then every hour...")
print()
sync()
schedule.every().hour.do(sync)

while True:
    schedule.run_pending()
    time.sleep(60)
