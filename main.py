import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk



class UltimateAgroApp:

    def __init__(self, root):
        self.root = root
        self.root.title("AgroAssistant Pro — Робоче місце агронома")
        self.root.geometry("900x750")  # Трохи розширили вікно для статистики
        self.root.configure(bg="#F4F6F4")

        # Налаштування стилів та великих шрифтів
        self.setup_styles()

        # Початкові базові дані полів
        self.fields_data = {
            1: ["Поле 'За Річкою'", "Пшениця", 50.0],
            2: ["Поле 'Біля Шосе'", "Соняшник", 35.0],
            3: ["Поле 'Центральне'", "Оранка (Вільне)", 120.0],
            4: ["Поле 'Пагорб'", "Кукурудза", 40.0],
            5: ["Поле 'Долина'", "Ріпак", 60.0],
            6: ["Поле 'Східне'", "Оранка (Вільне)", 25.0],
        }

        # Головне меню (Вкладки)
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(expand=True, fill="both", padx=15, pady=15)

        self.tab_map = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.tab_calc = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.tab_weather = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.tab_help = ttk.Frame(self.notebook, style="Custom.TFrame")

        self.notebook.add(self.tab_map, text="🗺️ Карта полів")
        self.notebook.add(self.tab_calc, text="🧮 Агро-Калькулятори")
        self.notebook.add(self.tab_weather, text="☀️ Оптимальна погода")
        self.notebook.add(self.tab_help, text="📖 Як користуватись")

        self.build_map_tab()
        self.build_calc_tab()
        self.build_weather_tab()
        self.build_help_tab()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TFrame", background="#F4F6F4")
        style.configure(
            "Custom.TNotebook", background="#E2E8E2", borderwidth=0
        )

        # Текст вкладок меню
        style.configure(
            "Custom.TNotebook.Tab",
            background="#D2DED2",
            foreground="#2C3E2C",
            padding=[15, 8],
            font=("Arial", 12, "bold"),
        )
        style.map(
            "Custom.TNotebook.Tab", background=[("selected", "#F4F6F4")]
        )

        # Заголовки
        style.configure(
            "Title.TLabel",
            background="#F4F6F4",
            foreground="#2C3E2C",
            font=("Arial", 16, "bold"),
        )

        # Звичайний текст
        style.configure(
            "Text.TLabel",
            background="#F4F6F4",
            foreground="#4A554A",
            font=("Arial", 13),
        )

        # Кнопки калькулятора
        style.configure(
            "Calc.TButton",
            font=("Arial", 11, "bold"),
            background="#A3C1AD",
            foreground="#2C3E2C",
        )

        # Шрифти для таблиці погоди
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=30)

        self.culture_colors = {
            "Оранка (Вільне)": "#E6D7C3",
            "Пшениця": "#C2D9C2",
            "Соняшник": "#FAE19C",
            "Кукурудза": "#F5C293",
            "Ріпак": "#E8E8A6",
        }

    # ================= РОБОТА З ФАЙЛАМИ =================
    def save_data_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Файли JSON", "*.json"), ("Усі файли", "*.*")],
            title="Зберегти звіт про поля як...",
            initialfile="Мої_Поля_Господарства.json",
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.fields_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo(
                    "Успіх",
                    f"Дані успішно збережено у файл:\n{os.path.basename(file_path)}",
                )
            except Exception as e:
                messagebox.showerror(
                    "Помилка", f"Не вдалося зберегти дані: {str(e)}"
                )

    def load_data_from(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Файли JSON", "*.json"), ("Усі файли", "*.*")],
            title="Оберіть збережений файл полів",
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    self.fields_data = {int(k): v for k, v in raw_data.items()}
                self.update_map_and_stats()
                messagebox.showinfo(
                    "Успіх",
                    f"Дані з файлу '{os.path.basename(file_path)}' успішно завантажені!",
                )
            except Exception as e:
                messagebox.showerror(
                    "Помилка", f"Не вдалося прочитати файл:\n{str(e)}"
                )

    def reset_all_fields(self):
        """Нова функція: Скидає всі поля в статус Оранка"""
        if messagebox.askyesno(
            "Підтвердження",
            "Ви впевнені, що хочете очистити карту? ВСІ поля будуть переведені в статус 'Оранка (Вільне)'.",
        ):
            for f_id in self.fields_data:
                self.fields_data[f_id][1] = "Оранка (Вільне)"
            self.update_map_and_stats()

    def update_map_and_stats(self):
        """Оновлює сітку полів та блок статистики одночасно"""
        self.draw_field_grid()
        self.calculate_statistics()

    # ================= ВКЛАДКА 1: КАРТА ПОЛІВ =================
    def build_map_tab(self):
        top_bar = ttk.Frame(self.tab_map, style="Custom.TFrame")
        top_bar.pack(fill="x", pady=10)

        lbl = ttk.Label(
            top_bar,
            text="Інтерактивна схема господарства",
            style="Title.TLabel",
        )
        lbl.pack(side="left", padx=10, pady=5)

        # Червона кнопка скидання (НОВА)
        btn_reset = tk.Button(
            top_bar,
            text="🔄 СКИНУТИ ВСЕ",
            bg="#D32F2F",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=5,
            activebackground="#9A0007",
            activeforeground="white",
            cursor="hand2",
            command=self.reset_all_fields,
        )
        btn_reset.pack(side="right", padx=10)

        # Синя кнопка завантаження
        btn_load = tk.Button(
            top_bar,
            text="📥 ВІДКРИТИ З ПК",
            bg="#0288D1",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=5,
            activebackground="#01579B",
            activeforeground="white",
            cursor="hand2",
            command=self.load_data_from,
        )
        btn_load.pack(side="right", padx=10)

        # Зелена кнопка збереження
        btn_save = tk.Button(
            top_bar,
            text="💾 ЗБЕРЕГТИ ЯК...",
            bg="#2E7D32",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=5,
            activebackground="#1B5E20",
            activeforeground="white",
            cursor="hand2",
            command=self.save_data_as,
        )
        btn_save.pack(side="right", padx=10)

        # Сітка полів
        self.grid_frame = ttk.Frame(self.tab_map, style="Custom.TFrame")
        self.grid_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Легенда кольорів
        self.legend_frame = ttk.LabelFrame(
            self.tab_map, text=" Що означають кольори "
        )
        self.legend_frame.pack(fill="x", padx=15, pady=5)
        self.draw_legend()

        # БЛОК СТАТИСТИКИ ТА АНАЛІТИКИ (НОВИЙ)
        self.stats_frame = ttk.LabelFrame(
            self.tab_map, text=" 📊 Звіт по культурах (Аналітика) "
        )
        self.stats_frame.pack(fill="x", padx=15, pady=10)
        self.lbl_stats_text = ttk.Label(
            self.stats_frame,
            text="",
            font=("Arial", 11, "bold"),
            foreground="#2C3E2C",
        )
        self.lbl_stats_text.pack(padx=15, pady=10)

        # Первинне малювання елементів
        self.update_map_and_stats()

    def draw_field_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for f_id, data in self.fields_data.items():
            name, culture, area = data
            bg_color = self.culture_colors.get(culture, "#FFFFFF")

            btn_text = f"{name}\n\n🌾 {culture}\n📐 {area} га"

            btn = tk.Button(
                self.grid_frame,
                text=btn_text,
                bg=bg_color,
                fg="#2C3E2C",
                font=("Arial", 11, "bold"),
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground="#BDCBD0",
                command=lambda id=f_id: self.click_field(id),
            )

            row = (f_id - 1) // 3
            col = (f_id - 1) % 3
            btn.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

            self.grid_frame.grid_columnconfigure(col, weight=1)
            self.grid_frame.grid_rowconfigure(row, weight=1)

    def draw_legend(self):
        for cult, color in self.culture_colors.items():
            frame = ttk.Frame(self.legend_frame)
            frame.pack(side="left", padx=10, pady=5)

            color_spot = tk.Label(frame, bg=color, width=3, relief="flat")
            color_spot.pack(side="left")

            lbl_text = ttk.Label(
                frame, text=f" — {cult}", font=("Arial", 10, "italic")
            )
            lbl_text.pack(side="left", padx=2)

    def calculate_statistics(self):
        """Нова функція: Рахує сумарну площу під кожну культуру"""
        total_area = 0
        culture_sums = {cult: 0.0 for cult in self.culture_colors}

        for data in self.fields_data.values():
            _, culture, area = data
            total_area += area
            if culture in culture_sums:
                culture_sums[culture] += area

        # Формуємо текст звіту
        stats_string = f"Загальна площа земель: {total_area} га  |  "
        details = []
        for cult, s in culture_sums.items():
            if s > 0:
                details.append(f"{cult}: {s} га")

        stats_string += " • ".join(details)
        self.lbl_stats_text.config(text=stats_string)

    def click_field(self, field_id):
        name, current_cult, area = self.fields_data[field_id]

        win = tk.Toplevel(self.root)
        win.title(f"Керування: {name}")
        win.geometry("380x250")
        win.configure(bg="#F4F6F4")
        win.grab_set()

        tk.Label(
            win,
            text=name,
            font=("Arial", 13, "bold"),
            bg="#F4F6F4",
            fg="#2C3E2C",
        ).pack(pady=10)
        tk.Label(
            win,
            text=f"Поточна культура: {current_cult}",
            font=("Arial", 11),
            bg="#F4F6F4",
            fg="#4A554A",
        ).pack(pady=5)
        tk.Label(
            win,
            text="Змінити культуру на:",
            font=("Arial", 11),
            bg="#F4F6F4",
            fg="#4A554A",
        ).pack(pady=5)

        cb = ttk.Combobox(
            win,
            values=list(self.culture_colors.keys()),
            state="readonly",
            font=("Arial", 11),
        )
        cb.set(current_cult)
        cb.pack(pady=5)

        def save():
            self.fields_data[field_id][1] = cb.get()
            self.update_map_and_stats()  # Оновлюємо і карту, і аналітику внизу
            win.destroy()

        tk.Button(
            win,
            text="Оновити культуру",
            font=("Arial", 11, "bold"),
            bg="#A3C1AD",
            command=save,
            relief="groove",
        ).pack(pady=15)

    # ================= ВКЛАДКА 2: АГРО-КАЛЬКУЛЯТОРИ =================
    def build_calc_tab(self):
        # Робимо два блоки калькуляторів через LabelFrame

        # БЛОК 1: Калькулятор добрив
        frame_fert = ttk.LabelFrame(self.tab_calc, text=" 🧮 1. Розрахунок добрив ")
        frame_fert.pack(fill="x", padx=20, pady=10)

        ttk.Label(
            frame_fert, text="Площа поля (га):", font=("Arial", 11)
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.entry_area = ttk.Entry(frame_fert, font=("Arial", 11), width=10)
        self.entry_area.grid(row=0, column=1, padx=15, pady=10)

        ttk.Label(
            frame_fert, text="Норма внесення (кг/га):", font=("Arial", 11)
        ).grid(row=0, column=2, padx=15, pady=10, sticky="w")
        self.entry_rate = ttk.Entry(frame_fert, font=("Arial", 11), width=10)
        self.entry_rate.grid(row=0, column=3, padx=15, pady=10)

        btn_fert = ttk.Button(
            frame_fert, text="Порахувати добрива", command=self.calc_fert
        )
        btn_fert.grid(row=1, column=0, columnspan=2, padx=15, pady=10)

        self.lbl_res_fert = ttk.Label(
            frame_fert,
            text="Разом потрібно: 0 кг",
            font=("Arial", 11, "bold"),
            foreground="#2E5A2E",
        )
        self.lbl_res_fert.grid(row=1, column=2, columnspan=2, padx=15, pady=10)

        # БЛОК 2: Калькулятор насіння (НОВИЙ)
        frame_seed = ttk.LabelFrame(
            self.tab_calc, text=" 🌱 2. Розрахунок норми висіву насіння "
        )
        frame_seed.pack(fill="x", padx=20, pady=15)

        ttk.Label(
            frame_seed, text="Маса 1000 насінин (г):", font=("Arial", 11)
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.entry_m1000 = ttk.Entry(frame_seed, font=("Arial", 11), width=10)
        self.entry_m1000.grid(row=0, column=1, padx=15, pady=10)

        ttk.Label(
            frame_seed, text="Густота (млн шт/га):", font=("Arial", 11)
        ).grid(row=0, column=2, padx=15, pady=10, sticky="w")
        self.entry_density = ttk.Entry(frame_seed, font=("Arial", 11), width=10)
        self.entry_density.grid(row=0, column=3, padx=15, pady=10)

        ttk.Label(
            frame_seed, text="Схожість насіння (%):", font=("Arial", 11)
        ).grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.entry_germ = ttk.Entry(frame_seed, font=("Arial", 11), width=10)
        self.entry_germ.grid(row=1, column=1, padx=15, pady=10)
        self.entry_germ.insert(0, "95")  # Стандартне середнє значення

        btn_seed = ttk.Button(
            frame_seed, text="Порахувати норму висіву", command=self.calc_seeding
        )
        btn_seed.grid(row=2, column=0, columnspan=2, padx=15, pady=15)

        self.lbl_res_seed = ttk.Label(
            frame_seed,
            text="Вага насіння: 0 кг/га",
            font=("Arial", 11, "bold"),
            foreground="#2E5A2E",
        )
        self.lbl_res_seed.grid(row=2, column=2, columnspan=2, padx=15, pady=15)

    def calc_fert(self):
        try:
            area = float(self.entry_area.get().replace(",", "."))
            rate = float(self.entry_rate.get().replace(",", "."))
            self.lbl_res_fert.config(text=f"Разом потрібно: {area * rate:.1f} кг")
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числа у блок добрив!")

    def calc_seeding(self):
        try:
            m1000 = float(self.entry_m1000.get().replace(",", "."))
            density = float(self.entry_density.get().replace(",", "."))
            germ = float(self.entry_germ.get().replace(",", "."))

            if germ <= 0 or germ > 100:
                raise ValueError

            # Агрономічна формула: (Маса 1000 * Густоту) / (Схожість / 100)
            rate_kg_ha = (m1000 * density) / (germ / 100.0)
            self.lbl_res_seed.config(text=f"Вага насіння: {rate_kg_ha:.1f} кг/га")
        except ValueError:
            messagebox.showerror(
                "Помилка",
                "Перевірте введені числа! Схожість має бути від 1 до 100%.",
            )

    # ================= ВКЛАДКА 3: ПОГОДНИЙ КОНТРОЛЬ =================
    def build_weather_tab(self):
        lbl = ttk.Label(
            self.tab_weather,
            text="🌤️ Оптимальні умови для польових робіт",
            style="Title.TLabel",
        )
        lbl.pack(pady=15)

        columns = ("work", "temp", "wind", "notes")
        self.tree = ttk.Treeview(
            self.tab_weather, columns=columns, show="headings", height=6
        )

        self.tree.heading("work", text="Вид роботи")
        self.tree.heading("temp", text="Температура (°C)")
        self.tree.heading("wind", text="Макс. вітер (м/с)")
        self.tree.heading("notes", text="Важлива примітка")

        self.tree.column("work", width=200, anchor="w")
        self.tree.column("temp", width=140, anchor="center")
        self.tree.column("wind", width=140, anchor="center")
        self.tree.column("notes", width=280, anchor="w")

        weather_rules = [
            (
                "Обприскування (ЗЗР)",
                "+12°C ... +22°C",
                "до 3-4 м/с",
                "Краще вносити ввечері, щоб сонце не спалило листя",
            ),
            (
                "Внесення КАС / Добрив",
                "+5°C ... +20°C",
                "до 5 м/с",
                "Не бажано вносити в сильну спеку (випаровується азот)",
            ),
            (
                "Посів пшениці",
                "+12°C ... +15°C (ґрунт)",
                "Будь-який",
                "Потрібна достатня вологість верхнього шару",
            ),
            (
                "Посів кукурудзи",
                "+8°C ... +10°C (ґрунт)",
                "Будь-який",
                "Ранній посів у холодну землю призводить до гниття",
            ),
            (
                "Посів соняшника",
                "+10°C ... +12°C (ґрунт)",
                "Будь-який",
                "Грунт має прогрітися на глибині висіву",
            ),
        ]

        for rule in weather_rules:
            self.tree.insert("", "end", values=rule)

        self.tree.pack(fill="x", padx=15, pady=10)

        tip_box = ttk.LabelFrame(self.tab_weather, text=" 💡 Порада дня ")
        tip_box.pack(fill="x", padx=15, pady=15)
        ttk.Label(
            tip_box,
            text="Ніколи не окропляйте поля, якщо швидкість вітру перевищує 5 м/с — препарат знесе на сусідні ділянки, а ефективність обробки впаде на 70%.",
            font=("Arial", 11, "italic"),
            wraplength=700,
            justify="left",
        ).pack(padx=10, pady=10)

    # ================= ВКЛАДКА 4: ІНСТРУКЦІЯ =================
    def build_help_tab(self):
        lbl = ttk.Label(
            self.tab_help, text="📖 Інструкція користувача", style="Title.TLabel"
        )
        lbl.pack(pady=15)

        help_text = (
            "1️⃣ Вкладка 'Карта полів':\n"
            "   • Зміна культури: Клікніть по блоку поля та оберіть потрібну рослину.\n"
            "   • 『📊 Звіт по культурах』: Автоматично підраховує гектари внизу екрана.\n"
            "   • 『💾 ЗБЕРЕГТИ ЯК...』: Зберігає поточний стан полів у файл на комп'ютер.\n"
            "   • 『📥 ВІДКРИТИ З ПК』: Завантажує раніше створений файл назад у програму.\n"
            "   • 『🔄 СКИНУТИ ВСЕ』: Червона кнопка для повної зачистки карти під статус оранки.\n\n"
            "2️⃣ Вкладка 'Агро-Калькулятори':\n"
            "   • Калькулятор 1 (Добрива): Розрахунок загальної ваги добрив на все поле.\n"
            "   • Калькулятор 2 (Насіння): Розрахунок норми висіву (кг/га) залежно від ваги насінин та схожості.\n\n"
            "3️⃣ Вкладка 'Оптимальна погода':\n"
            "   • Шпаргалка-довідник температур та умов вітру для виїзду техніки в поле."
        )

        lbl_info = ttk.Label(
            self.tab_help,
            text=help_text,
            font=("Arial", 12),
            style="Text.TLabel",
            justify="left",
            wraplength=750,
        )
        lbl_info.pack(padx=20, pady=10, anchor="w")


if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateAgroApp(root)
    root.mainloop()



