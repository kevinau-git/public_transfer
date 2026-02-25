import flet as ft

def main(page: ft.Page):
    page.title = "Flet App with Left and Right Frames"
    page.window.width = 800
    page.window.height = 600
    
    # Left frame components
    def on_radio_change(e):
        result_text.value = f"Selected option: {radio_group.value}"
        page.update()
    
    def on_button_click(e):
        if radio_group.value:
            result_text.value = f"Button clicked! Current selection: {radio_group.value}"
            # Add item to list view
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Selection: {radio_group.value}"),
                    subtitle=ft.Text(f"Added at {len(list_view.controls) + 1}")
                )
            )
        else:
            result_text.value = "Button clicked! No radio option selected."
            # Add item to list view
            list_view.controls.append(
                ft.ListTile(

                    title=ft.Text("No selection made"),
                    subtitle=ft.Text(f"Added at {len(list_view.controls) + 1}")
                )
            )
        page.update()
    
    # Radio button group
    radio_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="option1", label="Option 1"),
            ft.Radio(value="option2", label="Option 2"),
            ft.Radio(value="option3", label="Option 3"),
        ]),
        on_change=on_radio_change
    )
    
    # Normal button
    normal_button = ft.Button(
        "Click Me",
        on_click=on_button_click
    )
    
    # Left frame container
    left_frame = ft.Container(
        content=ft.Column([
            ft.Text("Left Frame", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Radio Buttons:", size=14, weight=ft.FontWeight.W_500),
            radio_group,
            ft.Divider(),
            ft.Text("Action Button:", size=14, weight=ft.FontWeight.W_500),
            normal_button,
        ], spacing=10),
        bgcolor=ft.Colors.LIGHT_BLUE_50,
        padding=20,
        border_radius=10,
        width=300,
        height=500,
        border=ft.Border.all(2, ft.Colors.BLUE_200)
    )
    
    # Right frame components
    result_text = ft.Text("Right frame with ListView and scrollbar", size=14)
    
    # Create ListView with sample data and scrollbar
    list_view = ft.ListView(
        expand=1,
        spacing=10,
        padding=ft.Padding.all(20),
        auto_scroll=True,
    )
    
    # Add some initial items to the list
    for i in range(1, 6):
        list_view.controls.append(
            ft.ListTile(
                title=ft.Text(f"List Item {i}"),
                subtitle=ft.Text(f"This is the subtitle for item {i}")
            )
        )
    
    # Clear list function
    def clear_list(e):
        list_view.controls.clear()
        result_text.value = "List cleared!"
        page.update()
    
    clear_button = ft.Button(
        "Clear List",
        on_click=clear_list,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_400
    )
    
    # Right frame container
    right_frame = ft.Container(
        content=ft.Column([
            ft.Text("Right Frame", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("ListView with Scrollbar:", size=14, weight=ft.FontWeight.W_500),
            result_text,
            ft.Container(
                content=list_view,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                border=ft.Border.all(1, ft.Colors.GREY_400),
                height=300,
            ),
            clear_button,
        ], spacing=10),
        bgcolor=ft.Colors.LIGHT_GREEN_50,
        padding=20,
        border_radius=10,
        width=400,
        height=500,
        border=ft.Border.all(2, ft.Colors.GREEN_200)
    )
    
    # Main layout with left and right frames
    main_row = ft.Row([
        left_frame,
        ft.VerticalDivider(width=20),
        right_frame
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(
        ft.Container(
            content=main_row,
            padding=20,
            alignment=ft.Alignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.run(main)
