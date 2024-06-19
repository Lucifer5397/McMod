# -*- coding: utf-8 -*-
from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass


@registerGenericClass("TutorialPart")
class TutorialPart(PartBase):
	def __init__(self):
		super(TutorialPart, self).__init__()
		self.name = "Super的示例项目"

	def InitClient(self):
		pass

	def InitServer(self):
		import mod.server.extraServerApi as serverApi
		serverSystem = serverApi.GetSystem("Minecraft", "preset")
		# 监听实体受攻击
		serverSystem.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.OnDamageEvent)

	def OnDamageEvent(self, dats):
		# 实体攻击检测, 爆炸
		# 这是监听实体受到攻击的函数
		import mod.server.extraServerApi as serverApi
		src_id = dats["srcId"] # 实体受伤来源 id
		entity_id = dats["entityId"] # 受伤的实体 id
		fac = serverApi.GetEngineCompFactory()
		entityPos = fac.CreatePos(entity_id).GetPos() # 实体的坐标
		pname = fac.CreateName(src_id).GetName() # 伤害来源的名字, 如果不是玩家, 则会返回 None
		if not pname: # 排除非玩家攻击
			return
		# 产生爆炸
		res = fac.CreateExplosion(serverApi.GetLevelId()).CreateExplosion(
			entityPos,
			10,
			False,
			False,
			entity_id,
			src_id
		)
		print ("EXPLOSION " + str(res))

	def TickClient(self):
		pass

	def TickServer(self):
		pass

	def DestroyClient(self):
		pass

	def DestroyServer(self):
		import mod.server.extraServerApi as serverApi
		serverSystem = serverApi.GetSystem("Minecraft", "preset")
		# 解除监听实体受攻击
		serverSystem.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.OnDamageEvent)

# Super 自己挖的 API 表

"""
AddEntityTickEventWhiteList
CreateComponent
DestroyComponent
GenerateColor
GetBtNodeCls
GetBtStatusEnum
GetComponent
GetComponentCls
GetCustomGoalCls
GetDirFromRot
GetEngineActor
GetEngineCompFactory
GetEngineNamespace
GetEngineSystemName
GetEntityLimit
GetLevelId
GetLocalPosFromWorld
GetMcpModLogCanPostDump
GetMinecraftEnum
GetPlatform
GetPlayerList
GetRotFromDir
GetServerSystemCls
GetServerTickTime
GetSystem
GetUseEventTuple
GetWorldPosFromLocal
ImportModule
IsInApollo
IsInServer
NeedsUpdate
PostMcpModDump
RegisterCmd
RegisterComponent
RegisterSystem
SetArenaGameResult
SetArenaGameStart
SetEntityLimit
SetEscapedWhiteList
SetMcpModLogCanPostDump
SetUseEventTuple
StartCoroutine
StartMemProfile
StartMultiProfile
StartProfile
StartRecordEvent
StartRecordPacket
StartRecordPythonEvent
StopCoroutine
StopMemProfile
StopMultiProfile
StopProfile
StopRecordEvent
StopRecordPacket
StopRecordPythonEvent
TutorialServerInit_exceptV
UnRegisterCmd
__builtins__
__doc__
__file__
__name__
__package__
__pathname__
_doing_record_event
_doing_record_packet
_flameGraphS
_memFlameGraph
colorUtil
conf
engineCompFactoryServer
enum
game
gameConfig
game_ruler
getEntitiesOrBlockFromRay
logger
server_entity_module
serverlevel
======== 2 ===========
CreateAchievement
CreateAction
CreateActorCollidable
CreateActorLoot
CreateActorMotion
CreateActorOwner
CreateActorPushable
CreateAiCommand
CreateAttr
CreateAuxValue
CreateBiome
CreateBlock
CreateBlockEntity
CreateBlockEntityData
CreateBlockInfo
CreateBlockState
CreateBlockUseEventWhiteList
CreateBreath
CreateBulletAttributes
CreateChatExtension
CreateChestBlock
CreateChunkSource
CreateCollisionBox
CreateCommand
CreateControlAi
CreateDimension
CreateEffect
CreateEngineType
CreateEntityComponent
CreateEntityDefinitions
CreateEntityEvent
CreateExp
CreateExplosion
CreateExtraData
CreateFeature
CreateFly
CreateGame
CreateGameplay
CreateGravity
CreateHttp
CreateHurt
CreateInteract
CreateItem
CreateItemBanned
CreateLoot
CreateLv
CreateMobSpawn
CreateModAttr
CreateModel
CreateMoveTo
CreateMsg
CreateName
CreatePersistence
CreatePet
CreatePlayer
CreatePortal
CreatePos
CreateProjectile
CreateRecipe
CreateRedStone
CreateRide
CreateRot
CreateScale
CreateShareables
CreateSystemAudio
CreateTag
CreateTame
CreateTime
CreateWeather
__class__
__delattr__
__dict__
__doc__
__format__
__getattribute__
__hash__
__init__
__module__
__new__
__reduce__
__reduce_ex__
__repr__
__setattr__
__sizeof__
__str__
__subclasshook__
__weakref__
"""