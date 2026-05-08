import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # Основной фрейм
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка весов строк и столбцов для растягивания
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 1. Выбор валюты «Из»
        ttk.Label(main_frame, text="Из валюты:").grid(
            row=0, column=0, padx=5, pady=10, sticky=tk.W
        )
        self.from_currency = ttk.Combobox(main_frame, state="readonly", width=15)
        self.from_currency.grid(row=0, column=1, padx=5, pady=10, sticky=(tk.W, tk.E))

        # 2. Выбор валюты «В»
        ttk.Label(main_frame, text="В валюту:").grid(
            row=1, column=0, padx=5, pady=10, sticky=tk.W
        )
        self.to_currency = ttk.Combobox(main_frame, state="readonly", width=15)
        self.to_currency.grid(row=1, column=1, padx=5, pady=10, sticky=(tk.W, tk.E))

        # 3. Поле ввода суммы
        ttk.Label(main_frame, text="Сумма:").grid(
            row=2, column=0, padx=5, pady=10, sticky=tk.W
        )
        self.amount_entry = ttk.Entry(main_frame, width=20)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=10, sticky=(tk.W, tk.E))

        # 4. Кнопка конвертации
        self.convert_btn = ttk.Button(main_frame, text="Конвертировать", command=self.on_convert)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # 5. Таблица истории
        history_label = ttk.Label(main_frame, text="История операций:")
        history_label.grid(row=4, column=0, columnspan=2, padx=5, pady=(20, 5), sticky=tk.W)

        # Фрейм для таблицы и скроллбара
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Столбцы таблицы
        columns = ("№", "Из", "В", "Сумма", "Результат")
        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=8
        )

        # Заголовки столбцов
        self.history_tree.heading("№", text="№")
        self.history_tree.heading("Из", text="Из")
        self.history_tree.heading("В", text="В")
        self.history_tree.heading("Сумма", text="Сумма")
        self.history_tree.heading("Результат", text="Результат")

        # Ширина столбцов
        self.history_tree.column("№", width=40, anchor=tk.CENTER)
        self.history_tree.column("Из", width=80, anchor=tk.CENTER)
        self.history_tree.column("В", width=80, anchor=tk.CENTER)
        self.history_tree.column("Сумма", width=120, anchor=tk.E)
        self.history_tree.column("Результат", width=120, anchor=tk.E)

        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # Размещение таблицы и скроллбара
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Заполняем списки валют (пример)
        currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "RUB", "UAH"]
        self.from_currency['values'] = currencies
        self.to_currency['values'] = currencies

    def on_convert(self):
        """Обработчик кнопки конвертации (заглушка)"""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        amount_str = self.amount_entry.get().strip()

        if not from_curr or not to_curr:
            messagebox.showwarning("Внимание", "Выберите валюты для конвертации")
            return

        if not amount_str:
            messagebox.showwarning("Внимание", "Введите сумму для конвертации")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return

            # Здесь будет логика конвертации
            result = amount * 1.1  # Заглушка: условный курс 1.1

            # Добавляем запись в историю
            self.add_to_history(from_curr, to_curr, amount, result)

            messagebox.showinfo(
                "Результат",
                f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}"
            )

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму (число)")

    def add_to_history(self, from_curr, to_curr, amount, result):
        """Добавляет запись в таблицу истории"""
        # Номер записи — количество строк + 1
        record_num = len(self.history_tree.get_children()) + 1

        self.history_tree.insert("", "end", values=(
            record_num,
            from_curr,
            to_curr,
            f"{amount:.2f}",
            f"{result:.2f}"
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterUI(root)
    root.mainloop()
