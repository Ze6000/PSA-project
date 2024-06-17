#include <WiFi.h>

#define SSID "Beatriz's Galaxy S22"
#define PASSWD "ddgg2208"

unsigned long int last_time = millis();

const uint16_t port = 90;
const char *host = "193.137.172.20";

// Commands to send to robot
const char *action[4] = {"movej([-0.2313, -1.8350, 2.0363, -1.7614, 4.7199, -0.2670], a=1.0, v=0.5) \n", "movej([-0.2321, -1.3067, 2.3631, -2.5958, 4.7999, -0.2319], a=1.0, v=0.5) \n", "movej([-2.1749, -2.0431, 2.4363, -1.9733, 4.7789, -0.5318], a=1.0, v=0.5) \n", "movej([-3.5826, -1.3708, 2.4033, -2.5944, 4.7721, -0.5318], a=1.0,v=0.5)\n"};
int a = 0;
int t_delay = 5500;
const int sensorPin = 26;

bool connected = false;
WiFiClient client;

bool sensorAtivo = false;
bool objetoDetectado = false;

void setup()
{
    //ligações do robô
    Serial.begin(115200);

    WiFi.begin(SSID, PASSWD);
    while (WiFi.status() != WL_CONNECTED){
        delay(100);}

    Serial.print("IP: ");
    Serial.println(WiFi.localIP());

    //ligações do sensor capacitivo
    pinMode(sensorPin, INPUT);



}

void loop(){
  if (!connected){
    if (!client.connect(host, port)){
        Serial.println("Falha de conexao");
        delay(1000);
        return;}
    else{
        Serial.println("Conectado");
        connected = true;}
  }
  //ler o que o sensor está a detetar
  //valores elevados -> não está a detetar
  //valores baixos -> está a detetar

  //código para ler o valor do sensor
  int sensorValue = digitalRead(sensorPin);
  // Serial.println(sensorValue);

  if (sensorValue == 0 && !objetoDetectado){
    // Detetou o objeto pela primeira vez
    objetoDetectado = true;
    Serial.println("Object detected. Preparing robot.");}
  
  else if (sensorValue == 0 && objetoDetectado){
    // à espera que o objeto saia do sensor
    Serial.println("Waiting for the object to pass the sensor.");}

  else if (sensorValue == 1 && objetoDetectado){
    // O objeto foi detetado e agora o sensor vai deixar de detetar o objeto
    Serial.println("Executing robot...");
    sensorAtivo = true;}

  else if (sensorValue == 1 && !objetoDetectado){
    // O objeto não está a ser detetado ou não está mais presente
    Serial.println("Waiting for new object.");
    sensorAtivo = false;
  }
  else{
    Serial.println("Something unexpected went wrong. Please try again.");
    sensorAtivo = false;
    objetoDetectado = false;
  }

  if (sensorAtivo){
    //ligação do robô
    for (int a = 0; a < 4; a++){
        client.print(action[a]);
        //Serial.println(action[a]);
        delay(t_delay); // Espera um tempo entre os comandos
    }
    Serial.println("Program completed. Waiting for the new object.");
    objetoDetectado = false;
  }

  delay(700);
}



