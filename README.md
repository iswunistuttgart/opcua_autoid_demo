# AutoId Sample Server
This project is a Sample OPC UA Server for a Barcode scanner. It implements the  Companion Specification OPC UA for AutoID Devices (https://reference.opcfoundation.org/AutoID/docs/)
This project is implemented in the SeRoNet Project (https://www.seronet-projekt.de/) 

## Dependency and Installation
- asyncio
- cv2
- pyzbar
- asyncua


 ## Usage
 Run python main.py with an computer with webcam. If the webcam image scan a Barcode an OpticalScanEventType is send.
 
 ## Acknolegdement
 This project was developed in the course of the SeRoNet research project.
 The SeRoNet research and development project is funded by the Federal Ministry of Economic Affairs and Energy (BMWi). It is part of the technology program ”PAICE Digitale Technologien fuer die Wirtschaft” and is guided by the DLR Project Management Agency Information Technologies/Electromobility, Cologne, Germany. The authors are responsible for the contents of this publication.
