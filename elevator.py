from collections import namedtuple
from enum import Enum, unique

Call = namedtuple("Call", "floor type direction")

@unique
class DirectionEnum(Enum):
    """
    this class is an enumeration for listing the direction that an elevator can take: UP or DOWN
    """
    UP = "UP"
    DOWN = "DOWN"

@unique
class StatusEnum(Enum):
    """
    this class is an enumeration for listing the status that an elevator can take: STOP, MOVE, HOLD
    """
    STOP = "STOP"
    MOVE = "MOVE"
    HOLD = "HOLD"
    
class StrategyChoice:
    """
    A class with only one function to define the strategy with wich a call will be affected to an elevator
    """

    def op_choice(self, elevators, call=None):
        """
        This function returns the elevator from a list of elevators to assing a call to it
        It is an abstract function to be impelmented in the classes that extends the StrategyChoice

        :param elevators: list of Elevator objects from which the function will get the most appropriate one to response to the call
        :param call: the call to search for the elevator to answer for it
        :return: the elevator to answer for the call
        """
        pass


class StrategyChoiceFree(StrategyChoice):
    """
    a class that extends the StrategyChoice to define a new strategy to get the elevator based only on availability
    """

    def op_choice(self, elevators, call=None):
        """
        This function returns the elevator from a list of elevators to assign a call to it
        is is a concrete implementation of the op_choice method of the StrategyChoice class
        the choice is based only on availability

        :param elevators: list of Elevator objects from which the function will get the most appropriate one to response
        to the call
        :param call: the call to search for the elevator to answer for it
        :return: the elevator to answer for the call
        """
        for elv in elevators:
            if len(elv.to_visit) < elv.max_call:
                return elv
        return None


class StrategyChoiceNearest(StrategyChoice):
    """
    a class that extends the StrategyChoice to define a new strategy to get the elevator based on the current position
    of  elevators and their direction
    """

    def op_choice(self, elevators, call=None):
        """
            This function returns the elevator from a list of elevators to assign a call to it
            is is a concrete implementation of the op_choice method of the StrategyChoice class
            the choice is based on the current position of elevators and their
            direction

            :param elevators: list of Elevator objects from which the function will get the most appropriate
            one to response to the call
            :param call: the call to search for the elevator to answer for it
            :return: the elevator to answer for the call
        """
        free_elvs = [elv for elv in elevators if len(elv.to_visit) < elv.max_call]
        elv = None
        if free_elvs:
            elv = free_elvs[0]
            free_elvs_near = list(map(lambda x: (x, x.current_floor - call.floor), free_elvs))
            def filtre(x):
                return x[0].direction == call.direction\
                       or (x[0].status == StatusEnum.HOLD.value)
            free_elvs_near = list(filter(filtre, free_elvs_near))
            m = abs(min(free_elvs_near, key=lambda x: abs(x[1]))[1])
            free_elvs_near = list(filter(lambda x: abs(x[1]) == m, free_elvs_near))
            free_elvs_near = list(map(lambda x: x[0], free_elvs_near))
            if len(free_elvs_near) > 0:
                elv = free_elvs_near[0]
        return elv


