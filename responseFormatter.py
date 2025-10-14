class ResponseFormatter:
    @staticmethod
    def success(message, data=None):
        resp = {"message": message}
        if data:
            resp.update(data)
        return resp

    @staticmethod
    def error(message):
        return {"message": message}