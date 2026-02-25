import flet as ft

def main(page: ft.Page):
    page.title = "Flet App with Left and Right Frames"
    page.window.width = 800
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.AUTO
    
    # Left frame components
    def on_radio_change(e):
        result_text.value = f"Selected option: {radio_group.value}"
        log_to_console(f"Radio selection changed to: {radio_group.value}")
        page.update()

    def log_to_console(message):
        """Add a log message to the console list view"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        console_list_view.controls.append(
            ft.ListTile(
                title=ft.Text(f"[{timestamp}] {message}", size=12),
                dense=True
            )
        )
        # Auto-scroll to the bottom
        console_list_view.scroll_to(offset=-1, duration=100)
        page.update()

    def on_menu_option_1(e):
        """Handle menu option 1 click"""
        log_to_console("Menu Option 1 clicked")
        result_text.value = "Menu Option 1 was selected"
        page.update()

    def on_menu_option_2(e):
        """Handle menu option 2 click"""
        log_to_console("Menu Option 2 clicked")
        result_text.value = "Menu Option 2 was selected"
        page.update()

    def on_menu_option_4(e):
        """Handle menu option 4 click"""
        log_to_console("Menu Option 4 clicked")
        result_text.value = "Menu Option 4 was selected"
        page.update()

    def on_menu_option_5(e):
        """Handle menu option 5 click"""
        log_to_console("Menu Option 5 clicked")
        result_text.value = "Menu Option 5 was selected"
        page.update()
    
    def on_button_click(e):
        if radio_group.value:
            result_text.value = f"Button clicked! Current selection: {radio_group.value}"
            # Add item to list view with checkbox
            list_view.controls.append(
                ft.ListTile(
                    leading=ft.Checkbox(value=False),
                    title=ft.Text(f"Selection: {radio_group.value}"),
                    subtitle=ft.Text(f"Added at {len(list_view.controls) + 1}")
                )
            )
            # Log to console
            log_to_console(f"Button clicked: Selected {radio_group.value}")
        else:
            result_text.value = "Button clicked! No radio option selected."
            # Add item to list view with checkbox
            list_view.controls.append(
                ft.ListTile(
                    leading=ft.Checkbox(value=False),
                    title=ft.Text("No selection made"),
                    subtitle=ft.Text(f"Added at {len(list_view.controls) + 1}")
                )
            )
            # Log to console
            log_to_console("Button clicked: No selection made")
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

    # Text input field
    text_input = ft.TextField(
        label="Enter text here",
        hint_text="Type something...",
        multiline=False,
        width=250
    )

    # Read text button
    def on_read_text_click(e):
        """Read text from input field and display in console"""
        text_value = text_input.value if text_input.value else "(empty)"
        log_to_console(f"Text input read: {text_value}")
        page.update()

    read_text_button = ft.Button(
        "Read Text",
        on_click=on_read_text_click,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_600
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
            ft.Divider(),
            ft.Text("Text Input:", size=14, weight=ft.FontWeight.W_500),
            text_input,
            read_text_button,
        ], spacing=10),
        bgcolor=ft.Colors.LIGHT_BLUE_50,
        padding=1,
        border_radius=10,
        width=300,
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
    
    # Add some initial items to the list with checkboxes
    for i in range(1, 6):
        list_view.controls.append(
            ft.ListTile(
                leading=ft.Checkbox(value=False),
                title=ft.Text(f"List Item {i}"),
                subtitle=ft.Text(f"This is the subtitle for item {i}")
            )
        )
    
    # Clear list function
    def clear_list(e):
        list_view.controls.clear()
        result_text.value = "List cleared!"
        log_to_console("Right frame list cleared")
        page.update()

    # Print checked items function
    def print_checked_items(e):
        checked_items = []
        for i, list_tile in enumerate(list_view.controls):
            if hasattr(list_tile, 'leading') and list_tile.leading and list_tile.leading.value:
                title_text = list_tile.title.value if hasattr(list_tile.title, 'value') else str(list_tile.title)
                checked_items.append(f"Item {i+1}: {title_text}")
        
        if checked_items:
            log_to_console(f"Checked items ({len(checked_items)}):")
            for item in checked_items:
                log_to_console(f"  - {item}")
        else:
            log_to_console("No items are checked")
        page.update()

    # Clear console function
    def clear_console(e):
        console_list_view.controls.clear()
        log_to_console("Console cleared")
        page.update()
    
    clear_button = ft.Button(
        "Clear List",
        on_click=clear_list,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_400
    )

    # Print checked items button
    print_checked_button = ft.Button(
        "Print Checked Items",
        on_click=print_checked_items,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_600
    )

    # Console list view
    console_list_view = ft.ListView(
        expand=1,
        spacing=5,
        padding=ft.Padding.all(10),
        auto_scroll=True,
    )

    # Console clear button
    console_clear_button = ft.Button(
        "Clear Console",
        on_click=clear_console,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.ORANGE_600
    )

    # Console frame container
    console_frame = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Console Output", size=16, weight=ft.FontWeight.BOLD),
                console_clear_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(
                content=console_list_view,
                bgcolor=ft.Colors.BLACK87,
                border_radius=8,
                border=ft.Border.all(1, ft.Colors.GREY_600),
                height=150,
            ),
        ], spacing=10),
        bgcolor=ft.Colors.GREY_100,
        padding=1,
        border_radius=10,
        width=740,
        border=ft.Border.all(2, ft.Colors.GREY_400)
    )

    # Menu bar
    menu_bar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Menu", size=12),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Option 1", size=12),
                        on_click=on_menu_option_1
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Option 2", size=12),
                        on_click=on_menu_option_2
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Option 4", size=12),
                        on_click=on_menu_option_4
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Option 5", size=12),
                        on_click=on_menu_option_5
                    ),
                ]
            ),
             ft.SubmenuButton(
                content=ft.Text("Menu", size=12),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Option 1", size=12),
                        on_click=on_menu_option_1
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Option 2", size=12),
                        on_click=on_menu_option_2
                    )
                    
                ]
            )
        ]
    )
    
    # Right frame container
    right_frame = ft.Container(
        content=ft.Column([
            ft.Text("Right Frame", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("ListView with Checkboxes:", size=14, weight=ft.FontWeight.W_500),
            result_text,
            ft.Container(
                content=list_view,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                border=ft.Border.all(1, ft.Colors.GREY_400),
                height=300,
            ),
            ft.Row([
                clear_button,
                print_checked_button
            ], spacing=10),
        ], spacing=10),
        bgcolor=ft.Colors.LIGHT_GREEN_50,
        padding=1,
        border_radius=10,
        width=400,
        border=ft.Border.all(2, ft.Colors.GREEN_200)
    )
    
# Main layout with left and right frames in top row
    top_row = ft.Row([
        left_frame,
        ft.VerticalDivider(width=5),
        right_frame
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Main layout with menu bar, top frames, and console at bottom
    main_layout = ft.Column([
        ft.Container(
            content=menu_bar,
            bgcolor=ft.Colors.GREY_200,
            height=20
        ),
        ft.Container(
            content=top_row,
            padding=ft.Padding.only(left=20, right=20, top=20, bottom=10),
            alignment=ft.Alignment.CENTER
        ),
        ft.Container(
            content=console_frame,
            padding=ft.Padding.only(left=20, right=20, bottom=20),
            alignment=ft.Alignment.CENTER
        )
    ], spacing=0)

    page.add(main_layout)

    # Add initial console message
    log_to_console("Application started")

if __name__ == "__main__":
    ft.run(main)
