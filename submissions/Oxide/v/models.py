import json


class Profile:
    name       = None
    profilePic = None
    history    = []
    cookies    = []
    passwords  = []

    def to_json(self):
        return {
            'name': self.name,
            'profile_pic': self.profilePic,
            'history': self.history,
            'cookies': self.cookies,
            'passwords': self.passwords,
        }