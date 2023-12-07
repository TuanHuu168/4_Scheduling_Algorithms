from Table import Table
import customtkinter as ct

# Hiển thị thông tin chi tiết của các process trong bảng trong bảng


def print_in_table(processes, simulationWindow):
    # Nếu process có start time, sắp xếp theo trình tự này
    if processes[0].getStartTime():
        processes = sorted(processes, key=lambda p: p.getStartTime())

    # Thêm các process dict vào list
    dictProcesses = []
    for process in processes:
        dictProcesses.append(process.getDict())
    # Tạo bảng và in ra các process dưới dạng bảng
    table = Table(simulationWindow)
    table.addData(dictProcesses)
    return table.display()

# In ra các giá trị trung bình đã được tính toán
def print_off_table(processes, processFrame):
    # Lấy số lượng tiến trình
    n = len(processes)

    # Tìm thời gian hoàn thành cuối cùng của process
    total_time = 0
    for process in processes:
        if total_time < process.getFinishTime():
            total_time = process.getFinishTime()

    avg_waiting_time = sum(p.getWaitingTime() for p in processes) / n

    # Thời gian chờ trung bình (burst -> turnaround)
    averageVal = ct.CTkLabel(processFrame, text="Average Waiting Time: {:.2f}".format(
        avg_waiting_time), font=("Time New Roman", 20), justify="left")
    averageVal.pack(padx=10, pady=5)

# Hàm để chọn màu sắc cho sơ đồ Gantt


def get_color(index):
    # Danh sách các màu sắc
    colors = ['light blue', 'light green', 'light coral', 'light goldenrod',
              'light pink', 'light salmon', 'light grey', 'light cyan']
    return colors[index % len(colors)]

# In sơ đồ Gantt


def printGanttChart(ganttChart, processFrame):
    # Tính toán chiều rộng cần thiết dựa trên tổng burst time
    total_burst_time = sum([process[1] for process in ganttChart])
    # 40 pixels cho mỗi đơn vị thời gian + lề
    canvas_width = total_burst_time * 25 + 50
    canvas_height = 100  # Chiều cao cố định cho canvas

    # Tạo canvas
    canvas = ct.CTkCanvas(
        processFrame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)

    # Vẽ sơ đồ Gantt
    x_start = 20  # Vị trí bắt đầu của công việc đầu tiên
    y_top = 20   # Vị trí y cố định cho đỉnh trên của hình chữ nhật
    y_bottom = 60  # Chiều dài của hình chữ nhật

    for index, process in enumerate(ganttChart):
        # Tính toán vị trí kết thúc dựa trên burst time
        x_end = x_start + process[1] * 25
        color = get_color(index)  # Lấy màu từ hàm get_color
        # Vẽ hình chữ nhật
        canvas.create_rectangle(x_start, y_top, x_end, y_bottom, fill=color)
        # Vẽ nhãn cho mỗi process
        canvas.create_text((x_start + x_end) / 2, (y_top +
                           y_bottom) / 2, text=process[0], fill="black")
        x_start = x_end  # Cập nhật vị trí bắt đầu cho process tiếp theo

    # Vẽ trục thời gian
    x_start = 20  # Khởi tạo lại vị trí bắt đầu
    time = 0  # Thời gian bắt đầu từ 0
    for process in ganttChart:
        # Vẽ số cho mỗi mốc thời gian
        canvas.create_text(x_start, y_bottom + 20, text=str(time))
        x_start += process[1] * 25  # Cập nhật vị trí cho số tiếp theo
        time += process[1]  # Cập nhật thời gian

    # Vẽ số cuối cùng
    canvas.create_text(x_start, y_bottom + 20, text=str(time))
