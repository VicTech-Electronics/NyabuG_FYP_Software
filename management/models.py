from django.db import models


# Create your models here.
class Device(models.Model):
    device_id = models.CharField(max_length=100)
    vibration = models.FloatField()
    noise = models.FloatField()
    status = models.CharField(
    	max_length=20,
    	choices=[
    		('active', 'Active'),
    		('inactive', 'Inactive')
    	],
    	default='active'
    )
    
    def __str__(self):
        return self.device_id


class Fault(models.Model):
	device = models.ForeignKey(Device, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	vibration_during_fault = models.FloatField()
	noise_during_fault = models.FloatField()
	fault_type = models.CharField(
		max_length=20,
		choices=[
			('vibration_fault', 'Vibration Fault'),
			('noise_fault', 'Noise Fault'),
			('both_faults', 'Both Faults')
		],
		default='noise_fault'
	)

	def __str__(self):
		return self.device.device_id