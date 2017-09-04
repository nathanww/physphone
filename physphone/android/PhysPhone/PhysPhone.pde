

import ketai.camera.*;
import android.view.WindowManager;
import android.view.View;
import android.os.Bundle;
import cassette.audiofiles.SoundFile;
import ketai.sensors.*;
PImage buffer;
KetaiCamera cam;
boolean camConfigSet=false;
int startTime;
int lastAq=0;
float total=0;
float count=0;
int samples=0;
boolean lightstatus=true;
String urltarget="";


KetaiSensor accel;
SoundFile highbeep;
SoundFile lowbeep;
int totalRounds=0;
int streamid;
float acX,acY,acZ;
void onCreate(Bundle bundle) 
{
  super.onCreate(bundle);
  // fix so screen doesn't go to sleep when app is active
  getActivity().getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
}

void setup() {
  orientation(PORTRAIT);
fullScreen();

   highbeep = new SoundFile(this, "highbeep.mp3"); 
   lowbeep = new SoundFile(this, "lowbeep.mp3");
  
  imageMode(CENTER);
  textSize(70);
  cam = new KetaiCamera(this, 640, 480, 24);
  cam.enableFlash();
  cam.start();
  startTime=millis();
 streamid=int(random(1,20000));
  accel = new KetaiSensor(this);
  accel.start();
  
}

void draw() {

  if(cam != null && cam.isStarted() && lightstatus) {
    image(cam, width/2, height/2, width*2, height*2);
    if (millis() > startTime+5000 && !camConfigSet){
      camConfigSet=true;
      cam.manualSettings(); //try to lock autofocus and exposure so it doesn't djust itself in the middle of recording
}

buffer=cam.get();
buffer.loadPixels();
buffer.updatePixels();for (int i=0; i< 640*480; i++) {
  total=total+red(buffer.pixels[i]);
  count=count+1;
}
//print(total/count);
if (millis() - lastAq >= 250) {
  samples++;
  totalRounds++;
  int trigger=0;
  if (totalRounds == 40) {
    totalRounds=0;
    float stimulus=random(10)+1;
    if (stimulus > 8) {
      trigger=2;
      highbeep.play();
    }
    else {
      trigger=1;
      lowbeep.play();
    }
  }
  
  lastAq=millis();
  //multithreaded method, ensures a constant sample rate but data frames may arrive out of order and/or duplicated.
  urltarget="http://biostream-1024.appspot.com/sendStream?streamname="+streamid+"&rawdata="+(total/count)+"&trigger="+trigger+"&sample="+samples+"&xacc="+acX+"&yacc="+acY+"&zacc="+acZ;
  thread("netSend");
  //direct strema method, simpler reading but the sampling rate will vary depending on network speed.
 // loadStrings("http://biostream-1024.appspot.com/sendStream?streamname=1&rawdata="+(total/count)+"&trigger="+trigger+"&sample="+totalRounds);
  total=0;
  count=0;
  
}



}
  else
    {
      background(128);
      text("Recording paused\nTap to resume.", 100, height/2);
    }
    
    fill(0);
rect(0,0,displayWidth,300);
fill(255);
text("Stream ID:"+streamid,10,90);
    
}

void onCameraPreviewEvent()
{
  cam.read();
}


void onPause() {
  
  super.onPause();
  

  cam.disableFlash();
  cam.stop();
  cam.dispose();
  System.exit(0);
     
  
}



void onStop() {
  

   super.onStop();
  cam.disableFlash();
  cam.stop();
  cam.dispose();
  System.exit(0);
 
  
}

void mousePressed() {
  if(cam == null)
    return;
    if (lightstatus) {
      cam.disableFlash();
    }
    else {
      cam.enableFlash();
    }
    lightstatus=!lightstatus;
   
  
}

void netSend() {

  loadStrings(urltarget);
  

  
}


void onAccelerometerEvent(float x, float y, float z)
{
  acX = x;
  acY = y;
  acZ = z;
}