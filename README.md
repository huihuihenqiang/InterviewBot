# InterviewBot 🚀
[![Python 3.8+](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3109/)

这是一个基于 PyQt 构建的大模型面试辅助工具,透明界面不用左顾右盼，专注于面试。旨在为面试提供智能支持，提升面试体验。此项目旨在模拟面试场景，训练面试技巧和能力。

不推荐也禁止将此工具应用到面试作弊中，并且强烈谴责任何作弊行为！！！任何人使用此工具造成任何后果都与本项目和作者本人无关。

<img src="https://github.com/user-attachments/assets/1ca41254-fe0b-42e9-8790-8face6fb36d3" alt="Image" style="border: 10px solid black;"/>

工具具备以下功能：

## 功能特点 ✨（不是画饼，功能都已经实现）

- **与大模型对话**：通过大模型进行智能问答，帮助模拟面试情境，准备问题与答案。接入的是gpt4.0，使用前请替换成自己的key。目前是单论对话，后续会修改成多轮对话。
- **语音识别对话**：支持语音识别功能，轻松与模型进行语音对话，提升互动性。使用的是百度的语音识别，使用前请替换成自己的key。
- **截图获取编程题**：可以截图当前屏幕内的算法编程题，自动识别并返回程序代码，这个准确率还不错哈哈哈哈哈。
![图片](https://github.com/user-attachments/assets/d6268096-f88a-460b-8b39-cfd195792082)

- **清空屏幕**：支持清空当前界面，保持整洁和专注。
- **透明界面**：界面为透明设计，共有四个模式可以调整，适配不同场景。
- **知识库构建**：支持通过问答 Excel 文件快速构建自定义知识库，快速获取精准答案，其实只要知识库搭建的好，效果不比大模型差，大模型太慢了。需要自己优化查询和数据库的结构，目前只是demo。
- **个性化简历回答**：用户可以上传个人简历，系统将根据简历提供个性化的回答（如与自身相关的经历）。
- **多线程**：反正就是用了一下，维持系统稳定性。
  
## 配置要求 ⚙️

1. **OCR软件**：在使用截图识别编程题时，需要下载并安装 OCR 软件tesseract。
2. **Jieba 分词**：分词库用于处理中文文本，确保准确的文本识别。
3. **OpenAI Key**：需要配置 OpenAI 的 API 密钥，用于与大模型进行对话。获取免费的大模型：[通义千问的官网](https://www.aliyun.com/product/bailian)
4. **百度云语音识别 Key**：需要配置百度云的语音识别 API 密钥。获取语音功能api:[百度云](https://cloud.baidu.com/product/speech.html)
5. **具体包的版本**：请查看requirement.txt文件。

## 使用指南 📖
1. **克隆项目**：
   首先，克隆项目到本地计算机：
   ```bash
   git clone https://github.com/huihuihenqiang/InterviewBot.git
2.**安装依赖**： 进入项目目录并安装所需的依赖包。建议使用 venv 或 conda 创建虚拟环境。参考

3.**配置 API 密钥**：
申请并配置 OpenAI 的 API 密钥，用于与大模型进行对话。
申请并配置百度云的语音识别 API 密钥。
将这些密钥添加到项目中的配置文件中（config.json）.
```json
{
  "API_URL": "https:///",
  "MODEL_NAME": "gpt-4-turbo",
  "OPENAI_API_KEY": "key",


 "API_KEY": "百度语音识别详见",
 "SECRET_KEY": "百度语音识别详见",
 "CUID": "百度语音识别详见",
 "tesseract_path": "D:\\ocr\\tesseract.exe"
}
```

4.**OCR 软件**：
下载并安装 OCR 软件（如 Tesseract）用于图像文字识别。

5.**构建知识库**：
使用query.py先生成Excel 文件，构建面试问题和答案的知识库。文件应包含“问题”和“答案”两列数据。

6.**运行项目**：启动主程序并进入面试环境,使用功能：
```bash
python main.py
```
上传简历：上传你的简历文件（PDF格式），系统将根据简历中的信息提供个性化回答。

语音识别：通过麦克风与系统进行语音对话，模拟面试互动。目前语音功能有一些问题：1、只能识别中文。2、只能识别自己的声音，无法识别对方的声音，可能是因为只收集到了自己麦克风声音，可以使用虚拟音频设备：你可以安装 Voicemeeter 或 Virtual Audio Cable 等虚拟音频驱动来捕捉系统音频。？？?这个还没测试，待定。

截图编程题识别：使用截图工具识别当前屏幕中的编程题并自动生成程序代码。

透明界面：项目的界面是透明的，适合实际面试中使用，减少干扰。

快速回答：根据构建的知识库，快速回答常见的面试问题。

构建知识库：点击按钮将excel文档导入到db里面。

## 贡献 👨‍💻

我们欢迎任何形式的贡献！无论是修复bug、提出建议、还是增加新功能，您的参与都将对项目的发展起到重要作用。
说真的因为是全用python做的，稳定性和实用性肯定不高，而且本人技术有限，很多东西都没做好，只能说提供一个思路，一些想法。欢迎大家使用不同的语言或者不同的技术路线构建稳定快速的工具。
希望可以抛砖引玉，共同为开源社区做贡献。

### 如何贡献：

1. **Fork** 本项目并创建您自己的分支。
2. 在您的分支中进行修改，确保修改后代码可以正常运行。
3. 提交您的修改，并创建 **pull request**。
4. 在提交前，请确保您的代码风格符合项目规范，尽量编写单元测试。

如果您遇到问题或有任何建议，请通过 **Issues** 提交反馈。

### 贡献者 🧑‍🤝‍🧑：

- [huihui] - 项目发起人
- [贡献者名单]

## 许可证 📄

本项目采用 **MIT 许可证**，您可以自由使用、修改和分发本项目的代码。


以下是该项目的英文版本 README 文件，基于你提供的信息：


# InterviewBot 🚀
[![Python 3.8+](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3109/)

This is a large model interview assistant tool built with PyQt, designed with a transparent interface so you can focus solely on the interview. The goal of this project is to simulate interview scenarios and help train your interview skills and techniques.

**This tool is not intended for use in cheating during interviews, and any form of cheating is strictly condemned!** Any consequences arising from the use of this tool are not the responsibility of this project or the author.

<img src="https://github.com/user-attachments/assets/1ca41254-fe0b-42e9-8790-8face6fb36d3" alt="Image" style="border: 10px solid black;"/>

The tool has the following features:

## Features ✨ (No empty promises, all features are implemented)

- **Chat with the large model**: Simulate an interview scenario by chatting with the model, preparing questions and answers. The system is connected to GPT-4, but make sure to replace it with your own API key.
- **Voice recognition conversation**: Supports voice recognition, enabling easy communication with the model via speech. This uses Baidu’s speech recognition, please replace it with your own API key.
- **Screenshot programming questions**: Take a screenshot of an algorithm programming question on your screen, automatically recognize it and return the program code. The accuracy is quite good, haha.
  ![Image](https://github.com/user-attachments/assets/d6268096-f88a-460b-8b39-cfd195792082)
- **Clear the screen**: Supports clearing the current interface to maintain cleanliness and focus.
- **Transparent interface**: The interface is designed to be transparent, with four modes to choose from, adapting to different scenarios.
- **Knowledge base creation**: Supports building a custom knowledge base using Excel files with Q&A. If your knowledge base is well-organized, it can perform just as well as the large model (since large models can be slow).
- **Personalized resume responses**: Upload your resume, and the system will give personalized answers based on your resume (e.g., answers related to your own experience).
- **Multithreading**: Used to maintain system stability.

## Configuration Requirements ⚙️

1. **OCR Software**: To use the screenshot programming question recognition, you need to download and install OCR software like Tesseract.
2. **Jieba Tokenizer**: A tokenization library for processing Chinese text to ensure accurate text recognition.
3. **OpenAI Key**: You need to configure an OpenAI API key for interaction with the large model.
4. **Baidu Speech Recognition Key**: You need to configure a Baidu speech recognition API key.

## Usage Guide 📖

1. **Clone the project**:  
   Clone the project to your local machine:
   ```bash
   git clone https://github.com/huihuihenqiang/InterviewBot.git
   ```

2. **Install dependencies**:  
   Navigate to the project directory and install the required dependencies. It is recommended to use `venv` or `conda` to create a virtual environment。

3. **Configure API Keys**:  
   Apply for and configure your OpenAI API key for interacting with the model.  
   Apply for and configure your Baidu Speech Recognition API key.  
   Add these keys to the project's configuration file (e.g., `config.json`).
   ```json
   {
     "API_URL": "https:///",
     "MODEL_NAME": "gpt-4-turbo",
     "OPENAI_API_KEY": "your-openai-api-key",
     "API_KEY": "baidu-speech-api-key",
     "SECRET_KEY": "baidu-speech-secret-key",
     "CUID": "baidu-speech-cuid",
     "tesseract_path": "C:\\ocr\\tesseract.exe"
   }
   ```

4. **OCR Software**:  
   Download and install OCR software (e.g., Tesseract) for image text recognition.

5. **Build Knowledge Base**:  
   Use `query.py` to generate an Excel file for building the interview question and answer knowledge base. The file should contain two columns: "Question" and "Answer".

6. **Run the project**:  
   Start the main program and enter the interview environment. Use the following command:
   ```bash
   python main.py
   ```

7. **Features**:  
   - **Upload Resume**: Upload your resume (PDF format), and the system will provide personalized answers based on the information in your resume.
   - **Voice Recognition**: Use the microphone to interact with the system in a voice-based interview simulation.
   - **Screenshot Programming Question Recognition**: Use a screenshot tool to recognize programming questions on the screen and automatically generate code.
   - **Transparent Interface**: The interface is transparent, ideal for real interviews as it reduces distractions.
   - **Quick Answers**: Quickly retrieve answers to common interview questions from the knowledge base.
   - **Build Knowledge Base**: Click the button to import the Excel document into the database.

## Contributing 👨‍💻

We welcome contributions of all kinds! Whether it’s fixing bugs, suggesting improvements, or adding new features, your involvement will be a valuable addition to the project.

Since this project is written entirely in Python, the stability and usability are not as high as they could be. My technical skills are limited, and many aspects are still unfinished. But it serves as a starting point with some ideas. I encourage everyone to build stable and fast tools using different languages or technologies. Let’s work together and contribute to the open-source community.

### How to Contribute:

1. **Fork** this project and create your own branch.
2. Make changes in your branch, ensuring the code runs smoothly.
3. Submit your changes and create a **pull request**.
4. Before submitting, please ensure your code follows the project style guidelines and include unit tests where possible.

If you encounter any issues or have suggestions, feel free to submit an **issue**.

### Contributors 🧑‍🤝‍🧑:

- [huihui] - Project Creator
- [Contributor List]

## License 📄

This project is licensed under the **MIT License**. You are free to use, modify, and distribute the code. Please refer to the [LICENSE](LICENSE) file for more details.

