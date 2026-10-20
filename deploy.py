"""Automated deployment script to push Garmin Connect Track to GitHub Pages."""

import os
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_interactive(cmd_list):
    """Run command interactively so Git Credential Manager and terminal prompts work seamlessly."""
    print(f"\n>> {' '.join(cmd_list)}")
    try:
        res = subprocess.run(cmd_list)
        return res.returncode
    except Exception as e:
        print(f"[執行異常]: {e}")
        return 1


def main():
    repo_dir = Path(__file__).resolve().parent
    os.chdir(repo_dir)

    print("=" * 65)
    print("🚀 Garmin Connect Track - GitHub Pages 自動推送工具 (互動模式)")
    print(f"📁 工作目錄: {repo_dir}")
    print("🎯 目標儲存庫: https://github.com/SinLiongToo/GARMIN_CONNET_TRACK.git")
    print("=" * 65)

    # 1. Check Git
    try:
        subprocess.run(["git", "--version"], check=True)
    except Exception:
        print("\n❌ 錯誤：系統找不到 git 指令，請確認已安裝 Git for Windows。")
        input("\n請按 Enter 鍵結束...")
        return

    # 2. Init Git Repo
    if not (repo_dir / ".git").exists():
        print("\n[1/5] 初始化本地 Git 儲存庫...")
        run_interactive(["git", "init", "-b", "main"])
    else:
        print("\n[1/5] 確保本地處於 main 分支...")
        run_interactive(["git", "branch", "-M", "main"])

    # 3. Configure Remote
    print("\n[2/5] 設定遠端儲存庫 Origin...")
    run_interactive(["git", "remote", "remove", "origin"])
    run_interactive(["git", "remote", "add", "origin", "https://github.com/SinLiongToo/GARMIN_CONNET_TRACK.git"])
    run_interactive(["git", "remote", "-v"])

    # 4. Stage Files
    print("\n[3/5] 加入儀表板、金句系列與 GitHub Pages 檔案 (安全排除帳密與 Token)...")
    run_interactive([
        "git", "add",
        "index.html",
        "garmin_health_dashboard.html",
        "sport_english.html",
        ".github",
        "README.md",
        ".gitignore",
        "requirements.txt",
        "deploy.py",
        "deploy.bat"
    ])

    # 5. Commit
    print("\n[4/5] 建立提交 (Commit)...")
    run_interactive(["git", "commit", "-m", "feat: deploy Garmin Health Dashboard, Athlete Quotes and Sport English"])

    # 6. Push
    print("\n[5/5] 推送到 GitHub (main 分支)...")
    print("💡 提示：若彈出 GitHub 登入視窗，請點擊『Sign in with your browser』完成授權。")
    code = run_interactive(["git", "push", "-u", "origin", "main"])
    if code != 0:
        print("\n⚠️ 一般推送未成功（可能遠端已有初始檔案或衝突），嘗試強制同步 (force push)...")
        code = run_interactive(["git", "push", "-u", "origin", "main", "--force"])

    print("\n" + "=" * 65)
    if code == 0:
        print("✅ 推送大功告成！所有檔案已成功發佈至 GitHub！")
        print("🌐 您的 GitHub Pages 網址:")
        print("   👉 https://sinliongtoo.github.io/GARMIN_CONNET_TRACK/")
        print("   (GitHub Actions 會在 1~2 分鐘內自動發佈完成，重新整理即可查看)")
    else:
        print(f"❌ 推送未完成 (錯誤代碼: {code})。")
        print("請查看上方終端機顯示的具體錯誤訊息。")
    print("=" * 65)
    input("\n請按 Enter 鍵結束...")


if __name__ == "__main__":
    main()
