from picamera import PiCamera
from time import sleep

# Initialize Camera
camera = PiCamera()

# Rotate Camera (acceptable values 0, 90, 180, 270)
camera.rotation=180

# Camera Preview
def preview(waittime=2,alpha_value=255):
    """
        waittime: int (default 2) - time to preview in seconds
        alpha_value: int (between 0 and 255) - transparency setting - 255=No Transparency
    """
    camera.start_preview(alpha=alpha_value)
    sleep(waittime)
    camera.stop_preview()

#preview()
#preview(waittime=5,alpha_value=230)


# Capture Image
def capture(file_location,preview_waittime=2):
    """
        file_location: str - location to save image
        preview_waittime: int (default 2) - time to preview in seconds
    """

    camera.start_preview()
    camera.image_effect = 'cartoon'
    sleep(preview_waittime)
    camera.capture(file_location)
    camera.stop_preview()    

capture('/home/pi/Desktop/test.jpg')



