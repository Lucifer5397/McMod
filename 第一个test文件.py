"""
文件名称: 第一个test文件.py
作者名称: 彭镜文

介绍:
这是一个脚本，一个简易的组队系统

Python版本：
Python3.9

用法:
命令行键入：python 第一个test文件.py
"""
import time
from threading import Timer


class TeamPlugin:
    def __init__(self, mod):
        self.mod = mod
        self.pending_invites = {}
        self.teams = {}
        self.team_members = {}
        self.mod.register_event('player_interact', self.on_player_interact)
        self.mod.register_event('player_message', self.on_player_message)
        self.mod.register_event('player_logout', self.on_player_logout)
        self.mod.schedule_task(self.check_invites, 60, repeat=True)
        self.mod.schedule_task(self.check_teams, 60, repeat=True)

    def on_player_interact(self, event):
        player = event['player']
        target = event['target_player']
        if target and player != target:
            self.send_invite(player, target)

    def send_invite(self, player, target):
        player_id = player['uuid']
        target_id = target['uuid']
        self.pending_invites[target_id] = {
            'inviter_id': player_id,
            'timestamp': time.time(),
            'handled': False
        }
        player.send_message(f"组队邀请已发送给 {target['name']}")
        target.send_message(f"{player['name']} (等级: {player['level']}) 邀请你组队，输入 yes 或 no 来接受或拒绝。")

    def on_player_message(self, event):
        player = event['player']
        message = event['message'].strip().lower()
        player_id = player['uuid']
        if player_id in self.pending_invites:
            invite = self.pending_invites[player_id]
            if not invite['handled']:
                if message == 'yes':
                    inviter_id = invite['inviter_id']
                    inviter = self.mod.get_player(inviter_id)
                    if inviter:
                        inviter.send_message(f"{player['name']} 接受了你的组队邀请！")
                        player.send_message(f"你已加入 {inviter['name']} 的队伍！")
                        if inviter_id not in self.teams:
                            team_id = inviter_id
                            self.team_members[team_id] = [inviter_id]
                            self.teams[inviter_id] = team_id
                        else:
                            team_id = self.teams[inviter_id]
                        self.teams[player_id] = team_id
                        self.team_members[team_id].append(player_id)
                    invite['handled'] = True
                elif message == 'no':
                    inviter = self.mod.get_player(invite['inviter_id'])
                    if inviter:
                        inviter.send_message(f"{player['name']} 拒绝了你的组队邀请。")
                        player.send_message(f"你拒绝了 {inviter['name']} 的组队邀请。")
                    invite['handled'] = True

    def on_player_logout(self, event):
        player_id = event['player']['uuid']
        self.pending_invites.pop(player_id, None)
        if player_id in self.teams:
            team_id = self.teams.pop(player_id, None)
            if team_id in self.team_members:
                self.team_members[team_id].remove(player_id)
                if len(self.team_members[team_id]) < 2:
                    for member_id in self.team_members[team_id]:
                        self.teams.pop(member_id, None)
                        member = self.mod.get_player(member_id)
                        if member:
                            member.send_message("你的队伍已解散，因为人数不足。")
                    self.team_members.pop(team_id, None)

    def check_invites(self):
        current_time = time.time()
        expired_invites = [player_id for player_id, invite in self.pending_invites.items()
                           if current_time - invite['timestamp'] > 60]
        for player_id in expired_invites:
            player = self.mod.get_player(player_id)
            if player:
                player.send_message("你的组队邀请已超时。")
            self.pending_invites.pop(player_id, None)

    def check_teams(self):
        for team_id, members in list(self.team_members.items()):
            if len(members) < 2:
                for member_id in members:
                    self.teams.pop(member_id, None)
                    member = self.mod.get_player(member_id)
                    if member:
                        member.send_message("你的队伍已解散，因为人数不足。")
                self.team_members.pop(team_id, None)

