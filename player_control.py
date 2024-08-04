# -*- coding: utf-8 -*-
from mcdreforged.api.all import *
import json
import os

PLUGIN_METADATA = {
    'id': 'player_control',
    'version': '1.0.0',
    'name': 'Player Control',
    'description': '召唤和删除假人的插件',
    'author': 'Shusao & GPT-4'
}

config_dir = './config/player_control'
op_file = os.path.join(config_dir, 'player_ops.json')
dummy_file = os.path.join(config_dir, 'dummy_list.json')

DEFAULT_COORDS = (0, 1000, 0)
waiting_for_join = {}

def on_load(server: PluginServerInterface, prev_module):
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(op_file):
        with open(op_file, 'w') as f:
            json.dump([], f)
    if not os.path.exists(dummy_file):
        with open(dummy_file, 'w') as f:
            json.dump({}, f)

    server.register_command(
        Literal('!!player')
        .then(
            Literal('spawn')
            .then(
                Text('id')
                .runs(lambda src, ctx: spawn_dummy(src, ctx, DEFAULT_COORDS))
                .then(
                    Text('x')
                    .then(
                        Text('y')
                        .then(
                            Text('z')
                            .runs(lambda src, ctx: spawn_dummy_with_coords(src, ctx))
                        )
                    )
                )
            )
        )
        .then(
            Literal('kill')
            .then(
                Text('id')
                .runs(lambda src, ctx: kill_dummy(src, ctx))
            )
        )
        .then(
            Literal('op')
            .then(
                Text('player')
                .runs(lambda src, ctx: op_player(src, ctx))
            )
        )
        .then(
            Literal('deop')
            .then(
                Text('player_id')
                .runs(lambda src, ctx: deop_player(src, ctx))
            )
        )
    )

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def is_player_op(player_id):
    ops = load_json(op_file)
    return player_id in ops

def op_player(src, ctx):
    if src.has_permission(4):
        player_id = ctx['player']
        ops = load_json(op_file)
        if player_id not in ops:
            ops.append(player_id)
            save_json(op_file, ops)
            src.reply(f'{player_id} 已被赋予召唤假人权限')
        else:
            src.reply(f'{player_id} 已经拥有权限')
    else:
        src.reply('你没有权限执行该命令')

def deop_player(src, ctx):
    if src.has_permission(4):
        player_id = ctx['player_id']
        ops = load_json(op_file)
        if player_id in ops:
            ops.remove(player_id)
            save_json(op_file, ops)
            src.reply(f'{player_id} 的召唤假人权限已被移除')
        else:
            src.reply(f'{player_id} 不在权限列表中')
    else:
        src.reply('你没有权限执行该命令')

def spawn_dummy(src, ctx, coords):
    player_id = ctx['id'].lower()
    if is_player_op(src.player):
        x, y, z = coords
        command = f'/player {player_id} spawn at {x} {y} {z}'
        server = src.get_server()
        server.execute(command)
        src.reply(f'已在坐标 {x} {y} {z} 召唤假人 {player_id}')

        dummies = load_json(dummy_file)
        dummies[player_id] = {'x': x, 'y': y, 'z': z, 'summoner': src.player}
        save_json(dummy_file, dummies)

        waiting_for_join[player_id] = src.player
    else:
        src.reply('你没有权限召唤假人')

def spawn_dummy_with_coords(src, ctx):
    player_id = ctx['id'].lower()
    if is_player_op(src.player):
        x = ctx['x']
        y = ctx['y']
        z = ctx['z']
        command = f'/player {player_id} spawn at {x} {y} {z}'
        server = src.get_server()
        server.execute(command)
        src.reply(f'已在坐标 {x} {y} {z} 召唤假人 {player_id}')

        dummies = load_json(dummy_file)
        dummies[player_id] = {'x': x, 'y': y, 'z': z, 'summoner': src.player}
        save_json(dummy_file, dummies)

        waiting_for_join[player_id] = src.player
    else:
        src.reply('你没有权限召唤假人')

def check_dummy_joined(server, player_id, log_line):
    if f'{player_id} joined the game'.lower() in log_line.lower():
        summoner = waiting_for_join.pop(player_id, None)
        if summoner:
            tp_command = f'/tp {player_id} {summoner}'
            server.execute(tp_command)
            server.logger.info(f'假人 {player_id} 已传送到召唤者 {summoner}')

def kill_dummy(src, ctx):
    player_id = ctx['id'].lower()
    if is_player_op(src.player):
        command = f'/player {player_id} kill'
        server = src.get_server()
        server.execute(command)
        src.reply(f'假人 {player_id} 已被删除')

        dummies = load_json(dummy_file)
        if player_id in dummies:
            del dummies[player_id]
            save_json(dummy_file, dummies)
    else:
        src.reply('你没有权限删除假人')

def on_info(server: PluginServerInterface, info: Info):
    for player_id in list(waiting_for_join):
        check_dummy_joined(server, player_id, info.content)

def on_unload(server: PluginServerInterface):
    server.logger.info("Player Control 插件已卸载")