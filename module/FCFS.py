from SchedulingAlgorithms import SchedulingAlgorithms

# FCFS (First Come First Serve)
# lớp FCFS kế thừa từ lớp SchedulingAlgorithms
class FCFS(SchedulingAlgorithms):
    #hàm tạo của FCFS nhận list các process làm đối số và gọi hàm tạo của lớp cha
    def __init__(self, processes):
        super().__init__(processes)

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
            self.executeNonPreemptive(process)