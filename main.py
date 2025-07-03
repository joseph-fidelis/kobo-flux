"""
Upload csv
"""

import datetime
import os
from pathlib import Path
import uuid
from annotated_types import T
from nicegui import events, ui
from file_processor import FileProcessor
from kobo_api import KoboAPI


@ui.page('/upload/', title='Kobo Form Uploader', dark=True)
async def upload_page(form_id: str, form_title: str):
    """
    This is the home page of the application.
    It contains the upload form and the table.
    """
    table_columns = []
    table_rows = []
    table_instance = None
    progress = None
    log_lines = []
    log_view = None
    tmp_dir = Path.cwd() / 'logs'
    log_file = tmp_dir / f"upload_log_{form_id}.log"
    
    def log_upload_result(message: str):
        tmp_dir.mkdir(exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        log_lines.append(log_line)
        if log_view:
            log_view.push(log_line)
        with open(log_file, "a") as f:
            f.write(log_line + "\n")

    async def handle_upload(e: events.UploadEventArguments):
        """
        Handle the upload event.
        """
        nonlocal table_columns, table_rows, table_instance
        try:
            file_processor = FileProcessor(e.content, e.type, e.name)
            file_path = file_processor.save_file_to_tmp()
            _columns, _rows = file_processor.format_for_nicegui_table(
                file_path)

            table_columns = _columns
            table_rows = _rows
            print(f"rows: {_rows}")
            print(f"column: {_columns}")

            # Update the table if it exists
            if table_instance:
                table_instance.columns = table_columns
                table_instance.rows = table_rows
                # Set row key to first column name
                if table_columns:
                    table_instance.row_key = table_columns[0]['field']
                table_instance.update()

                ui.notify(
                    f'File loaded successfully! {len(table_rows)} rows with {len(table_columns)} columns.',
                    type='positive')
        except Exception as error:
            ui.notify(f'Error processing file: {str(error)}', type='negative')
            print(f"Error: {error}")

    def on_upload_clicked():
        nonlocal progress, log_view
        kobo_api = KoboAPI()
        if len(table_rows) > 0:
            try:
                total = len(table_rows)
                if progress:
                    progress.value = 0
                    progress.visible = True
                if log_view:
                    log_view.clear()
                for idx, submission in enumerate(table_rows, 1):
                    url = "/submissions.json"
                    try:
                        form_unique_id = uuid.uuid4()
                        # Place meta inside submission
                        submission_with_meta = dict(submission)
                        submission_with_meta["meta"] = {"instanceID": f"uuid:{form_unique_id}"}
                        data = {"id": form_id, "submission": submission_with_meta}
                        response = kobo_api.post_with_auth(url, data)
                        msg = f"SUCCESS: {data} => {response.status_code}"
                        ui.notify(
                            f"Upload successful: {response.status_code}", type="positive")
                    except Exception as e:
                        msg = f"FAILED: {data} => {str(e)}"
                        ui.notify(f"Upload failed: {str(e)}", type="negative")
                    log_upload_result(msg)
                    if progress:
                        progress.value = idx / total
                if progress:
                    progress.visible = False
            except Exception as e:
                if progress:
                    progress.visible = False
                ui.notify(f"Upload failed: {str(e)}", type="negative")
        else:
            ui.notify("No data to upload, upload csv file", type="warning")

    def download_log():
        if log_file.exists():
            with open(log_file, "rb") as f:
                log_bytes = f.read()
            ui.download(log_bytes, log_file.name)
        else:
            ui.notify("No log file found.", type="warning")

    with ui.element('div').classes('columns-2 gap-2 h-full w-full'):
        card_style = 'w-full items-center justify-center h-full mb-2 p-2 break-inside-avoid h-1/2'
        with ui.card().classes(card_style):
            ui.label(f'Upload {form_title} Forms').classes(
                'text-center text-2xl font-bold')
            with ui.column().classes('w-full mt-4 h-[260px] m-4 p-4 border-2 border-gray-500 border-dashed rounded-md items-center justify-center'):
                ui.label('Supported file types: .xlsx, .xls, .csv').classes(
                    'text-center text-lg')

                ui.upload(on_upload=handle_upload, multiple=False,
                          auto_upload=True, label='Click on the plus mark to upload file').props(
                    'accept=.csv,.xlsx,.xls color=teal').classes('w-full mt-4 h-[200px] border-2 border-gray-500 border-dashed rounded-md')

            progress = ui.linear_progress(value=0, show_value=False).classes(
                'w-full mt-2').props('color=primary')
            progress.visible = False

            ui.button('Upload File', on_click=on_upload_clicked).classes(
                'w-full mt-4').props('color=green')

            log_view = ui.log().classes('w-full mt-4')
            for line in log_lines:
                log_view.push(line)

            ui.button('Download Log', on_click=download_log).classes(
                'w-full mt-2').props('color=primary')

        with ui.card().classes(card_style):
            ui.label('Preview uploaded file').classes(
                'text-center text-2xl font-bold')

            table_instance = ui.table(columns=table_columns, rows=table_rows,
                                      row_key='name').classes('w-full mt-4')


@ui.page('/', dark=True)
async def forms_page():
    """
    This is the forms page of the application.
    It contains the forms list.
    """
    def handle_form_selection(e: events.TableSelectionEventArguments):
        """
        Handle the form selection event.
        """
        row = e.selection[0]
        form_title = row['title']
        form_id = row['id_string']
        # form_uuid = row['uuid']
        ui.navigate.to(
            f'/upload?form_id={form_id}&form_title={form_title}')

    kobo_api = KoboAPI()
    forms = kobo_api.get_forms()

    # Define the columns for the table
    columns = [
        {"name": "title", "label": "Title", "field": "title",
            "required": True, "align": "left", "sortable": True},
        {"name": "description", "label": "Description", "field": "description",
         "required": False, "align": "left", "sortable": False},


        {"name": "id_string", "label": "ID String", "field": "id_string",
            "required": True, "align": "left", "sortable": True},


        {"name": "num_of_submissions", "label": "Num of Submissions",
            "field": "num_of_submissions", "required": True, "align": "left", "sortable": True},

        {"name": "uuid", "label": "UUID", "field": "uuid",
            "required": True, "align": "left", "sortable": True},
    ]

    # Prepare the rows for the table
    rows = []
    for form in forms:
        rows.append({
            "title": form.get("title", ""),
            "description": form.get("description", ""),
            "id_string": form.get("id_string", ""),
            "num_of_submissions": form.get("num_of_submissions",
                                           form.get("num_of_submission", form.get("num_of_submission", ""))),
            "uuid": form.get("uuid", ""),
        })

    ui.label('Kobo Forms').classes('text-center text-2xl font-bold')
    ui.table(columns=columns, rows=rows, selection='single', on_select=handle_form_selection,
             row_key='id_string').classes('w-full mt-4')


ui.run(title="KOBOFLUX", favicon="favicon.ico",dark=True,show_welcome_message=False)
