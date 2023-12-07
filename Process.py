from ProcessState import ProcessState

# Tạo class Process để lưu các thông tin các process
class Process:
    # Các thuộc tính
    __name = ""
    __burst_time = None
    __arrive_time = None
    __state = None
    __start_time = None
    __finish_time = None
    __turnaround_time = None
    __waiting_time = None
    __burst_time_remaining = None
    __isQueued = False
    __isCompleted = False

    # Hàm tạo gán tên, arrive và burst time cho đối tượng và để trạng thái của đối tượng là new
    def __init__(self, name, arrive_time, burst_time):
        self.__name = name
        self.__burst_time = burst_time
        self.__arrive_time = arrive_time
        self.__state = ProcessState.NEW
        self.__start_time = None
        self.__finish_time = None
        self.__turnaround_time = None
        self.__waiting_time = None
        self.__burst_time_remaining = burst_time
        self.__isQueued = False
        self.__isCompleted = False

    # Reset lại process

    def reset(self):
        self.__state = ProcessState.NEW
        self.__start_time = None
        self.__finish_time = None
        self.__turnaround_time = None
        self.__waiting_time = None
        self.__burst_time_remaining = self.__burst_time
        self.__isQueued = False
        self.__isCompleted = False

    # setter
    def setName(self, name):
        self.__name = name

    def setArriveTime(self, arrive_time):
        self.__arrive_time = arrive_time

    def setBurstTime(self, burst_time):
        self.__burst_time = burst_time

    def setState(self, state):
        self.__state = state

    def setStartTime(self, start_time):
        self.__start_time = start_time

    def getStartTime(self):
        return self.__start_time

    def setFinishTime(self, finish_time):
        self.__finish_time = finish_time

    def getFinishTime(self):
        return self.__finish_time

    def setTurnaroundTime(self, time=None):
        if time is None:
            self.__turnaround_time = self.__finish_time - self.__arrive_time
        else:
            self.__turnaround_time = time

    def setWaitingTime(self, time=None):
        if time is None:
            self.__waiting_time = self.__turnaround_time - self.__burst_time
        else:
            self.__waiting_time = time

    def setBurstTimeRemaining(self, time):
        self.__burst_time_remaining = time


    def setIsCompleted(self, isCompleted):
        self.__isCompleted = isCompleted

    # getter

    def getName(self):
        return self.__name

    def getArriveTime(self):
        return self.__arrive_time

    def getBurstTime(self):
        return self.__burst_time

    def getState(self):
        return self.__state

    def getStateValue(self):
        return self.__state.value

    def getTurnaroundTime(self):
        return self.__turnaround_time

    def getWaitingTime(self):
        return self.__waiting_time

    def getBurstTimeRemaining(self):
        return self.__burst_time_remaining

    # setter dan getter untuk is queued
    def setIsQueued(self, isQueued):
        self.__isQueued = isQueued

    def getIsQueued(self):
        return self.__isQueued

    def getIsCompleted(self):
        return self.__isCompleted

    # Lấy data dưới dạng dict
    def getDict(self):
        dict = {
            'Name': self.__name,
            'Arrive Time': self.__arrive_time,
            'Burst Time': self.__burst_time,
            'Start Time': self.__start_time,
            'Finish Time': self.__finish_time,
            'Turnaround Time': self.__turnaround_time,
            'Waiting Time': self.__waiting_time,
        }

        # Xóa các giá trị có giá trị None
        keys_to_remove = [k for k, v in dict.items() if v is None]
        for key in keys_to_remove:
            dict.pop(key)

        return dict
