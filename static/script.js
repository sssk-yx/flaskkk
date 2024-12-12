// 全局音频对象
let music;

document.addEventListener("DOMContentLoaded", function() {
    // 使用从HTML传递过来的全局变量作为音频文件路径
    music = new Audio(window.musicUrl);
    music.loop = true;

    document.getElementById('start-game').addEventListener('click', async () => {
        const nickname = prompt("请输入你的昵称:");
        if (!nickname) return;

        try {
            const playerId = await savePlayerInfoToServer(nickname);
            await loadPlayerInfoFromServer(playerId);
            playBackgroundMusic();
            await findTreasureWithAsyncAwait(playerId);
        } catch (error) {
            console.error("Error during game initialization:", error);
            alert(`游戏初始化失败: ${error.message}`);
        }
    });
});

function playBackgroundMusic() {
    if (music) {
        music.play();
    }
}

// TreasureMap class with game logic
class TreasureMap {
    static async getInitialClue() {
        return "在古老的图书馆里找到了第一个线索...";
    }

    static async decodeAncientScript(clue) {
        const riddle = "什么有钥匙但没有锁？";
        const answer = prompt(riddle);
        if (answer.toLowerCase() === "piano") {
            return "解码成功!宝藏在一座古老的神庙中，但你需要通过一片密林...";
        } else {
            throw new Error("解谜失败!无法继续寻宝。");
        }
    }

    static async searchTemple(location) {
        const problem = prompt("解决这个数学问题: 2 + 3 = ?");
        if (problem === "5") {
            return "通过了考验，找到了一个神秘的箱子...";
        } else {
            throw new Error("考验失败!无法继续寻宝。");
        }
    }

    static async openTreasureBox() {
        const keys = ['金钥匙', '银钥匙', '铁钥匙'];
        const correctKey = keys[Math.floor(Math.random() * keys.length)];
        const chosenKey = prompt(`请选择正确的钥匙来打开箱子: ${keys.join(', ')}`);
        if (chosenKey === correctKey) {
            return "恭喜!你找到了传说中的宝藏!";
        } else {
            throw new Error("选择了错误的钥匙，宝藏未能开启。");
        }
    }
}

// Game logic with async/await
async function findTreasureWithAsyncAwait(playerId) {
    try {
        document.getElementById('game-status').innerText = "正在寻找初始线索...";
        const clue = await TreasureMap.getInitialClue();
        document.getElementById('game-status').innerText = clue;

        document.getElementById('game-status').innerText = "尝试解码古老的文字...";
        const location = await TreasureMap.decodeAncientScript(clue);
        document.getElementById('game-status').innerText = location;

        document.getElementById('game-status').innerText = "探索神庙...";
        const box = await TreasureMap.searchTemple(location);
        document.getElementById('game-status').innerText = box;

        document.getElementById('game-status').innerText = "尝试打开宝藏箱...";
        const treasure = await TreasureMap.openTreasureBox();
        document.getElementById('game-status').innerText = treasure;
        alert(treasure);

        // Add score to server
        await addScoreToServer(playerId, 100); // Assuming a fixed score for simplicity
    } catch (error) {
        document.getElementById('game-status').innerText = `任务失败: ${error.message}`;
        alert(`任务失败: ${error.message}`);
    }
}

// Communicate with Flask backend
async function savePlayerInfoToServer(nickname) {
    const response = await fetch('/api/player', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nickname})
    });
    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    return data.id; // Return player ID
}

async function addScoreToServer(playerId, score) {
    const response = await fetch('/api/score', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({player_id: playerId, score})
    });
    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    console.log(data);
}

async function loadPlayerInfoFromServer(playerId) {
    const response = await fetch(`/api/player/${playerId}`);
    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    document.getElementById('player-nickname').innerText = data.nickname;
    const scoreList = document.getElementById('score-history');
    scoreList.innerHTML = ''; // Clear old scores
    data.scores.forEach(score => {
        const li = document.createElement('li');
        li.innerText = `${new Date(score.timestamp).toLocaleString()}: ${score.score}`;
        scoreList.appendChild(li);
    });
}