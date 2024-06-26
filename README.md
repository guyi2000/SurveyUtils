# 测量实习小工具

可以一步到位完成全站仪通信，格式转换，坐标计算，`CASS` 转换。

## 演示视频

https://github.com/guyi2000/SurveyUtils/assets/16850027/cfa457f4-d96c-4526-8938-1c9a06932b63

## 使用说明

使用前，请先仔细阅读本使用说明

### 基本使用

**在基本日常使用时**，默认将接续进行数据接收，格式转换，坐标计算，`CASS` 转换四项功能，因此，请先完成以下准备：

1. 先检查全站仪串口驱动是否已安装，全站仪是否已连接至计算机。在全站仪通过数据线连接的情况下，右击我的电脑（此电脑），点击属性，点击其中的设备管理器查看是否有串口设备，如有，则可进行下一步。

注：本软件仅适用于 `TOPCON GTS-102N`（其他机型未做测试）

2. 将控制点坐标存入 `KZD.dat` 中，坐标格式为 `点名,X坐标,Y坐标,H坐标`，示例如下：

```
14-A,387.872,958.983,49.571
```

保存完成后，方可正常使用其中坐标计算功能。

1. 准备完成后，双击打开 `run.bat`，即可启动程序，启动程序后如果电脑内仅有一个正在使用的串口，那么软件将自动检测串口号，否则，需要输入所在的串口，如 `COM6` 等，具体请在设备管理器中查看。如果出现 `No Available COM`，则表明全站仪连接失败，需要检查准备步骤是否完成。当软件提示 `Waiting for data...` 时，表明串口打开成功，可以在全站仪上发送数据。

2. 全站仪点击 `menu`，存储管理，翻页后找到数据传输，选择 `GTS` 格式的数据传输，选择相应文件，发送数据，可以看见计算机上有开始接收提示，表明计算机已经接收了数据。请耐心等待数据传输完成，如果出现了卡顿或进程未响应现象，请插拔 `USB` 接口，并重试，如果重复出现，请寻找老师。

3. 接收完成后，原始数据会保存在同目录 `raw` 文件夹下，并且以当前时间为文件名进行保存，如需更改默认文件名，请参阅二次开发章节。此后，软件将自动对接收数据进行转化，转化为 `SSS` 格式的数据，转化后的结果会自动保存到 `convert` 文件夹下便于上交。

4.在转化完成后，程序会自动开始计算，计算时，请注意保持文件格式正确，如果在 `SSS` 文件的第二三行没有 `STN` 数据，则程序会询问当前测站为何，如果第二三行没有 `BS` 数据，则程序会询问当前测站的后视点名为何。请特别注意，已有点名需要与 `KZD.dat` 中的保持一致，否则程序无法正确读取。例如：

在 `SSS` 文件中有

```
STN   14-10,1.524,
BS    14-6,1.800,
```

那么在 `KZD.dat` 就必须存在14-10与14-6两个点

```
14-6,552.402,1103.954,49.696
14-10,514.79,1100.839,49.8
```

否则，程序将因无法找到点而发出轮询。

如果在SSS文件中未读取到STN与BS信息，则程序会发出询问，请依次输入`STN`点名，仪器高，BS点名，后视方向角，这样程序就可以继续进行运算。（也要保证点名在KZD.dat中存在）


5. 坐标计算结束后，程序将结果保存在同目录 `output` 文件夹下，并自动开始转化为 `CASS` 格式，转换后的文件保存在同目录 `cass` 文件夹下，可以直接导入 `cass` 中进行绘图。

### 进阶使用

**对高级用户**，可以不必使用 `run.bat` ，在目录下打开命令提示符或 `powershell`，运行如下命令：

```bash
python receiveData.py
python convertData.py
python calculateData.py
python transferData.py
```

即可分别使用函数提供的功能，其中 `receiveData` 是接受全站仪数据并保存至 `raw` 文件夹下，`convertData` 是将 `raw` 文件夹内所有文件转换保存至 `convert` 文件夹下，`calculateData` 是将 `convert` 文件夹下所有文件转换保存至 `output` 文件夹下，`transferData` 是将 `output` 文件夹下所有文件转换保存至 `cass` 文件夹下。

### 二次开发

本软件是在测量小学期期间编成，因此并没有做过多的测试以及重度使用，仅仅服务于本组的数据处理，因而可能具有不稳定性，也有些代码习惯不够友好，注释也并不是很全，如果需要二次开发，可能稍有难度，不过基本分为四个函数，分别存储在四个 `python` 源文件中。在做整合开发时，可以不对函数内进行修改而使用函数提供的功能，下讲函数的接口列出，以备使用：

```python
def receiveCOMData(receiveDataFile)
```

该函数有一个参数，其意为存储数据的路径，其通过调用串口，将接受到的数据文件存储至receiveDataFile路径中。

```python
def convertData(rawDataFile, convertDataFile)
```

该函数有两个参数，第一个参数是待转换的全站仪数据源文件，第二个参数为转换后文件的路径（保存路径）。

```python
def caculateData(convertDataFile, caculateDataFile, KZDDataFile)
```

该函数有三个参数，第一个参数是待计算的SSS格式文件，第二个参数是计算后文件的保存路径，第三个参数是需要查阅的控制点坐标数据文件。

```python
def transferData(caculateDataFile, transerDataFile)
```

该函数有两个参数，第一个参数是待转换的坐标文件，第二个参数是转换后全站仪的文件。

以上接口可以正常使用，在 `main.py` 可以继续使用。
