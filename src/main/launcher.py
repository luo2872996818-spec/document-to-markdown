# 启动打包后的 Streamlit 应用并自动打开浏览器
import multiprocessing
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path
from urllib.request import urlopen

APP_URL = "http://localhost:8501"
HEALTH_URL = f"{APP_URL}/_stcore/health"


def isFrozenApplication() -> bool:
    """判断当前程序是否由 PyInstaller 打包运行。"""
    return bool(getattr(sys, "frozen", False))


def getResourceRoot() -> Path:
    """返回应用代码和静态资源所在目录。"""
    if isFrozenApplication():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parents[2]


def getApplicationHome() -> Path:
    """返回保存输出文件和报告的目录。"""
    if isFrozenApplication():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def getApplicationPath() -> Path:
    """返回需要交给 Streamlit 运行的页面文件。"""
    resourceRoot = getResourceRoot()
    if isFrozenApplication():
        return resourceRoot / "app" / "main" / "app.py"
    return resourceRoot / "src" / "main" / "app.py"


def isServiceRunning() -> bool:
    """检查本地工具是否已经启动。"""
    try:
        with urlopen(HEALTH_URL, timeout=0.8) as response:
            return response.status == 200
    except Exception:
        return False


def openBrowserWhenReady() -> None:
    """等待服务就绪后自动打开默认浏览器。"""
    for _ in range(40):
        if isServiceRunning():
            webbrowser.open(APP_URL)
            return
        time.sleep(0.5)


def main() -> None:
    """配置环境并启动 Streamlit 服务。"""
    multiprocessing.freeze_support()
    resourceRoot = getResourceRoot()
    if str(resourceRoot) not in sys.path:
        sys.path.insert(0, str(resourceRoot))

    if "--self-test" in sys.argv:
        from src.main.selftest import runSelfTest

        raise SystemExit(runSelfTest())

    applicationHome = getApplicationHome()
    applicationPath = getApplicationPath()
    if not applicationPath.is_file():
        raise FileNotFoundError(f"找不到应用页面：{applicationPath}")

    os.environ["DOCUMENT_TO_MARKDOWN_HOME"] = str(applicationHome)
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
    os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"

    # 服务已经运行时只打开页面，不重复占用端口
    if isServiceRunning():
        webbrowser.open(APP_URL)
        return

    threading.Thread(target=openBrowserWhenReady, daemon=True).start()
    from streamlit.web import cli as streamlitCli

    sys.argv = [
        "streamlit",
        "run",
        str(applicationPath),
        "--server.address",
        "127.0.0.1",
        "--server.port",
        "8501",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
        "--global.developmentMode",
        "false",
    ]
    streamlitCli.main()


if __name__ == "__main__":
    main()