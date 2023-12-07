# import thư viện
import glob
import sys
import customtkinter as ct
from tkinter import ttk
from tkinter import messagebox
# Thêm đường dẫn "module" vào list để python tìm module để import
sys.path.append("module")
from Process import Process
# import model
from module.RR import RR
from module.SRT import SRT
from module.SJF import SJF
from module.FCFS import FCFS
from fitur import print_in_table, print_off_table, printGanttChart



# Hàm xóa tất cả các widget ở cửa sổ cũ
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# In thông tin
def printInfo(processes, mainFrame, ganttChart=None):
    printGanttChart(ganttChart, mainFrame)
    # In thông tin trong bảng
    print_in_table(processes, mainFrame)
    # In thông tin ngoài bảng
    print_off_table(processes, mainFrame)


# MAIN PROGRAM

# Đọc các file txt trong thư mục test-case
txt_files = glob.glob("test-case/*.txt")

# Tên thuật toán
schedulingAlgorithms = ["1, FCFS (First Come First Served)", "2, SJF (Shortest Job First)",
                        "3, SRT (Shortest Remaining Time)", "4, RR (Round Robin)"]

# Tạo giao diện
root = ct.CTk()
width, height = 800, 500
x, y = (root.winfo_screenwidth() -
        width)//2, (root.winfo_screenheight() - height)//2
root.geometry(f"{width}x{height}+{x}+{y}")
ct.CTkLabel(root, text="Chương trình mô phỏng thuật toán lập lịch", font=(
    "Time New Roman", 22, "bold")).pack(pady=10)

mainFrame = ct.CTkFrame(root, border_width=3)
mainFrame.pack(fill="both", expand=True, padx=20, pady=20)
root.title("Chương trình mô phỏng thuật toán lập lịch")

# trang chủ
global processes
selfDataFrame = None

