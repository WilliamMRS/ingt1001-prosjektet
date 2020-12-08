from sense_hat import SenseHat
sh = SenseHat()
from time import sleep
from datetime import datetime as dt
import os
import csv

sh.set_imu_config(False, False, True)
sh.clear()

def write_to_logfile(data):
  """ Function for writing single data to logfile. with dd/mm/yy t/m/s"""
  now = dt.now().strftime("%d/%m/%Y %H:%M:%S")
  with open("datasett.csv", "a") as file:
    file.write(str(now) + ", " + str(data) + "\n")

def write(temp_hum, temp_pres, hum, pres, accel):
  """ Takes six values and saves it to a .csv file with date and timestamp"""
  date = dt.now().strftime("%d/%m/%Y")
  time = dt.now().strftime("%H:%M:%S")
  data = [(date), (time), (temp_hum), (temp_pres), (hum), (pres), (accel) ]
  desired_path = '/home/bendin/'
  file_path = os.path.join(desired_path, "Maalinger.csv")
  with open(file_path, "a") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(data)
    return (csvfile)

def show_on_matrix(data):
  """ Function for showing data as text on sensehat"""
  sh.show_message("%.1f C" % data, scroll_speed=0.10, text_colour=[0, 255, 0])

# Enviromental sensors
def sensor_temp_average():
  """ Calculates an average for temperature between humidity and rpessure sensor."""
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

def temp_hum():
  """ Gets temperature from humidity sensor. average from A number of measurements"""
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

def temp_hum():
  """ Gets temperature from humidity sensor. average from A number of measurements"""
  A = 5
  temp_sum = 0
  t = sh.get_temperature_from_humidity()
  for _ in range (0, A):
    temp_sum += t
    sleep(0.05)
  temp_sum = temp_sum / A
  return float(temp_sum)

def temp_pres():
  """ Gets temperature from pressure sensor. average from A number of measurements"""
  A = 5
  temp_sum = 0
  t = sh.get_temperature_from_pressure()
  for _ in range (0, A):
    temp_sum += t
    sleep(0.05)
  temp_sum = temp_sum / A
  return float(temp_sum)

def sensor_hum_average():
  """ Measure humidity A number of times. Returns average."""
  A = 5
  hum = 0
  h = sh.get_humidity()
  for _ in range (0, A):
    hum += h
    sleep(0.05)
    hum = hum / A
  return float(hum)

def sensor_pres_average():
  """" Measure pressure A number of times. Returns average."""
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
  """ Gets acceleration value from sensehat. Does A number of measurements and returns average in m/s^2
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

# Internal temperature   
def cpu_temp():
  """ Gets CPU temp from Raspberry and return it as a float"""
  temp = os.popen("vcgencmd measure_temp").readline()
  temp = (temp.replace("temp=",""))
  temp = (temp.replace("'C",""))
  return float(temp)

def temp_calibrated(sensor, CPU):
  """Function for calibrating measured temperature. Takes sensor and CPU temp.  """
  FACTOR = 1.12 #5.446
  temp_calibrated = sensor - (((CPU) - sensor)/FACTOR)
  return (temp_calibrated)


# Main code for executing logging 
while True:
  temp_average = sensor_temp_average()
  cpu = cpu_temp()
  hum_temp = temp_hum()
  pres_temp = temp_pres()
  hum = sensor_hum_average()
  pres = sensor_pres_average()
  accel = acceleration()

  time = dt.now().strftime("%H:%M:%S")
  date = dt.now().strftime("%d/%m/%Y")
  write(hum_temp, pres_temp, hum, pres, accel)

  print (date, time, temp_average, hum_temp, pres_temp, hum, pres, accel)
  sleep(0.05)