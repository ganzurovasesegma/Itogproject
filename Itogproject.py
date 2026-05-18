import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        # Форма ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(input_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Добавить тренировку",
                 command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтры
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры")
        filter_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(filter_frame, text="Тип тренировки:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(filter_frame, values=["Все", "Кардио", "Силовая", "Йога", "Растяжка"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(filter_frame, text="Применить фильтр",
                 command=self.apply_filter).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(filter_frame, text="Сбросить фильтры",
                 command=self.reset_filter).grid(row=0, column=5, padx=5, pady=5)

        # Таблица
        table_frame = ttk.Frame(self.root)
        table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        columns = ("Дата", "Тип", "Длительность")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)

        self.update_table()

    def validate_input(self, date_str, duration_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return False

        try:
            duration = float(duration_str)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        return True

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not date or not training_type or not duration:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        if self.validate_input(date, duration):
            training = {
                "date": date,
                "type": training_type,
                "duration": float(duration)
            }
            self.trainings.append(training)
            self.save_data()
            self.update_table()
            self.clear_form()

    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for training in self.trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']} мин"
            ))

    def apply_filter(self):
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        filtered = self.trainings

        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]

        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты фильтра")
                return

        self.update_filtered_table(filtered)

    def reset_filter(self):
        self.filter_type.set("Все")
        self.filter_date.delete(0, tk.END)
        self.update_table()

    def update_filtered_table(self, filtered_trainings):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for training in filtered_trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']} мин"
            ))

    def save_data(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists("trainings.json"):
            try:
                with open("trainings.json", "r", encoding="utf-8") as f:
                    self.trainings = json.load(f)
            except json.JSONDecodeError:
                self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()



