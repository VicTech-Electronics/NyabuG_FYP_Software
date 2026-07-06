from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializer import DeviceSerializer
from nyabu_kiyoyozi.data import FAULT, WARNING
from management.models import Device, Fault


# Create your views here.
@api_view(['GET'])
def documentation(request):
 info = [
  {
   'endpoint': '.../api/',
   'method': 'GET',
   'body': None,
   'description': 'View documetation of this API'
  }, 
  {
   'endpoint': '.../api/device-data/',
   'method': 'POST',
   'body': '{"device_id": str, "vibration": float, "noise": float}',
   'description': 'Device post new data to the site'
  },
  {
   'endpoint': '.../api/deactivate-device/',
   'method': 'POST',
   'body': '{"device_id": str}',
   'description': 'Device post deactivated request'
  }
 ]

 return Response(info, status=status.HTTP_200_OK)



@api_view(['POST'])
def deviceData(request):
 device_data = {
  'device_id': request.data.get('device_id'),
  'vibration': request.data.get('vibration'),
  'noise': request.data.get('noise')
 }

 if not Device.objects.filter(device_id = device_data['device_id']).exists():
  return Response('Device not exist in this system!', status=status.HTTP_404_NOT_FOUND)

 device = Device.objects.get(device_id = device_data['device_id'])
 serializer = DeviceSerializer(instance = device, data = device_data);

 print(f'Device PK: {device.pk}')

 if serializer.is_valid():
  #    Check fault existance and kind
  if device_data['vibration'] >= FAULT['vibration'] and device_data['noise'] >= FAULT['noise']:
   fault_type = "both_faults"
  elif device_data['vibration'] >= FAULT['vibration']:
   fault_type = "vibration_fault"
  elif device_data['noise'] >= FAULT['noise']:
   fault_type = "noise_fault"
  else:
   fault_type = False

  #   Create fault instance if device has fault
  if fault_type:
   Fault.objects.create(
    device = device,
    vibration_during_fault = device_data['vibration'],
    noise_during_fault = device_data['noise'],
    fault_type = fault_type
   )
  
  #   Save serialized device instance 
  device.status = 'active'
  device.save();
  serializer.save();

  #   Prepeare response
  server_response = "SAFE";
  if(fault_type): server_response = "FAULT"
  elif(device_data["vibration"] >= WARNING["vibration"] or device_data["noise"] >= WARNING["noise"]):
   server_response = "WARNING"

  return Response(server_response, status=status.HTTP_202_ACCEPTED)
 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def deactivateDevice(request):
 device_id = request.data.get('device_id')

 if not Device.objects.filter(device_id = device_id).exists():
  return Response('Device not exist in this system!', status=status.HTTP_404_NOT_FOUND)

 device = Device.objects.get(device_id = device_id)
 device.status = "inactive"
 device.save()

 return Response(f'Device deactivated', status=status.HTTP_202_ACCEPTED)