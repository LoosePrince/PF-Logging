# -*- coding: utf-8 -*-
import json
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'pf_logging',
    'version': '1.0.0',
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

default_config_path = './config/PF_Logging/config.yml'
log_storage = []
log_counter = 0

def on_load(server: PluginServerInterface, old):
    global config
    config = server.load_config_simple(file_path=default_config_path, default_config=config)
    server.register_command(
        Literal('log').requires(lambda src: src.has_permission(4)).runs(query_log).then(
            Integer('log_id').runs(lambda src, ctx: query_log_by_id(src, ctx['log_id']))))

def on_info(server: PluginServerInterface, info: Info):
    global log_counter, log_storage
    if config['log_length'] > 0 and len(log_storage) >= config['log_length']:
        log_storage.pop(0)
    log_storage.append({'id': log_counter, 'content': info.content})
    log_counter += 1

def query_log(source: CommandSource):
    for log in log_storage[-10:]:
        source.reply(f"#{log['id']}: {log['content']}")

def query_log_by_id(source: CommandSource, log_id: int):
    for log in log_storage:
        if log['id'] == log_id:
            source.reply(f"#{log['id']}: {log['content']}")
            return
    source.reply(f"未找到编号为{log_id}的日志。")

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
    global log_storage
    log_storage.clear()
