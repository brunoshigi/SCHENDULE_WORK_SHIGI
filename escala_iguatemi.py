import pandas as pd
import calendar
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def generate_schedule(year: int, month: int, employees: Dict[str, Dict[str, str]],
                      sunday_rotation: List[List[str]], weekdays_off: Dict[str, int],
                      vendor_rotation: List[List[str]]) -> pd.DataFrame:
    start_date = pd.Timestamp(year, month, 1)
    end_date = start_date + pd.offsets.MonthEnd()
    days = pd.date_range(start=start_date, end=end_date)
    
    schedule = pd.DataFrame(index=days, columns=[name.upper() for name in employees.keys()])

    for day in days:
        if day.dayofweek < 6:  # De segunda a sábado
            for employee, shifts in employees.items():
                schedule.at[day, employee.upper()] = shifts['weekday']
        else:  # Domingo
            for employee in employees:
                schedule.at[day, employee.upper()] = None

    sundays = days[days.dayofweek == 6]
    for i, sunday in enumerate(sundays):
        active_employees = sunday_rotation[i % len(sunday_rotation)]
        for active_employee in active_employees:
            schedule.at[sunday, active_employee.upper()] = employees[active_employee]['sunday']
        team = vendor_rotation[i % len(vendor_rotation)]
        for vendor in team:
            schedule.at[sunday, vendor.upper()] = employees[vendor]['sunday']

    for employee, off_day in weekdays_off.items():
        off_days = days[days.dayofweek == off_day]
        schedule.loc[off_days, employee.upper()] = None

    schedule.fillna('FOLGA', inplace=True)
    
    return schedule

