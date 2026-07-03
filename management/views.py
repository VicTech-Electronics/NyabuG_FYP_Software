from nyabu_kiyoyozi.data import SECURITY_CODE, FAULT, WARNING
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Device, Fault


# Create your views here.
def security(request):
    if request.method == "POST":
        security_code = request.POST.get("security_code")
        print(security_code)
        try:
            if int(security_code) == SECURITY_CODE:
                return redirect("dashboard")
            messages.error(request, "Sorry! Incorrect security code.")
        except:
            messages.error(request, "Please! Fill the security code before proceed")
    return render(request, "security.html")


def dashboard(request):
    devices = list(Device.objects.all())
    for device in devices:
        is_fault = (device.vibration > FAULT['vibration'] or device.noise > FAULT['noise'])
        is_warning = (device.vibration > WARNING['vibration'] or device.noise > WARNING['noise'])

        if is_fault:
            device.condition = 'fault'
        elif is_warning:
            device.condition = 'warning'
        else:
            device.condition = 'safe'

    return render(request, "dashboard.html", {"devices": devices})


def showFaults(request):
    if request.method == "POST":
        device_id = request.POST.get('device_id')
        if not Device.objects.filter(device_id=device_id).exists():
            messages.error(request, 'Sorry! Such device not exist.')
            return redirect('dashboard')

        fault_device = Device.objects.get(device_id=device_id)
        if not Fault.objects.filter(device=fault_device.pk).exists():
            messages.info(request, 'The Device selected has no Fault History!')
            return redirect('dashboard')

        faults = list(Fault.objects.filter(device=fault_device.pk))
        for fault in faults:
            fault.fault_type = fault.fault_type.replace('_', ' ').title()
            fault.time = fault.created_at.strftime("%d %b %Y | %H:%M")
        return render(request, 'fault_history.html', {'device_id': device_id, 'faults': faults})
    return redirect('dashboard')


def deleteFault(request):
    if request.method == 'POST':
        fault_id = request.POST.get('fault_id')
        fault = Fault.objects.get(pk = fault_id)
        fault.delete();
        messages.success(request, 'Fault history deleted successfully')
    else: messages.error(request, 'Sorry! Request method not allowed')

    # Render remaining faults back
    faults = list(Fault.objects.filter(device=fault.device.pk))
    for fault in faults:
        fault.fault_type = fault.fault_type.replace('_', ' ').title()
        fault.time = fault.created_at.strftime("%d %b %Y | %H:%M")
    return render(request, 'fault_history.html', {'device_id': fault.device.device_id, 'faults': faults})