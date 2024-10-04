#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <ESPAsyncWebServer.h>
#include <Adafruit_NeoPixel.h>

#include "web.h"

#define RGB_PIN 15
#define NUM_PIXELS 28
Adafruit_NeoPixel NeoPixel(NUM_PIXELS,RGB_PIN, NEO_GRB + NEO_KHZ800);
uint32_t randomColor = NeoPixel.Color(random(256), random(256), random(256));

const char* ssid = "TP-Link_3330"; //Enter SSID
const char* password = "raikar@123"; //Enter Password

using namespace websockets;
WebsocketsServer server;
AsyncWebServer webserver(80);

int M1value,M2value,M3value,commaIndex;

int motor1Pin1 = 14; 
int motor1Pin2 = 12;

int motor2Pin1 = 26; 
int motor2Pin2 = 25;

int motor3Pin1 = 32; 
int motor3Pin2 = 4; 

int enable1Pin = 13; 
int enable2Pin = 27; 
int enable3Pin = 33;

const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 200;

void setup()
{ 
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  pinMode(motor3Pin1, OUTPUT);
  pinMode(motor3Pin2, OUTPUT);
  pinMode(enable3Pin, OUTPUT);

  NeoPixel.begin();
  NeoPixel.setBrightness(50);
    // configure LED PWM functionalities
  ledcSetup(pwmChannel, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel);
  ledcAttachPin(enable2Pin, pwmChannel);
  ledcAttachPin(enable3Pin, pwmChannel);

  Serial.begin(9600);

  // Connect to WiFi network
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi!");

  // Print local IP address
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());

  // HTTP handler assignment
  webserver.on("/", HTTP_GET, [](AsyncWebServerRequest * request) {
    AsyncWebServerResponse *response = request->beginResponse_P(200, "text/html", index_html_gz, sizeof(index_html_gz));
    response->addHeader("Content-Encoding", "gzip");
    request->send(response);
  });

  // start server
  webserver.begin();
  server.listen(82);
  Serial.print("Is server live? ");
  Serial.println(server.available());
 
}
 
// handle http messages
void handle_message(WebsocketsMessage msg) {
  commaIndex = msg.data().indexOf(',');
  int secondCommaIndex = msg.data().indexOf(',', commaIndex + 1); // Find the index of the second comma
  M1value = msg.data().substring(0, commaIndex).toInt();
  M2value = msg.data().substring(commaIndex + 1, secondCommaIndex).toInt();
  M3value = msg.data().substring(secondCommaIndex + 1).toInt(); // Extract the third value after the second comma


  // Serial.println("MOTOR 1:");
  // Serial.println(M1value);
  // Serial.println();
  
  // Serial.println("MOTOR 2:");
  // Serial.println(M2value);
  // Serial.println();
  
  // Serial.println("MOTOR 3:");
  // Serial.println(M3value);
  // Serial.println();

  if (M1value > 0) {
    // Motor 1 forward
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    analogWrite(enable1Pin, M1value); // Set motor 1 speed
  } else if (M1value < 0) {
    // Motor 1 backward
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
    analogWrite(enable1Pin, abs(M1value)); // Set motor 1 speed
  } else {
    // Motor 1 stop
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
    analogWrite(enable1Pin, 0);
  }

   if (M2value > 0) {
    // Motor 1 forward
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
    analogWrite(enable2Pin, M2value); // Set motor 1 speed
  } else if (M2value < 0) {
    // Motor 1 backward
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
    analogWrite(enable2Pin, abs(M2value)); // Set motor 1 speed
  } else {
    // Motor 1 stop
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
    analogWrite(enable2Pin, 0);
  }

   if (M3value > 0) {
    // Motor 1 forward
    digitalWrite(motor3Pin1, HIGH);
    digitalWrite(motor3Pin2, LOW);
    analogWrite(enable3Pin, M3value); // Set motor 1 speed
  } else if (M3value < 0) {
    // Motor 1 backward
    digitalWrite(motor3Pin1, LOW);
    digitalWrite(motor3Pin2, HIGH);
    analogWrite(enable3Pin, abs(M3value)); // Set motor 1 speed
  } else {
    // Motor 1 stop
    digitalWrite(motor3Pin1, LOW);
    digitalWrite(motor3Pin2, LOW);
    analogWrite(enable3Pin, 0);
  }
  // delay(500);
  
}
 
