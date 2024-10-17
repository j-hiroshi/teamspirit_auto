from time import sleep
from src.pop_up import PopUp
from src.user_info import UserInfo
from src.browser_operation import BrowserOperation
import traceback

LOGIN_URL = "https://teamspirit-7491.my.salesforce.com/"
WORK_SCHEDULE_URL = (
    "https://teamspirit-7491.lightning.force.com/lightning/n/teamspirit__AtkWorkTimeTab"
)


def main():
    pop_up = PopUp()
    user_info = UserInfo()

    isStart = pop_up.init_info_entry(user_info)
    print("定時：{}~{}".format(pop_up._start_time, pop_up._end_time))
    print(("入力日付：{}~{}".format(pop_up._start_date, pop_up._end_date)))

    if not isStart:
        return

    browser = BrowserOperation()
    try:
        browser.pageMove(LOGIN_URL)
        browser.login(user_info.username, user_info.password)
        print("ログイン成功")
    except Exception as e:
        print(traceback.format_exc())
        pop_up.err_pop("ログインに失敗しました。")
        browser.session_clear()
        return

    try:
        browser.pageMove(WORK_SCHEDULE_URL)
        sleep(5)
        browser.work_entry(
            user_info.start_time,
            user_info.end_time,
            user_info.start_date,
            user_info.end_date,
        )
        pop_up.info_pop("処理完了")
    except Exception as e:
        print(e)
        pop_up.err_pop("勤怠入力でエラーが発生しました。")

    browser.session_clear()


if __name__ == "__main__":
    main()
