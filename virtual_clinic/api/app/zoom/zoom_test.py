from zoom_api import ZoomAPI

#zoom = ZoomAPI('g6S1fCr5Q22bF7ZuA5NwTA', 'u3tu7Wu09SlDXKnb0JZCi2ehaWf5itt0sJa6', 'adamsyd951@gmail.com')

zoom = ZoomAPI()
# 1,209,600 = 14 days
start_url, join_url = zoom.create_zoom_meeting('2020-08-13T16:47:00', 30, 'Clinic Consultation', 'consultation with patient name', 7200)
print(start_url)
print(join_url)