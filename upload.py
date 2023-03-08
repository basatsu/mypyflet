from typing import Dict
import flet
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerFileType,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    icons,
    Divider,
    IconButton,
    PopupMenuButton,
    PopupMenuItem,
    colors,
    Icon,
    AppBar,
    border

)
import pandas as pd
import simpledatatable  # simpledt and not simpledatatable


def main(page: Page):
    page.scroll = "hidden"

    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()
    rowcount = Text()
    colcount = Text()

    my_simpledt_table: simpledatatable.CSVDataTable

    page.appbar = AppBar(
        leading=Icon(icons.PALETTE),
        leading_width=40,
        title=Text("CSV Data Product Processor"),
        center_title=False,
        bgcolor=colors.SURFACE_VARIANT,
        actions=[
            IconButton(icons.ADMIN_PANEL_SETTINGS),
            IconButton(icons.DETAILS),
            PopupMenuButton(
                items=[
                    PopupMenuItem(text="Page 1"),
                    PopupMenuItem(text="Page 2"),
                ]
            ),
        ],
    )

    def file_picker_result(e: FilePickerResultEvent):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(
                    value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(Row([prog, Text(f.path)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    def upload_files(e):

        nonlocal my_simpledt_table

        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                df = pd.read_csv(f.path)

                #特定の文字列で絞り込み
                df_fil=df[df['name'].str.contains('William')]

                #my_simpledt_table = simpledatatable.CSVDataTable(f.path)

                my_simpledt_table = simpledatatable.DataFrame(df_fil)  # Initialize simpledt DataFrame object
                # Extract DataTable instance from simpledt
                simpledt_dt = my_simpledt_table.datatable

                simpledt_dt.bgcolor = colors.YELLOW # Change background color of generated DataTable
                simpledt_dt.border = border.all(10, colors.PINK_600) # Add ping border to DataTable
                page.add(simpledt_dt)
                

                rowcount.value = str(len(df_fil))
                colcount.value = str(len(df_fil.columns))
                page.update()

    # add export function
    def export_results(_):
        """
        Exports the table contents into an excel file.
        """
        # _df here gives you access to a pandas dataframe containing the contents of your table. If you need better explanations let me know.
        my_simpledt_table._df.to_csv("export.csv")

    file_picker = FilePicker(on_result=file_picker_result,
                             on_upload=on_upload_progress)
    page.overlay.append(file_picker)

    page.add(
        ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=False,
                file_type=FilePickerFileType.CUSTOM,
                allowed_extensions=["csv"]
            )
        ),
        Column(ref=files),
        ElevatedButton(
            "Upload",
            ref=upload_button,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ),
        Text("行数",size=15),
        rowcount,
        Divider(height=9, thickness=3),
        Text("列数",size=15),
        colcount,
        ElevatedButton(text="Export", on_click=export_results),
    )


flet.app(target=main)
