from datetime import datetime, timedelta, date


class Slot:
    def __init__(self, time):
        self.time = time
        self.energy = None
        self.act = None

    def put_energy(self, energy):
        self.energy = energy

    def put_act(self, act):
        self.act = act


class Slots:
    def __init__(self):
        def datetime_range(start, end, delta):
            current = start

            while current < end:
                yield current
                current += delta

        today = date.today()
        today = today.strftime("%Y-%m-%d")
        start = datetime.strptime(today + " 00:00", "%Y-%m-%d %H:%M")
        end = datetime.strptime(today + " 23:59", "%Y-%m-%d %H:%M")
        self._slots = [Slot(dt) for dt in datetime_range(start, end,
                                                         timedelta(minutes=10))]

    def get_slots(self):
        return [(s.time, s.energy, s.act) for s in self._slots]

    def put_energy(self, energy, start, end):
        def time_to_index(t):
            t = datetime.strptime(t, "%H:%M").time()
            t = datetime.strptime('{}:{}'.format(t.hour, (t.minute // 10) * 10), "%H:%M").time()
            print(t)
            return t.hour * 6 + t.minute // 10

        start, end = time_to_index(start), time_to_index(end)
        for i in range(start, end):
            self._slots[i].energy = energy

    def __repr__(self):
        return self.get_slots()

    def __str__(self):
        return str(self.get_slots())

