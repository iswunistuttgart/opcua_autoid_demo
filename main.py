import asyncio
import logging
import sys

import cv2
import pyzbar.pyzbar as pyzbar
import asyncua
from asyncua.common.structures import Struct

sys.path.insert(0, "..")


async def main() -> object:
    logging.basicConfig(level=logging.WARNING)
    server = asyncua.Server()
    server.set_endpoint("opc.tcp://0.0.0.0:48400/")
    await server.init()
    # import some nodes from xml
    di = await server.import_xml("nodesets/Opc.Ua.Di.NodeSet2.xml")
    await server.import_xml("nodesets/Opc.Ua.AutoID.NodeSet2.xml")
    autodid_nsi = await server.get_namespace_index("http://opcfoundation.org/UA/AutoID/")
    di_nsi = await server.get_namespace_index("http://opcfoundation.org/UA/DI/")
    uri = "http://examples.seronet-project.de"
    idx = await server.register_namespace(uri)

    device_set = await server.nodes.objects.get_child([f"{di_nsi}:DeviceSet"])  # get proxy to our device state variable
    autoid_type_nodeid = asyncua.ua.NodeId(1008, autodid_nsi)
    autoid_type = server.get_node(nodeid=(autoid_type_nodeid))
    myDevice = await device_set.add_object(idx, "myQRCodeReader", objecttype=autoid_type)

    OpticalScanEventType_NodeID = asyncua.ua.NodeId(1009, autodid_nsi)
    OpticalScanEventType = server.get_node(nodeid=(OpticalScanEventType_NodeID))

    OpticalScanEvent_generator = await server.get_event_generator(OpticalScanEventType, myDevice)

    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN

    # starting!
    async with server:
        while True:
            await asyncio.sleep(0)
            _, frame = cap.read()
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                print("Data", obj.data)
                OpticalScanEvent_generator.event.Message = asyncua.ua.LocalizedText(str(obj.data))
                OpticalScanEvent_generator.event.Severity = 100
                OpticalScanEvent_generator.event.DeviceName = "ISW Barcode Scanner"
                ScanResult = Struct("OpticalScanResult")
                ScanResult.CodeType = "RAW:STRING"
                ScanResult.ScanData = obj.data
                ScanResult.Timestamp = asyncua.ua.datetime.now()
                OpticalScanEvent_generator.event.ScanResult = [ScanResult]
                await OpticalScanEvent_generator.trigger()
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)

            c = cv2.waitKey(1)
            if c == 27:
                break


if __name__ == "__main__":
    asyncio.run(main())