class Elevator:

    """
    Class that represents an Elevator
    """
    def __init__(self, max_floor, min_floor, id, max_call=3):

        """
        Constructor of the class Elevator

        :param max_floor: the highest floor an elevator can reach
        :param min_floor:  the lowest floor an elevator can reach
        :param id:  the id of the elevator
        :param max_call: the number of calls that an elevator can manage at one time
        """

        self.current_floor = 0
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.to_visit = []
        self.status = StatusEnum.HOLD.value
        self.id = id
        self.max_call = max_call
        self.direction = DirectionEnum.UP.value

    def __move_up(self):

        """
        method to move an elevator from floor i to floor i+1. Updates its status and its direction
        :return: None
        """

        dest = self.current_floor + 1
        self.direction = DirectionEnum.UP.value
        self.status = StatusEnum.MOVE.value
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("Moving from {} to {}".format(self.current_floor, dest))
        self.current_floor = dest
        if dest == self.max_floor:
            self.direction = DirectionEnum.DOWN.value
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))

    def __move_down(self):

        """
            method to move an elevator from floor i to floor i-1. Updates its status and its direction
            :return: None
        """

        dest = self.current_floor - 1
        self.direction = DirectionEnum.DOWN.value
        self.status = StatusEnum.MOVE.value
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("moving from {} to {}".format(self.current_floor, dest))
        self.current_floor = dest
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))

    def __open_door(self):

        """
        method to open the door of an elevator when it reaches a destination floor
        :return: None
        """

        self.status = StatusEnum.STOP.value
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("Elevator {}: open door ".format(self.id))

    def __close_door(self):

        """
            method to open the door of an elevator when it leaves a floor
            :return: None
        """
        self.status = StatusEnum.STOP.value
        print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
        print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))
        print("Elevator {}: close door ".format(self.id))

    def receive_call(self, call):
        """
        method to get a new call and assign it to the list of to_vist floors of the elevator
        :param call: the call to manage by the elevator
        :return: None
        """
        print("Elevator {}: gets the call-> {}, {} ".format(self.id, call.floor, call.type))
        self.to_visit.append(call)

    def __getInputForCallD(self):
        """
        Method to simulate the dashboard in an elevator. For simulation purposes this method gets the internal calls
        of an user
        :return: None
        """
        a = input("You go to floor : ")
        try:
            a = int(a)
            if len(self.to_visit) > 2:
                if a <= self.max_floor and a >= self.min_floor:
                    cond1 = self.direction == DirectionEnum.UP.value and a <= self.current_floor
                    cond2 = self.direction == DirectionEnum.DOWN.value and a >= self.current_floor
                    if cond1 or cond2:
                        message = "Elevator going  {}  from {} and do not serve floor {}"
                        raise ValueError(message.format(self.direction, self.current_floor, a))
                else:
                    raise ValueError("number of floor not between {} and  {}".format(self.min_floor, self.max_floor))
            else:
                c = Call(a, "D", self.to_visit[0].direction)
        except Exception as e:
            print('wrong entry {}'.format(str(e)))
            print('-' * 20)
            return None
        else:
            c = Call(a, "D", self.direction)
        return c

    def next_action(self):

        """
        for simulation purposes this method lunches the next action of the elevator
        (__close_door, __open_door, __move_down, __move_up, __getInputForCalD, receive_call)
        :return: None
        """
        if len(self.to_visit) > 0:
            call = self.to_visit[0]
            if call.floor < self.current_floor:
                self.__move_down()
                self.to_visit.sort(key=lambda x: x.floor, reverse=True)
            elif call.floor > self.current_floor:
                self.__move_up()
                self.to_visit.sort(key=lambda x: x.floor)
            else:
                self.__open_door()
                if call.type == "E":
                    c = self.__getInputForCallD()
                    if c:
                        self.receive_call(c)
                self.to_visit.pop(0)
                self.__close_door()

        else:
            if self.current_floor != 0:
                self.__move_down()
            if self.current_floor == 0:
                self.status = StatusEnum.HOLD.value
                self.direction = DirectionEnum.UP.value
                print("Elevator {}: current Position -> {}".format(self.id, self.current_floor))
                print("Elevator {}: status -> {}, direction -> {}".format(self.id, self.status, self.direction))


class Plateform:
    """
    the class that represents the entry point of the system
    it presents the building with elevators
    """
    def __init__(self, nb_floor, nb_elevator, min_floor, max_floor, choice_strategy=StrategyChoiceNearest()):

        """
        the constructor of the Plateforme class

        :param nb_floor: the number of floors in the simulation
        :param nb_elevator: the number of elevators in the simulatio
        :param min_floor: the number of the first floor
        :param max_floor: the number of the last floor
        :param choice_strategy: the strategy class to be used ( instances of StrategyChoice)
        """
        self.nb_floor = nb_floor
        self.nb_elevator = nb_elevator
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.elevators = [Elevator(self.max_floor, self.min_floor, i) for i in range(self.nb_elevator)]
        self.choice_strategy = choice_strategy

    def receive_call(self, call):
        """
        method to receive a call, get the right elevator for it applying the proper strategy
        and affect it to it
        :param call: the call
        :return: None
        """
        elv = self.choice_strategy.op_choice(self.elevators, call)
        if elv is not None:
            elv.receive_call(call)

    def next(self):
        """
        method for simulation purposes
        :return: None
        """
        for elv in self.elevators:
            elv.next_action()


def get_external_call(max_floor, min_floor):
    """
    this method is used to get user input to simulate external calls for elevators
    :return: the call
    """
    try:
        a = input("Ask for an elevator from floor number: ")
        if a != "pass":
            a = int(a)
            if a == max_floor:
                direction = DirectionEnum.DOWN.value
            elif a == min_floor:
                direction = DirectionEnum.UP.value
            elif a <= max_floor and a >= min_floor:
                direction = input("Indicate direction : ")
                if direction != DirectionEnum.UP.value and direction != DirectionEnum.DOWN.value:
                    raise ValueError("direction must be {} or {}".format(DirectionEnum.UP, DirectionEnum.DOWN))
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
    p = Plateform(10, 4, 0, 10)
    while True:
        c = get_external_call(p.max_floor, p.min_floor)
        if c is not None:
            p.receive_call(c)
        p.next()
        print('-' * 20)


9
