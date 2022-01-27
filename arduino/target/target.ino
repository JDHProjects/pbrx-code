/* Medium example for ESP8266 (not for Arduino, uses additional Base64 layer) */
#include <Crypto.h>
#include <AES.h>
AES128 aes128;

enum command {
  UNSET,
  //P
  PLAINTEXT,
  //C
  CIPHERTEXT,
  //K
  KEY,
};

// https://the-x.cn/en-us/cryptography/Aes.aspx
byte out[16];
byte in[16];
command currentCommand;
int indexCounter;

String byteArrayToString(byte byteArray[16]){
  String hexString = "";

  for(int i = 0; i < 16; i++) {
    if(byteArray[i] < 0x10) {
      hexString += '0';
    }

    hexString += String(byteArray[i], HEX);
  }
  return hexString;
}

int charToLiteralHexValue(char c){
  if (c >= '0' && c <= '9')
    return c - '0' ;
  if (c >= 'a' && c <= 'f')
    return c - 'a' + 10 ;
  return -1;
}

void setup() {
  Serial.begin(9600);
  serialReset();
  while (!Serial);
  aes128.setKey(in, sizeof(in));
}

void serialReset(){
  currentCommand = UNSET;
  indexCounter = 0;
  memset(in,0x00,sizeof(in));
  memset(out,0x00,sizeof(out));
}


void serialEvent(){
  char currentChar = Serial.read();
  if(currentChar == '\n'){
    //Reset command if end character seen
    if(currentCommand == PLAINTEXT){
      //trigger
      aes128.encryptBlock(out, in);
      //end trigger
      Serial.print("C"+byteArrayToString(out)+"\n");
    }
    else if (currentCommand == CIPHERTEXT){
      aes128.decryptBlock(out, in);
      Serial.print("P"+byteArrayToString(out)+"\n");
    }
    else if (currentCommand == KEY){
      aes128.setKey(in, sizeof(in));
      Serial.print("K"+byteArrayToString(in)+"\n");
    }
    serialReset();
  }
  else if (currentCommand != UNSET) {
    if(indexCounter >= 32) {
      //Reset command if command too long
      serialReset();
      return;
    }
    int currentHex = charToLiteralHexValue(currentChar);
    if(currentHex == -1){
      serialReset();
      return;
    }
    if(indexCounter%2 == 0){
      in[indexCounter/2]=currentHex<<4;
    }
    else{
      in[indexCounter/2]+=currentHex;
    }
    indexCounter++;
  }
  else if (currentChar == 'P') {
    currentCommand = PLAINTEXT;
  }
  else if (currentChar == 'C') {
    currentCommand = CIPHERTEXT;
  }
  else if (currentChar == 'K') {
    currentCommand = KEY;
  }
}


void loop(){
}
