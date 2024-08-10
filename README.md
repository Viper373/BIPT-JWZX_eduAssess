# 🚀 assess.py 自动化脚本

`assess.py` 是一个自动化脚本，主要功能是使用 Selenium 控制浏览器进行特定操作，并使用 OCR 技术进行字符识别。该脚本包括自动下载依赖、登录系统等功能。

## 📋 功能概述

- 🖥️ **自动化浏览器操作**：使用 Selenium 驱动 Edge 浏览器进行自动化操作。
- 🔍 **OCR 识别**：自动下载并安装 Tesseract OCR 进行图片中的字符识别。
- 🔐 **账号登录**：自动化输入用户名和密码进行系统登录。
- 📥 **依赖下载**：自动检测并下载所需依赖项。

## 📦 环境依赖

- Python 3.x
- Selenium
- Edge 浏览器和对应的驱动程序
- ddddocr 模块

## 🔧 安装指南

1. **克隆仓库**:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

3. **配置 Edge WebDriver**:
    - 请确保您的系统中安装了 Edge 浏览器，并且已配置相应的 WebDriver。

4. **运行脚本**:
    - 执行以下命令开始脚本运行：
    ```bash
    python assess.py
    ```

## ⚙️ 使用方法

- **首次运行**:
    - 运行脚本后，会提示是否需要下载 OCR 识别技术的依赖项。根据提示选择相应选项并完成下载和安装。

- **登录功能**:
    - 使用 `login(username, password)` 函数自动输入账号和密码进行系统登录。

## 📄 文件结构

- `assess.py`：主脚本文件，包含所有功能实现。
- `requirements.txt`：Python 依赖项文件。

## 🛠️ 脚本功能

- **download()**：用于自动下载并安装 OCR 依赖项的函数。
- **login(username, pwd)**：用于模拟用户登录系统的函数。

## 📝 备注

- 请确保您有足够的权限来运行安装和浏览器操作。
- 如果遇到问题，可以在此处查看 [Tesseract OCR 安装说明](https://github.com/tesseract-ocr/tesseract)。

## 📧 联系方式

如果有任何问题或建议，欢迎通过 [邮件](mailto:2020311228@bipt.edu.cn) 与我联系。