# Lưu các process sau khi đã nhập thông in ở process được nhập thủ công
def saveProcesses():
    processes = []
    entryData = [int(widget.get()) for widget in selfDataFrame.winfo_children(
    ) if isinstance(widget, ct.CTkEntry)]
    j = 0
    for i in range(len(entryData)//2):
        processes.append(Process("P"+str(i), entryData[j], entryData[j+1]))
        j += 2
    simulation(processes)

# Tạo các ô để nhập các process thủ công
def createEntry(n):
    r = 0
    col = 0
    global selfDataFrame
    if selfDataFrame is not None:
        selfDataFrame.destroy()
    selfDataFrame = ct.CTkFrame(mainFrame)
    selfDataFrame.pack(padx=25)
    for i in range(n):
        ct.CTkLabel(
            selfDataFrame, text=f"Nhập Arrive time process thứ {i+1}", font=("Time New Roman", 16, "bold")).grid(row=r, column=col, padx=15)
        arrive = ct.CTkEntry(selfDataFrame, width=120)
        arrive.grid(row=r+1, column=col)
        ct.CTkLabel(
            selfDataFrame, text=f"Nhập Burst time process thứ {i+1}", font=("Time New Roman", 16, "bold")).grid(row=r+2, column=col, padx=15)
        burst = ct.CTkEntry(selfDataFrame, width=120)
        burst.grid(row=r+3, column=col)
        r += 4
        if (r == 8):
            col += 1
            r = 0
    saveData = ct.CTkButton(selfDataFrame, text="Lưu", font=("Time New Roman", 16, "bold"),
                            command=lambda: saveProcesses(), width=100, height=50)
    saveData.grid(columnspan=3, sticky="ew", padx=10, pady=10)

# Tạo trang để người dùng có thể nhập process thủ công
def selfEnterPage():
    clear_frame(mainFrame)
    quantityFrame = ct.CTkFrame(mainFrame)
    quantityFrame.pack(padx=20, pady=20)
    processQuantityLabel = ct.CTkLabel(
        quantityFrame, text="Nhập số lượng process: ", font=("Time New Roman", 16, "bold"))
    processQuantityLabel.grid(
        row=0, column=0, padx=20, pady=20)
    processQuantityEntry = ct.CTkEntry(quantityFrame, width=50)
    processQuantityEntry.grid(
        row=0, column=1, padx=20, pady=20)

    confirmBtn = ct.CTkButton(quantityFrame, text="Tạo ô", font=("Time New Roman", 16, "bold"), command=lambda: createEntry(
        int(processQuantityEntry.get())), width=80, height=50)
    confirmBtn.grid(row=0, column=2, padx=20)

# Trang để người dùng có thể import các data có sẫn
def importData():
    clear_frame(mainFrame)
    selectDataLabel = ct.CTkLabel(mainFrame, text="Chọn data có sẵn:", font=("Time New Roman", 16, "bold"))
    selectDataLabel.pack(padx=10)

    selectedOpt = ct.StringVar()
    opt = [f"{i+1}, {j}" for i, j in enumerate(txt_files)]
    selectOpt = ct.CTkOptionMenu(mainFrame, variable=selectedOpt, font=("Time New Roman", 16, "bold"), values=opt)
    selectOpt.pack(padx=10, pady=10)
    selectedOpt.set(opt[0])

    # Lấy thông tin các process được import từ file
    def getData(*args):
        processes = []
        choice = int(selectedOpt.get().split(",")[0])
        filename = txt_files[choice-1]
        # Đọc test-case
        with open(filename, 'r') as f:
            data = f.readlines()
        # Đọc dữ liệu của từng process
        for line in data:
            values = line.strip().split()
            if len(values) == 3:
                name, arrival_time, burst_time = values
                processes.append(
                    Process(name, int(arrival_time), int(burst_time)))
        simulation(processes)

    #Kiểm tra sự thay đổi khi người dùng lựa chọn các data có sẵn
    runBtn = ct.CTkButton(mainFrame, text="Chạy", font=("Time New Roman", 16, "bold"), command=lambda: getData())
    runBtn.pack(padx=10,pady=10)

    #selectedOpt.trace("w", getData) 

# Thoát ứng dụng (lựa chọn thứ 3)
def exitApp():
    root.destroy()

# Tạo 3 lựa chọn cho người dùng chọn ở phần trang chủ
def createOptionInput(frame, i, cmd=None):
    return ct.CTkButton(frame, text=i, command=cmd, font=("Time New Roman", 16, "bold"), width=120, height=50)


optInput = ["Tự nhập", "Import data có sẵn", "Thoát"]
optFrame = ct.CTkFrame(mainFrame)
optFrame.pack(padx=10, pady=10, expand=True)

self_enter = createOptionInput(optFrame, optInput[0], cmd=selfEnterPage)
self_enter.grid(row=0, column=0, padx=40, pady=50)

available_data = createOptionInput(optFrame, optInput[1], cmd=importData)
available_data.grid(row=0, column=1, padx=40, pady=50)

exit_app = createOptionInput(optFrame, optInput[2], cmd=exitApp)
exit_app.grid(row=0, column=2, padx=40, pady=50)


# Chạy giả lập các thuật toán
processFrame = None
# Chạy giả lập sau khi đã lấy được thông tin các process
def simulation(processes):
    # Tạo frame và các widget để nhập số lượng quantum
    def setupQuantumInput():
        global processFrame
        if processFrame is not None:
            processFrame.destroy()
        processFrame = ct.CTkFrame(mainFrame)
        processFrame.pack(padx=20, pady=10)
        ct.CTkLabel(processFrame, text="Nhập số lượng quantum", font=("Time New Roman", 16, "bold")).pack(padx=10)
        quantumInput = ct.CTkEntry(processFrame)
        quantumInput.pack(padx=10)
        quantumBtn = ct.CTkButton(
            processFrame, text="Xác nhận", font=("Time New Roman", 16, "bold"), command=lambda: getQuantum(quantumInput.get()))
        quantumBtn.pack(padx=10, pady=10)

    # Lấy số lượng quantum sau khi người dùng bấm nút xác nhận
    def getQuantum(quantum_val):
        try:
            global quantum
            quantum = int(quantum_val)
            setupQuantumInput()
            runRoundRobin()
        except ValueError:
            messagebox.showinfo(
                "Thông báo", "Giá trị nhập vào không phải là số nguyên")

    # Chạy thuật toán RR sau khi đã lấy được số lượng quantum hợp lệ
    def runRoundRobin():
        nonlocal processes
        # Chạy thuật toán RR với giá trị quantum mới
        rr = RR(processes, quantum)
        rr.run()
        processes = rr.getCompletedProcesses()

        # Hiển thị thông tin
        printInfo(processes, processFrame, rr.getGanttChart())

        # Reset các processes sau khi chạy xong thuật toán
        for process in processes:
            process.reset()

    # Chạy các thuật toán
    def runAlgorithm(*args):
        nonlocal processes
        global quantum
        global processFrame
        try:
            if processFrame is not None:
                processFrame.destroy()
        except Exception:
            pass
        processFrame = ct.CTkFrame(mainFrame)
        processFrame.pack(padx=20, pady=20)
        # Lấy lựa chọn của người dùng từ ô option menu
        choice = int(selectedAlgorithm.get().split(",")[0])

        # FCFS (First Come First Served)
        if choice == 1:
            fcfs = FCFS(processes)
            fcfs.run()
            processes = fcfs.getCompletedProcesses()
            # Hiển thị thông tin
            printInfo(processes, processFrame, fcfs.getGanttChart())

        # SJF (Shortest Job First)
        elif choice == 2:
            sjf = SJF(processes)
            sjf.run()
            processes = sjf.getCompletedProcesses()
            # Hiển thị thông tin
            printInfo(processes, processFrame, sjf.getGanttChart())

        # SRT (Shortest Remaining Time)
        elif choice == 3:
            srt = SRT(processes)
            srt.run()
            processes = srt.getCompletedProcesses()
            # Hiển thị thông tin
            printInfo(processes, processFrame, srt.getGanttChart())
            
        # RR (Round Robin)
        elif choice == 4:
            setupQuantumInput()

        # reset để có thể tiếp tục chạy khi sử dụng thuật toán khác
        for process in processes:
            process.reset()
    # Kiểm tra xem có process nào không. nếu không có thì thông báo không có process để chạy
    if processes:
        # Tạo cửa sổ mới để hiển thị thông tin cũng như chọn các thuật toán cho data đã chọn
        simulationWindow = ct.CTk()
        simulationWindow.geometry(f"800x500")
        ct.CTkLabel(simulationWindow, text="Chương trình mô phỏng thuật toán lập lịch", font=(
            "Time New Roman", 22, "bold")).pack(pady=10)
        mainFrame = ct.CTkFrame(simulationWindow, border_width=3)
        mainFrame.pack(fill="both", expand=True, padx=20, pady=20)
        simulationWindow.title("Simulation")

        # In thông tin về các process
        print_in_table(processes, mainFrame)

        # Người dùng chọn 1 trong 4 thuật toán
        ct.CTkLabel(mainFrame, text="Chọn thuật toán lập lịch", font=("Time New Roman", 16, "bold")).pack(
            padx=10, pady=10, anchor="w")
        selectedAlgorithm = ct.StringVar()
        algorithmOpt = ct.CTkOptionMenu(
            mainFrame, variable=selectedAlgorithm, font=("Time New Roman", 16, "bold"), values=schedulingAlgorithms)
        algorithmOpt.pack(padx=10, anchor="w")
        selectedAlgorithm.set(schedulingAlgorithms[0])
        selectedAlgorithm.trace("w", runAlgorithm)
        
        simulationWindow.mainloop()
    else:
        messagebox.showinfo("Thông báo", "Không có process nào để chạy!")


# chạy cửa sổ
root.mainloop()
