import flet as ft
import logic

def main(page: ft.Page):
    page.title = "가계부 프로그램"
    
    # Data state
    data = logic.load_data()

    # UI Components
    desc_input = ft.TextField(label="내역", expand=True)
    amount_input = ft.TextField(label="금액", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    category_dropdown = ft.Dropdown(
        label="구분",
        options=[
            ft.dropdown.Option("수입"),
            ft.dropdown.Option("지출"),
        ],
        value="수입",
        width=100
    )
    # error_text: TextField(error_text=...) 대신 별도의 Text 사용
    error_text = ft.Text("", color="red")
    
    # 스크롤이 가능한 Column 생성
    list_container = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=300)
    
    summary_income = ft.Text("총 수입: 0")
    summary_expense = ft.Text("총 지출: 0")
    summary_balance = ft.Text("잔액: 0")

    def update_ui():
        nonlocal data
        # Update List
        list_container.controls.clear()
        for i, item in enumerate(data):
            list_container.controls.append(
                ft.Row([
                    ft.Text(f"[{item['category']}] {item['description']}", expand=True),
                    ft.Text(logic.format_currency(item['amount']), expand=True),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, idx=i: delete_item_event(idx)
                    )
                ])
            )
        
        # Update Totals
        inc, exp, bal = logic.calculate_totals(data)
        summary_income.value = f"총 수입: {logic.format_currency(inc)}"
        summary_expense.value = f"총 지출: {logic.format_currency(exp)}"
        summary_balance.value = f"잔액: {logic.format_currency(bal)}"
        
        page.update()

    def add_item_event(e):
        nonlocal data
        description = desc_input.value
        amount = amount_input.value
        category = category_dropdown.value

        if not description:
            error_text.value = "내역을 입력해주세요."
            page.update()
            return

        new_data, err = logic.add_item(data, description, amount, category)
        
        if err:
            error_text.value = err
        else:
            data = new_data
            logic.save_data(data)
            desc_input.value = ""
            amount_input.value = ""
            error_text.value = ""
            update_ui()
            
        page.update()

    def delete_item_event(index):
        nonlocal data
        data = logic.delete_item(data, index)
        logic.save_data(data)
        update_ui()

    def on_add_click(e):
        add_item_event(e)

    # Initial UI Setup
    # Button 인자 오류 방지를 위해 content=ft.Text 사용
    add_button = ft.TextButton(content=ft.Text("추가"), on_click=on_add_click)
    
    input_row = ft.Row([desc_input, amount_input, category_dropdown, add_button])
    
    # 페이지 구성
    page.add(
        ft.Column([
            ft.Text("가계부", size=30, weight="bold"),
            input_row,
            error_text,
            ft.Divider(),
            ft.Text("거래 내역", size=20, weight="bold"),
            # Container의 scroll 인자를 제거하고 list_container(Column)의 scroll을 사용
            list_container,
            ft.Divider(),
            ft.Column([
                summary_income,
                summary_expense,
                summary_balance,
            ])
        ])
    )
    
    # Initialize UI with loaded data
    update_ui()

if __name__ == "__main__":
    ft.run(main)
