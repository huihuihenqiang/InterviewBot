import sqlite3
import sys
import os
import pandas as pd
import pyaudio
import wave
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from chatbot.bot import get_bot_answer
from chatbot.bot import get_bot_answer_wenti
from chatbot.utils import speech_to_text
from PyQt5.QtWidgets import QMessageBox, QLabel
from chatbot.bot import capture_and_extract_text
from PyQt5.QtWidgets import QPushButton, QFileDialog
#from chatbot.audio_thread import AudioThread  # 导入刚刚创建的音频线程类
from chatbot.bot import generate_prompt
from PyQt5.QtWidgets import QSlider, QLabel, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QRadioButton, QVBoxLayout, QTextEdit, QWidget
from chatbot.taskthread import TaskThread
from chatbot.bot import get_kg_answer


class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Professional Interview Chatbot")
        self.setGeometry(100, 100, 1000, 900)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 去掉窗口边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        # 创建底部按钮布局
        self.button_layout = QHBoxLayout()
        self.is_dragging = False  # 初始化拖动标志
        self.drag_position = None  # 初始化拖动位置

        self.layout = QVBoxLayout(self)
        # 设置聊天记录框，显示用户和机器人的对话
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)  # 设置为只读，用户不能修改聊天记录
        self.chat_history.setStyleSheet("""
            background-color: rgba(0, 0, 0, 70);
            color: red;
            font-size: 25px;
            font-weight: bold;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    
        """)
        self.layout.addWidget(self.chat_history)  # 将聊天框添加到布局中
        # 设置用户输入框和发送按钮
        self.input_layout = QHBoxLayout()
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Enter your interview question...")
        self.user_input.setStyleSheet(
            "background-color: rgba(0, 0, 0, 200); color: white; font-size: 14px; padding: 10px;")
        self.input_layout.addWidget(self.user_input)

        # 创建发送按钮
        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: white; font-size: 14px; padding: 10px;")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)
        # 设置输入框获得焦点
        self.user_input.setFocus()
        # 定时器，用于逐段显示消息
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_next_message)
        self.messages = []
        self.current_message_index = 0


        # 语音录音按钮
        self.voice_button = QPushButton("🎤录音", self)
        self.voice_button.setStyleSheet("""
                                  background-color: rgba(0, 0, 255, 150);
                                  color: white;
                                  font-size: 20px;
                                  padding: 5px;
                                  border-radius: 10px;
                              """)
        #self.voice_button.setGeometry(60, 90, 40, 40)
        self.voice_button.setFixedSize(90, 50)
        self.voice_button.clicked.connect(self.toggle_recording)
        #
        # 录音相关变量
        self.is_recording = False
        self.audio = None
        self.stream = None
        self.frames = []
        self.output_filename = "assets/recorded_audio.wav"

        # 捕获键盘空格键事件，用于开始/停止录音
        self.user_input.installEventFilter(self)
        # 连接回车键事件，当按下 Enter 键时发送消息
        self.user_input.returnPressed.connect(self.send_message)

        # 知识库按钮
        self.kg_button = QPushButton("📕", self)
        self.kg_button.setStyleSheet("""
                                  background-color: rgba(0, 0, 0, 150);
                                  color: white;
                                  font-size: 20px;
                                  padding: 5px;
                                  border-radius: 10px;
                              """)
        self.kg_button.setGeometry(850, 0, 40, 40)
        self.kg_button.setFixedSize(40, 40)
        self.kg_button.pressed.connect(self.stru_kg)

        # 拖动按钮
        self.drag_button = QPushButton("☰", self)
        self.drag_button.setStyleSheet("""
                          background-color: rgba(0, 0, 0, 150);
                          color: white;
                          font-size: 20px;
                          padding: 5px;
                          border-radius: 10px;
                      """)
        self.drag_button.setGeometry(900, 0, 40, 40)
        self.drag_button.setFixedSize(40, 40)
        self.drag_button.pressed.connect(self.start_drag)

        # 关闭按钮
        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("""
            background-color: rgba(255, 0, 0, 180); 
            color: white; 
            font-size: 20px; 
            padding: 5px;
            border-radius: 10px;
        """)
        self.close_button.clicked.connect(self.close)
        self.close_button.setGeometry(950, 0, 40, 40)
        self.close_button.setFixedSize(40, 40)

        # 创建截图按钮
        self.capture_button = QPushButton("📷截图", self)
        self.capture_button.setStyleSheet("""
            background-color: rgba(0, 0, 255, 150);
            color: white;
            font-size: 20px;
            padding: 5px;
            border-radius: 10px;
        """)
        self.capture_button.setFixedSize(90, 50)
        # 连接按钮点击事件
        self.capture_button.clicked.connect(self.on_capture_button_click)

        # 创建清空聊天记录按钮
        self.clear_button = QPushButton("清空记录", self)
        self.clear_button.setStyleSheet("""
                background-color: rgba(255, 0, 0, 150);
                color: white;
                font-size: 20px;
                padding: 5px;
                border-radius: 10px;
            """)
        self.clear_button.setFixedSize(90, 50)
        self.clear_button.clicked.connect(self.clear_chat_history)



        # 创建另一个按钮用于加载文件并生成 prompt.txt
        self.load_button = QPushButton("加载简历", self)
        self.load_button.setStyleSheet("""
                        background-color: rgba(0, 255, 0, 150);
                        color: white;
                        font-size: 20px;
                        padding: 5px;
                        border-radius: 10px;
                    """)
        self.load_button.setFixedSize(90, 50)
        self.load_button.clicked.connect(self.load_resume)

        # 创建知识库模式按钮
        self.kga_button = QPushButton("启用KG", self)
        self.kga_button.setStyleSheet("""
                                background-color: rgba(0, 0, 255, 150);
                                color: white;
                                font-size: 20px;
                                padding: 5px;
                                border-radius: 10px;
                            """)
        self.kga_button.setFixedSize(90, 50)
        self.kga_button.clicked.connect(self.toggle_kg)
        self.is_kg=False



        # 将按钮添加到底部按钮布局
        self.button_layout.addWidget(self.voice_button)
        self.button_layout.addWidget(self.capture_button)
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addWidget(self.kga_button)
        # 将按钮布局添加到主布局的底部
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)


        # 创建单选按钮：控制字体颜色
        self.black_radio = QRadioButton("代码模式", self)
        self.black_radio.setChecked(False)  # 默认b选中黑色字体
        self.black_radio.toggled.connect(self.update_font_color)

        self.white_radio = QRadioButton("浅色模式", self)
        self.white_radio.setChecked(False)  # 默认不选中白色字体
        self.white_radio.toggled.connect(self.update_font_color)

        self.red_radio = QRadioButton("默认模式", self)
        self.red_radio.setChecked(True)  # 默认选中红色字体
        self.red_radio.toggled.connect(self.update_font_color)

        self.black_radio1 = QRadioButton("专注模式", self)
        self.black_radio1.setChecked(False)  # 默认b选中黑色字体
        self.black_radio1.toggled.connect(self.update_font_color)


        # 设置单选按钮的样式
        self.black_radio.setStyleSheet("""
                    font-size: 20px;
                    padding: 10px;
                """)
        self.white_radio.setStyleSheet("""
                    font-size: 20px;
                    padding: 10px;
                """)
        self.red_radio.setStyleSheet("""
                    font-size: 20px;
                    padding: 10px;
                """)
        self.black_radio1.setStyleSheet("""
                            font-size: 20px;
                            padding: 10px;
                        """)

        # 将单选按钮添加到布局
        self.button_layout.addWidget(self.black_radio)
        self.button_layout.addWidget(self.white_radio)
        self.button_layout.addWidget(self.red_radio)
        self.button_layout.addWidget(self.black_radio1)
        # self.button_layout.addWidget(self.white_radio1)
        # 将按钮布局添加到主布局的底部
        self.layout.addLayout(self.button_layout)

        # 设置布局
        self.setLayout(self.layout)

    def toggle_kg(self):
        """切换知识库状态"""
        if self.is_kg:
            self.kga_button.setText("启用KG")
            self.stop_kg()
        else:
            self.kga_button.setText("🔴")
            self.start_kg()

    def start_kg(self):
        self.is_kg=True
        self.chat_history.append('知识库已经启用...')
        pass
    def stop_kg(self):
        self.is_kg=False
        self.chat_history.append('知识库已经禁用...')
        pass

    def stru_kg(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel Files (*.xlsx)")  # 只允许选择 .xlsx 文件
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                self.chat_history.append('正在构建知识库！请耐心等待....')
                self.load_excel_to_db(file_path)
            else:
                print("没有选择文件，程序退出。")
        return None

    def load_excel_to_db(self,file_path, db_name="knowledge/knowledge.db"):
        # 加载 Excel 文件
        df = pd.read_excel(file_path)

        # 检查数据格式是否符合要求
        if '问题' not in df.columns or '答案' not in df.columns:
            print("Excel 格式错误，请确保包含 '问题' 和 '答案' 列。")
            return

        # 连接到数据库
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 创建表格（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        ''')

        # 插入数据，避免重复
        for _, row in df.iterrows():
            question, answer = row['问题'], row['答案']

            # 检查数据库中是否已存在相同的问答对
            cursor.execute("SELECT COUNT(*) FROM knowledge WHERE question = ? AND answer = ?", (question, answer))
            if cursor.fetchone()[0] == 0:
                # 不重复，插入新记录
                cursor.execute("INSERT INTO knowledge (question, answer) VALUES (?, ?)", (question, answer))
            else:
                # print(f"重复数据：'{question}' 已存在，跳过插入。")
                pass

        # 提交并关闭数据库连接
        conn.commit()
        conn.close()
        print(f"数据已从 '{file_path}' 导入到数据库 '{db_name}' 中。")
        self.show_popup_message("成功", "个人专属知识库已生成！如需使用请选择知识库模式！")


    def update_font_color(self):
        """更新字体颜色，根据单选按钮的选择来应用颜色"""
        if self.black_radio.isChecked():
            self.chat_history.setStyleSheet(f"""
                        background-color: rgba(0, 0, 0, 200);
                        color: white;
                        font-size: 18px;
                        font-weight: bold;
                        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                    """)
            #color = "black"
            #print("1")
        elif self.white_radio.isChecked():
            self.chat_history.setStyleSheet(f"""
                                    background-color: rgba(0, 0, 0, 0);
                                    color: yellow;
                                    font-size: 30px;
                                    font-weight: bold;
                                    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                                """)
        elif self.red_radio.isChecked():
            self.chat_history.setStyleSheet(f"""
                                    background-color: rgba(0, 0, 0, 70);
                                    color: red;
                                    font-size: 25px;
                                    font-weight: bold;
                                    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                                """)
        elif self.black_radio1.isChecked():
            self.chat_history.setStyleSheet(f"""
                                    background-color: rgba(0, 0, 0, 250);
                                    color: white;
                                    font-size: 30px;
                                    font-weight: bold;
                                    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                                """)
        else:
            self.chat_history.setStyleSheet(f"""
                                                background-color: rgba(0, 0, 0, 70);
                                                color: red;
                                                font-size: 25px;
                                                font-weight: bold;
                                                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                                            """)

    def load_resume(self):
        """选择文件并生成 prompt.txt"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.pdf)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            #generate_prompt(file_path)  # 调用函数处理文件
            self.chat_history.append('正在执行任务！所需时间较长，请耐心等待....')
            #加入多线程
            self.thread_merge = TaskThread(generate_prompt,file_path)
            self.thread_merge.finished_signal.connect(self.load_resum_informa)
            # 回收线程
            self.thread_merge.finished_signal.connect(self.thread_merge.deleteLater)
            self.thread_merge.start()



    def load_resum_informa(self):
        """处理合并后的数据"""
        #print("合并后的数据：", result)# 弹出提示框提醒用户
        self.show_popup_message("成功", "prompt.txt 文件已生成！请重启应用更新信息！")

    def show_popup_message(self, title, message):
        """显示提示框"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def clear_chat_history(self):
        """清空聊天记录"""
        self.chat_history.clear()
        print("聊天记录已清空！")

    def on_capture_button_click(self):
        self.chat_history.append('Start screenshot...')
        text=capture_and_extract_text()

        # 加入多线程
        self.thread_merge = TaskThread(get_bot_answer_wenti,text)
        self.thread_merge.result_signal.connect(self.split)
        # 回收线程
        self.thread_merge.finished_signal.connect(self.thread_merge.deleteLater)
        self.thread_merge.start()


    def send_message(self):
        """处理发送消息事件"""
        user_message = self.user_input.text().strip()
        if user_message:
            self.chat_history.append(f"You: {user_message}")
            self.chat_history.append("")  # 空行分隔
            self.user_input.clear()
            '''
            这里的写法是：如果知识库启用优先使用知识库查询，如果没找到就使用大模型。如果禁用直接使用大模型。
            '''
            if self.is_kg:
                results = get_kg_answer(user_message)
                if results:
                    self.chat_history.append(f"找到 {len(results)} 条相关记录：")
                    for idx, (question, answer) in enumerate(results, 1):
                        self.chat_history.append(f"{idx}. 问题: {question}\n   答案: {answer}\n")
                else:
                    self.chat_history.append(f"本地知识库未查询到相关记录，大模型回答中...")
                    answer = get_bot_answer(user_message)
                    self.split(answer)
            else:
                answer = get_bot_answer(user_message)
                self.split(answer)


    def display_next_message(self):
        """逐段显示机器人的消息"""
        if self.current_message_index < len(self.messages):
            message = self.messages[self.current_message_index]
            self.chat_history.append(message)
            self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
            self.current_message_index += 1
        else:
            self.timer.stop()

    def start_drag(self):
        """开始拖动窗口"""
        self.is_dragging = True
        self.drag_position = QCursor.pos() - self.frameGeometry().topLeft()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def toggle_recording(self):
        """切换录音状态"""
        if self.is_recording:
            self.voice_button.setText("🎤录音")  # 设置为红点表情，表示正在录音
            self.stop_recording()
        else:
            self.voice_button.setText("🔴")  # 设置为红点表情，表示正在录音
            self.start_recording()

    def start_recording(self):
        """开始录音"""
        self.chat_history.append('Start recording...')
        if self.is_recording:
            return  # 如果已经在录音，直接返回

        self.is_recording = True
        self.frames = []

        # 初始化 pyaudio 和音频流
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=1024)
        self.voice_button.setText("🔴")  # 更改按钮文本
        #self.chat_history.append('start')
        self.record_audio()  # 开始录音

    def stop_recording(self):
        """停止录音并保存文件"""
        # self.voice_button.setText("🎤")
        if not self.is_recording:
            return

        self.is_recording = False
        # 恢复按钮文本
        # 停止并关闭音频流
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

        # 保存文件
        if not os.path.exists('assets'):
            os.makedirs('assets')  # 确保 assets 文件夹存在

        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(self.frames))


        # 录音完成后进行语音识别

        self.on_recording_complete()
        # 清理录音数据
        self.frames = []
        self.stream = None
        self.audio = None  # 彻底清除音频流对象

    def on_recording_complete(self):
        """录音完成后进行语音识别"""
        result = speech_to_text(self.output_filename)
        if result.get('err_no') == 0:
            recognized_text = result.get('result', [])[0]
            self.chat_history.append(f"You：{recognized_text}")
            print(f"识别结果: {recognized_text}")
            # 将识别的文本发送给大模型
            if self.is_kg:
                results = get_kg_answer(recognized_text)
                if results:
                    self.chat_history.append(f"找到 {len(results)} 条相关记录：")
                    for idx, (question, answer) in enumerate(results, 1):
                        self.chat_history.append(f"{idx}. 问题: {question}\n   答案: {answer}\n")
                else:
                    self.chat_history.append(f"本地知识库未查询到相关记录，大模型回答中...")

                    self.thread_merge = TaskThread(get_bot_answer, recognized_text)
                    # print('ddddd')
                    self.thread_merge.result_signal.connect(self.split)
                    # 回收线程
                    self.thread_merge.finished_signal.connect(self.thread_merge.deleteLater)
                    self.thread_merge.start()

                    # answer = get_bot_answer(user_message)
                    # self.split(answer)
            else:
                # answer = get_bot_answer(user_message)
                # self.split(answer)
                self.thread_merge = TaskThread(get_bot_answer, recognized_text)
                # print('ddddd')
                self.thread_merge.result_signal.connect(self.split)
                # 回收线程
                self.thread_merge.finished_signal.connect(self.thread_merge.deleteLater)
                self.thread_merge.start()

            # 加入多线程
            #print('fff')
            # self.thread_merge = TaskThread(get_bot_answer, recognized_text)
            # #print('ddddd')
            # self.thread_merge.result_signal.connect(self.split)
            # # 回收线程
            # self.thread_merge.finished_signal.connect(self.thread_merge.deleteLater)
            # self.thread_merge.start()


        else:
            print(f"语音识别失败: {result.get('err_msg')}")

    def split(self, result):
        answer = result + '\n----------------------end----------------------------'
        #answer = get_bot_answer(recognized_text) + '\n结束'
        #print("kkkkkk")
        self.messages = answer.split('\n')
        self.current_message_index = 0
        self.timer.start(0)

    def record_audio(self):
        """持续录音"""
        if self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
            QTimer.singleShot(10, self.record_audio)  # 递归调用继续录音



    def eventFilter(self, source, event):
        """捕获空格键事件"""
        if event.type() == event.KeyPress and event.key() == Qt.Key_Space:
            self.toggle_recording()
            return True
        elif event.type() == event.KeyPress and event.modifiers() == (Qt.ControlModifier | Qt.AltModifier):
            # Ctrl + Alt 触发截图按钮点击事件
            self.capture_button.click()  # 模拟点击截图按钮
            return True  # 事件已处理
        return super().eventFilter(source, event)
