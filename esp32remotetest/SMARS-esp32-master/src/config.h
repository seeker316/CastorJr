const char* ssid = "ESP32_ROBv1"; //Enter SSID
const char* password = "yourpasswd"; //Enter Password
 
using namespace websockets;
WebsocketsServer server;
AsyncWebServer webserver(80);

int LValue, RValue, commaIndex;