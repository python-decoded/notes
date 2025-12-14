import flet as ft


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def reduce_click(event: ft.ControlEvent):
        print(vars(event))
        txt_number.value = str(int(txt_number.value) - 1)
        event.page.update()

    def add_click(event: ft.ControlEvent):
        txt_number.value = str(int(txt_number.value) + 1)
        event.page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=reduce_click),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=add_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(main)
