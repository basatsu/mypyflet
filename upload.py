import flet as ft
from simpledatatable import DataFrame
import pandas as pd


def main(page: ft.Page):
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        )
    )
    
    if selected_files != None:
        df = pd.read_csv(selected_files)
        simpledt_df = DataFrame(df)  # Initialize simpledt DataFrame object
        simpledt_dt = simpledt_df.datatable  # Extract DataTable instance from simpledt
        
        simpledt_dt.bgcolor = ft.colors.RED # Change background color of generated DataTable
        simpledt_dt.border = ft.border.all(10, ft.colors.PINK_600) # Add ping border to DataTable
        dr = simpledt_df.datarows

        for i in dr:
            rownum = i.cells[0].content.value
            if int(rownum) % 1 == 0:
                i.color = ft.colors.GREEN
        
        dc = simpledt_df.datacolumns

        for i in dc:
            i.label=ft.Row([i.label, ft.Icon(ft.icons.AC_UNIT)])
        
        page.add(simpledt_dt)

ft.app(target=main)