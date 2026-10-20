import flet as ft
from datetime import datetime
from logic import calculate_parking_fee, format_currency

class ParkingCalculatorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "주차 요금 계산기"
        self.page.padding = 20
        self.records = []
        
        self.selected_entry_date = None
        self.selected_entry_time = None
        self.selected_exit_date = None
        self.selected_exit_time = None

        self.entry_date_picker = ft.DatePicker()
        self.exit_date_picker = ft.DatePicker()
        self.entry_time_picker = ft.TimePicker()
        self.exit_time_picker = ft.TimePicker()
        self.page.overlay.extend([
            self.entry_date_picker, self.exit_date_picker,
            self.entry_time_picker, self.exit_time_picker
        ])

        self.entry_info_text = ft.Text("입차: 날짜/시간을 선택하세요")
        self.exit_info_text = ft.Text("출차: 날짜/시간을 선택하세요")
        self.records_list_view = ft.ListView(expand=True, spacing=10, padding=10)
        self.total_fee_text = ft.Text("총 합계: 0원", size=24, weight="bold")
        self.pending_delete_index = None

        self.delete_confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("삭제 확인"),
            content=ft.Text("정말 삭제하시겠습니까?"),
            actions=[
                ft.TextButton("예", on_click=self._confirm_delete),
                ft.TextButton("아니오", on_click=self._cancel_delete),
            ],
        )
        self.page.overlay.append(self.delete_confirm_dialog)
        self.build_ui()

    def build_ui(self):
        # 입력 영역
        input_section = ft.Column(
            controls=[
                ft.Text("주차 정보 입력", size=20, weight="bold"),
                ft.Row([
                    ft.TextButton("입차 날짜 선택", on_click=lambda _: self.entry_date_picker.pick_date()),
                    ft.TextButton("입차 시간 선택", on_click=lambda _: self.entry_time_picker.pick_time()),
                ]),
                self.entry_info_text,
                ft.Divider(),
                ft.Row([
                    ft.TextButton("출차 날짜 선택", on_click=lambda _: self.exit_date_picker.pick_date()),
                    ft.TextButton("출차 시간 선택", on_click=lambda _: self.exit_time_picker.pick_time()),
                ]),
                self.exit_info_text,
                ft.Divider(),
                # 가장 단순한 형태의 버튼 (색상/배경 제거)
                ft.TextButton("계산하기", on_click=self._handle_calculate),
            ],
            spacing=10
        )

        # 출력 영역
        display_section = ft.Column(
            controls=[
                ft.Text("주차 기록 목록", size=20, weight="bold"),
                # 테두리 관련 에러를 피하기 위해 Container의 복잡한 속성을 제거
                ft.Container(
                    content=self.records_list_view,
                    height=300,
                ),
                ft.Divider(),
                ft.Row([self.total_fee_text], alignment="end"),
            ],
            expand=True,
            spacing=10
        )

        self.page.add(ft.Column([input_section, display_section], expand=True))

        # 이벤트 연결
        self.entry_date_picker.on_change = self._on_entry_date_change
        self.exit_date_picker.on_change = self._on_exit_date_change
        self.entry_time_picker.on_change = self._on_entry_time_change
        self.exit_time_picker.on_change = self._on_exit_time_change

    def _on_entry_date_change(self, e):
        self.selected_entry_date = self.entry_date_picker.value
        self._update_input_displays()

    def _on_exit_date_change(self, e):
        self.selected_exit_date = self.exit_date_picker.value
        self._update_input_displays()

    def _on_entry_time_change(self, e):
        self.selected_entry_time = self.entry_time_picker.value
        self._update_input_displays()

    def _on_exit_time_change(self, e):
        self.selected_exit_time = self.exit_time_picker.value
        self._update_input_displays()

    def _update_input_displays(self):
        entry_str = "입차: "
        if self.selected_entry_date: entry_str += self.selected_entry_date.strftime("%Y-%m-%d")
        if self.selected_entry_time: entry_str += f" {self.selected_entry_time.strftime('%H:%M')}"
        else: entry_str += " [시간 미선택]"
        self.entry_info_text.value = entry_str

        exit_str = "출차: "
        if self.selected_exit_date: exit_str += self.selected_exit_date.strftime("%Y-%m-%d")
        if self.selected_exit_time: exit_str += f" {self.selected_exit_time.strftime('%H:%M')}"
        else: exit_str += " [시간 미선택]"
        self.exit_info_text.value = exit_str
        self.page.update()

    def _handle_calculate(self, e):
        if not all([self.selected_entry_date, self.selected_entry_time, self.selected_exit_date, self.selected_exit_time]):
            self.page.snack_bar = ft.SnackBar(ft.Text("모든 날짜와 시간을 선택해주세요."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        entry_dt = datetime.combine(self.selected_entry_date, self.selected_entry_time.time())
        exit_dt = datetime.combine(self.selected_exit_date, self.selected_exit_time.time())
        try:
            minutes, fee = calculate_parking_fee(entry_dt, exit_dt)
            self.records.insert(0, {
                "entry": entry_dt.strftime("%Y-%m-%d %H:%M"),
                "exit": exit_dt.strftime("%Y-%m-%d %H:%M"),
                "duration": f"{minutes}분",
                "fee": fee
            })
            self._refresh_list()
        except ValueError as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ex)))
            self.page.snack_bar.open = True
            self.page.update()

    def _refresh_list(self):
        self.records_list_view.controls.clear()
        total_sum = 0
        for index, rec in enumerate(self.records):
            total_sum += rec["fee"]
            self.records_list_view.controls.append(ft.Row([
                ft.Text(f"{rec['entry']} ~ {rec['exit']}", expand=True),
                ft.Text(f"{rec['duration']}, "),
                ft.Text(f"{format_currency(rec['fee'])}", weight="bold"),
                ft.IconButton(icon="delete", on_click=lambda e, idx=index: self._show_delete_dialog(idx))
            ]))
        self.total_fee_text.value = f"총 합계: {format_currency(total_sum)}"
        self.page.update()

    def _show_delete_dialog(self, index):
        self.pending_delete_index = index
        self.delete_confirm_dialog.open = True
        self.page.update()

    def _confirm_delete(self, e):
        if self.pending_delete_index is not None:
            self.records.pop(self.pending_delete_index)
            self.pending_delete_index = None
            self.delete_confirm_dialog.open = False
            self._refresh_list()
            self.page.update()

    def _cancel_delete(self, e):
        self.pending_delete_index = None
        self.delete_confirm_dialog.open = False
        self.page.update()

def main(page: ft.Page):
    ParkingCalculatorApp(page)

if __name__ == "__main__":
    import flet as ft
    try:
        ft.app(target=main)
    except AttributeError:
        ft.run(main)
