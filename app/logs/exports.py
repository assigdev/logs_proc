from datetime import datetime

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


class LogToExcelExporter:
    def __init__(self, queryset):
        self.queryset = queryset
        self.filename = f"report-{datetime.now().strftime('%m-%d-%Y_%H:%M:%S')}.xlsx"

    def export(self):
        wb = Workbook()
        ws = wb.get_active_sheet()
        ws.append(("IP", "date", "method", "uri", "status code", "body size"))
        for o in self.queryset:
            ws.append((o.ip, o.datetime, o.method, o.uri, o.status_code, o.body_size))
        self._set_column_dimensions(ws)
        return self._get_response(wb)

    @staticmethod
    def _set_column_dimensions(ws):
        ws.column_dimensions["A"].width = 20
        ws.column_dimensions["B"].width = 25
        ws.column_dimensions["C"].width = 10
        ws.column_dimensions["D"].width = 40
        ws.column_dimensions["E"].width = 10
        ws.column_dimensions["F"].width = 10

    def _get_response(self, workbook):
        response = HttpResponse(content=save_virtual_workbook(workbook),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={self.filename}'
        return response
