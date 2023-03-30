import pymem
import time

dwLocalPlayer = 0xDC14CC
dwEntityList = 0x4DDD93C
dwGlowObjectManager = 0x5326638
m_iGlowIndex = 0x10488
m_iTeamNum = 0xF4

pm = pymem.Pymem('csgo.exe')
    
client = pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll


def glowmodule():
    while True:
        glow = pm.read_int(client + dwGlowObjectManager)
        player = pm.read_int(client + dwLocalPlayer)
        localTeam = pm.read_int(player+m_iTeamNum)
        time.sleep(0.001)
        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entityglowing = pm.read_int(entity + m_iGlowIndex)
                entity_id = pm.read_int(entity + m_iTeamNum)
                player = pm.read_int(client + dwLocalPlayer)
                localTeam = pm.read_int(player+m_iTeamNum)
                if entity_id != localTeam:
                    pm.write_float(glow + entityglowing * 0x38 + 0x8, float(0))
                    pm.write_float(glow + entityglowing * 0x38 + 0xC, float(1))
                    pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))
                    pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                    pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)

def main():
    glowmodule()

if __name__ == '__main__':
    main()
