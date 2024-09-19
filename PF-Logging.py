# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'pf_logging',
    'version': '1.1.0',
    'name': 'PF-Logging',
    'description': '日志记录与查询插件',
    'author': 'Shusao & GPT-4',
    'dependencies': {
        'mcdreforged': '>=2.0.0',
    }
}

config = {
    'log_level': 'INFO',
    'log_length': 0,
    'allow_in_game_query': True,
    'include_plugin_log': False
}

default_config_path = './config.yml'
log_storage = []
log_counter = 0
current_date = datetime.now().strftime('%Y-%m-%d')

log_directory = './logs/pf_logging/'

def on_load(server: PluginServerInterface, old):
    global config, log_counter
    server.logger.info("PF-Logging 插件正在加载...")
    try:
        config = server.load_config_simple(default_config_path, default_config=config)
        server.logger.info(f"配置已加载: {config}")
    except Exception as e:
        server.logger.error(f"加载配置失败: {e}")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    load_logs_from_file()
    server.logger.info("PF-Logging 插件已成功加载。")

def load_logs_from_file():
    global log_storage, log_counter, current_date
    log_storage = []
    log_counter = 0

    log_file_path = os.path.join(log_directory, f"{current_date}.json")
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_storage = json.load(f)
        if log_storage:
            log_counter = log_storage[-1]['id'] + 1

def save_logs_to_file():
    global current_date
    log_file_path = os.path.join(log_directory, f"{current_date}.json")
    with open(log_file_path, 'w', encoding='utf-8') as f:
        json.dump(log_storage, f, ensure_ascii=False, indent=4)

def on_info(server: PluginServerInterface, info: Info):
    global log_counter, log_storage, current_date
    # server.logger.info(f"Received info: {info.content}")

    now_date = datetime.now().strftime('%Y-%m-%d')
    if now_date != current_date:
        save_logs_to_file()
        current_date = now_date
        load_logs_from_file()

    if config['log_length'] > 0 and len(log_storage) >= config['log_length']:
        log_storage.pop(0)

    log_storage.append({'id': log_counter, 'content': info.content, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    # server.logger.info(f"添加了日志,ID: {log_counter}")
    log_counter += 1

    # 检查消息内容是否为查询命令
    if info.content.startswith('!!log'):
        handle_query_log_command(server, info)

def handle_query_log_command(server: PluginServerInterface, info: Info):
    parts = info.content.split()
    command = parts[0]

    if command == '!!log':
        query_log(server, info)
    elif command == '!!log_id' and len(parts) > 1:
        try:
            log_id = int(parts[1])
            query_log_by_id(server, info, log_id)
        except ValueError:
            server.execute(f'tellraw {info.player} "无效的日志ID: {parts[1]}"')

def query_log(server: PluginServerInterface, source: Info):
    # server.logger.info("调用 query_log 函数")
    if server.get_permission_level(source.player) < 4:
        server.execute(f'tellraw {source.player} "你没有权限执行该命令。"')
        return
    
    if not log_storage:
        server.execute(f'tellraw {source.player} "没有日志记录。"')
        return

    # 发送标题行
    title_message = {
        "text": "========日志内容========",
        "color": "yellow"
    }
    server.execute(f'tellraw {source.player} {json.dumps(title_message)}')

    # 发送日志内容
    for log in log_storage[-40:]:
        log_message = {
            "text": f"[{log['time']}] {log['id']}: {log['content']}",
            "clickEvent": {
                "action": "copy_to_clipboard",
                "value": f"{log['content']}"
            },
            "hoverEvent": {
                "action": "show_text",
                "value": {"text": "点击复制日志"}
            }
        }
        server.execute(f'tellraw {source.player} {json.dumps(log_message)}')

def query_log_by_id(server: PluginServerInterface, source: Info, log_id: int):
    # server.logger.info(f"使用 log_id 调用 query_log_by_id 函数: {log_id}")
    if server.get_permission_level(source.player) < 4:
        server.execute(f'tellraw {source.player} "你没有权限执行该命令。"')
        return

    # 发送标题行
    title_message = {
        "text": "========日志内容========",
        "color": "yellow"
    }
    server.execute(f'tellraw {source.player} {json.dumps(title_message)}')

    # 发送指定日志内容
    for log in log_storage:
        if log['id'] == log_id:
            log_message = {
                "text": f"[{log['time']}] {log['id']}: {log['content']}",
                "clickEvent": {
                    "action": "copy_to_clipboard",
                    "value": f"{log['content']}"
                },
                "hoverEvent": {
                    "action": "show_text",
                    "value": {"text": "点击复制日志"}
                }
            }
            server.execute(f'tellraw {source.player} {json.dumps(log_message)}')
            return
    server.execute(f'tellraw {source.player} "未找到编号为{log_id}的日志。"')

def get_logs_containing(content: str):
    return [log for log in log_storage if content in log['content']]

def execute_command_and_get_result(server: PluginServerInterface, command: str):
    result = server.rcon_query(command)
    return result

def get_log_by_id(log_id: int):
    for log in log_storage:
        if log['id'] == log_id:
            return log
    return None

def on_unload(server: PluginServerInterface):
    save_logs_to_file()
