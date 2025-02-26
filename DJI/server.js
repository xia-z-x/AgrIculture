// server.js
const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// ʹ�� body-parser ���� JSON ����
app.use(bodyParser.json());

// ���屣���ļ���·��
const configFolder = path.join(__dirname, 'config');
if (!fs.existsSync(configFolder)) {
    fs.mkdirSync(configFolder); // ����ļ��в������򴴽�
}

// API: ���ղ������ļ�
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