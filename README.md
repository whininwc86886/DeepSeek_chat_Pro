# DeepSeek 对话程序

## 安装
1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 复制`.env.example`为`.env`并填写你的API密钥
4. 运行程序：`python cli.py`

## 功能特性
- 多模型切换支持
- 对话历史持久化
- 智能错误重试机制
- 实时性能监控
- 交互式配置向导

## 配置选项
- `DEEPSEEK_API_KEY`: 必须的API密钥
- `MODEL_NAME`: 模型名称（默认：deepseek-chat）
- `API_URL`: API端点
- `TEMPERATURE`: 生成随机性（0-1）
- `MAX_TOKENS`: 最大生成长度
## 命令列表
- `/help` 查看帮助
- `/config` 显示当前配置
- `/model` 切换模型
- `/new` 重置对话
- `/exit` 退出程序

## 快速开始

1. 复制环境文件
```bash
cp .env.example .env