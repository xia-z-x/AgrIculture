// server.js
const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// 使用 body-parser 解析 JSON 数据
app.use(bodyParser.json());

// 定义保存文件的路径
const configFolder = path.join(__dirname, 'config');
if (!fs.existsSync(configFolder)) {
    fs.mkdirSync(configFolder); // 如果文件夹不存在则创建
}

// API: 接收并保存文件
app.post('/save-fly-info', (req, res) => {
    const fileContent = req.body.data;
    const filePath = path.join(configFolder, './config/fly_info.txt');

    fs.writeFile(filePath, fileContent, (err) => {
        if (err) {
            console.error('Error saving file:', err);
            res.status(500).send('Failed to save file');
        } else {
            console.log('File saved successfully at:', filePath);
            res.send('File saved successfully!');
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});