def calculate_work_stats(schedule: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    total_days = schedule.apply(lambda x: (x != 'FOLGA').sum())
    sunday_days = schedule[schedule.index.dayofweek == 6].apply(lambda x: (x != 'FOLGA').sum())
    return total_days, sunday_days

def style_schedule(schedule: pd.DataFrame) -> pd.io.formats.style.Styler:
    def highlight_cells(val):
        color_map = {
            '10h às 18h': 'background-color: #E6F3FF',
            '14h às 22h': 'background-color: #FFF0E6',
            '14h às 20h': 'background-color: #E6FFE6',
            'FOLGA': 'background-color: #FFCCCB'
        }
        return color_map.get(val, '')

    def highlight_sundays(val):
        if isinstance(val.name, pd.Timestamp) and val.name.dayofweek == 6:
            return ['background-color: #FFD700; font-weight: bold'] * len(val)
        return [''] * len(val)

    total_days, sunday_days = calculate_work_stats(schedule)
    
    # Adicionar linhas com as estatísticas
    schedule_with_stats = schedule.copy()
    schedule_with_stats.loc['TOTAL DIAS'] = total_days
    schedule_with_stats.loc['DOMINGOS'] = sunday_days

    styled = schedule_with_stats.style.applymap(highlight_cells) \
                           .apply(highlight_sundays, axis=1) \
                           .format_index(lambda x: f"{x.strftime('%d/%m')} ({calendar.day_abbr[x.dayofweek]})" if isinstance(x, pd.Timestamp) else x, axis=0) \
                           .set_table_styles([
                               {'selector': 'th', 'props': 'background-color: #4CAF50; color: white; font-weight: bold; text-align: center;'},
                               {'selector': 'td', 'props': 'text-align: center;'},
                           ]) \
                           .set_properties(**{'font-weight': 'bold'}, subset=pd.IndexSlice[schedule.index[schedule.index.dayofweek == 6], :]) \
                           .set_properties(subset=pd.IndexSlice[:, schedule.columns], **{'font-weight': 'normal'}) \
                           .set_properties(subset=pd.IndexSlice[:, :], **{'border': '1px solid black'}) \
                           .set_properties(**{'background-color': '#EFEFEF', 'font-weight': 'bold'}, subset=pd.IndexSlice[['Total de dias', 'Domingos trabalhados'], :])
                           
    return styled

def create_monthly_schedule(year: int, month: int, employees: Dict[str, Dict[str, str]],
                            sunday_rotation: List[List[str]], weekdays_off: Dict[str, int],
                            vendor_rotation: List[List[str]]) -> Tuple[pd.DataFrame, pd.io.formats.style.Styler]:
    schedule = generate_schedule(year, month, employees, sunday_rotation, weekdays_off, vendor_rotation)
    styled_schedule = style_schedule(schedule)
    return schedule, styled_schedule

def save_schedule(styled_schedule: pd.io.formats.style.Styler, filename: str):
    try:
        styled_schedule.to_excel(filename, engine='openpyxl', index=True)
        print(f"Escala salva como {filename}")
    except Exception as e:
        print(f"Erro ao salvar a escala: {e}")

class ScheduleApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerador de Escalas")

        # Campos para ano e mês
        self.label_year = ttk.Label(master, text="Ano:")
        self.label_year.grid(row=0, column=0, padx=5, pady=5)
        self.entry_year = ttk.Entry(master)
        self.entry_year.grid(row=0, column=1, padx=5, pady=5)
        self.entry_year.insert(0, pd.Timestamp.now().year)

        self.label_month = ttk.Label(master, text="Mês (1-12):")
        self.label_month.grid(row=1, column=0, padx=5, pady=5)
        self.entry_month = ttk.Entry(master)
        self.entry_month.grid(row=1, column=1, padx=5, pady=5)
        self.entry_month.insert(0, pd.Timestamp.now().month)

        # Botão para adicionar funcionários
        self.button_add_employees = ttk.Button(master, text="Adicionar Funcionários", command=self.add_employees)
        self.button_add_employees.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Botão para gerar a escala
        self.button_generate = ttk.Button(master, text="Gerar Escala", command=self.generate_schedule_gui)
        self.button_generate.grid(row=3, column=0, columnspan=2, pady=5)

        # Inicializa dados
        self.employees = {}
        self.sunday_rotation = []
        self.weekdays_off = {}
        self.vendor_rotation = []

    def add_employees(self):
        # Janela para entrada de dados dos funcionários
        employee_window = tk.Toplevel(self.master)
        employee_window.title("Dados dos Funcionários")

        # Labels e campos de entrada
        lbl_name = ttk.Label(employee_window, text="Nome:")
        lbl_name.grid(row=0, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(employee_window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        
        lbl_weekday_shift = ttk.Label(employee_window, text="Turno Semana:")
        lbl_weekday_shift.grid(row=1, column=0, padx=5, pady=5)
        entry_weekday_shift = ttk.Entry(employee_window)
        entry_weekday_shift.grid(row=1, column=1, padx=5, pady=5)
        
        lbl_sunday_shift = ttk.Label(employee_window, text="Turno Domingo:")
        lbl_sunday_shift.grid(row=2, column=0, padx=5, pady=5)
        entry_sunday_shift = ttk.Entry(employee_window)
        entry_sunday_shift.grid(row=2, column=1, padx=5, pady=5)
        
        lbl_off_day = ttk.Label(employee_window, text="Dia de Folga (0=Seg, 6=Dom):")
        lbl_off_day.grid(row=3, column=0, padx=5, pady=5)
        entry_off_day = ttk.Entry(employee_window)
        entry_off_day.grid(row=3, column=1, padx=5, pady=5)
        
        # Botão para adicionar funcionário
        def add_employee():
            try:
                name = entry_name.get()
                weekday_shift = entry_weekday_shift.get()
                sunday_shift = entry_sunday_shift.get()
                off_day = int(entry_off_day.get())
                if not name or not weekday_shift or not sunday_shift:
                    raise ValueError("Todos os campos devem ser preenchidos.")
                if off_day < 0 or off_day > 6:
                    raise ValueError("Dia de folga deve ser entre 0 (Seg) e 6 (Dom).")
                self.employees[name] = {'weekday': weekday_shift, 'sunday': sunday_shift}
                self.weekdays_off[name] = off_day
                messagebox.showinfo("Sucesso", f"{name} adicionado com sucesso.")
                employee_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Erro", str(ve))
        
        btn_add = ttk.Button(employee_window, text="Adicionar", command=add_employee)
        btn_add.grid(row=4, column=0, columnspan=2, pady=10)
    
    def generate_schedule_gui(self):
        try:
            year = int(self.entry_year.get())
            month = int(self.entry_month.get())
            
            if not self.employees:
                messagebox.showwarning("Aviso", "Por favor, adicione funcionários antes de gerar a escala.")
                return

            # Configurar rotações (esta parte pode ser aprimorada para coletar dados da interface)
            self.sunday_rotation = [list(self.employees.keys())]
            self.vendor_rotation = [list(self.employees.keys())]
            
            # Gera a escala usando os dados coletados
            schedule, styled_schedule = create_monthly_schedule(
                year, month, self.employees, self.sunday_rotation, self.weekdays_off, self.vendor_rotation
            )
            # Salva o arquivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Salvar Escala"
            )
            if filename:
                save_schedule(styled_schedule, filename)
                messagebox.showinfo("Sucesso", f"Escala salva em {filename}")
        except ValueError:
            messagebox.showerror("Erro", "Ano e mês devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()