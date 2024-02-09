import json, typing
import faust


class Car(faust.Record, serializer='json'):
    fin: str
    zeit: str
    geschwindigkeit: int
    durchschnittsgeschwindigkeit: typing.Optional[float]
    beschleunigung: typing.Optional[int]

    def to_json(self):
        dict  = self.__dict__
        dict.pop('__evaluated_fields__')
        return json.dumps(dict)



