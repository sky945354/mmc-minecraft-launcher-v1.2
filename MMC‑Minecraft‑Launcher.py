import os
import json
import traceback

def main():
    from tkinter import Tk, ttk, messagebox, filedialog, Toplevel, Label, Menu

    APP_NAME = "MMC‑Minecraft‑Launcher"
    CONFIG_FILE = "config.json"
    CONFIG_TMP = "config.tmp.json"

    LANG_DATA = {
        "English": {
            "m_file": "File",
            "m_file_add_folder": "Add Versions Folder",
            "m_file_exit": "Exit",
            "m_action": "Action",
            "m_action_copy_id": "Copy Version ID",
            "m_action_open_dot_minecraft": "Open .minecraft Folder",
            "m_view": "View",
            "m_view_refresh": "Refresh List",
            "m_view_language": "Language(restart required)",
            "m_window": "Window",
            "m_window_reset_size": "Reset Window Size",
            "m_help": "Help",
            "m_help_about": "About",
            "about_text": f"{APP_NAME}\nSimple MC version viewer.\nVersion 1.2\nChange language needs restart app.",
            "detail_title": "Version Detail",
            "copy_success": "Version ID copied to clipboard",
            "no_select": "Please select an item",
            "col_version_id": "Version ID",
            "col_type": "Type",
            "col_jar": "Jar File",
            "col_size_kb": "Size(KB)",
            "folder_count_template": "{path} ({count} versions)"
        },
        "简体中文": {
            "m_file": "文件",
            "m_file_add_folder": "添加版本文件夹",
            "m_file_exit": "退出",
            "m_action": "操作",
            "m_action_copy_id": "复制选中版本ID",
            "m_action_open_dot_minecraft": "打开.minecraft目录",
            "m_view": "视图",
            "m_view_refresh": "刷新列表",
            "m_view_language": "语言(需要重启程序)",
            "m_window": "窗口",
            "m_window_reset_size": "重置窗口大小",
            "m_help": "帮助",
            "m_help_about": "关于",
            "about_text": f"{APP_NAME}\n简易Minecraft版本查看工具。\n版本 1.2\n切换语言需要重启程序生效",
            "detail_title": "版本详情",
            "copy_success": "版本ID已复制到剪贴板",
            "no_select": "请先选中条目",
            "col_version_id": "版本ID",
            "col_type": "类型",
            "col_jar": "Jar文件",
            "col_size_kb": "大小(KB)",
            "folder_count_template": "{path}（共{count}个版本）"
        },
        "繁體中文": {
            "m_file": "檔案",
            "m_file_add_folder": "新增版本資料夾",
            "m_file_exit": "離開",
            "m_action": "操作",
            "m_action_copy_id": "複製版本ID",
            "m_action_open_dot_minecraft": "打開.minecraft資料夾",
            "m_view": "檢視",
            "m_view_refresh": "重新整理清單",
            "m_view_language": "語言(需重啟程式)",
            "m_window": "視窗",
            "m_window_reset_size": "重置視窗大小",
            "m_help": "說明",
            "m_help_about": "關於",
            "about_text": f"{APP_NAME}\n簡易Minecraft版本檢視工具。\n版本1.2\n切換語言需要重啟程式",
            "detail_title": "版本詳細資訊",
            "copy_success": "版本ID已複製到剪貼簿",
            "no_select": "請先選擇項目",
            "col_version_id": "版本ID",
            "col_type": "類型",
            "col_jar": "Jar檔案",
            "col_size_kb": "大小(KB)",
            "folder_count_template": "{path}（共{count}個版本）"
        },
        "한국어": {
            "m_file": "파일",
            "m_file_add_folder": "버전 폴더 추가",
            "m_file_exit": "종료",
            "m_action": "동작",
            "m_action_copy_id": "버전 ID 복사",
            "m_action_open_dot_minecraft": ".minecraft 폴더 열기",
            "m_view": "보기",
            "m_view_refresh": "목록 새로고침",
            "m_view_language": "언어(재시작 필요)",
            "m_window": "창",
            "m_window_reset_size": "창 크기 초기화",
            "m_help": "도움말",
            "m_help_about": "정보",
            "about_text": f"{APP_NAME}\n간단한 MC 버전 뷰어.\n버전1.2\n언어 변경은 재시작 후 적용",
            "detail_title": "버전 상세",
            "copy_success": "버전 ID 복사 완료",
            "no_select": "항목을 선택하세요",
            "col_version_id": "버전ID",
            "col_type": "타입",
            "col_jar": "Jar파일",
            "col_size_kb": "크기(KB)",
            "folder_count_template": "{path} ({count}개 버전)"
        },
        "日本語": {
            "m_file": "ファイル",
            "m_file_add_folder": "バージョンフォルダ追加",
            "m_file_exit": "終了",
            "m_action": "操作",
            "m_action_copy_id": "バージョンIDコピー",
            "m_action_open_dot_minecraft": ".minecraftフォルダを開く",
            "m_view": "表示",
            "m_view_refresh": "リスト更新",
            "m_view_language": "言語(再起動必要)",
            "m_window": "ウィンドウ",
            "m_window_reset_size": "ウィンドウサイズリセット",
            "m_help": "ヘルプ",
            "m_help_about": "について",
            "about_text": f"{APP_NAME}\n簡易MCバージョン閲覧ツール。\nVersion1.2\n言語変更は再起動後有効",
            "detail_title": "バージョン詳細",
            "copy_success": "バージョンIDをクリップボードにコピー",
            "no_select": "項目を選択してください",
            "col_version_id": "バージョンID",
            "col_type": "タイプ",
            "col_jar": "Jarファイル",
            "col_size_kb": "サイズ(KB)",
            "folder_count_template": "{path} ({count}個のバージョン)"
        }
    }

    DEFAULT_CONFIG = {
        "language": "简体中文",
        "folders": []
    }

    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                for k in DEFAULT_CONFIG:
                    if k not in d:
                        d[k] = DEFAULT_CONFIG[k]
                return d
            except Exception:
                return dict(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    def save_config(cfg):
        with open(CONFIG_TMP, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        os.rename(CONFIG_TMP, CONFIG_FILE)

    def scan_versions(versions_folder):
        ver_list = []
        if not os.path.isdir(versions_folder):
            return ver_list
        try:
            all_entries = os.listdir(versions_folder)
            for name in all_entries:
                sub = os.path.join(versions_folder, name)
                if not os.path.isdir(sub):
                    continue
                json_candidate = None
                guess_json = os.path.join(sub, f"{name}.json")
                if os.path.exists(guess_json):
                    json_candidate = guess_json
                else:
                    for subfile in os.listdir(sub):
                        if subfile.lower().endswith(".json"):
                            json_candidate = os.path.join(sub, subfile)
                            break
                if json_candidate is None:
                    continue
                try:
                    with open(json_candidate, "r", encoding="utf-8") as f:
                        j = json.load(f)
                except Exception:
                    continue
                jar_path = os.path.join(sub, f"{name}.jar")
                jar_exists = os.path.exists(jar_path)
                jar_size_kb = round(os.path.getsize(jar_path)/1024,1) if jar_exists else 0
                ver_list.append({
                    "id": j.get("id", name),
                    "type": j.get("type", "unknown"),
                    "inheritsFrom": j.get("inheritsFrom", ""),
                    "assets": j.get("assets", ""),
                    "jar_exists": jar_exists,
                    "jar_kb": jar_size_kb,
                    "folder": versions_folder
                })
        except Exception:
            pass
        return ver_list

    class MainApp:
        def __init__(self, root):
            self.root = root
            self.cfg = load_config()
            self.lang_key = self.cfg["language"]
            lang = LANG_DATA[self.lang_key]
            self.root.title(APP_NAME)
            self.root.geometry("900x600")

            self.folder_list = self.cfg["folders"].copy()
            # 自动追加官方默认versions目录（不存在就跳过，不重复添加）
            default_ver_path = os.path.normpath(os.path.join(os.environ["APPDATA"], ".minecraft", "versions"))
            if os.path.isdir(default_ver_path) and default_ver_path not in self.folder_list:
                self.folder_list.append(default_ver_path)

            self.folder_ver_cache = dict()
            self.current_ver_data = []
            self.folder_id_map = dict()

            self.menu_bar = Menu(root)
            root.config(menu=self.menu_bar)

            self.m_file = Menu(self.menu_bar, tearoff=0)
            self.m_file.add_command(label=lang["m_file_add_folder"], command=self.add_folder)
            self.m_file.add_separator()
            self.m_file.add_command(label=lang["m_file_exit"], command=self.on_close)
            self.menu_bar.add_cascade(menu=self.m_file, label=lang["m_file"])

            self.m_action = Menu(self.menu_bar, tearoff=0)
            self.m_action.add_command(label=lang["m_action_copy_id"], command=self.copy_selected_version_id)
            self.m_action.add_command(label=lang["m_action_open_dot_minecraft"], command=self.open_dot_minecraft)
            self.menu_bar.add_cascade(menu=self.m_action, label=lang["m_action"])

            self.m_view = Menu(self.menu_bar, tearoff=0)
            self.m_view.add_command(label=lang["m_view_refresh"], command=self.full_refresh_all)
            self.m_view_lang_sub = Menu(self.m_view, tearoff=0)
            for lang_name in LANG_DATA.keys():
                self.m_view_lang_sub.add_command(label=lang_name, command=lambda ln=lang_name:self.set_language(ln))
            self.m_view.add_cascade(menu=self.m_view_lang_sub, label=lang["m_view_language"])
            self.menu_bar.add_cascade(menu=self.m_view, label=lang["m_view"])

            self.m_window = Menu(self.menu_bar, tearoff=0)
            self.m_window.add_command(label=lang["m_window_reset_size"], command=self.reset_window_size)
            self.menu_bar.add_cascade(menu=self.m_window, label=lang["m_window"])

            self.m_help = Menu(self.menu_bar, tearoff=0)
            self.m_help.add_command(label=lang["m_help_about"], command=self.show_about)
            self.menu_bar.add_cascade(menu=self.m_help, label=lang["m_help"])

            self.paned = ttk.PanedWindow(root, orient="horizontal")
            self.paned.pack(fill="both", expand=True, padx=4, pady=4)

            self.frame_left = ttk.Frame(self.paned)
            self.paned.add(self.frame_left, weight=1)
            self.tree_folder = ttk.Treeview(self.frame_left, show="tree")
            sb_left = ttk.Scrollbar(self.frame_left, orient="vertical", command=self.tree_folder.yview)
            self.tree_folder.configure(yscrollcommand=sb_left.set)
            self.tree_folder.pack(side="left", fill="both", expand=True)
            sb_left.pack(side="right", fill="y")
            self.tree_folder.bind("<<TreeviewSelect>>", self.on_folder_select)

            self.frame_right = ttk.Frame(self.paned)
            self.paned.add(self.frame_right, weight=3)
            self.tree_ver = ttk.Treeview(self.frame_right, columns=("vid","vtype","jarok","sizekb"), show="headings")
            sb_ver = ttk.Scrollbar(self.frame_right, orient="vertical", command=self.tree_ver.yview)
            self.tree_ver.configure(yscrollcommand=sb_ver.set)
            self.tree_ver.pack(side="left", fill="both", expand=True)
            sb_ver.pack(side="right", fill="y")
            self.tree_ver.bind("<Double-1>", self.on_version_double_click)

            self.tree_ver.heading("vid", text=lang["col_version_id"])
            self.tree_ver.heading("vtype", text=lang["col_type"])
            self.tree_ver.heading("jarok", text=lang["col_jar"])
            self.tree_ver.heading("sizekb", text=lang["col_size_kb"])
            self.tree_ver.column("vid", width=220)
            self.tree_ver.column("vtype", width=100)
            self.tree_ver.column("jarok", width=80)
            self.tree_ver.column("sizekb", width=80)

            self.refresh_folder_tree()
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        def get_text(self, key):
            return LANG_DATA[self.lang_key][key]

        def set_language(self, new_lang):
            self.cfg["language"] = new_lang
            save_config(self.cfg)
            messagebox.showinfo("提示", self.get_text("about_text"))

        def refresh_folder_tree(self):
            self.tree_folder.delete(*self.tree_folder.get_children())
            self.folder_ver_cache.clear()
            self.folder_id_map.clear()
            for idx, fp in enumerate(self.folder_list):
                verlist = scan_versions(fp)
                self.folder_ver_cache[fp] = verlist
                disp_text = self.get_text("folder_count_template").format(path=fp, count=len(verlist))
                node_id = f"f{idx}"
                self.folder_id_map[node_id] = fp
                self.tree_folder.insert("", "end", iid=node_id, text=disp_text)

        def on_folder_select(self, event):
            sel = self.tree_folder.selection()
            self.tree_ver.delete(*self.tree_ver.get_children())
            self.current_ver_data.clear()
            if not sel:
                return
            node_id = sel[0]
            folder_path = self.folder_id_map.get(node_id)
            if not folder_path:
                return
            verlist = self.folder_ver_cache.get(folder_path, [])
            self.current_ver_data = verlist
            for v_idx, v in enumerate(verlist):
                jar_txt = "OK" if v["jar_exists"] else "-"
                self.tree_ver.insert("", "end", iid=str(v_idx), values=(v["id"], v["type"], jar_txt, v["jar_kb"]))

        def add_folder(self):
            fp = filedialog.askdirectory(title=self.get_text("m_file_add_folder"))
            if not fp:
                return
            fp = os.path.normpath(fp)
            if fp not in self.folder_list:
                self.folder_list.append(fp)
                self.cfg["folders"] = self.folder_list
                save_config(self.cfg)
            self.refresh_folder_tree()

        def full_refresh_all(self):
            self.refresh_folder_tree()
            self.tree_ver.delete(*self.tree_ver.get_children())
            self.current_ver_data.clear()

        def copy_selected_version_id(self):
            sel = self.tree_ver.selection()
            if not sel:
                messagebox.showinfo("", self.get_text("no_select"))
                return
            idx = int(sel[0])
            v = self.current_ver_data[idx]
            self.root.clipboard_clear()
            self.root.clipboard_append(v["id"])
            messagebox.showinfo("", self.get_text("copy_success"))

        def open_dot_minecraft(self):
            dot_mc = os.path.join(os.environ["APPDATA"], ".minecraft")
            if os.path.isdir(dot_mc):
                os.startfile(dot_mc)

        def on_version_double_click(self, event):
            sel = self.tree_ver.selection()
            if not sel:
                return
            idx = int(sel[0])
            vdata = self.current_ver_data[idx]
            win = Toplevel(self.root)
            win.title(self.get_text("detail_title"))
            lines = [
                f'ID: {vdata["id"]}',
                f'Type: {vdata["type"]}',
                f'inheritsFrom: {vdata["inheritsFrom"]}',
                f'assets: {vdata["assets"]}',
                f'Jar exists: {vdata["jar_exists"]}',
                f'Jar size KB: {vdata["jar_kb"]}',
                f'Source folder: {vdata["folder"]}'
            ]
            Label(win, text="\n".join(lines), justify="left", padx=12, pady=12).pack()

        def reset_window_size(self):
            self.root.geometry("900x600")

        def show_about(self):
            messagebox.showinfo("", self.get_text("about_text"))

        def on_close(self):
            self.root.destroy()

    root = Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        err_msg = traceback.format_exc()
        from tkinter import Tk, messagebox
        temp_root = Tk()
        temp_root.withdraw()
        messagebox.showerror("程序异常", err_msg)
        temp_root.destroy()
