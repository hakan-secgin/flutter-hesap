import flet as ft

class Calculator(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        self.result = ft.Text(
            value="0", 
            color=ft.Colors.BLACK87, 
            size=45, 
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.RIGHT,
            animate_opacity=300,
            animate_scale=ft.Animation(300, ft.AnimationCurve.DECELERATE)
        )
        
        self.width = 380
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 40
        self.padding = 30
        self.shadow = ft.BoxShadow(
            blur_radius=50,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 20)
        )
        self.content = self.build_ui()

    def build_ui(self):
        def create_button(text, color, text_color=ft.Colors.BLACK87, expand=1):
            return ft.Container(
                content=ft.Text(text, color=text_color, weight=ft.FontWeight.W_600, size=22),
                alignment=ft.Alignment(0, 0),
                bgcolor=color,
                border_radius=20,
                ink=True,
                expand=expand,
                on_click=self.button_clicked,
                data=text,
                height=75,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                on_hover=lambda e: self.on_button_hover(e, color)
            )

        return ft.Column(
            controls=[
                ft.Container(
                    content=self.result,
                    padding=25,
                    alignment=ft.Alignment(1, 0),
                    height=130,
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=25,
                    margin=ft.Margin(0, 0, 0, 15), # Fixed margin
                    border=ft.Border(
                        ft.BorderSide(1, ft.Colors.GREY_200),
                        ft.BorderSide(1, ft.Colors.GREY_200),
                        ft.BorderSide(1, ft.Colors.GREY_200),
                        ft.BorderSide(1, ft.Colors.GREY_200)
                    )
                ),
                ft.Row(
                    controls=[
                        create_button("AC", ft.Colors.RED_50, ft.Colors.RED_400),
                        create_button("+/-", ft.Colors.GREY_100),
                        create_button("%", ft.Colors.GREY_100),
                        create_button("/", ft.Colors.BLUE_50, ft.Colors.BLUE_600),
                    ],
                    spacing=12
                ),
                ft.Row(
                    controls=[
                        create_button("7", ft.Colors.GREY_50),
                        create_button("8", ft.Colors.GREY_50),
                        create_button("9", ft.Colors.GREY_50),
                        create_button("*", ft.Colors.BLUE_50, ft.Colors.BLUE_600),
                    ],
                    spacing=12
                ),
                ft.Row(
                    controls=[
                        create_button("4", ft.Colors.GREY_50),
                        create_button("5", ft.Colors.GREY_50),
                        create_button("6", ft.Colors.GREY_50),
                        create_button("-", ft.Colors.BLUE_50, ft.Colors.BLUE_600),
                    ],
                    spacing=12
                ),
                ft.Row(
                    controls=[
                        create_button("1", ft.Colors.GREY_50),
                        create_button("2", ft.Colors.GREY_50),
                        create_button("3", ft.Colors.GREY_50),
                        create_button("+", ft.Colors.BLUE_50, ft.Colors.BLUE_600),
                    ],
                    spacing=12
                ),
                ft.Row(
                    controls=[
                        create_button("0", ft.Colors.GREY_50, expand=2),
                        create_button(".", ft.Colors.GREY_50),
                        create_button("=", ft.Colors.BLUE_500, ft.Colors.WHITE),
                    ],
                    spacing=12
                ),
            ],
            spacing=12
        )

    def on_button_hover(self, e, original_color):
        if e.data == "true":
            e.control.bgcolor = ft.Colors.GREY_200 if original_color == ft.Colors.GREY_50 else ft.Colors.BLUE_100
        else:
            e.control.bgcolor = original_color
        e.control.update()

    def button_clicked(self, e):
        data = e.control.data
        
        # Simple animation effect on click
        self.result.scale = 0.95
        self.result.update()
        self.result.scale = 1.0
        
        if data == "AC":
            self.reset()
        elif data == "+/-":
            try:
                val = float(self.value)
                self.value = str(int(val * -1)) if val.is_integer() else f"{val * -1:.4g}"
            except: pass
        elif data == "%":
            try:
                val = float(self.value) / 100
                self.value = str(int(val)) if val.is_integer() else f"{val:.4g}"
            except: pass
        elif data == "=":
            self.calculate()
        elif data in ("+", "-", "*", "/"):
            self.operator = data
            try:
                self.operand1 = float(self.value)
            except:
                self.operand1 = 0
            self.new_operand = True
        else:
            if self.new_operand or self.value == "0":
                if data == ".":
                    self.value = "0."
                else:
                    self.value = data
                self.new_operand = False
            else:
                if data == "." and "." in self.value:
                    pass
                else:
                    self.value += data
                    
        self.update_display()

    def reset(self):
        self.value = "0"
        self.operator = None
        self.operand1 = 0
        self.new_operand = True

    def calculate(self):
        try:
            operand2 = float(self.value)
            if self.operator == "+":
                res = self.operand1 + operand2
            elif self.operator == "-":
                res = self.operand1 - operand2
            elif self.operator == "*":
                res = self.operand1 * operand2
            elif self.operator == "/":
                res = self.operand1 / operand2 if operand2 != 0 else "Error"
            else:
                res = operand2
                
            if isinstance(res, float) and res.is_integer():
                self.value = str(int(res))
            else:
                self.value = f"{res:.8g}"
                
            self.operator = None
            self.new_operand = True
        except:
            self.value = "Error"
            self.reset()

    def update_display(self):
        self.result.value = self.value
        self.update()

def main(page: ft.Page):
    page.title = "Modern Light Calculator"
    page.window_width = 420
    page.window_height = 750
    page.bgcolor = ft.Colors.GREY_100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_resizable = False
    
    calc = Calculator()
    
    def on_keyboard(e: ft.KeyboardEvent):
        key = e.key
        if key.isdigit():
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data=key, control=ft.Container(data=key)))
        elif key == "Enter" or key == "=":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data="=", control=ft.Container(data="=")))
        elif key == "Backspace":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data="AC", control=ft.Container(data="AC")))
        elif key == "+":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data="+", control=ft.Container(data="+")))
        elif key == "-":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data="-", control=ft.Container(data="-")))
        elif key == "*":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data="*", control=ft.Container(data="*")))
        elif key == "/":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data="/", control=ft.Container(data="/")))
        elif key == "." or key == ",":
            calc.button_clicked(ft.ControlEvent(target=None, name="click", data=".", control=ft.Container(data=".")))

    page.on_keyboard_event = on_keyboard
    page.add(calc)

if __name__ == "__main__":
    ft.app(target=main) # Using app() instead of run() as it's more common in local dev
