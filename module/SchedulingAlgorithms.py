from ProcessState import ProcessState

# SchedulingAlgorithms: định nghĩa lớp cơ sở cho các thuật toán lập lịch
class SchedulingAlgorithms:
    # Thuộc tính
    processes = [] # Danh sách các process cần được lập lịch
    ready_queues = [] # Hàng đợi các process sẵn sàng để thực hiện
    remaining_process = 0 # Số lượng process còn lại chưa hoàn thành
    completed_processes = [] # Danh sách các process đã hoàn thành
    current_time = 0 # Thời gian hiện tại trong mô phỏng lập lịch
    n = 0 # Tổng số process
    run_time = 0 # Thời gian chạy của process hiện tại
    temp_process = None # Quá trình tạm thời hiện tại
    gantt_chart = [] # Dữ liệu cho biểu đồ Gantt
    delay = 0 # Thời gian chờ

    def __init__(self, processes):
        self.processes = processes
        self.ready_queues = []
        self.completed_processes = []
        self.current_time = 0
        self.n = len(processes)
        self.remaining_process = self.n
        self.run_time = 0
        self.temp_process = None
        self.gantt_chart = []
        self.delay = 0

        # Sắp xếp các process theo thời gian đến
        self.processes.sort(key=lambda x: x.getArriveTime())

    # Thêm 1 hoặc nhiều process vào process list
    def addProcesses(self, process):
        # Thêm nhiều process
        if isinstance(process, list):
            for p in process:
                self.processes.append(p)
        # Thêm 1 process
        elif isinstance(process, object):
            self.processes.append(process)

    # getter
    def getN(self):
        return self.n

    def getProcesses(self):
        return self.processes

    def getCompletedProcesses(self):
        if not self.completed_processes:
            return self.processes
        else:
            return self.completed_processes
    
    def getCurrentTime(self):
        return self.current_time

    def getGanttChart(self):
        return self.gantt_chart
    


    # Cập nhật hàng đợi sẵn sàng với các quá trình đã đến và sẵn sàng chạy
    def setReadyQueues(self):
        # Thêm các process mới vào hàng đợi
        for process in self.processes:
            # Nếu thời gian đến của process > thời gian hiện tại, dừng vòng lặp
            if process.getArriveTime() > self.current_time:
                break

            # thêm vào hàng đợi nếu process chưa trong hàng đợi, chưa hoàn thành và thời gian đến <= thời gian hiện tại
            if not process.getIsQueued() and not process.getIsCompleted() and process.getArriveTime() <= self.current_time:
                # Cập nhật trạng thái và thêm vào hàng đợi
                process.setState(ProcessState.READY)
                process.setIsQueued(True)
                self.ready_queues.append(process)
            
    # Lấy process đầu tiên từ hàng đợi sẵn sàng để chạy
    def getRunningProcess(self):
        # Kiểm tra xem process đầu tiên có ở trạng thái ready hay không
        if self.ready_queues[0].getState() == ProcessState.READY:
            # Lấy khỏi hàng đợi và chuyển state thành running
            process = self.ready_queues.pop(0)
            process.setState(ProcessState.RUNNING)

            # Cập nhật thời gian bắt đầu nếu chưa có
            if process.getStartTime() is None:
                process.setStartTime(self.current_time)

            return process
        # Trả về none nếu không có process nào trong hàng đợi
        return None
    
    # Đánh dấu một process là đã hoàn thành và cập nhật các thông số
    def setCompletedProcess(self, process):

        # Cập nhật thời gian hoàn thành
        process.setFinishTime(self.current_time)

        # Tính Toán thời gian chuyển đổi
        process.setTurnaroundTime()

        # Tính toán thời gian chờ
        process.setWaitingTime()


        # Cập nhật trạng thái của quá trình
        process.setState(ProcessState.EXIT)
        process.setIsCompleted(True)
        process.setIsQueued(False)

        # Cập nhật process list
        self.completed_processes.append(process)
        self.processes.remove(process)

        self.remaining_process -= 1

    # Kiểm tra trễ
    def checkDelay(self):
        # Nếu trong một khoảng thời gian không có process nào thực hiện
        if self.delay:
            # Trễ được biểu diễn bằng dấu ##
            self.gantt_chart.append(['##', self.delay]) 
            # Đặt lại trễ
            self.delay = 0

    # Thực hiện một quá trình theo thuật toán không chia sẻ thời gian
    def executeNonPreemptive(self, process):
        # Kiểm tra delay
        self.checkDelay()

        # Chạy process
        # Thời gian hiện tại được tăng lên bằng thời gian chạy process
        self.current_time += process.getBurstTime() 
        # Đặt thời gian còn lại = 0 -> Hoàn thành
        process.setBurstTimeRemaining(0) 

        # Ngừng tiến trình nếu nó đã hoàn thành
        if process.getBurstTimeRemaining() == 0:
            # Thêm thông tin process (tên, thời gian) vào sơ đồ Gantt
            self.gantt_chart.append([process.getName(),
                                    process.getBurstTime()])
            # Đánh dấu process đã hoàn thành
            self.setCompletedProcess(process)

    # Thực hiện một quá trình theo thuật toán chia sẻ thời gian
    def executePreemptive(self, process):
        # Kiểm tra delay
        self.checkDelay()

        # Kiểm tra process hiện tại có phải process tạm thời hay không?
        if process != self.temp_process:
            # Nếu process tạm thời chưa hoàn thành, thêm vào sơ đồ Gantt
            if self.temp_process and not self.temp_process.getIsCompleted():
                self.gantt_chart.append([self.temp_process.getName(), self.run_time])
                self.run_time = 0 # Thời gian chạy = 0
            self.temp_process = process # Cập nhật process tạm thời = process hiện tại
        self.run_time += 1 # Tăng thời gian chạy của process hiện tại lên 1

        # Tăng thời gian chạy hiện tại lên 1 và giảm đi 1 ở thời gian còn lại
        self.current_time += 1
        process.setBurstTimeRemaining(process.getBurstTimeRemaining() - 1)

        # Ngừng process nếu đã hoàn thành
        if process.getBurstTimeRemaining() == 0:
            self.gantt_chart.append([process.getName(), self.run_time])
            self.temp_process = process
            self.run_time = 0

            # Đánh dấu process đã hoàn thành
            self.setCompletedProcess(process)

        # Nếu process vẫn chạy, thêm lại vào queue và đặt lại trạng thái thành ready
        elif process.getState() == ProcessState.RUNNING:
            process.setState(ProcessState.READY)
            self.ready_queues.append(process)
