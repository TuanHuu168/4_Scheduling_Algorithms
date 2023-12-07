from ProcessState import ProcessState
from SchedulingAlgorithms import SchedulingAlgorithms

# RR (Round Robin)
# lớp RR kế thừa từ lớp SchedulingAlgorithms
class RR(SchedulingAlgorithms):
    quantum = 0

    def __init__(self, processes, quantum):
        super().__init__(processes)
        self.quantum = quantum #khoảng thời gian tối đa mà mỗi quá trình được chạy

    def execute(self, process):
        self.checkDelay()
        # nếu thời gian còn lại của quá trình nhỏ hơn hoặc bằng quantum, quá trình đó sẽ hoàn thành và được ghi vào biểu đồ Gantt.
        if process.getBurstTimeRemaining() <= self.quantum:
            self.gantt_chart.append([process.getName(), process.getBurstTimeRemaining()])
            # cập nhật thời gian hiện tại thêm 1 khoảng là quantum
            self.current_time += process.getBurstTimeRemaining()

            # Đánh dấu là process đã hoàn thành
            self.setCompletedProcess(process)

        # nếu quá trình vẫn đang chạy, thời gian còn lại của nó sẽ được giảm đi bởi quantum và quá trình sẽ được đưa trở lại vào hàng đợi sẵn sàng.
        elif process.getState() == ProcessState.RUNNING:

            # process đang chạy sẽ giảm đi một khoảng thời gian là quantum
            process.setBurstTimeRemaining(process.getBurstTimeRemaining() - self.quantum)
            self.gantt_chart.append([process.getName(), self.quantum])
            # Tăng 1 khoảng là quantum
            self.current_time += self.quantum

            # Nếu thời gian còn lại của process > 0 -> thêm lại vào queue
            if self.remaining_process != 0:
                self.setReadyQueues()

            process.setState(ProcessState.READY)
            self.ready_queues.append(process)

    def run(self):
        # lặp cho đến khi tất cả các process được thực hiện
        while self.remaining_process:
            # Thêm các hàng đợi vào queue
            self.setReadyQueues()
            # nếu không có process nào trong hàng đợi sẵn sàng (tức là CPU đang rảnh), thời gian hiện tại và độ trễ được tăng lên.
            if not self.ready_queues:
                self.current_time += 1
                self.delay += 1
                continue

            # lấy ra process sẽ được thực hiện tiếp theo
            process = self.getRunningProcess()
 
            # thực hiện process đã chọn
            self.execute(process)