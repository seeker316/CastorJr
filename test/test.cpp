#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char *ssid = "TP-Link_3330";
const char *password = "raikar@123";

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/html", getPage());
  });

  // Start server
  server.begin();
}

void loop() {
  // Nothing to do here
}

String getPage() {
  String page = "<!DOCTYPE html>";
  page += "<html>";
  page += "<head>";
  page += "<title>ESP32 Joystick and Buttons</title>";
  page += "<style>";
  page += "html {";
  page += "  background-image: url('https://github.com/seeker316/CastorJr/raw/main/webserverbackground.jpg');";
  page += "  background-size: cover;";
  page += "  background-position: center;";
  page += "  height: 100%;";
  page += "}";
  page += "body {";
  page += "  font-family: 'Lucida Console', Monaco, monospace;"; /* Setting font stack to Lucida Console */
  page += "  color: white;";
  page += "  margin: 0;";
  page += "  padding: 0;";
  page += "  text-align: center;"; /* Aligning everything to the center */
  page += "}";
  page += ".container {";
  page += "  max-width: 600px;";
  page += "  margin: 0 auto;";
  page += "  padding: 40px;";
  page += "}";
  page += "h1 {";
  page += "  font-size: 48px;";
  page += "  margin-bottom: 64px;";
  page += "  font-weight: bold;"; /* Making the heading bold */
  page += "  text-align: center;"; /* Aligning text to center */
  page += "}";
  page += ".joystick-container {";
  page += "  width: 240px;";
  page += "  height: 240px;";
  page += "  border: 1px solid #ccc;";
  page += "  margin: 64px auto 48px;";
  page += "  position: relative;";
  page += "  border-radius: 50%;";
  page += "  transform: scale(1.2);";
  page += "}";
  page += "#joystick {";
  page += "  width: 100%;";
  page += "  height: 100%;";
  page += "  position: absolute;";
  page += "}";
  page += ".triangle-button {";
  page += "  width: 0;";
  page += "  height: 0;";
  page += "  border-left: 50px solid transparent;";
  page += "  border-right: 50px solid transparent;";
  page += "  border-top: 100px solid rgba(255, 255, 255, 0.5);"; /* Set transparency to match joystick */
  page += "  display: inline-block;";
  page += "  cursor: pointer;";
  page += "}";
  page += ".clockwise-button {";
  page += "  transform: rotate(90deg);"; /* Rotate clockwise button 90 degrees */
  page += "  margin-left: 20px;"; /* Adjust horizontal position */
  page += "  margin-top: 20px;"; /* Move downward */
  page += "}";
  page += ".anticlockwise-button {";
  page += "  transform: rotate(-90deg);"; /* Rotate anticlockwise button -90 degrees */
  page += "  margin-right: 20px;"; /* Adjust horizontal position */
  page += "  margin-top: 20px;"; /* Move downward */
  page += "}";
  page += "</style>";
  page += "</head>";
  page += "<body>";
  page += "<div class='container'>";
  page += "<h1>CASTOR Jr.</h1>"; // Increased margin-bottom, added bold formatting, and aligned text to center
  page += "<div class='joystick-container'>";
  page += "<div id='joystick'></div>";
  page += "</div>";
  page += "<div>";
  page += "<div class='triangle-button clockwise-button' id='clockwiseButton'></div>"; // Clockwise button
  page += "<span style='width: 20px; display: inline-block;'></span>"; // Space between buttons
  page += "<div class='triangle-button anticlockwise-button' id='anticlockwiseButton'></div>"; // Anticlockwise button
  page += "</div>";
  page += "</div>";
  page += "<script>";
  page += "function sendButton(button) {";
  page += "var xhttp = new XMLHttpRequest();";
  page += "xhttp.open('GET', '/button?btn=' + button, true);";
  page += "xhttp.send();";
  page += "}";
  page += "</script>";
  page += "<script src='https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.8.1/nipplejs.min.js'></script>";
  page += "<script>";
  page += "var options = {";
  page += "  zone: document.getElementById('joystick'),";
  page += "  mode: 'static',";
  page += "  position: { left: '50%', top: '50%' },";
  page += "  color: 'rgba(255, 255, 255, 0.5)'"; // White color with same transparency
  page += "};";
  page += "var joystick = nipplejs.create(options);";
  page += "joystick.on('move', function(evt, data) {";
  page += "  var xhttp = new XMLHttpRequest();";
  page += "  xhttp.open('GET', '/joystick?x=' + data.instance.frontPosition.x + '&y=' + data.instance.frontPosition.y, true);";
  page += "  xhttp.send();";
  page += "});";
  page += "document.getElementById('clockwiseButton').addEventListener('click', function() { sendButton(1); });";
  page += "document.getElementById('anticlockwiseButton').addEventListener('click', function() { sendButton(2); });";
  page += "</script>";
  page += "</body>";
  page += "</html>";
  return page;
}

















