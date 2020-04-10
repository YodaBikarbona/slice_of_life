class Validation:

    @staticmethod
    def login_validation(data):
        try:
            data['username']
            data['password']
            return True
        except Exception as ex:
            print(ex)
            return False
