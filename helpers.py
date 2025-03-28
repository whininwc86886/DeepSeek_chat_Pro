from typing import Callable, Optional
from config.settings import app_config

def get_console():
    from rich.console import Console
    return Console()

def get_prompt():
    from rich.prompt import Prompt
    return Prompt

def input_with_validation(
    prompt: str,
    validator: Callable[[str], bool] = lambda x: True,
    error_msg: str = "输入无效",
    style: str = "cyan"  # 新增样式参数
) -> str:
    console = get_console()
    Prompt = get_prompt()
    while True:
        try:
            styled_prompt = f"[{style}]{prompt}[/]"
            value = Prompt.ask(styled_prompt)
            if validator(value):
                return value
            console.print(f"[red]✖ {error_msg}[/]")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            console.print(f"[red]错误: {str(e)}[/]")

def select_model() -> str:
    console = get_console()
    Prompt = get_prompt()
    models = app_config.get_config()["available_models"]
    return Prompt.ask(
        "[bold cyan]选择模型[/] :robot:",
        choices=models,
        default=models[0]
    )

def toggle_feature(feature_name: str) -> bool:
    from rich.prompt import Confirm
    return Confirm.ask(f"[bold cyan]启用{feature_name}功能[/]?")

def format_response_time(seconds: float) -> str:
    return f"{seconds:.2f}s"