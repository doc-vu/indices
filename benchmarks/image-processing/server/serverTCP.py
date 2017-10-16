# import the necessary packages
import numpy as np
import cv2
import datetime
import time
import socket

def file_upload():

        port = 8080                    # Reserve a port for your service.
        s = socket.socket()             # Create a socket object
        host = '0.0.0.0'     # Get local machine name
        s.bind((host, port))            # Bind to the port
        s.listen(5)
        while True:
                try:
                        conn, addr = s.accept()     # Establish connection with client.
                        print 'Got connection from', addr
                        data = conn.recv(1024)

                        print('Server received header : ', repr(data))
                        conn.send('OK')
                        while True:
                                chunksize = 4096
                                filesize = conn.recv(32)
                                filesize = int(filesize, 2)
                                imagebuf = b''
                                while filesize > 0:
                                        if filesize < chunksize:
                                                chunksize = filesize
                                        data = conn.recv(chunksize)
                                        imagebuf += data
                                        filesize -= len(data)

                                start = time.time()
                                kp, des = sift(imagebuf)
                                #print len(np.getbuffer(des))
                                end = time.time()
                                duration = str(round((end-start)*1000,3)).encode('utf-8')
                                conn.sendall(duration)
                except Exception ,e :
                        print "exception", str(e)
        s.close()

def sift(imageval):
        file_bytes = np.asarray(bytearray(imageval), dtype=np.uint8)
        #file_bytes = np.asarray(imageval, dtype=np.uint8)
        img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
        gray = cv2.cvtColor(img_data_ndarray, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT(40)
        kp, des = sift.detectAndCompute(gray,None)
        return kp, des

def surf(imageval):
        file_bytes = np.asarray(bytearray(imageval), dtype=np.uint8)
        #file_bytes = np.asarray(imageval, dtype=np.uint8)
        img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
        gray = cv2.cvtColor(img_data_ndarray, cv2.COLOR_BGR2GRAY)
        surf = cv2.SURF(40)
        kp, des = surf.detectAndCompute(gray,None)
        return kp, des



if __name__ == '__main__':
        print 'server started ...'
        file_upload()
