import tkinter as tk
from tkinter import ttk
from src.user_info import UserInfo
import datetime


class PopUp:
    def __init__(self):
        self.start_time = "0900"  # 始業時間
        self.end_time = "1800"  # 終業時間

    # 画面を中央に配置する
    def centering_window(self, root: tk.Tk):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        x = screen_width / 2 - window_width / 2
        y = screen_height / 2 - window_height / 2
        root.geometry("+%d+%d" % (x, y))

    # 初期情報入力ポップアップ
    def init_info_entry(self, user_info: UserInfo) -> bool:
        global is_start
        is_start = False

        root = tk.Tk()
        root.title("初期情報入力")
        root.geometry("350x310")
        self.centering_window(root)

        # スタイル
        style = ttk.Style(root)
        # テーマ
        style.theme_use("default")

        # 通常時
        style.configure("Normal.TEntry", insertcolor="black")
        # エラー時のスタイル
        style.configure("Err.TEntry", fieldbackground="red")

        # 時間の入力制限
        def validate_time(
            P,
            S,
        ):
            if not S.encode("utf-8").isdigit() or len(P) >= 5:
                # 数字以外と5桁以上の入力を拒否
                return False
            return True

        validate_time_comd = root.register(validate_time)

        # ユーザー名
        user_entry = self.create_input_frame(root, "ユーザ名:", 10, 30, False)

        # パスワード
        password_entry = self.create_input_frame(root, "パスワード:", 5, 30, True)

        # 始業時間
        start_time_entry = self.create_input_frame(
            root, "始業時間(デフォルト 0900)", 30, 5, False
        )
        start_time_entry.config(
            validatecommand=(validate_time_comd, "%P", "%S"),
            validate="key",
        )

        # 終業時間
        end_time_entry = self.create_input_frame(
            root, "終業時間(デフォルト 1800)", 5, 5, False
        )
        end_time_entry.config(
            validatecommand=(validate_time_comd, "%P", "%S"),
            validate="key",
        )

        # 初期値設定
        start_time_entry.insert(0, self.start_time)
        end_time_entry.insert(0, self.end_time)

        def validate_confirm(entry: ttk.Entry, is_time: bool) -> bool:
            if is_time:
                # 時間のバリデーションチェック
                length = len(entry.get())
                if not (length == 0 or length == 4):
                    # 桁数が0または4以外の場合
                    return False
                elif length == 4:
                    try:
                        # datetimeに変換できれば正常
                        datetime.datetime.strptime(entry.get(), "%H%M")
                    except Exception:
                        return False
            else:
                if len(entry.get()) <= 0:
                    return False
            return True

        def confirm():
            global is_start
            validate_ok = True

            if validate_confirm(user_entry, False):
                user_entry.config(style="Normal.TEntry")
            else:
                user_entry.config(style="Err.TEntry")
                validate_ok = False
            if validate_confirm(password_entry, False):
                password_entry.config(style="Normal.TEntry")
            else:
                password_entry.config(style="Err.TEntry")
                validate_ok = False
            if validate_confirm(start_time_entry, True):
                start_time_entry.config(style="Normal.TEntry")
            else:
                start_time_entry.config(style="Err.TEntry")
                validate_ok = False
            if validate_confirm(end_time_entry, True):
                end_time_entry.config(style="Normal.TEntry")
            else:
                end_time_entry.config(style="Err.TEntry")
                validate_ok = False

            if validate_ok:
                user_info.set_info(
                    user_entry.get(),
                    password_entry.get(),
                    start_time_entry.get(),
                    end_time_entry.get(),
                )
                is_start = True
                root.destroy()

        def cancel():
            root.destroy()

        self.create_button_frame(root, "開始", confirm, "キャンセル", cancel)

        root.mainloop()

        return is_start

    def create_input_frame(
        self,
        root: tk.Tk,
        label: str,
        upper_gap: int,
        text_width: int,
        is_mask: bool,
    ):
        frame = tk.Frame(root)
        frame.pack(pady=(upper_gap, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        entry = ""
        if is_mask:
            # 入力時の文字列をマスキング
            entry = ttk.Entry(
                frame,
                show="*",
                width=text_width,
                style="Normal.TEntry",
            )
        else:
            entry = ttk.Entry(frame, width=text_width, style="Normal.TEntry")

        entry.pack(padx=30)
        return entry

    def create_button_frame(
        self,
        root: tk.Tk,
        confirm_text: str,
        confirm_func: any,
        cancel_text: str,
        cancel_func: any,
    ):
        frame = ttk.Frame(root)
        frame.pack(pady=(20, 5), anchor=tk.CENTER)
        confirm_button = ttk.Button(frame, text=confirm_text, command=confirm_func)
        confirm_button.pack(side=tk.LEFT)
        cancel_button = ttk.Button(frame, text=cancel_text, command=cancel_func)
        cancel_button.pack(side=tk.RIGHT)

    def err_pop(self, message: str):
        root = tk.Tk()
        root.geometry("200x100")
        root.title("エラー")
        self.centering_window(root)
        tk.Label(root, text=message, foreground="red").pack(
            anchor=tk.CENTER, expand=True
        )
        tk.Button(root, text="閉じる", command=lambda: root.destroy()).pack(pady=5)
        root.mainloop()

    def info_pop(self, message: str):
        root = tk.Tk()
        root.geometry("200x100")
        root.title("確認")
        self.centering_window(root)
        tk.Label(root, text=message).pack(anchor=tk.CENTER, expand=True)
        tk.Button(root, text="OK", command=lambda: root.destroy()).pack(pady=5)
        root.mainloop()
