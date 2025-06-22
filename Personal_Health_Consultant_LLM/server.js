require('dotenv').config();      // NEW
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios'); // 用于调用 OpenAI 和 Kimi 的 API
const { OpenAI } = require('openai'); // 新增：Kimi 的 SDK（需安装）
const bcrypt = require('bcryptjs'); // NEW
const mysql = require('mysql2/promise'); // NEW
const multer = require('multer');       // NEW
const app = express();
app.use(bodyParser.json());
//const PORT = 3000;

// 配置项
const CONFIG = {
    openai: {
        apiKey: '你的_OPENAI_API_KEY', // 替换为你的 OpenAI API 密钥
        baseURL: 'https://api.openai.com/v1',
        model: 'gpt-3.5-turbo',
    },
    kimi: {
        apiKey: 'sk-uiByJDUG94Zy53zPBXtTOGSIc4eq4w1EuWjis7cw7j33Je0H',    // 替换为你的 Kimi API 密钥
        baseURL: 'https://api.moonshot.cn/v1',
        model: 'moonshot-v1-8k',
        systemMessage: {
            role: 'system',
            content: '你是 Kimi，由 Moonshot AI 提供的人工智能助手，擅长中英文对话。'
        }
    }
};

// 全局状态
let currentModel = 'kimi'; // 默认使用 OpenAI
let kimiMessages = [];       // 存储 Kimi 的多轮对话历史
let currentPrompt = 
'你是一位具有医学专业知识背景的AI个人健康管理专家。你的任务是基于用户的各个指标评分、疾病风险评估、生活方式分析等多维度信息，生成一份结构清晰、语言友好、具有实用价值的个性化健康管理建议报告。要求： 1.该用户的长寿潜力评分为【高】，这意味着他现在的健康状况更好。 2该用户的疾病风险评分如下：甲状腺功能亢进(甲亢)[高] 胰岛素依赖型糖尿病[低] 非胰岛素依赖型糖尿病[低] 肥胖[低] 体液、电解质及酸碱平衡紊乱[高] 高血压性心脏病[低] 心绞痛[高]急性心肌梗死[中]慢性缺血性心脏病[中][中] 其他肺源性心脏病[中] 动脉粥样硬化 血清阳性类风湿关节炎[高] 系统性红斑狼疮[中] 结缔组织的其他全身受累[中] 慢性肾衰竭[中] 男性生殖器官疾病[中] 除子宫颈外的其他子宫非炎性疾病[中] 2中所提到的疾病评分代表这样一个含义：如果该疾病风险评分为高，这意味着此人患这种疾病的风险值较低，如果疾病评分为中等，这意味着此人患这种疾病的风险值较低，如果该疾病风险评分为低，则因为着此人患该疾病的风险较高。 3.要求1和2中给你的得分是通过额外的模型计算而得到的该用户的长寿潜力预测以及各种疾病的风险评分，通过这些得分，我们能够了解到用户在各个方面的健康状况，你需要根据这些健康状况的评价指标，对用户进行引导式的提问，进而给出一定的建议，建议的多少取决于用户的整体长寿潜力评分以及各种疾病风险得分。原则上，对于评分比较低的用户，你需要设计更多轮的对话，尽可能了解更多的信息，用相对更加温和的语言，给出相对更多的生活习惯上的建议。而对于评分相对较高的用户，你可以在有限的较少轮对话中总结信息，给出一定的生活习惯上的建议。 4.在你试图给出运动习惯和饮食偏好的建议之前，你需要询问用户的所在地、收入以及习惯的运动方式，根据用户所在地区的整体饮食习惯做一个推荐，根据用户的收入来决定推荐何种饮食以及进行何种运动，避免因为花费过高导致计划难以实现。此外，如果用户已经有了一定的运动习惯，你需要更倾向于让用户保持并加强锻炼，这时候你的推荐的额外的运动种类可以少一些，但是如果用户没有运动的习惯，你则需要引导用户回答其更可能接受的运动方式，并且在给出建议的时候，你需要给出更多方面的运动习惯以供用户挑选。在你询问用户的作息规律的时候，你需要确保先询问了用户的工作情况，避免由于用户的工作内容需要在晚上工作导致你给出的建议和他的工作冲突。 5你应该按照如下的问诊流程，根据用户的总体健康得分和疾病得分自由灵活开放的设计问题，对于哪些评分较低的疾病，意味着用户患该疾病的风险值较高，你应该运用自己的知识，多增加一些轮次和问题来询问相关的能减少相关疾病风险的情况。 以下是一个标准化的问诊流程设计，按照健康管理的关键领域分类，适合用于健康管理、体检后随访或慢性病管理场景： 您近期主要关注哪些健康问题？ 目前有无明显不适症状？（疼痛、疲劳、头晕等） 症状出现的时间、频率和持续时间？ 基础体征 近期体重是否有明显变化？ 睡眠质量如何？（入睡困难、早醒、多梦等） 大小便是否正常？ 第二轮：饮食习惯评估 饮食结构与质量 每日几餐？是否有规律进餐时间？ 主食类型（精米白面/粗粮占比）？ 蔬菜水果摄入量？（具体份数/种类） 蛋白质与脂肪来源 主要蛋白质来源？（红肉/白肉/豆制品/奶制品） 烹饪用油类型及用量？（动物油/植物油） 零食、甜饮料摄入频率？ 特殊饮食习惯 是否有食物过敏或不耐受？ 是否补充营养品/保健品？ 饮酒习惯？（种类/频率/量） 第三轮：作息规律评估 睡眠模式： 通常几点入睡？几点醒来？ 夜间醒来的频率？ 日间是否补觉？ 工作与休息 工作时间是否固定？有无夜班？ 午休习惯及时长？ 周末作息是否与工作日差异大？ 生物节律 晨起后精力状态如何？ 午后是否常感疲倦？ 夜间几点开始有困意？ 第四轮：运动习惯评估 运动频率与强度 每周运动次数及时长？ 主要运动类型？（有氧/力量/柔韧）运动时心率变化？（是否达到靶心率） 日常活动量 每日步数？久坐时间？（每小时是否起身活动） 通勤方式？（步行/骑车/驾车） 第五轮：心理与压力评估 情绪状态 近期情绪基调？（平静/焦虑/低落） 是否有持续两周以上的情绪低落？ 压力源与应对 主要压力来源？（工作/家庭/经济） 常用的解压方式？ 是否有放松技巧？（冥想/呼吸练习）第六轮：既往史与环境因素 健康背景 慢性病史（高血压/糖尿病等）手术史/住院史 药物使用情况（处方药/非处方药）生活环境 居住环境（空气质量/噪音）饮用水源（自来水/过滤水/桶装水）家庭烹饪方式（煎炸/蒸煮）6.你提问的时候，需要自由且灵活，我给你的流程只是一个参考，你需要根据这个大概的流程灵活的组织问题，并且根据用户得分的不同来改变询问的详细程度：对于那些总体得分更高的用户，倾向于简短的询问，如果当前有好的运动习惯或者饮食习惯，倾向于让他保持。对于那些总体得分更低的用户，倾向于更详细的询问和细致的推荐生活方式的改变。7.你给出建议的目的是尽可能地改善用户的健康状况，因此你在最终给出建议的时候，需要针对性的提出每个部分改变的意义。8. 你要用通俗语言简明扼要地总结本次预测分析结果，包括寿命预测、主要疾病风险点、生活方式评估等核心信息。9. 下属是你需要输出时给予的结果反馈模块：>预防性筛查：基于预测中某疾病风险升高，建议做哪些体检或生物标志物监测；>生活方式干预：饮食、运动、睡眠调整等个性化建议；>药物或营养补充：若有特定蛋白或代谢通路受影响，建议进一步临床评估或咨询专业医生；>心理/社交支持：若长寿模型提示需关注心理健康、社交活动对健康的影响；>持续监测方案：如何跟踪蛋白指标变化、疾病风险变化；>应急预案或警示：若风险骤增或出现预警信号，应如何及时就医等。9.最终输出的结构要以整体的概述为先，再将第三步列出的每一个模块惊醒详细解释。最后加以总结，鼓励用户关注自身健康，如对报告有疑问，可进一步说明模块详情.请勿：- 提及政治人物- 使用专业缩写'

