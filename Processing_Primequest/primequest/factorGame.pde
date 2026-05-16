// ==========================================
// ゲーム①: 因数分解チャレンジ
// ==========================================
class FactorGame {
  int targetNumber;
  ArrayList<Integer> correctFactors; // 正解の素因数リスト（ソート済み）
  String inputString = "";
  String message = "Input factors space-separated (e.g. '2 2 3')";
  int timer = 1000; // 簡易タイマー
  boolean showingExplanation = false;
  
  FactorGame() {
    nextLevel();
  }
  
  void nextLevel() {
    // 問題生成（難易度に応じて上限を変える）
    if (level%3 == 0){
      targetNumber = int(random(10, 100));
      timer = 3000;
    } else if (level%3 == 1){
      targetNumber = int(random(10, 160));
      timer = 2000;
    } else {
      targetNumber = int(random(50, 300));
      timer = 1000;
    }
    correctFactors = getPrimeFactors(targetNumber);
    inputString = "";
    showingExplanation = false;
  }
  
  // 素因数分解ロジック
  ArrayList<Integer> getPrimeFactors(int n) {
    ArrayList<Integer> factors = new ArrayList<Integer>();
    int d = 2;
    int temp = n;
    while (d * d <= temp) {
      while (temp % d == 0) {
        factors.add(d);
        temp /= d;
      }
      d++;
    }
    if (temp > 1) factors.add(temp);
    java.util.Collections.sort(factors); // 正解判定のためにソートしておく
    return factors;
  }
  
  void run() {
    if (showingExplanation) {
      drawExplanation();
      return;
    }
    
    timer--;
    if (timer <= 0) handleFail();
    
    fill(0); textAlign(CENTER);
    text("Target: " + targetNumber, width/2, 150);
    text("Input: " + inputString, width/2, 250);
    text(message, width/2, 350);
    text((isLifeMode ? "Life: " + life : "Life: " + life +  "  Streak: " + consecutiveWins + "/5"), width/2, 50);
    text("Time: " + timer, 60, 40);
    text("Score: " + score, width - 60, 40);

    // ヒント表示（時間経過で簡易表示）
    if (hintEnabled && timer < 500) {
      String hintStr = "Hint: " + correctFactors.get(0) + "...";
      fill(255, 0, 0); text(hintStr, width/2, 400);
    }
  }
  
  void handleClick() {
    if (showingExplanation) {
      // 解説中ならクリックで次へ
      message = "You can do it!";
      nextLevel();
      return;
    }
  }
  
  void handleKey(char k) {
    if ((k >= '0' && k <= '9') || k == ' ') {
      inputString += k;
    } else if (k == BACKSPACE && inputString.length() > 0) {
      inputString = inputString.substring(0, inputString.length()-1);
    } else if (k == ENTER || k == RETURN) {
      checkAnswer();
    }
  }
  
  void checkAnswer() {
    // 1. 入力をスペースで分割して数値リスト化
    String[] parts = split(inputString, ' ');
    ArrayList<Integer> userFactors = new ArrayList<Integer>();
    
    // 空白除去やパース処理
    for (String s : parts) {
      if (s.length() > 0){
        userFactors.add(int(s));
        count += 1;
      }
    }
    
    // 2. 順序不同にするためソート
    java.util.Collections.sort(userFactors);
    
    // 3. 正解と比較（リストの中身が完全に一致するか）
    if (userFactors.equals(correctFactors)) {
      message = "Good. Correct!";
      handleWin();
      score += 100 * count;
      count = 0;
    } else {
      message = "Wrong. Try again!";
      //handleFail();
    }
  }
  
  void handleWin() {
    consecutiveWins++;
    if (!isLifeMode && consecutiveWins >= GOAL_STREAK) {
      currentState = STATE_GAME_CLEAR; // クリア
    } else {
      score += timer * ((level%3)+1) * 0.3;
      delay(500); // 一瞬待つ（実際は非同期処理推奨）
      nextLevel();
    }
  }
  
  void handleFail() {
    life--;
    if (life <= 0) currentState = STATE_GAME_OVER;
    if (!isLifeMode) {
      consecutiveWins = 0; // ストリークリセット
    }
    showingExplanation = true; // 解説へ
  }
  
  void drawExplanation() {
    background(50);
    textAlign(CENTER);
    fill(255); text("OOPS! Look at the ANSWER. Click to Next.", width/2, 400);
    text("Target: " + targetNumber, width/2, 150);
    String factorText = "";
    for (int i = 0; i < correctFactors.size(); i++) {
      factorText += correctFactors.get(i);
      if (i < correctFactors.size() - 1) {
        factorText += " × ";
      }
    }

text(factorText, width/2, 500);

  }
}
