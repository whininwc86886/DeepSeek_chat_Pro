import time
start_time = time.time()

from core.client import DeepSeekClient


def get_console():
    """动态获取Console实例"""
    from rich.console import Console
    return Console()

def get_panel():
    """动态获取Panel类"""
    from rich.panel import Panel
    return Panel

def get_prompt():
    """动态获取Prompt类"""
    from rich.prompt import Prompt
    return Prompt

console = get_console()
Panel = get_panel()
Prompt = get_prompt()

# 移除原有依赖检查相关代码
class ChatInterface:
    def __init__(self):
        # 修改初始化方法，移除版本检查
        from core.client import DeepSeekClient
        from config.settings import app_config
        from utils.storage import save_history, load_history
        from utils.helpers import (
            input_with_validation,
            select_model,
            toggle_feature,
            format_response_time
        )
        
        self.client = None
        self.history = load_history()
        self.DeepSeekClient = DeepSeekClient
        self.app_config = app_config
        self.save_history = save_history
        self.safe_prompt = input_with_validation
        self.select_model = select_model
        self.toggle_feature = toggle_feature
        self.format_response_time = format_response_time
        
        self._setup_config()
        self._init_client()

    # 移除_check_dependencies方法
    def _setup_config(self):
        """配置设置（保留原有逻辑）"""
        config = self.app_config.get_config()
        
        if not config["api_key"]:
            api_key = self.safe_prompt("请输入API密钥", style="red")
            self.app_config.update_setting("api_key", api_key)
            
        self.app_config.update_setting("default_model", self.select_model())
        self.app_config.update_setting("enable_search", self.toggle_feature("联网搜索"))
        self.app_config.update_setting("deep_think", self.toggle_feature("深度思考"))
        self.app_config.validate()


    def _init_client(self):
        """初始化API客户端"""
        with console.status("[bold green]初始化对话引擎...", spinner="dots"):
            try:
                self.client = DeepSeekClient()
            except Exception as e:
                console.print(Panel.fit(
                    f"[red]初始化失败: {str(e)}[/]",
                    title="启动错误"
                ))
                exit(1)

    def _show_welcome(self):
        """显示欢迎界面"""
        welcome_art = r"""
        ██████╗ ███████╗███████╗███████╗███████╗███████╗██╗  ██╗
        ██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝██║ ██╔╝
        ██║  ██║█████╗  █████╗  █████╗  █████╗  █████╗  █████╔╝ 
        ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══╝  ██╔══╝  ██╔═██╗ 
        ██████╔╝███████╗██║     ██║     ███████╗███████╗██║  ██╗
        ╚═════╝ ╚══════╝╚═╝     ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
        """
        console.print(Panel.fit(
            f"[bold purple]{welcome_art}[/]",
            title="DeepSeek AI 智能助手",
            subtitle="输入 /help 查看命令列表",
            border_style="bold magenta"
        ))

    def _process_command(self, cmd: str) -> bool:
        """处理系统命令"""
        cmd_processor = {
            "/exit": self._exit_app,
            "/help": self._show_help,
            "/model": self._change_model,
            "/config": self._show_config,
            "/new": self._new_chat,
            "/save": self._save_chat
        }.get(cmd, None)
        
        if not cmd_processor:
            console.print(Panel.fit(
                f"[yellow]未知命令: {cmd}[/]",
                title="命令错误",
                border_style="yellow"
            ))
            return False
            
        return cmd_processor()

    def _show_help(self):
        """显示帮助信息"""
        help_content = """
[bold]可用命令列表:[/]
  /help    - 显示本帮助信息
  /exit    - 退出程序
  /model   - 切换AI模型
  /config  - 显示当前配置
  /new     - 开始新的对话
  /save    - 保存当前对话历史
        """
        console.print(Panel.fit(
            help_content,
            title="帮助文档",
            border_style="green"
        ))
        return False

    def run(self):
        """主运行循环"""
        self._show_welcome()
        
        while True:
            try:
                # 获取用户输入
                user_input = self.safe_prompt("请输入消息", style="green")
                
                # 处理空输入
                if not user_input.strip():
                    console.print("[yellow]⚠ 输入内容不能为空[/]")
                    continue
                    
                # 处理系统命令
                if user_input.startswith("/"):
                    if self._process_command(user_input):
                        break
                    continue
                    
                # 添加用户消息到历史
                self.history.append({
                    "role": "user",
                    "content": user_input
                })
                
                # 生成响应
                start_time = time.time()
                with console.status("[cyan]思考中...", spinner="dots"):
                    try:
                        response = self.client.generate(self.history)
                        response_time = time.time() - start_time
                    except Exception as e:
                        response = f"[red]错误: {str(e)}[/]"
                        response_time = 0
                        
                # 添加助手响应
                self.history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # 显示对话结果
                console.print(Panel.fit(
                    f"[bold green]您[/]\n{user_input}\n\n"
                    f"[bold magenta]助手[/]\n{response}\n\n"
                    f"[dim]响应耗时: {self.format_response_time(response_time)}[/]",
                    border_style="blue",
                    padding=(0, 1)
                )
                )

            except KeyboardInterrupt:
                console.print("\n[yellow]对话已终止[/]")
                break

if __name__ == "__main__":
    try:
        ChatInterface().run()
    except Exception as e:
        console = get_console()
        Panel = get_panel()
        console.print(Panel.fit(
            f"[bold red]致命错误: {str(e)}[/]",
            border_style="red",
            title="系统错误"
        ))