// 初始化 Kimi 客户端
const kimiClient = new OpenAI({
    apiKey: CONFIG.kimi.apiKey,
    baseURL: CONFIG.kimi.baseURL,
});

// MySQL 连接池
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

// multer 保存上传文件到 /uploads
const upload = multer({ dest: 'uploads/' });

// Middleware
app.use(bodyParser.json());
app.use(express.static('.')); // Serve static files (e.g., index.html)

// 调用 OpenAI API
async function callOpenAI(question) {
    try {
        const response = await axios.post(
            `${CONFIG.openai.baseURL}/chat/completions`,
            {
                model: CONFIG.openai.model,
                messages: [
                    { role: 'system', content: currentPrompt },
                    { role: 'user', content: question }
                ],
                temperature: 0.7,
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${CONFIG.openai.apiKey}`,
                },
            }
        );
        return response.data.choices[0].message.content;
    } catch (error) {
        console.error('OpenAI API 错误:', error.response?.data || error.message);
        return 'OpenAI 暂时无法回答。';
    }
}

// 调用 Kimi API（支持多轮对话）
async function callKimi(question) {
    try {
        // 1. 构造消息历史（包含系统提示和用户输入）
        kimiMessages.push({ role: 'system', content: currentPrompt },{ role: 'user', content: question });
        const messages = [CONFIG.kimi.systemMessage, ...kimiMessages.slice(-20)]; // 保留最近20条消息

        // 2. 调用 Kimi API
        const completion = await kimiClient.chat.completions.create({
            model: CONFIG.kimi.model,
            messages: messages,
            temperature: 0.3,
        });

        // 3. 保存 Kimi 的回复到历史
        const assistantMessage = completion.choices[0].message;
        kimiMessages.push(assistantMessage);
        return assistantMessage.content;
    } catch (error) {
        console.error('Kimi API 错误:', error.response?.data || error.message);
        return 'Kimi 暂时无法回答。';
    }
}

// API endpoint for chat
app.post('/api/chat', async (req, res) => {
    const { question } = req.body;
    try {
        const answer = currentModel === 'openai' 
            ? await callOpenAI(question) 
            : await callKimi(question);
        res.json({ answer });
    } catch (error) {
        res.status(500).json({ error: '服务器错误' });
    }
});

// API endpoint to update the prompt
app.post('/api/update-prompt', (req, res) => {
    const { prompt } = req.body;
    if (prompt) {
        currentPrompt = prompt;
        res.json({ success: true, message: '提示词已更新' });
    } else {
        res.status(400).json({ error: '提示词不能为空' });
    }
});

// API endpoint to switch models
app.post('/api/switch-model', (req, res) => {
    const { model } = req.body;
    if (['openai', 'kimi'].includes(model)) {
        currentModel = model;
        res.json({ success: true, message: `已切换到 ${model} 模型` });
    } else {
        res.status(400).json({ error: '无效的模型名称' });
    }
});

app.post('/api/register', async (req, res) => {
  const { phone, password } = req.body;
  if (!/^1\\d{10}$/.test(phone) || !password) {
    return res.status(400).json({ error: '手机号或密码格式不正确' });
  }

  try {
    const [rows] = await pool.query('SELECT id FROM users WHERE phone=?', [phone]);
    if (rows.length) return res.status(409).json({ error: '账号已存在' });

    const hash = await bcrypt.hash(password, 10);
    await pool.query('INSERT INTO users (phone, password) VALUES (?, ?)', [phone, hash]);
    res.json({ success: true, message: '注册成功' });
  } catch (e) {
    res.status(500).json({ error: '数据库错误' });
  }
});

app.post('/api/login', async (req, res) => {
  const { phone, password } = req.body;
  try {
    const [rows] = await pool.query('SELECT id, password FROM users WHERE phone=?', [phone]);
    if (!rows.length) return res.status(401).json({ error: '账号不存在' });

    const match = await bcrypt.compare(password, rows[0].password);
    if (!match) return res.status(401).json({ error: '密码错误' });

    // 简单返回 userId，真实项目建议发 JWT
    res.json({ success: true, userId: rows[0].id });
  } catch (e) {
    res.status(500).json({ error: '数据库错误' });
  }
});

app.post('/api/upload', upload.single('file'), async (req, res) => {
  const { userId } = req.body; // 前端需传
  if (!req.file) return res.status(400).json({ error: '未检测到文件' });

  try {
    await pool.query(
      'INSERT INTO user_files (user_id, file_path) VALUES (?, ?)',
      [userId, req.file.path]
    );
    res.json({ success: true, path: req.file.path });
  } catch (e) {
    res.status(500).json({ error: '数据库错误' });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
// 绑定到 0.0.0.0 明确监听所有网卡
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server listening on port ${PORT}`);
});