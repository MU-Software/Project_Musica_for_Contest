#include <CapacitiveSensor.h>

CapacitiveSensor   cs_4_1 = CapacitiveSensor(5,13);
CapacitiveSensor   cs_4_2 = CapacitiveSensor(6,12);
CapacitiveSensor   cs_4_3 = CapacitiveSensor(7,11);
CapacitiveSensor   cs_4_4 = CapacitiveSensor(8,10);

void setup() {
   cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF); // turn off autocalibrate on channel 1 - just as an example
   Serial.begin(9600);
}

void loop() {
	long start = millis();
	long total1 =  cs_4_1.capacitiveSensor(30);
	long total2 =  cs_4_2.capacitiveSensor(30);
	long total3 =  cs_4_3.capacitiveSensor(30);
	long total4 =  cs_4_4.capacitiveSensor(30);

	Serial.print(millis() - start);
	Serial.print("\t");
	
	Serial.print(total1);
	Serial.print("\t");
	Serial.print(total2);
	Serial.print("\t");
	Serial.print(total3);
	Serial.print("\t");
	Serial.println(total4);
	
	delay(10);
}