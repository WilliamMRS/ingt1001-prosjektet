
from sense_hat import SenseHat
sh = SenseHat()
from time import sleep, strftime
from datetime import datetime as dt
import os
import csv

sh.set_imu_config(False, False, True)
sh.clear()

def write_to_logfile(data):
  """ Function for writing single data to logfile. in  dd/mm/yy t/m/s"""
  now = dt.now().strftime("%d/%m/%Y %H:%M:%S")
  with open("datasett.csv", "a") as file:
    file.write(str(now) + ", " + str(data) + "\n")

def write(temp, hum, pres, accel):
  """ Takes four values and save it to a .csv file"""
  date = dt.now().strftime("%d/%m/%Y")
  time = dt.now().strftime("%H:%M:%S")
  data = [(date), (time), (temp), (hum), (pres), (accel) ]
  desired_path = '/home/bendin/'
  file_path = os.path.join(desired_path, "testsett2.csv")
  with open(file_path, "a") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(data)
    return (csvfile)

def show_on_matrix(data):
  """ For    vise frem data p   sensehat"""
  sh.show_message("%.1f C" % data, scroll_speed=0.10, text_colour=[0, 255, 0])

# Enviromental sensors
def sensor_temp_average():
  """ Gir tilbake gjennomsnittstemperaturen av A ant m  linger med 0.25s mellomrom.
  Henter data fra b  de humidity- og pressure sensor."""
  A = 5
  temp_sum = 0
  t1 = sh.get_temperature_from_humidity()
  t2 = sh.get_temperature_from_pressure()
  t = (t1+t2)/2
  for _ in range (0, A):
    temp_sum += t
    sleep(0.05)
  temp_sum = temp_sum / A
  return (temp_sum)

def sensor_hum_average():
  """ Gj  r A ant m  linger av luftfuktighet med 0.25s mellom hver m  ling"""
  A = 5
  hum = 0
  h = sh.get_humidity()
  for _ in range (0, A):
    hum += h
    sleep(0.05)
  hum = hum / A
  return float(hum)

def sensor_pres_average():
  """" Gj  r A ant ml  inger av lufttrykk med 0.25s pause mellom hver m  ling"""
  A = 5
  pres = 0
  h = sh.get_pressure()
  for _ in range (0, A):
    pres += h
    sleep(0.05)
  pres = pres / A
  return float(pres)

# IMU sensors 

def acceleration():
  """ Gets acceleration value from sensehat. Does A number of measurements and returns average in m/s^
  """
  A = 4
  average_Gs = 0
  accel = sh.get_accelerometer_raw()
  upwards_accel = float("{z}".format(**accel))
  for _ in range (0, A):
    average_Gs += upwards_accel
  average_Gs = average_Gs / A
  mps2 = (average_Gs * 9.80665)
  return (mps2)

# Try to compensate for CPU temp. Unsure if we need this.
# Internal temperature   
def cpu_temp():
  """ Gets CPU temp from Raspberry"""
  temp = os.popen("vcgencmd measure_temp").readline()
  temp = (temp.replace("temp=",""))
  temp = (temp.replace("'C",""))
  return float(temp)

def temp_calibrated(sensor, CPU):
  """ Funksjon for kalibrering av m  linger. """
  FACTOR = 1.12 #5.446
  temp_calibrated = sensor - (((CPU) - sensor)/FACTOR)
  return (temp_calibrated)


# Main code for executing logging 
while True:
  temp = sensor_temp_average()
  calibrated = temp_calibrated(sensor_temp_average(), cpu_temp())
  hum = sensor_hum_average()
  pres = sensor_pres_average()
  accel = acceleration()

  time = dt.now().strftime("%H:%M:%S")
  date = dt.now().strftime("%d/%m/%Y")
  write(temp, hum, pres, accel)

  print (date, time, calibrated, hum, pres, accel)
  sleep(0.05)