void loop()
{ NeoPixel.clear();
    for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {           // for each pixel
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(255,0, 0));  // it only takes effect if pixels.show() is called
    NeoPixel.show();                                           // update to the NeoPixel Led Strip
    delay(10);  // 500ms pause between each pixel
  }
  auto client = server.accept();

  for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {           
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(0, 255, 0));
    NeoPixel.show();
    delay(20);
  }
  delay(1000);
  client.onMessage(handle_message);
  while (client.available()) {
    for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {           
    NeoPixel.setPixelColor(pixel, randomColor);
    }
    NeoPixel.show();
    client.poll();
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////


#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <ESPAsyncWebServer.h>
#include <Adafruit_NeoPixel.h>

#include "web.h"

#define RGB_PIN 15
#define NUM_PIXELS 28
Adafruit_NeoPixel NeoPixel(NUM_PIXELS,RGB_PIN, NEO_GRB + NEO_KHZ800);
uint32_t randomColor = NeoPixel.Color(random(256), random(256), random(256));

const char* ssid = "TP-Link_3330"; //Enter SSID
const char* password = "raikar@123"; //Enter Password

using namespace websockets;
WebsocketsServer server;
AsyncWebServer webserver(80);

int M1value,M2value,M3value,commaIndex;

int motor1Pin1 = 14; 
int motor1Pin2 = 12;

int motor2Pin1 = 26; 
int motor2Pin2 = 25;

int motor3Pin1 = 32; 
int motor3Pin2 = 4; 

int enable1Pin = 13; 
int enable2Pin = 27; 
int enable3Pin = 33;

const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 200;

void setup()
{ 
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  pinMode(motor3Pin1, OUTPUT);
  pinMode(motor3Pin2, OUTPUT);
  pinMode(enable3Pin, OUTPUT);

  NeoPixel.begin();
  NeoPixel.setBrightness(50);
    // configure LED PWM functionalities
  ledcSetup(pwmChannel, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel);
  ledcAttachPin(enable2Pin, pwmChannel);
  ledcAttachPin(enable3Pin, pwmChannel);

  Serial.begin(9600);

  // Connect to WiFi network
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi!");

  // Print local IP address
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());

  // HTTP handler assignment
  webserver.on("/", HTTP_GET, [](AsyncWebServerRequest * request) {
    AsyncWebServerResponse *response = request->beginResponse_P(200, "text/html", index_html_gz, sizeof(index_html_gz));
    response->addHeader("Content-Encoding", "gzip");
    request->send(response);
  });

  // start server
  webserver.begin();
  server.listen(82);
  Serial.print("Is server live? ");
  Serial.println(server.available());
 
}
 
// handle http messages
void handle_message(WebsocketsMessage msg) {
  commaIndex = msg.data().indexOf(',');
  int secondCommaIndex = msg.data().indexOf(',', commaIndex + 1); // Find the index of the second comma
  M1value = msg.data().substring(0, commaIndex).toInt();
  M2value = msg.data().substring(commaIndex + 1, secondCommaIndex).toInt();
  M3value = msg.data().substring(secondCommaIndex + 1).toInt(); // Extract the third value after the second comma

  if (M1value > 0) {
    // Motor 1 forward
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    analogWrite(enable1Pin, M1value); // Set motor 1 speed
  } else if (M1value < 0) {
    // Motor 1 backward
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
    analogWrite(enable1Pin, abs(M1value)); // Set motor 1 speed
  } else {
    // Motor 1 stop
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
    analogWrite(enable1Pin, 0);
  }

   if (M2value > 0) {
    // Motor 1 forward
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
    analogWrite(enable2Pin, M2value); // Set motor 1 speed
  } else if (M2value < 0) {
    // Motor 1 backward
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
    analogWrite(enable2Pin, abs(M2value)); // Set motor 1 speed
  } else {
    // Motor 1 stop
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
    analogWrite(enable2Pin, 0);
  }

   if (M3value > 0) {
    // Motor 1 forward
    digitalWrite(motor3Pin1, HIGH);
    digitalWrite(motor3Pin2, LOW);
    analogWrite(enable3Pin, M3value); // Set motor 1 speed
  } else if (M3value < 0) {
    // Motor 1 backward
    digitalWrite(motor3Pin1, LOW);
    digitalWrite(motor3Pin2, HIGH);
    analogWrite(enable3Pin, abs(M3value)); // Set motor 1 speed
  } else {
    // Motor 1 stop
    digitalWrite(motor3Pin1, LOW);
    digitalWrite(motor3Pin2, LOW);
    analogWrite(enable3Pin, 0);
  }
  // delay(500);
  
}
 
void loop()
{ NeoPixel.clear();
    for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {           // for each pixel
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(255,0, 0));  // it only takes effect if pixels.show() is called
    NeoPixel.show();                                           // update to the NeoPixel Led Strip
    delay(10);  // 500ms pause between each pixel
  }
  auto client = server.accept();

  for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {           
    NeoPixel.setPixelColor(pixel, NeoPixel.Color(0, 255, 0));
    NeoPixel.show();
    delay(20);
  }
  delay(1000);
  client.onMessage(handle_message);
  while (client.available()) {
    for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {           
    NeoPixel.setPixelColor(pixel, randomColor);
    }
    NeoPixel.show();
    client.poll();
  }
}