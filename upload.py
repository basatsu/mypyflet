from typing import Dict
import flet
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    FilePickerFileType,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    icons,
    Divider
)
import pandas as pd
from simpledatatable import DataFrame, CSVDataTable

simpledt_dt: pd.DataFrame  # define dataframe


def main(page: Page):
    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()
    rowcount = Text()
    colcount = Text()

    filepath = Text()

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

    file_picker = FilePicker(on_result=file_picker_result,
                             on_upload=on_upload_progress)

    def upload_files(e):
        if file_picker.result is not None and file_picker.result.files is not None:

            filepath.value = file_picker.result.files[0].path
            df = pd.read_csv(filepath.value)

            rowcount.value = str(len(df))

            colcount.value = str(len(df.columns))
            page.update()

            # for f in file_picker.result.files:

            # df = pd.read_csv(f.path[0])

            # simpledt_df = DataFrame(df)
            # simpledt_dt = simpledt_df.datatable

            # rowcount.value = str(len(df))

            # colcount.value = str(len(df.columns))
            # page.update()

    def export_results(_):
        upload_files(_)
        simpledt_dt.to_excel("export.xlsx", index=False)
    page.overlay.append(file_picker)

    # print("--------------------ファイルパスは----------------")
    # print(filepath)
    if filepath.value is not None:
        csv = CSVDataTable(filepath.value)
        dt = csv.datatable

    page.add(
        ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=False,
                # this option is needed for the 'allowed_extensions' to work !
                file_type=FilePickerFileType.CUSTOM,
                # the file picker mainly show csv files and not all files which is the default
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
        rowcount,
        Divider(height=9, thickness=3),
        colcount,
        Divider(height=9, thickness=5, color="red"),
        filepath,

        # add UI of Datatable and export button
        ElevatedButton(text="Export", on_click=export_results),

    )

    if filepath.value is not None:
        page.add(dt)


flet.app(target=main)
