import subprocess

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

WEB_OS_SUCCESS_RETURN_VALUE = "'returnValue': True"
WEB_OS_IP = "192.168.50.196"
WEB_OS_API_SUCCESS = "nice"
WEB_OS_API_ERROR = "no"


def execute_command(command, value=""):
    result = subprocess.Popen(f"bscpylgtvcommand {WEB_OS_IP} {command} {value}", shell=True,
                              stdout=subprocess.PIPE).stdout.read()
    return str(result)


def is_webos_success(result):
    return WEB_OS_SUCCESS_RETURN_VALUE in str(result)


def command_api_handler(command, value=""):
    if is_webos_success(execute_command(command, value)):
        return WEB_OS_API_SUCCESS, 200
    return WEB_OS_API_ERROR, 500


def get_api_handler(command):
    return execute_command(command), 200


class WebOSPowerGetState(Resource):
    def get(self):
        return get_api_handler("get_power_state")


class WebOSPowerOn(Resource):
    def get(self):
        return command_api_handler("power_on")


class WebOSPowerOff(Resource):
    def get(self):
        return command_api_handler("power_off")


class WebOSScreenOff(Resource):
    def get(self):
        return command_api_handler("turn_screen_off")


class WebOSScreenOn(Resource):
    def get(self):
        return command_api_handler("turn_screen_on")


class WebOSAudioGetStatus(Resource):
    def get(self):
        return get_api_handler("get_audio_status")


class WebOSAudioSetVolume(Resource):
    def get(self, volume_value_str):
        volume_value = int(volume_value_str)
        if volume_value < 0 or volume_value > 100:
            return WEB_OS_API_ERROR, 400
        return command_api_handler("set_volume", volume_value_str)


class WebOSAudioGetVolume(Resource):
    def get(self):
        return get_api_handler("get_volume")


class WebOSAudioMute(Resource):
    def get(self):
        return command_api_handler("set_mute", "true")


class WebOSAudioUnmute(Resource):
    def get(self):
        return command_api_handler("set_mute", "false")


class WebOSAudioGetMuted(Resource):
    def get(self):
        return get_api_handler("get_muted")


class WebOSSystemGetSoftwareInfo(Resource):
    def get(self):
        return get_api_handler("get_software_info")


class WebOSSystemGetSystemInfo(Resource):
    def get(self):
        return get_api_handler("get_system_info")


class WebOSSystemGetConfigs(Resource):
    def get(self):
        return get_api_handler("get_configs")


class WebOSAppsGetApps(Resource):
    def get(self):
        # "get_apps_all" includes hidden ones, "get_apps" for regular ones
        return get_api_handler("get_apps_all")


class WebOSAppsGetCurrentApp(Resource):
    def get(self):
        return get_api_handler("get_current_app")


class WebOSMiscSendMessage(Resource):
    def get(self, message_text):
        if len(message_text) == 0:
            return WEB_OS_API_ERROR, 400
        return command_api_handler("send_message", message_text)


api.add_resource(WebOSPowerGetState, '/lg/get-state')
api.add_resource(WebOSPowerOn, '/lg/on')
api.add_resource(WebOSPowerOff, '/lg/off')

api.add_resource(WebOSScreenOff, '/lg/screen-off')
api.add_resource(WebOSScreenOn, '/lg/screen-on')

api.add_resource(WebOSAudioGetStatus, '/lg/get-audio-status')
api.add_resource(WebOSAudioSetVolume, '/lg/set-volume/<string:volume_value_str>')
api.add_resource(WebOSAudioGetVolume, '/lg/get-volume')
api.add_resource(WebOSAudioUnmute, '/lg/unmute')
api.add_resource(WebOSAudioMute, '/lg/mute')
api.add_resource(WebOSAudioGetMuted, '/lg/get-muted')

api.add_resource(WebOSSystemGetSoftwareInfo, '/lg/get-software-info')
api.add_resource(WebOSSystemGetSystemInfo, '/lg/get-system-info')
api.add_resource(WebOSSystemGetConfigs, '/lg/get-configs')

api.add_resource(WebOSAppsGetApps, '/lg/get-apps')
api.add_resource(WebOSAppsGetCurrentApp, '/lg/get-current-app')

api.add_resource(WebOSMiscSendMessage, '/lg/send-notification/<string:message_text>')

if __name__ == '__main__':
    app.run(debug=False)
