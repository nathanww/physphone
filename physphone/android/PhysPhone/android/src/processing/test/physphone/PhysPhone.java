package processing.test.physphone;

import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import ketai.camera.*; 
import android.view.WindowManager; 
import android.view.View; 
import android.os.Bundle; 
import cassette.audiofiles.SoundFile; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class PhysPhone extends PApplet {

/**
 * <p>Ketai Sensor Library for Android: http://KetaiProject.org</p>
 *
 * <p>Ketai Camera Features:
 * <ul>
 * <li>Interface for built-in camera</li>
 * <li>TODO: fix HACK of camera registration that currently exceptions in setup() at the moment.</li>
 * </ul>
 * <p>Updated: 2012-10-21 Daniel Sauter/j.duran</p>
 */



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




 
SoundFile highbeep;
SoundFile lowbeep;
int totalRounds=0;
int streamid;
public void onCreate(Bundle bundle) 
{
  super.onCreate(bundle);
  // fix so screen doesn't go to sleep when app is active
  getActivity().getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
}

public void setup() {
  orientation(PORTRAIT);


   highbeep = new SoundFile(this, "highbeep.mp3"); 
   lowbeep = new SoundFile(this, "lowbeep.mp3");
  
  imageMode(CENTER);
  textSize(70);
  cam = new KetaiCamera(this, 640, 480, 24);
  cam.enableFlash();
  cam.start();
  startTime=millis();
 streamid=PApplet.parseInt(random(1,20000));
  
}

public void draw() {

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
  urltarget="http://biostream-1024.appspot.com/sendStream?streamname="+streamid+"&rawdata="+(total/count)+"&trigger="+trigger+"&sample="+samples;
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

public void onCameraPreviewEvent()
{
  cam.read();
}


public void onPause() {
  
  super.onPause();
  

  cam.disableFlash();
  cam.stop();
  cam.dispose();
  System.exit(0);
     
  
}



public void onStop() {
  

   super.onStop();
  cam.disableFlash();
  cam.stop();
  cam.dispose();
  System.exit(0);
 
  
}

public void mousePressed2() {
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

public void netSend() {

  loadStrings(urltarget);
  

  
}
  public void settings() { 
fullScreen(); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "PhysPhone" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
