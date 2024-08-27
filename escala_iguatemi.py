import pandas as pd
import calendar
from pandas.io.formats.style import Styler
from typing import Dict, List, Tuple

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

def style_schedule(schedule: pd.DataFrame) -> Styler:
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
                            vendor_rotation: List[List[str]]) -> Tuple[pd.DataFrame, Styler]:
    schedule = generate_schedule(year, month, employees, sunday_rotation, weekdays_off, vendor_rotation)
    styled_schedule = style_schedule(schedule)
    return schedule, styled_schedule

def save_schedule(styled_schedule: Styler, filename: str):
    styled_schedule.to_excel(filename, engine='openpyxl', index=True)
    print(f"Escala salva como {filename}")

# Exemplo de uso
if __name__ == "__main__":
    employees = {
        'Levi': {'weekday': '10h às 18h', 'sunday': '14h às 20h'},
        'Nathaly': {'weekday': '10h às 18h', 'sunday': '14h às 20h'},
        'Yuri': {'weekday': '10h às 18h', 'sunday': '14h às 20h'},
        'Bruno': {'weekday': '10h às 18h', 'sunday': '14h às 20h'},
        'Gabriel': {'weekday': '14h às 22h', 'sunday': '14h às 20h'},
        'Edevaldo': {'weekday': '14h às 22h', 'sunday': '14h às 20h'},
        'Larissa': {'weekday': '14h às 22h', 'sunday': '14h às 20h'},
        'Maria': {'weekday': '14h às 22h', 'sunday': '14h às 20h'},
    }

    sunday_rotation = [['Levi', 'Edevaldo'], ['Nathaly', 'Maria']]
    vendor_rotation = [['Bruno', 'Gabriel'], ['Larissa', 'Yuri']]

    weekdays_off = {
        'Levi': 0, 'Nathaly': 3, 'Yuri': 0, 'Bruno': 1,
        'Gabriel':2 , 'Edevaldo': 1, 'Larissa': 3, 'Maria': 2
    }

    year, month = 2024, 9
    schedule, styled_schedule = create_monthly_schedule(year, month, employees, sunday_rotation, weekdays_off, vendor_rotation)
    save_schedule(styled_schedule, f'Escala_{calendar.month_name[month].upper()}_{year}_IGUATEMI.xlsx')
    
    # Para visualização em notebook
    #display(styled_schedule) 