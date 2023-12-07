from SchedulingAlgorithms import SchedulingAlgorithms

# SJF (Shortest Job First)
# lớp SJF kế thừa từ lớp SchedulingAlgorithms
class SJF(SchedulingAlgorithms):
    def __init__(self, processes):
        super().__init__(processes)

    def run(self):
        # Lặp cho tới khi không còn process
        while self.remaining_process:
            
            # Thêm các process vào queue
            self.setReadyQueues()

            # nếu không có quá trình nào trong hàng đợi sẵn sàng (tức là CPU đang rảnh), thời gian hiện tại và độ trễ được tăng lên.
            if not self.ready_queues:
                self.current_time += 1
                self.delay += 1
                continue

            # Sắp xếp các process dựa vào burst time
            self.ready_queues.sort(key=lambda x: x.getBurstTime()) 
            
            # Lấy thông tin process đang chạy
            process = self.getRunningProcess()

            # thực hiện process đã chọn
            self.executeNonPreemptive(process)