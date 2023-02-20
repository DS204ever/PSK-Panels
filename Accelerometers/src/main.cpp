#include <PeakDetection.h>
#include <math.h>

AcceleroMMA7361 accelero1;
AcceleroMMA7361 accelero2;
AcceleroMMA7361 accelero3;

PeakDetection peakDetection1;
PeakDetection peakDetection2;
PeakDetection peakDetection3;

float z1;
float z2;
float z3;
float fz1;
float fz2;
float fz3;

#define LAG 64
#define THRESHOLD 2
#define INFLUENCE 0.5

void setup() {
  Serial.begin(9600);
  delay(3000);
  accelero1.begin(NULL, NULL, NULL, NULL, NULL, NULL, A0);
  accelero2.begin(NULL, NULL, NULL, NULL, NULL, NULL, A1);
  accelero3.begin(NULL, NULL, NULL, NULL, NULL, NULL, A2);
  accelero1.calibrate();
  accelero2.calibrate();
  accelero3.calibrate();
  peakDetection1.begin(LAG, THRESHOLD, INFLUENCE);
  peakDetection2.begin(LAG, THRESHOLD, INFLUENCE);
  peakDetection3.begin(LAG, THRESHOLD, INFLUENCE);
  analogReadResolution(12);
}

long t1;
long t2;
int impact_region = 0;
int num_samples = 10;
float threshold = 1.0;
int maximum = 0;

int stabilize_num_samples = 500;

bool data_peaked = false;

bool detection_status = false;

void loop() {

  if(Serial.available()>0){
    int msg = Serial.parseInt();
    if(msg==1){
      detection_status=true;
    }
  }

  z1 = map(analogRead(A0), 0, 4095, 0, 3300);
  z2 = map(analogRead(A1), 0, 4095, 0, 3300);
  z3 = map(analogRead(A2), 0, 4095, 0, 3300);

  float sum[3];
  sum[0] = 0;
  sum[1] = 0;
  sum[2] = 0;
  for (int i = 0; i < num_samples; i++) {
    sum[0] = sum[0] + (analogRead(A0) * 3300.0 / 4095.0 - 1650.0) / (200.0);
    sum[1] = sum[1] + (analogRead(A1) * 3300.0 / 4095.0 - 1650.0) / (200.0);
    sum[2] = sum[2] + (analogRead(A2) * 3300.0 / 4095.0 - 1650.0) / (200.0);
  }

  z1 = fabs(sum[0] / num_samples);
  z2 = fabs(sum[1] / num_samples);
  z3 = fabs(sum[2] / num_samples);

  peakDetection1.add(z1);
  peakDetection2.add(z2);
  peakDetection3.add(z3);

  fz1 = peakDetection1.getFilt();
  fz2 = peakDetection2.getFilt();
  fz3 = peakDetection3.getFilt();

  if (detection_status) {
    if (fz1 > maximum && fz1 > threshold) {
      maximum = fz1;
      impact_region = 1;
      stabilize_num_samples = 0;
      data_peaked = true;
    } else if (fz2 > maximum && fz2 > threshold) {
      maximum = fz2;
      impact_region = 2;
      stabilize_num_samples = 0;
      data_peaked = true;
    } else if (fz3 > maximum && fz3 > threshold) {
      maximum = fz3;
      impact_region = 3;
      stabilize_num_samples = 0;
      data_peaked = true;
    } else {
      maximum = 0;
      if (data_peaked) {
        Serial.println(impact_region);
        data_peaked = false;
        detection_status = false;
      }
    }
  }

}