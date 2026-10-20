import flet as ft
from logic import AccountBookLogic

class AccountBookApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.logic = AccountBookLogic()
        
        # Categories defined by user
        self.categories = ["식비", "교통", "주거", "쇼핑", "기타"]
        
        # --- UI Components: Input Section ---
        self.type_dropdown = ft.Dropdown(
            label="구분",
            options=[ft.dropdown.Option("수입"), ft.dropdown.Option("지출")],
            width=100,
        )
        
        self.amount_input = ft.TextField(
            label="금액",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.amount_error = ft.Text("", color="red", size=12)
        
        self.category_dropdown = ft.Dropdown(
            label="카테고리",
            options=[ft.dropdown.Option(cat) for cat in self.categories],
            width=120,
        )
        
        self.desc_input = ft.TextField(
            label="내용",
            expand=True,
            max_length=50,
        )
        
        self.add_button = ft.TextButton(
            text="추가",
            on_click=self.add_entry_clicked,
            style=ft.ButtonStyle(color="white", bgcolor="indigo")
        )

        # --- UI Components: List Section ---
        self.list_view = ft.ListView(expand=True, spacing=5, padding=10)
        
        # --- UI Components: Summary Section ---
        self.income_text = ft.Text("총 수입: 0", color="green", size=16)
        self.expense_text = ft.Text("총 지출: 0", color="red", size=16)
        self.balance_text = ft.Text("현재 잔액: 0", size=18, weight="bold")

        self.setup_layout()
        self.refresh_ui()

    def refresh_ui(self):
        # Clear and rebuild ListView
        self.list_view.controls.clear()
        entries = self.logic.get_all_entries()
        
        for i, entry in enumerate(entries):
            type_col = "blue" if entry['type'] == "수입" else "red"
            
            # Container for the row to allow easy replacement for confirmation
            row_container = ft.Container()
            
            # The actual data row
            data_row = ft.Row(
                controls=[
                    ft.Text(entry['type'], color=type_col, width=40, weight="bold"),
                    ft.Text(entry['category'], width=60),
                    ft.Text(entry['description'], expand=True),
                    ft.Text(f"{entry['amount']:,}", width=80, text_align="right"),
                    ft.TextButton(
                        "삭제", 
                        on_click=lambda e, idx=i, r=row_container: self.show_confirm(idx, r),
                        style=ft.ButtonStyle(color="red")
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            
            row_container.content = data_row
            self.list_view.controls.append(row_container)

        # Update Summary
        summary = self.logic.get_summary()
        self.income_text.value = f"총 수입: {summary['total_income']:,}원"
        self.expense_text.value = f"총 지출: {summary['total_expense']:,}원"
        self.balance_text.value = f"현재 잔액: {summary['balance']:,}원"
        
        self.page.update()

    def show_confirm(self, index, container):
        confirm_row = ft.Row(
            controls=[
                ft.Text("삭제할까요?", size=12, color="orange"),
                ft.TextButton("예", on_click=lambda _: self.delete_confirmed(index), style=ft.ButtonStyle(color="red")),
                ft.TextButton("아니오", on_click=lambda _: self.refresh_ui(), style=ft.ButtonStyle(color="grey")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        container.content = confirm_row
        self.page.update()

    def delete_confirmed(self, index):
        self.logic.delete_entry(index)
        self.refresh_ui()

    def add_entry_clicked(self, e):
        self.amount_error.value = ""
        if not self.type_dropdown.value:
            self.show_error("구분을 선택하세요")
            return
        try:
            val = self.amount_input.value
            if not val:
                raise ValueError("금액을 입력하세요")
            amt = int(val)
            if amt <= 0:
                raise ValueError("0보다 커야 합니다")
        except ValueError as err:
            self.show_error(str(err))
            return
        if not self.category_dropdown.value:
            self.show_error("카테고리 선택 필수")
            return
        success, msg = self.logic.add_entry(
            self.type_dropdown.value,
            amt,
            self.category_dropdown.value,
            self.desc_input.value
        )
        if success:
            self.amount_input.value = ""
            self.desc_input.value = ""
            self.refresh_ui()
        else:
            self.show_error(msg)

    def show_error(self, msg):
        self.amount_error.value = msg
        self.page.update()

def main(page: ft.Page):
    AccountBookApp(page)

if __name__ == "__main__":
    ft.app(target=main)

