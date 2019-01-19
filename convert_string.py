from datetime import datetime
import struct

def convertString(data):
    ''' Converts string received from device via socket as the device is capable of sending data through on server gateway'''
    try:
        dg = ''
        eb = ''
        today = datetime.today()
        d = {}
        keyword = ''
        bytestrans = ''
        packet = ''
        hardver = ''
        softver = ''
        imei = ''
        sim = ''
        signal = ''
        lat = ''
        dlat = ''
        lon = ''
        dlon = ''
        ff = ''
        crc = ''

        string = data
        data_check = data[0:63]
        n = 2
        data = [data[i:i+n] for i in range(0, len(data), n)]
        print(data)
        j = 0
        for i in data:
            if j in range(0, 5):
                keyword = keyword + i
                if j == 4:
                    print("keyword = ", keyword)
                    keyword = bytearray.fromhex(keyword).decode()

            elif j in range(5, 6):
                bytestrans = bytestrans + i
                print("bytes Transmitted = ", bytestrans)
                bytestrans = int(bytestrans, 16)

            elif j in range(6, 7):
                packet = packet + i
                print("Packet Received = ", packet)

            elif j in range(7, 11):
                hardver = hardver + i
                if j == 10:
                    print("Hardware Version = ", hardver)
                    hardver = bytearray.fromhex(hardver).decode()

            elif j in range(11, 15):
                softver = softver + i
                if j == 14:
                    print("Software Version = ", softver)
                    softver = bytearray.fromhex(softver).decode()

            elif j in range(15, 30):
                imei = imei + i
                if j == 29:
                    print("Device ID = ", imei)
                    imei = bytearray.fromhex(imei).decode()

            elif j in range(30, 34):
                sim = sim + i
                if j == 33:
                    print("Sim = ", sim)
                    try:
                        sim = bytearray.fromhex(sim).decode()
                    except Exception as e:
                        print ("error can't decode sim hex: ", e)

            elif j in range(34, 35):
                signal = signal + i
                print("Signal Strength = ", signal)
                signal = int(signal, 16)

            elif j in range(35, 39):
                lat = lat + i
                if j == 38:
                    print("Latitude = ", lat)
                    lat = "".join(map(str.__add__, lat[-2::-2] , lat[-1::-2])) 
                    lat = struct.unpack('!f', lat.decode('hex'))[0]

            elif j in range(39, 40):
                dlat = dlat + i
                print("Direction of LAT = ", dlat)
                dlat = bytearray.fromhex(dlat).decode()

            elif j in range(40, 44):
                lon = lon + i
                if j == 43:
                    print("Longitude = ", lon)
                    lon = "".join(map(str.__add__, lon[-2::-2] , lon[-1::-2])) 
                    lon = struct.unpack('!f', lon.decode('hex'))[0]

            elif j in range(44, 45):
                dlon = dlon + i
                print("Direction of LON = ", dlon)
                dlon = bytearray.fromhex(dlon).decode()

            elif j in range(45, 49):
                ff = ff + i
                if j == 48:
                    print(ff," got ff")
                    ff = "".join(map(str.__add__, ff[-2::-2] , ff[-1::-2])) 
                    ff = struct.unpack('!f', ff.decode('hex'))[0]
                    ff = format(ff, '.2f')

            elif j == 49:
                year = '20' + str(data[j])

                month = data[j + 1]

                day = data[j + 2]

                hours = data[j + 3]

                minutes = data[j + 4]

                seconds = data[j + 5]
                print("CHECK here Jyess ;-)")
                print(year)
                print(month)
                print(day)
                print(hours)
                print(minutes)
                print(seconds)
                try:
                    if year != "2000":
                        today = datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds))
                    print("Date Time by Device = ", str(today))
                except Exception as e:
                    print (e)
                    print ("YMDHMS")


            elif j == 55:
                h_size = len(i) * 4
                status = (bin(int(i, 16))[2:]).zfill(h_size)

                print("old status = ",status)
                status = status[::-1]    
                print("new status = ",status)

                dg = status[0]
                eb = status[1]
                if dg == '1' and eb == '1':
                    pt = '1'
                else:
                    pt = '0'
                supply_batt = status[2]
                acc_s = status[3]
                s_bit4 = status[4]
                s_bit5 = status[5]
                s_bit6 = status[6]
                s_bit7 = status[7]
                print("DG = ", dg)
                print("EB = ", eb)
                print("Supply from External Battery = ", supply_batt)
                print("Accelerometer Status = ", acc_s)
                print("Future Status bit 4 = ", s_bit4)
                print("Future Status bit 5 = ", s_bit5)
                print("Future Status bit 6 = ", s_bit6)
                print("Future Status bit 7 = ", s_bit7)

            elif j == 56:
                fut1 = data[j]
                fut1 = int(fut1, 16)

                fut2 = data[j + 1]
                fut2 = int(fut2, 16)

                fut3 = data[j + 2]
                fut3 = int(fut3, 16)

                fut4 = data[j + 3]
                fut4 = int(fut4, 16)

                fut5 = data[j + 4]
                fut5 = int(fut5, 16)

                fut6 = data[j + 5]
                fut6 = int(fut6, 16)

                fut7 = data[j + 6]
                fut7 = int(fut7, 16)
                fut_bit = str(fut1) + str(fut2) + str(fut3) + str(fut4) + str(fut5) + str(fut6) + str(fut7)
                print("Future Byte 1 to 7 = ", fut_bit)

            elif j in range(63, 65):
                crc = crc + i
                if j == 64:
                    print ("CRC is ", crc)
                    old_crc = crc
                    crc = int(crc, 16)

            j += 1
########################################################################################################################################
        d.update({'keyword': str(keyword), 'bytestrans': bytestrans, 'packet': packet, 'hardver': str(hardver), 'softver': str(softver), 
            'ID': str(imei), 'sim': str(sim), 'signal': signal, 'lat': lat, 'lon': lon, 'dlat': str(dlat), 'dlon': str(dlon), 
            'ff': ff, 'date': str(datetime.date(today)), 'time': str(datetime.time(today).strftime("%H:%M:%S")), 'dg': dg, 'eb': eb, 
            'supply_batt': supply_batt, 'acc_s': acc_s, 'crc': crc, 'pt': pt, 'Receive_Type': 'INTERNET'})

        print(d)
        date = d.get('date', None)
        time = d.get('time', None)
        print ("date = ", date)
        print ("time = ", time)

        decoded = str(keyword) + str(bytestrans) + packet + hardver + softver + str(imei) + sim + str(signal) + str(lat) + dlat + str(lon) + dlon + ff + year + month + day + hours + minutes + seconds + status +  fut_bit + str(crc)
        return decoded


    except Exception as e:
        print (e)

with open("net_logs.txt", 'r') as fd:
    data = fd.read().split()


fdd = open("decoded_napino.txt", "w+")
dat_log = []
for string in data:
    if string[:10] == '4c47555255':
        dat_log.append(string)

for logs in dat_log:
    decoded = convertString(logs)
    fdd.write("%s\n" % str(decoded))

fdd.close()
