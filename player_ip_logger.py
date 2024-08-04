# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'player_ip_logger',
    'version': '1.1.0',
    'name': 'Player IP Logger',
    'description': '记录玩家IP地址的插件',
    'author': 'Shusao & GPT-4',
    'dependencies': {
        'mcdreforged': '>=2.0.0',
    }
}

config = {
    'log_directory': './logs/player_ips/',
}

ip_storage = {}
log_directory = config['log_directory']

def on_load(server: PluginServerInterface, old):
    global ip_storage
    server.logger.info("Player IP Logger 插件正在加载...")
    
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    ip_storage = load_ip_logs()
    server.logger.info("Player IP Logger 插件已成功加载。")

def load_ip_logs():
    ip_log_file_path = os.path.join(log_directory, 'player_ips.json')
    if os.path.exists(ip_log_file_path):
        with open(ip_log_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_ip_logs():
    ip_log_file_path = os.path.join(log_directory, 'player_ips.json')
    with open(ip_log_file_path, 'w', encoding='utf-8') as f:
        json.dump(ip_storage, f, ensure_ascii=False, indent=4)

def on_info(server: PluginServerInterface, info: Info):
    if "logged in with entity id" in info.content or \
       "lost connection" in info.content or \
       "Disconnecting" in info.content:
        handle_player_login(server, info)

def handle_player_login(server: PluginServerInterface, info: Info):
    global ip_storage
    player_name, player_ip = extract_player_info(info.content)
    
    if player_name and player_ip:
        if player_name not in ip_storage:
            ip_storage[player_name] = []
        
        if player_ip not in ip_storage[player_name]:
            ip_storage[player_name].append(player_ip)
            save_ip_logs()

def extract_player_info(content: str):
    try:
        # 处理格式: Shusao[/127.0.0.1:25567] logged in with entity id 359776
        if '[' in content and ']' in content:
            start_index = content.find('[') + 1
            end_index = content.find(']')
            if start_index != -1 and end_index != -1:
                ip_info = content[start_index:end_index]
                if ':' in ip_info:
                    player_ip = ip_info.split('/')[1].split(':')[0]
                    player_name = content[:content.find('[')].strip()
                    return player_name, player_ip

        # # 处理格式: Disconnecting Shusao (/127.0.0.1:25567)
        # if "Disconnecting" in content or "lost connection" in content:
        #     start_index = content.find('(/') + 2
        #     end_index = content.find(')', start_index)
        #     if start_index != -1 and end_index != -1:
        #         ip_info = content[start_index:end_index]
        #         player_ip = ip_info.split(':')[0]
        #         # 确定玩家名称从 "Disconnecting " 到 " (/" 之间的部分
        #         player_name_start = content.find('Disconnecting ') + len('Disconnecting ')
        #         player_name_end = content.find(' (/', player_name_start)
        #         player_name = content[player_name_start:player_name_end].strip()
        #         return player_name, player_ip

        # # 处理格式: Shusao (/127.0.0.1:25567) lost connection
        # # 有问题，以后再说
        # if "(/" in content and ":)" in content:
        #     start_index = content.find('(/') + 2
        #     end_index = content.find(')', start_index)
        #     if start_index != -1 and end_index != -1:
        #         ip_info = content[start_index:end_index]
        #         player_ip = ip_info.split(':')[0]
        #         player_name = content.split(' ')[0]
        #         return player_name, player_ip
        
    except Exception as e:
        server.logger.error(f"解析玩家信息时出错: {e}")
    return None, None

def on_unload(server: PluginServerInterface):
    save_ip_logs()
