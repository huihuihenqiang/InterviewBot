from PyQt5.QtCore import QThread, pyqtSignal


class TaskThread(QThread):
    result_signal = pyqtSignal(object)  # 返回结果信号

    progress_signal = pyqtSignal(str)  # 进度更新信号
    finished_signal = pyqtSignal() #执行完成信号

    def __init__(self, task_func, *args, **kwargs):

        super().__init__()

        self.task_func = task_func

        self.args = args

        self.kwargs = kwargs

    def run(self):



        try:

            result = self.task_func(*self.args, **self.kwargs)
            #print(result)
            self.result_signal.emit(result)

        except Exception as e:

            self.result_signal.emit(e)

        finally:
            self.finished_signal.emit()  # 任务完成后发送结束信号
