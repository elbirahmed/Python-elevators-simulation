from collections import namedtuple

Call = namedtuple("Call", "floor type direction")

class StrategyChoice:

    def op_choice(self, elevators, call=None):
        pass


class StrategyChoiceFree(StrategyChoice):

    def op_choice(self, elevators, call=None):
        for elv in elevators:
            if len(elv.to_visit) < elv.max_call:
                return elv
        return None


class StrategyChoiceNearest(StrategyChoice):

    def op_choice(self, elevators, call=None):
        free_elvs = [elv for elv in elevators if len(elv.to_visit) < elv.max_call]
        elv = None
        if free_elvs:
            elv = free_elvs[0]
            free_elvs_near = list(map(lambda x: (x, x.current_floor - call.floor), free_elvs))
            def filtre(x):
                return x[0].direction == call.direction or x[0].status == "HOLD"
            free_elvs_near = list(filter(filtre, free_elvs_near))
            m = abs(min(free_elvs_near, key=lambda x: abs(x[1]))[1])
            free_elvs_near = list(filter(lambda x: abs(x[1]) == m, free_elvs_near))
            free_elvs_near = list(map(lambda x: x[0], free_elvs_near))
            if len(free_elvs_near) > 0:
                elv = free_elvs_near[0]
        return elv


class Elevator:

    def __init__(self, max_floor, min_floor, id, max_call=2):
        self.current_floor = 0
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.to_visit = []
        self.status = "HOLD"
        self.id = id
        self.max_call = max_call
        self.direction = "UP"

    def __move_up(self):
        dest = self.current_floor + 1
        self.direction = "UP"
        self.status = "MOVE"
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("Moving from {} to {}".format(self.current_floor, dest))
        self.current_floor = dest
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))

    def __move_down(self):
        dest = self.current_floor - 1
        self.direction = "DOWN"
        self.status = "MOVE"
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("moving from {} to {}".format(self.current_floor, dest))
        self.current_floor = dest
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))

    def __open_door(self):
        self.status = "STOP"
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("Elevator {}: open door ".format(self.id))

    def __close_door(self):
        self.status = "STOP"
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("Elevator {}: close door ".format(self.id))

    def next_action(self):
        if len(self.to_visit) > 0:
            call = self.to_visit[0]
            if call.floor < self.current_floor:
                self.__move_down()
            elif call.floor > self.current_floor:
                self.__move_up()
            else:
                self.__open_door()
                if call.type == "E":
                    c = self.__getInputForCallD()
                    self.receive_call(c)
                self.to_visit.pop(0)
                self.__close_door()
        else:
            if self.current_floor != 0:
                self.__move_down()
            if self.current_floor == 0:
                self.status = "HOLD"
                self.direction = "UP"
                print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
                print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))


    def receive_call(self, call):
        print("Elevator {}: gets the call-> {}, {} ".format(self.id, call.floor, call.type))
        self.to_visit.append(call)
        self.to_visit.sort(key=lambda x: x[0])


    def __getInputForCallD(self):
        a = input("You go to floor : ")
        try:
            a = int(a)
            if a < self.max_floor and a > self.min_floor:
                cond1 = self.direction == "UP" and a <= self.current_floor
                cond2 = self.direction == "DOWN" and a >= self.current_floor
                if cond1 or cond2:
                    message = "Elevator going  {}  from {} and do not serve floor {}"
                    raise ValueError(message.format(self.direction, self.current_floor, a))
            else:
                raise ValueError("number of floor not between {} and  {}".format(self.min_floor, self.max_floor))
        except Exception as e:
            print('wrong entry {}'.format(str(e)))
            print('-' * 20)
            return None
        else:
            return Call(a, "D", self.direction)


class Plateform:

    def __init__(self, nb_floor, nb_elevator, min_floor, max_floor, choice_strategy=StrategyChoiceNearest()):
        self.nb_floor = nb_floor
        self.nb_elevator = nb_elevator
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.elevators = [Elevator(self.max_floor, self.min_floor, i) for i in range(self.nb_elevator)]
        self.choice_strategy = choice_strategy

    def receive_call(self, call):
        elv = self.choice_strategy.op_choice(self.elevators, call)
        if elv is not None:
            elv.receive_call(call)

    def next(self):
        for elv in self.elevators:
            elv.next_action()

    @staticmethod
    def getInputForCallE(max_floor, min_floor):
        try:
            a = input("Ask for an elevator from floor number: ")
            if a != "pass":
                a = int(a)
                if a == max_floor:
                    direction = "DOWN"
                elif a == min_floor:
                    direction = "UP"
                elif a < max_floor and a > min_floor:
                    direction = input("Indicate direction : ")
                    if direction != "UP" and direction != "DOWN":
                        raise ValueError("direction must be {} or {}".format("UP", "DOWN"))
                else:
                    raise ValueError("number of floor not between {} and  {}".format(min_floor, max_floor))
            else:
                return None
        except Exception as e:
            print('wrong entry {}'.format(str(e)))
            print('-' * 20)
            return None
        else:
            return Call(a, "E", direction)




if __name__ == "__main__":

    p = Plateform(4, 2, 0, 3)
    while True:
        c = Plateform.getInputForCallE(p.max_floor, p.min_floor)
        if c:
            p.receive_call(c)
        else:
            p.next()
        print('-' * 20)


9
