# -*- coding: utf-8 -*-
from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass
import time  # 导入time模块，用于时间相关操作

@registerGenericClass("TeamPlugin")
class TeamPlugin(PartBase):
    def __init__(self):
        super(TeamPlugin, self).__init__()
        self.name = "Team Plugin"
        self.pending_invites = {}  # 存储待处理的组队邀请
        self.teams = {}  # 存储玩家和队伍的映射
        self.team_members = {}  # 存储每个队伍的成员

    def InitServer(self):
        import mod.server.extraServerApi as serverApi
        serverSystem = serverApi.GetSystem("Minecraft", "preset")
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerInteractEvent", self, self.on_player_interact)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerMessageEvent", self, self.on_player_message)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerLogoutEvent", self, self.on_player_logout)
        serverSystem.ScheduleTask(self.check_invites, 60, repeat=True)

    def OnServerChat(self, args):
        pass

    def on_player_interact(self, event):
        player = event['player']
        target = event['target_player']
        if target and player != target:
            self.send_invite(player, target)

    def send_invite(self, player, target):
        import mod.server.extraServerApi as serverApi
        player_id = player['uuid']
        target_id = target['uuid']

        self.pending_invites[target_id] = {
            'inviter_id': player_id,
            'timestamp': time.time(),
            'handled': False
        }

        self.send_message(player_id, f"组队邀请已发送给 {target['name']}")
        self.send_message(target_id, f"{player['name']} (等级: {player['level']}) 邀请你组队，输入 yes 或 no 来接受或拒绝。")

    def send_message(self, playerId, message):
        import mod.server.extraServerApi as serverApi
        player = serverApi.GetPlayerByUUID(playerId)
        if player:
            player.SendChatMessage(message)

    def on_player_message(self, event):
        player = event['player']
        message = event['message'].strip().lower()
        player_id = player['uuid']

        if player_id in self.pending_invites:
            invite = self.pending_invites[player_id]

            if not invite['handled']:
                inviter_id = invite['inviter_id']
                inviter = self.get_player(inviter_id)

                if message == 'yes':
                    if inviter:
                        self.send_message(inviter_id, f"{player['name']} 接受了你的组队邀请！")
                        self.send_message(player_id, f"你已加入 {inviter['name']} 的队伍！")

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
                    if inviter:
                        self.send_message(inviter_id, f"{player['name']} 拒绝了你的组队邀请。")
                        self.send_message(player_id, f"你拒绝了 {inviter['name']} 的组队邀请。")
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
                        self.send_message(member_id, "你的队伍已解散，因为人数不足。")
                    self.team_members.pop(team_id, None)

    def check_invites(self):
        current_time = time.time()
        expired_invites = [player_id for player_id, invite in self.pending_invites.items()
                           if current_time - invite['timestamp'] > 60]

        for player_id in expired_invites:
            player = self.get_player(player_id)
            if player:
                self.send_message(player_id, "你的组队邀请已超时。")
            self.pending_invites.pop(player_id, None)

    def get_player(self, playerId):
        import mod.server.extraServerApi as serverApi
        return serverApi.GetPlayerByUUID(playerId)

    def DestroyServer(self):
        import mod.server.extraServerApi as serverApi
        serverSystem = serverApi.GetSystem("Minecraft", "preset")
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerInteractEvent", self, self.on_player_interact)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerMessageEvent", self, self.on_player_message)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerLogoutEvent", self, self.on_player_logout)
    def InitServer(self):
        import mod.server.extraServerApi as serverApi
        serverSystem = serverApi.GetSystem("Minecraft", "preset")
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerInteractEvent", self, self.on_player_interact)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerMessageEvent", self, self.on_player_message)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerLogoutEvent", self, self.on_player_logout)
        serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerAttackEntityEvent", self, self.on_player_attack)
        serverSystem.ScheduleTask(self.check_invites, 60, repeat=True)

    def on_player_attack(self, event):
        attacker_id = event['attacker']
        target_id = event['target']
        if attacker_id in self.teams and target_id in self.teams:
            if self.teams[attacker_id] == self.teams[target_id]:
                event.Cancel()  # 取消攻击事件
                self.send_message(attacker_id, "你不能攻击你的队友。")
    def DestroyServer(self):
        import mod.server.extraServerApi as serverApi
        serverSystem = serverApi.GetSystem("Minecraft", "preset")
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerInteractEvent", self, self.on_player_interact)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerMessageEvent", self, self.on_player_message)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerLogoutEvent", self, self.on_player_logout)
        serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerAttackEntityEvent", self, self.on_player_attack)
