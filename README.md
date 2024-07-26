## 公告
> 2024/1/14
> - PFingan服务器已宣布关服，本插件将面临可能无限期的停更

# PF-Logging
> `PF-Logging`是为MCDReforged（一个Minecraft服务器插件框架）开发的插件，用于高效地记录、查询和管理服务器日志。提供了API功能，允许其它插件调用，实现了对日志内容的动态检索，以及通过执行Minecraft命令来获取反馈结果。此外，还支持在游戏内直接查询日志，为管理员提供了便利。

**特别鸣谢** ： ChatGPT-4.0


[![页面浏览量计数](https://badges.toozhao.com/badges/01HA948ZWH9JWY2DVPHEXXRD0E/green.svg)](/)
[![查看次数起始时间](https://img.shields.io/badge/查看次数统计起始于-2023/9/14-1?style=flat-square)](/)
[![仓库大小](https://img.shields.io/github/repo-size/LoosePrince/PF-Logging?style=flat-square&label=仓库占用)](/)
[![最新版](https://img.shields.io/github/v/release/LoosePrince/PF-Logging?style=flat-square&label=最新版)](https://github.com/LoosePrince/PF-Logging/releases/latest/download/PF-Logging.py)
[![Issues](https://img.shields.io/github/issues/LoosePrince/PF-Logging?style=flat-square&label=Issues)](https://github.com/LoosePrince/PF-Logging/issues)
[![已关闭issues](https://img.shields.io/github/issues-closed/LoosePrince/PF-Logging?style=flat-square&label=已关闭%20Issues)](https://github.com/LoosePrince/PF-Logging/issues?q=is%3Aissue+is%3Aclosed)
[![下载量](https://img.shields.io/github/downloads/LoosePrince/PF-Logging/total?style=flat-square&label=下载量)](https://github.com/LoosePrince/PF-Logging/releases)
[![最新发布下载量](https://img.shields.io/github/downloads/LoosePrince/PF-Logging/latest/total?style=flat-square&label=最新版本下载量)](https://github.com/LoosePrince/PF-Logging/releases/latest) 

## 插件功能

- **自动日志记录**：监听服务器的信息流，自动记录日志。
- **日志查询**：支持通过API和游戏内命令查询日志内容及其上下文。
- **命令执行与反馈**：允许通过API执行Minecraft命令并获取执行结果。
- **配置灵活**：提供配置文件，允许自定义日志记录的级别、长度等参数。
- **游戏内命令支持**：允许管理员在游戏内使用`!log`和`!log_id`命令查询日志。

### 使用方法

- **游戏内命令**：
  - `!log`：显示最近的日志条目。
  - ![image](https://github.com/user-attachments/assets/c49af5f1-eca9-4b97-9f4a-596fb33986fa) 
  - `#log_id <log_id>`：根据日志编号查询特定的日志内容。
  - ![image](https://github.com/user-attachments/assets/d7795fa6-a722-46d4-b211-7cf547f245fb)

## 安装教程

1. **下载插件**：将`PF-Logging.py`文件下载到服务器的`plugins`目录下。
2. **配置插件**：根据需要编辑`config/PF_Logging/config.yml`文件，调整日志记录的级别、长度等参数。
3. **重启插件**：重启插件后就会启动插件

## 注意

- 配置文件`config.yml`必须放在`config/PF_Logging`目录下，确保插件能正确读取配置。
- 根据服务器的权限设置，可能需要调整`#log`命令的权限级别。
- 为避免性能问题，合理设置日志保留长度。

## 插件API开发方法

### `get_logs_containing(content: str)`

- **用途**：获取包含指定内容的所有日志条目。
- **参数**：
  - `content`：字符串，需要在日志中查找的内容。
- **返回值**：包含所有匹配指定内容的日志条目的列表。

### `execute_command_and_get_result(server: PluginServerInterface, command: str)`

- **用途**：在Minecraft服务器上执行指定的命令并获取执行结果。
- **参数**：
  - `server`：`PluginServerInterface`，MCDReforged服务器实例。
  - `command`：字符串，要执行的Minecraft命令。
- **返回值**：命令执行的结果字符串。

### `get_log_by_id(log_id: int)`

- **用途**：根据日志编号获取特定的日志内容。
- **参数**：
  - `log_id`：整数，要查询的日志编号。
- **返回值**：一个字典，包含日志编号和内容。如果未找到指定编号的日志，则返回`None`。

# 有bug或是新的idea
如果需要更多联动或提交想法和问题请提交 [issues](https://github.com/LoosePrince/PF-Logging/issues) 或 QQ [1377820366](http://wpa.qq.com/msgrd?v=3&uin=1377820366&site=qq&menu=yes) 提交！ <br />
视情况添加，请勿联系他人！

# 使用条款
- 禁止声明为你原创
- 禁止商业服使用、盈利等
- 禁止售卖
- 允许二次创作，但请标明来源
