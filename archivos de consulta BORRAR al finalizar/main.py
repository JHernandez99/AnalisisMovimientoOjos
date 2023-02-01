from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread,pyqtSignal
import sys
import cv2
import numpy as np
from tracker import *

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray,np.ndarray)

    def __init__(self,ruta,velocidad,displayLCD):
        super().__init__()
        self.__run__flag = True
        self.rutaVideo = ruta
        self.velocidad = velocidad
        self.displayLCD = displayLCD
        print('running')

    def run(self):
        # Rangos para la paleta de colores principal
        rangoBajo = np.array([10, 90, 100], np.uint8)
        rangoAlto = np.array([180, 255, 255], np.uint8)
        # Rango de colores para la pala NECESITA CORRECCION
        rangopBajo = np.array([70, 10, 50], np.uint8)
        rangopAlto = np.array([100, 255, 255], np.uint8)
        # colores de prueba
        rangoBajoAmarillo = np.array([15, 70, 150], np.uint8)
        rangoAltoAmarillo = np.array([35, 255, 255], np.uint8)

        grosorPuntos = 10
        contadorPiezas = 0
        tracker = EuclideanDistTracker()
        kernel = np.ones((3, 3), np.uint8)
        cap = cv2.VideoCapture(self.rutaVideo);
        pixeles = 0
        while self.__run__flag:
            ret, frame = cap.read()
            if ret == True:
                frame = frame[:, 30:450]
                frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
                # re acomodar las imagenes para que siempre tengan la misma orientacion en la banda
                frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(frameHSV, rangoBajo, rangoAlto)
                # Pasarle unos filtrillos para que quede mejor la mascara
                #maskPala = cv2.inRange(frameHSV, rangopBajo, rangopAlto)
                maskAmarillos = cv2.inRange(frameHSV, rangoBajoAmarillo, rangoAltoAmarillo)
                maskAmarillos = cv2.erode(maskAmarillos, kernel, 1)
                maskAmarillos = cv2.dilate(maskAmarillos, kernel, 1)
                # maskVerde = cv2.inRange(frameHSV,rangoBajoVerde, rangoAltoVerde)
                maskf = mask + maskAmarillos  # +maskPala
                maskf = cv2.erode(maskf, kernel, 1)
                maskf = cv2.dilate(maskf, kernel, 1)
                # Contornos
                cnts, _ = cv2.findContours(maskf, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                detecciones = []
                for c in cnts:
                    area = cv2.contourArea(c)
                    # print('El area es: {}'.format(area))
                    if area > 500:
                        x, y, w, h = cv2.boundingRect(c)
                        detecciones.append([x, y, w, h])
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2);
                        # Dibujar los puntos de sujecion de la pieza
                        # Si el w es mas corto que h usar w
                        if w < h:
                            cv2.circle(frame, (int(x), int(y + h / 2)), grosorPuntos, (0, 0, 255), -1)
                            cv2.circle(frame, (int(x + w), int(y + h / 2)), grosorPuntos, (0, 0, 255), -1)

                            cv2.putText(frame, str('{} px'.format(w)),(x+25,y-15),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
                        else:
                            cv2.circle(frame, (int(x + w / 2), int(y)), grosorPuntos, (0, 0, 255), -1)
                            cv2.circle(frame, (int(x + w / 2), int(y + h)), grosorPuntos, (0, 0, 255), -1)
                            cv2.putText(frame, str('{} px'.format(h)), (x+25, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
                    # Tracking de objetos con conteo
                boxes_ids = tracker.update(detecciones)
                for box_id in boxes_ids:
                    x, y, w, h, id = box_id
                    cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

                    if contadorPiezas < id:
                        contadorPiezas = id
                        self.displayLCD.display(contadorPiezas)

                self.change_pixmap_signal.emit(frame,mask)


                if cv2.waitKey(self.velocidad) & 0xFF == ord('s'):
                    break
            else:
                self.__run__flag = False
        cap.release()
        cv2.destroyAllWindows()

class Objetivo4(QThread):
    cambiarSenialPixMap = pyqtSignal(np.ndarray)
    def __init__(self, ruta, velocidad,dispRojo,dispAmarillo,dispAzul,dispMorado,dispVerde):
        super().__init__()
        self.__run__flag_ = True
        self.ruta = ruta
        self.velocidad = velocidad
        self.displayRojo = dispRojo
        self.displayAmarillo = dispAmarillo
        self.displayAzul = dispAzul
        self.displayMorado = dispMorado
        self.displayVerde = dispVerde
        print('Objetivo 4 corriendo')

    def run(self):

        video = cv2.VideoCapture(self.ruta)
        trackerRojo = EuclideanDistTracker()
        trackerAmarillo = EuclideanDistTracker()
        trackerAzul = EuclideanDistTracker()
        trackerMorado = EuclideanDistTracker()
        trackerVerde = EuclideanDistTracker()
        rbRojo = np.array([160,100,100],np.uint8)
        raRojo = np.array([179,255,255], np.uint8)
        rbAmarillo = np.array([20,50,20], np.uint8)
        raAmarillo = np.array([35,255,255], np.uint8)
        rbAzul = np.array([85,100,100], np.uint8)
        raAzul = np.array([130,255,255], np.uint8)
        rbMorado = np.array([140,100,100], np.uint8)
        raMorado = np.array([155,255,255], np.uint8)
        rbVerde = np.array([35,80,80], np.uint8)
        raVerde = np.array([75,255,255], np.uint8)
        piezasRojo = 0
        piezasAmarillo = 0
        piezasAzul = 0
        piezasMorado = 0
        piezasVerde = 0
        while self.__run__flag_:

            ret,frame = video.read()
            if ret == True:
                frame = frame[:, 30:450]
                frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
                frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                maskRojo = cv2.inRange(frameHSV, rbRojo,raRojo)
                maskAmarillo = cv2.inRange(frameHSV,rbAmarillo,raAmarillo)
                maskAzul = cv2.inRange(frameHSV, rbAzul, raAzul)#Falta la pala
                maskMorado = cv2.inRange(frameHSV,rbMorado,raMorado)
                maskVerde = cv2.inRange(frameHSV, rbVerde, raVerde)
                #Busqueda de contornos
                cntsRojo,_ = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cntsAmarillo, _ = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cntsAzul,_ = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cntsMorado,_ = cv2.findContours(maskMorado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cntsVerde,_ =cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                deteccionesRojo = []
                deteccionesAmarillo= []
                deteccionesAzul = []
                deteccionesMorado = []
                deteccionesVerde = []
                for c in cntsRojo:
                    area = cv2.contourArea(c)
                    if area>500:
                        x,y,w,h = cv2.boundingRect(c)
                        deteccionesRojo.append([x,y,w,h])
                boxes_idsRojos = trackerRojo.update(deteccionesRojo)
                for box_id in boxes_idsRojos:
                    x,y,w,h, id = box_id
                    cv2.putText(frame, str(id)+' ROJO', (x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    if piezasRojo < id:
                        piezasRojo = id
                        self.displayRojo.display(piezasRojo)
                #AMARILLO
                for c in cntsAmarillo:
                    area = cv2.contourArea(c)
                    if area>500:
                        x,y,w,h = cv2.boundingRect(c)
                        deteccionesAmarillo.append([x,y,w,h])
                boxes_idsAmarillos = trackerAmarillo.update(deteccionesAmarillo)
                for box_id in boxes_idsAmarillos:
                    x,y,w,h, id = box_id
                    cv2.putText(frame, str(id)+' AMARILLO', (x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    if piezasAmarillo < id:
                        piezasAmarillo = id
                        self.displayAmarillo.display(piezasAmarillo)
                #Azul
                for c in cntsAzul:
                    area = cv2.contourArea(c)
                    if area>500:
                        x,y,w,h = cv2.boundingRect(c)
                        deteccionesAzul.append([x,y,w,h])
                boxes_idsAzul = trackerAzul.update(deteccionesAzul)
                for box_id in boxes_idsAzul:
                    x,y,w,h, id = box_id
                    cv2.putText(frame, str(id)+' AZUL', (x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    if piezasAzul < id:
                        piezasAzul = id
                        self.displayAzul.display(piezasAzul)
                #Morado
                for c in cntsMorado:
                    area = cv2.contourArea(c)
                    if area>500:
                        x,y,w,h = cv2.boundingRect(c)
                        deteccionesMorado.append([x,y,w,h])
                boxes_idsMorados = trackerMorado.update(deteccionesMorado)
                for box_id in boxes_idsMorados:
                    x,y,w,h, id = box_id
                    cv2.putText(frame, str(id)+' MORADO', (x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    if piezasMorado < id:
                        piezasMorado = id
                        self.displayMorado.display(piezasMorado)
                #VERDE
                for c in cntsVerde:
                    area = cv2.contourArea(c)
                    if area>500:
                        x,y,w,h = cv2.boundingRect(c)
                        deteccionesVerde.append([x,y,w,h])
                boxes_idsVerde = trackerVerde.update(deteccionesVerde)
                for box_id in boxes_idsVerde:
                    x,y,w,h, id = box_id
                    cv2.putText(frame, str(id)+' VERDE', (x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    if piezasVerde < id:
                        piezasVerde = id
                        self.displayVerde.display(piezasVerde)

                self.cambiarSenialPixMap.emit(frame)
                if cv2.waitKey(self.velocidad) & 0xFF == ord('s'):
                    break
            else:
                self.__run__flag_ = False
        video.release()
        cv2.destroyAllWindows()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        ui = uic.loadUi('gui.ui',self)
        self.show()
        self.setWindowTitle('PF - Vision por Computadora')
        botonIniciar = self.findChild(QtWidgets.QPushButton, 'btnIniciar')
        botonIniciar.clicked.connect(self.enviarVideo)
        self.image_label = self.findChild(QtWidgets.QLabel, 'imagenSalida')
        self.image_label2 = self.findChild(QtWidgets.QLabel, 'mascara')
        self.image_label3 = self.findChild(QtWidgets.QLabel, 'objetivo4')
        self.display_width = self.image_label.size().width()
        self.display_height = self.image_label.size().height()
        self.displayLCD = self.findChild(QtWidgets.QLCDNumber, 'lcdNumber')
        self.dispRojo = self.findChild(QtWidgets.QLCDNumber, 'lcdRojo')
        self.dispAmarillo = self.findChild(QtWidgets.QLCDNumber, 'lcdAmarillo')
        self.dispAzul = self.findChild(QtWidgets.QLCDNumber, 'lcdAzul')
        self.dispMorado = self.findChild(QtWidgets.QLCDNumber, 'lcdMorado')
        self.dispVerde = self.findChild(QtWidgets.QLCDNumber, 'lcdVerde')

    def convert_cv_qt(self, cv_img):
        """Convierte de  opencv image a QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def update_image(self, cv_img,cv_img2):
        qt_img = self.convert_cv_qt(cv_img)
        qt_img2 = self.convert_cv_qt(cv_img2)
        self.image_label.setPixmap(qt_img)
        self.image_label2.setPixmap(qt_img2)

    def update_image_objt4(self,cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label3.setPixmap(qt_img)

    def enviarVideo(self):
        self.display_width = self.image_label.size().width()
        self.display_height = self.image_label.size().height()
        self.displayLCD.display(0)
        self.dispRojo.display(0)
        self.dispAmarillo.display(0)
        self.dispAzul.display(0)
        self.dispMorado.display(0)
        self.dispVerde.display(0)
        lblRuta = self.findChild(QtWidgets.QLineEdit, 'rutaVideo')
        ruta = lblRuta.text()
        spbVelocidad = self.findChild(QtWidgets.QSpinBox, 'velocidad')
        velocidad = spbVelocidad.value()

        self.thread = VideoThread(ruta,velocidad,self.displayLCD)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.thread2 = Objetivo4(ruta,velocidad,self.dispRojo,self.dispAmarillo,self.dispAzul,self.dispMorado,self.dispVerde)
        self.thread2.cambiarSenialPixMap.connect(self.update_image_objt4)
        self.thread2.start()


app = QtWidgets.QApplication(sys.argv)
windows = Ui()
app.exec_()