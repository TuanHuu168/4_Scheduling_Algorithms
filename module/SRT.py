from SchedulingAlgorithms import SchedulingAlgorithms

# SRT (Shortest Remaining Time)
# lớp SRT kế thừa từ lớp SchedulingAlgorithms
class SRT(SchedulingAlgorithms):
    def __init__(self, processes):
        super().__init__(processes)

    def run(self):
        # Lặp cho tới khi không còn process nào
        while self.remaining_process:
            
            # Thêm các process vào queue
            self.setReadyQueues()

            # nếu không có tiến trình nào trong hàng đợi sẵn sàng (tức là CPU đang rảnh), thời gian hiện tại và độ trễ được tăng lên.
            if not self.ready_queues:
                self.current_time += 1
                self.delay += 1
                continue

            # Sắp xếp theo process có thời gian hoàn thành nhỏ nhất -> lớn nhất
            # ------------------------------------------------------
            self.ready_queues.sort(key=lambda x: x.getBurstTimeRemaining()) 
            # ------------------------------------------------------
            
            # Lấy process đang chạy
            process = self.getRunningProcess()

            # Thực hiện process đã chọn
            self.executePreemptive(process)