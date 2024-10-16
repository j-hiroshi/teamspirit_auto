import tkinter as tk
from tkinter import ttk
from src.user_info import UserInfo
import datetime


class PopUp:
    def __init__(self):
        self._start_time = "0900"  # 始業時間
        self._end_time = "1800"  # 終業時間
        self._start_date = "1"  # 開始日
        self._end_date = "31"  # 終了日

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

        # ユーザー名の枠作成
        user_frame = tk.Frame(root)
        user_frame.pack(pady=(10, 0))
        tk.Label(user_frame, text="ユーザ名:").pack(anchor=tk.W)
        user_entry = ttk.Entry(user_frame, width=30, style="Normal.TEntry")
        user_entry.pack(padx=30)

        # パスワードの枠作成
        password_frame = tk.Frame(root)
        password_frame.pack(pady=(5, 0))
        tk.Label(password_frame, text="パスワード:").pack(anchor=tk.W)
        password_entry = ttk.Entry(
            password_frame,
            show="*",
            width=30,
            style="Normal.TEntry",
        )
        password_entry.pack(padx=30)

        # 始業時間、終業時間の枠作成
        time_frame = tk.Frame(root)
        time_frame.pack(pady=(30, 0))
        tk.Label(time_frame, text="始業時間：終業時間").pack()
        start_time_entry = ttk.Entry(time_frame, width=5, style="Normal.TEntry")
        start_time_entry.pack(padx=5, side=tk.LEFT)
        end_time_entry = ttk.Entry(time_frame, width=5, style="Normal.TEntry")
        end_time_entry.pack(padx=5, side=tk.LEFT)

        # 入力制限設定
        start_time_entry.config(
            validatecommand=(validate_time_comd, "%P", "%S"),
            validate="key",
        )
        end_time_entry.config(
            validatecommand=(validate_time_comd, "%P", "%S"),
            validate="key",
        )

        # 開始日、終了日の枠作成
        date_frame = tk.Frame(root)
        date_frame.pack(pady=(10, 0))
        tk.Label(date_frame, text="開始日：終了日").pack()
        start_date_comb = ttk.Combobox(
            date_frame, values=list(range(1, 32)), width=4, state="readonly"
        )
        start_date_comb.pack(padx=5, side=tk.LEFT)
        end_date_comb = ttk.Combobox(
            date_frame, values=list(range(1, 32)), width=4, state="readonly"
        )
        end_date_comb.pack(padx=5, side=tk.LEFT)

        # 初期値設定
        start_time_entry.insert(0, self._start_time)
        end_time_entry.insert(0, self._end_time)
        start_date_comb.set(self._start_date)
        end_date_comb.set(self._end_date)

        # 開始時のバリデーション
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
                    start_date_comb.get().zfill(2),
                    end_date_comb.get().zfill(2),
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
