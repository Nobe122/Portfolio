/* Prime Quest Prototype
  仕様書に基づいた基本構造の実装
*/

// --- グローバル変数 ---
int STATE_HOME = 0;
int STATE_GAME_FACTOR = 1;
int STATE_GAME_HUNTER = 2;
int STATE_GAME_CLEAR = 3;
int STATE_GAME_OVER = 4;

int currentState = STATE_HOME;

// 設定・状態管理
boolean hintEnabled = true;       // ヒントON/OFF(ON:true)
boolean isLifeMode = false;       // false=通常(5連正解), true=TA(ライフ制)
int difficulty = 1;               // 1:Easy ... 4:Extreme
int score = 0;                    // スコアの管理
int life = 3;                     // 残り残機の管理
int consecutiveWins = 0;          // 連続正解数
final int GOAL_STREAK = 5;        // 通常モードのクリア条件
int count = 0;                    // カウント
int level = 0;

// 各ゲーム管理クラスのインスタンス
FactorGame factorGame;
HunterGame hunterGame;

PFont myFont;

void setup() {
  size(800, 600);
  myFont = createFont("Arial", 24); // 日本語フォントがあれば指定推奨
  textFont(myFont);
  resetGame();
}

void draw() {
  background(240);
  
  if (currentState == STATE_HOME) {
    drawHome();
  } else if (currentState == STATE_GAME_FACTOR) {
    factorGame.run();
  } else if (currentState == STATE_GAME_HUNTER) {
    hunterGame.run();
  } else if (currentState == STATE_GAME_CLEAR || currentState == STATE_GAME_OVER) {
    drawResult(currentState);
  }
}

// --- 入力処理 ---
void keyPressed() {
  if (currentState == STATE_GAME_FACTOR) {
    factorGame.handleKey(key);
  }
  if (keyPressed && keyCode == 'R'){
    currentState = STATE_HOME;
  }
}

void mousePressed() {
  if (currentState == STATE_HOME) {
    checkHomeClick();
  } else if (currentState == STATE_GAME_HUNTER) {
    hunterGame.handleClick(mouseX, mouseY);
  } else if (currentState == STATE_GAME_FACTOR) {
    factorGame.handleClick();
  } else if (currentState == STATE_GAME_CLEAR || currentState == STATE_GAME_OVER) {
    currentState = STATE_HOME; // クリックでホームへ
  }
}

// --- ホーム画面ロジック ---
void drawHome() {
  fill(0); textAlign(CENTER); textSize(40);
  text("PRIME QUEST", width/2, 100);
  
  textSize(20);
  text("[ Settings ]", width/2, 180);
  textAlign(LEFT);
  fill(0); text("Hint   : ", 200, 210);
  fill(0); text("Mode : ", 200, 240);
  fill(0); text("Level  : ", 200, 270);
  textAlign(CENTER);
  fill(240); rect(width/2 - 30, 190, 60, 30);
  fill(0); text((hintEnabled ? "ON" : "OFF"), width/2, 210);
  fill(240); rect(width/2 - 90, 220, 180, 30);
  fill(0); text((isLifeMode ? "Life Mode (3 Hearts)" : "Normal(5 Streaks)"), width/2, 240);
  fill(240); rect(width/2 - 40, 250, 80, 30);
  fill(0); text((level%3==0 ? "Easy" : level%3==1 ? "Normal" : "Hard"), width/2, 270);
  
  textAlign(CENTER);
  // ゲーム選択ボタン（簡易）
  fill(100, 200, 100); rect(200, 300, 400, 50);
  fill(255); text("Start: Factorization Challenge", 400, 335);
  
  fill(100, 100, 200); rect(200, 400, 400, 50);
  fill(255); text("Start: Prime Hunter", 400, 435);
}

void checkHomeClick() {
  // 簡易的なボタン判定
  if (mouseY > 300 && mouseY < 350 && 200 < mouseX && mouseX < 600) {
    initGame(STATE_GAME_FACTOR);
  } if (mouseY > 400 && mouseY < 450 && 200 < mouseX && mouseX < 600) {
    initGame(STATE_GAME_HUNTER);
  }
  
  // 設定切り替え（画面上部クリック）
  if (190 < mouseY && mouseY < 210 && width/2 - 30 < mouseX && mouseX < width/2 + 30) {
    hintEnabled = !hintEnabled;
  } if (220 < mouseY && mouseY < 250 && width/2 - 90 < mouseX && mouseX < width/2 + 90) {
    isLifeMode = !isLifeMode;
  } if (250 < mouseY && mouseY < 280 && width/2 - 40 < mouseX && mouseX < width/2 + 40) {
    level += 1;
  }
}

void initGame(int mode) {
  life = 3;
  score = 0;
  consecutiveWins = 0;
  currentState = mode;
  
  if (mode == STATE_GAME_FACTOR) factorGame = new FactorGame();
  if (mode == STATE_GAME_HUNTER) hunterGame = new HunterGame();
}

void resetGame() {
  currentState = STATE_HOME;
}

void drawResult(int currentState) {
  fill(0); textAlign(CENTER); textSize(40);
  if (currentState == STATE_GAME_CLEAR){
    text("GAME CLEAR", width/2, height/2);
  } else{
    text("GAME OVER", width/2, height/2);
  }
  textSize(20);
  text("Score: " + score, width/2, height/2 + 30);
  text("Click to return Home", width/2, height/2 + 70);
}

// --- 共通ユーティリティ: 素数判定 ---
boolean isPrime(int n) {
  if (n < 2) return false;
  for (int i = 2; i * i <= n; i++) {
    if (n % i == 0) return false;
  }
  return true;
}
