"""
<plugin key="rest980-domoticz" name="iRobot Roomba (rest980-domoticz)" version="0.0.1">
    <description>
      Simple plugin to manage iRobot Roomba
      <br/>
    </description>
    <params>
        <param field="Address" label="IP Address" width="300px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="300px" required="true" default="3000"/>

        <param field="Mode1" label="Off action" width="300px">
            <options>
                <option label="Turn off" value="0"/>
                <option label="Go to dock" value="1" default="true" />
            </options>
        </param>

    </params>
</plugin>
"""
import Domoticz
import requests

class BasePlugin:
    def __init__(self):
        return

    def onStart(self):
        iUnit = -1
        for Device in Devices:
            try:
                if (Devices[Device].DeviceID.strip() == "iRobot-Roomba"):
                    iUnit = Device
                    break
            except:
                pass
        if iUnit<0: # if device does not exists in Domoticz, than create it
            try:
                iUnit = 0
                for x in range(1,256):
                    if x not in Devices:
                        iUnit=x
                        break
                if iUnit==0:
                    iUnit=len(Devices)+1
                Domoticz.Device(Name="iRobot-Roomba", Unit=iUnit,TypeName="Switch",Used=1,DeviceID="iRobot-Roomba").Create()
            except Exception as e:
                Domoticz.Debug(str(e))
                return False

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        #Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        iUnit = -1
        for Device in Devices:
            try:
                if (Devices[Device].DeviceID.strip() == "iRobot-Roomba"):
                    iUnit = Device
                    break
            except:
                pass

        if(str(Command) == "On"):
            r = requests.get('http://'+str(Parameters["Address"])+':'+str(Parameters["Port"])+'/api/local/action/start')
            Devices[iUnit].Update(nValue=1,sValue="On")
        else:
            if(str(Parameters["Mode1"]) == "1"):
                r = requests.get('http://'+str(Parameters["Address"])+':'+str(Parameters["Port"])+'/api/local/action/stop')
                r = requests.get('http://'+str(Parameters["Address"])+':'+str(Parameters["Port"])+'/api/local/action/dock')
            else:
                r = requests.get('http://'+str(Parameters["Address"])+':'+str(Parameters["Port"])+'/api/local/action/stop')
            Devices[iUnit].Update(nValue=0,sValue="On")
        if(r.status_code == requests.codes.ok):
            return True
        else:
            return False

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
